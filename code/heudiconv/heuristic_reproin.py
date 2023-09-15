"""Reproin heuristic."""

from __future__ import annotations

from warnings import warn
from collections.abc import Iterable
from collections import Counter
from glob import glob
import logging
import os.path
import re
from typing import Optional

import pydicom as dcm

from heudiconv.utils import SeqInfo
from heudiconv.heuristics.reproin import (
    KNOWN_DATATYPES,
    fix_seqinfo,
    fixup_subjectid,
    get_study_description,
    get_unique,
    md5sum,
    sanitize_str,
)

lgr = logging.getLogger("heudiconv")


DWI_RES = {
    "1.6mm-iso": "highres",
    "2mm-iso": "lowres",
}


IGNORE_PROTOCOLS = (
    "DEV",
    "LABEL",
    "REPORT",
    "ADC",
    "TRACEW",
    "FA",
    "ColFA",
    "B0",
    "TENSOR",
    "10meas",  # dismiss a trial of fmap acquisition
)

bids_regex = re.compile(r"_(?=(dir|acq|task|run)-([A-Za-z0-9]+))")


# Terminology to harmonise and use to name variables etc
# experiment
#  subject
#   [session]
#    exam (AKA scanning session) - currently seqinfo, unless brought together from multiple
#     series  (AKA protocol?)
#      - series_spec - deduced from fields the spec (literal value)
#      - series_info - the dictionary with fields parsed from series_spec

# Which fields in seqinfo (in this order) to check for the ReproIn spec
series_spec_fields = ("protocol_name", "series_description")

# dictionary from accession-number to runs that need to be marked as bad
# NOTE: even if filename has number that is 0-padded, internally no padding
# is done
fix_accession2run: dict[str, list[str]] = {
    # e.g.:
    # 'A000035': ['^8-', '^9-'],
}

# A dictionary containing fixes/remapping for sequence names per study.
# Keys are md5sum of study_description from DICOMs, in the form of PI-Experimenter^protocolname
# You can use `heudiconv -f reproin --command ls --files  PATH
# to list the "study hash".
# Values are list of tuples in the form (regex_pattern, substitution).
# If the  key is an empty string`''''`, it would apply to any study.
protocols2fix: dict[str | re.Pattern[str], list[tuple[str, str]]] = {
    # e.g., QA:
    # '43b67d9139e8c7274578b7451ab21123':
    #     [
    #      ('BOLD_p2_s4_3\.5mm', 'func_task-rest_acq-p2-s4-3.5mm'),
    #      ('BOLD_', 'func_task-rest'),
    #      ('_p2_s4',        '_acq-p2-s4'),
    #      ('_p2', '_acq-p2'),
    #     ],
    # '':  # for any study example with regexes used
    #     [
    #         ('AAHead_Scout_.*', 'anat-scout'),
    #         ('^dti_.*', 'dwi'),
    #         ('^.*_distortion_corr.*_([ap]+)_([12])', r'fmap-epi_dir-\1_run-\2'),
    #         ('^(.+)_ap.*_r(0[0-9])', r'func_task-\1_run-\2'),
    #         ('^t1w_.*', 'anat-T1w'),
    #         # problematic case -- multiple identically named pepolar fieldmap runs
    #         # I guess we will just sacrifice ability to detect canceled runs here.
    #         # And we cannot just use _run+ since it would increment independently
    #         # for ap and then for pa.  We will rely on having ap preceding pa.
    #         # Added  _acq-mb8  so they match the one in funcs
    #         ('func_task-discorr_acq-ap', r'fmap-epi_dir-ap_acq-mb8_run+'),
    #         ('func_task-discorr_acq-pa', r'fmap-epi_dir-pa_acq-mb8_run='),
    # ]
}

# list containing StudyInstanceUID to skip -- hopefully doesn't happen too often
dicoms2skip: list[str] = [
    # e.g.
    # '1.3.12.2.1107.5.2.43.66112.30000016110117002435700000001',
]

DEFAULT_FIELDS = {
    # Let it just be in each json file extracted
    "Acknowledgements": "We thank the Heudiconv developers. ",
}

POPULATE_INTENDED_FOR_OPTS = {
    "matching_parameters": ["ImagingVolume", "Shims"],
    "criterion": "Closest",
}


def filter_dicom(dcmdata: dcm.dataset.Dataset) -> bool:
    """Return True if a DICOM dataset should be filtered out, else False"""
    return True if dcmdata.StudyInstanceUID in dicoms2skip else False


def filter_files(_fn: str) -> bool:
    """Return True if a file should be kept, else False.

    ATM reproin does not do any filtering. Override if you need to add some
    """
    return not _fn.endswith((".csv", ".dvs"))


def infotoids(seqinfos: Iterable[SeqInfo], outdir: str) -> dict[str, Optional[str]]:
    seqinfo_lst = list(seqinfos)
    # decide on subjid and session based on patient_id
    lgr.info("Processing sequence infos to deduce study/session")
    study_description = get_study_description(seqinfo_lst)
    study_description_hash = md5sum(study_description)
    subject = fixup_subjectid(get_unique(seqinfo_lst, "patient_id"))
    # TODO:  fix up subject id if missing some 0s
    if study_description:
        # Generally it is a ^ but if entered manually, ppl place space in it
        split = re.split("[ ^]", study_description, maxsplit=1)
        # split first one even more, since could be PI_Student or PI-Student
        split = re.split("[-_]", split[0], maxsplit=1) + split[1:]

        # locator = study_description.replace('^', '/')
        locator = "/".join(split)
    else:
        locator = "unknown"

    # TODO: actually check if given study is study we would care about
    # and if not -- we should throw some ???? exception

    # So -- use `outdir` and locator etc to see if for a given locator/subject
    # and possible ses+ in the sequence names, so we would provide a sequence
    # So might need to go through  parse_series_spec(s.protocol_name)
    # to figure out presence of sessions.
    ses_markers: list[str] = []

    # there might be fixups needed so we could deduce session etc
    # this copy is not replacing original one, so the same fix_seqinfo
    # might be called later
    seqinfo_lst = fix_seqinfo(seqinfo_lst)
    import pdb; pdb.set_trace()
    for s in seqinfo_lst:
        if s.is_derived:
            continue
        session_ = parse_series_spec(s.protocol_name).get("session", None)
        if session_ and "{" in session_:
            # there was a marker for something we could provide from our seqinfo
            # e.g. {date}
            session_ = session_.format(**s._asdict())
        if session_:
            ses_markers.append(session_)
    session: Optional[str] = None
    if ses_markers:
        # we have a session or possibly more than one even
        # let's figure out which case we have
        nonsign_vals = set(ses_markers).difference("+=")
        # although we might want an explicit '=' to note the same session as
        # mentioned before?
        if len(nonsign_vals) > 1:
            lgr.warning(  # raise NotImplementedError(
                "Cannot deal with multiple sessions in the same study yet!"
                " We will process until the end of the first session"
            )
        if nonsign_vals:
            # get only unique values
            ses_markers = list(set(ses_markers))
            if set(ses_markers).intersection("+="):
                raise NotImplementedError(
                    "Should not mix hardcoded session markers with incremental ones (+=)"
                )
            if not len(ses_markers) == 1:
                raise NotImplementedError(
                    "Should have got a single session marker.  Got following: %s"
                    % ", ".join(map(repr, ses_markers))
                )
            session = ses_markers[0]
        else:
            # TODO - I think we are doomed to go through the sequence and split
            # ... actually the same as with nonsign_vals, we just would need to figure
            # out initial one if sign ones, and should make use of knowing
            # outdir
            # raise NotImplementedError()
            # we need to look at what sessions we already have
            sessions_dir = os.path.join(outdir, locator, "sub-" + subject)
            prior_sessions = sorted(glob(os.path.join(sessions_dir, "ses-*")))
            # TODO: more complicated logic
            # For now just increment session if + and keep the same number if =
            # and otherwise just give it 001
            # Note: this disables our safety blanket which would refuse to process
            # what was already processed before since it would try to override,
            # BUT there is no other way besides only if heudiconv was storing
            # its info based on some UID
            if ses_markers == ["+"]:
                session = "%03d" % (len(prior_sessions) + 1)
            elif ses_markers == ["="]:
                session = (
                    os.path.basename(prior_sessions[-1])[4:]
                    if prior_sessions
                    else "001"
                )
            else:
                session = "001"

    if study_description_hash == "9d148e2a05f782273f6343507733309d":
        session = "siemens1"
        lgr.info("Imposing session {0}".format(session))


    return {
        # TODO: request info on study from the JedCap
        "locator": locator,
        # Sessions to be deduced yet from the names etc TODO
        "session": session,
        "subject": subject,
    }


def create_key(template, outtype=("nii.gz",), annotation_classes=None):
    if template is None or not template:
        raise ValueError("Template must be a valid format string")
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    t1w = create_key(
        "sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acquisition}{run_entity}_T1w"
    )
    t2w = create_key("sub-{subject}/{session}/anat/sub-{subject}_{session}{run_entity}_T2w")
    dwi = create_key(
        "sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_dir-{dir}{run_entity}_dwi"
    )
    mag = create_key("sub-{subject}/{session}/fmap/sub-{subject}_{session}{run_entity}_magnitude")
    phdiff = create_key(
        "sub-{subject}/{session}/fmap/sub-{subject}_{session}{run_entity}_phasediff"
    )
    epi = create_key(
        "sub-{subject}/{session}/fmap/sub-{subject}_{session}"
        "_acq-{acquisition}_dir-{dir}{part_entity}{run_entity}_epi"
    )
    func = create_key(
        "sub-{subject}/{session}/func/sub-{subject}_{session}"
        "_task-{task}{part_entity}{run_entity}_bold"
    )
    sbref = create_key(
        "sub-{subject}/{session}/func/sub-{subject}_{session}_task-{task}{run_entity}_sbref"
    )

    info = {t1w: [], t2w: [], dwi: [], mag: [], phdiff: [], epi: [], func: [], sbref: []}
    epi_desc = []
    bold_desc = []

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """

        # Ignore derived data and reports
        if (
            s.is_derived == "True"
            or s.is_derived is True
            or s.dcm_dir_name.split("_")[-1] in IGNORE_PROTOCOLS
        ):
            continue

        thisitem = {
            "item": s.series_id,
        }
        thiskey = None
        thisitem.update({k: v for k, v in bids_regex.findall(s.protocol_name)})
        thisitem["run_entity"] = f"{thisitem.pop('run', '')}"

        if "T1w" in s.protocol_name:
            thiskey = t1w
            thisitem["acquisition"] = (
                "original" if s.dcm_dir_name.endswith("_ND") else "undistorted"
            )
        elif "T2w" in s.protocol_name:
            thiskey = t2w
        elif s.protocol_name.startswith("dwi-dwi"):
            thiskey = dwi
        elif s.protocol_name.startswith("fmap-phasediff"):
            thiskey = phdiff if "P" in s.image_type else mag
        elif s.protocol_name.startswith("fmap-epi"):
            thiskey = epi
            thisitem["acquisition"] = "b0" if s.sequence_name.endswith("ep_b0") else "bold"

            # Check whether phase was written out
            thisdesc = s.series_id.split("-", 1)[-1]
            if thisdesc in epi_desc:
                thisitem["part_entity"] = "_part-phase"
                info[thiskey][epi_desc.index(thisdesc)]["part_entity"] = "_part-mag"
            else:
                thisitem["part_entity"] = ""

            epi_desc.append(thisdesc)

        elif s.protocol_name.startswith("func-bold"):
            # Likely an error
            if s.series_files < 100:
                warn(f"Dropping exceedingly short BOLD file with {s.series_files} time points.")
                continue

            thiskey = func

            # Check whether phase was written out
            thisdesc = s.series_id.split("-", 1)[-1]
            if thisdesc in bold_desc:
                thisitem["part_entity"] = "_part-phase"
                info[thiskey][bold_desc.index(thisdesc)]["part_entity"] = "_part-mag"
            else:
                thisitem["part_entity"] = ""

            bold_desc.append(thisdesc)

        if thiskey is not None:
            info[thiskey].append(thisitem)

    for mod, items in info.items():
        if len(items) < 2:
            continue

        info[mod] = _assign_run_on_repeat(items)

    return info


def _assign_run_on_repeat(modality_items):
    """
    Assign run IDs for repeated inputs for a given modality.

    Examples
    --------
    >>> _assign_run_on_repeat([
    ...     {"item": "discard1", "acq": "bold", "dir": "PA"},
    ...     {"item": "discard2", "acq": "bold", "dir": "AP"},
    ...     {"item": "discard3", "acq": "bold", "dir": "PA"},
    ... ])  # doctest: +NORMALIZE_WHITESPACE
    [{'item': 'discard1', 'acq': 'bold', 'dir': 'PA', 'run_entity': '_run-1'},
     {'item': 'discard2', 'acq': 'bold', 'dir': 'AP'},
     {'item': 'discard3', 'acq': 'bold', 'dir': 'PA', 'run_entity': '_run-2'}]

    >>> _assign_run_on_repeat([
    ...     {"item": "discard1", "acq": "bold", "dir": "PA"},
    ...     {"item": "discard2", "acq": "bold", "dir": "AP"},
    ...     {"item": "discard3", "acq": "bold", "dir": "PA"},
    ...     {"item": "discard4", "acq": "bold", "dir": "AP"},
    ... ])  # doctest: +NORMALIZE_WHITESPACE
    [{'item': 'discard1', 'acq': 'bold', 'dir': 'PA', 'run_entity': '_run-1'},
     {'item': 'discard2', 'acq': 'bold', 'dir': 'AP', 'run_entity': '_run-1'},
     {'item': 'discard3', 'acq': 'bold', 'dir': 'PA', 'run_entity': '_run-2'},
     {'item': 'discard4', 'acq': 'bold', 'dir': 'AP', 'run_entity': '_run-2'}]

    >>> _assign_run_on_repeat([
    ...     {"item": "discard1", "acq": "bold", "dir": "PA", "run": "1"},
    ...     {"item": "discard2", "acq": "bold", "dir": "AP"},
    ...     {"item": "discard3", "acq": "bold", "dir": "PA", "run": "2"},
    ... ])  # doctest: +NORMALIZE_WHITESPACE
    [{'item': 'discard1', 'acq': 'bold', 'dir': 'PA', 'run': '1'},
     {'item': 'discard2', 'acq': 'bold', 'dir': 'AP'},
     {'item': 'discard3', 'acq': 'bold', 'dir': 'PA', 'run': '2'}]

    >>> _assign_run_on_repeat([
    ...     {"item": "discard1", "acq": "bold", "dir": "PA", "run_entity": "_run-1"},
    ...     {"item": "discard2", "acq": "bold", "dir": "AP"},
    ...     {"item": "discard3", "acq": "bold", "dir": "PA", "run_entity": "_run-2"},
    ... ])  # doctest: +NORMALIZE_WHITESPACE
    [{'item': 'discard1', 'acq': 'bold', 'dir': 'PA', 'run_entity': '_run-1'},
     {'item': 'discard2', 'acq': 'bold', 'dir': 'AP'},
     {'item': 'discard3', 'acq': 'bold', 'dir': 'PA', 'run_entity': '_run-2'}]

    >>> _assign_run_on_repeat([
    ...     {"item": "discard1", "acq": "bold", "dir": "PA", "part_entity": "_part-mag"},
    ...     {"item": "discard2", "acq": "bold", "dir": "PA", "part_entity": "_part-phase"},
    ...     {"item": "discard3", "acq": "bold", "dir": "AP", "part_entity": "_part-mag"},
    ...     {"item": "discard4", "acq": "bold", "dir": "AP", "part_entity": "_part-phase"},
    ... ])  # doctest: +NORMALIZE_WHITESPACE
    [{'item': 'discard1', 'acq': 'bold', 'dir': 'PA', 'part_entity': '_part-mag'},
     {'item': 'discard2', 'acq': 'bold', 'dir': 'PA', 'part_entity': '_part-phase'},
     {'item': 'discard3', 'acq': 'bold', 'dir': 'AP', 'part_entity': '_part-mag'},
     {'item': 'discard4', 'acq': 'bold', 'dir': 'AP', 'part_entity': '_part-phase'}]

    """
    modality_items = modality_items.copy()

    str_patterns = [
        "_".join([
            f"{s[0]}-{s[1]}" for s in item.items() if s[0] != "item"
        ])
        for item in modality_items
    ]
    strcount = Counter(str_patterns)

    for string, count in strcount.items():
        if count < 2:
            continue

        runid = 1

        for index, item_string in enumerate(str_patterns):
            if string == item_string:
                modality_items[index].update({
                    "run_entity": f"_run-{runid}",
                })
                runid += 1

    return modality_items


def parse_series_spec(series_spec: str) -> dict[str, str]:
    """Parse protocol name according to our convention with minimal set of fixups"""
    series_spec = series_spec.replace("t1_mprage_pre_Morpho", "anat-T1w__mprage_morpho")
    series_spec = series_spec.replace(
        "micro_struct_137dir_BIPOLAR_b3000_1.6mm-iso",
        "dwi-dwi_acq-highres__137dir_bipolar",
    )
    series_spec = series_spec.replace(
        "micro_struct_137dir_BIPOLAR_b3000_1.6mm-iso",
        "dwi-dwi_acq-highres__137dir_bipolar",
    )
    series_spec = series_spec.replace(
        "micro_struct_137dir_BIPOLAR_b3000_2mm-iso",
        "dwi-dwi_acq-lowres__137dir_bipolar",
    )
    series_spec = series_spec.replace(
        "gre_field_mapping_1.6mmiso",
        "fmap-phasediff__gre",
    )

    series_spec = series_spec.replace(
        "cmrr_mbep2d_bold_me4_sms4_fa75_750meas",
        "func-bold_task-rest__750meas",
    )

    series_spec = series_spec.replace(
        "cmrr_mbep2d_bold_me4_sms4_fa80",
        "func-bold_task-rest_acq-fa80__cmrr",
    )

    series_spec = series_spec.replace(
        "cmrr_mbep2d_bold_me4_testJB",
        "func-bold_task-rest_acq-testJB__cmrr",
    )

    series_spec = series_spec.replace(
        "cmrr_mbep2d_bold_fmap_fa80",
        "fmap-epi_acq-bold__cmrr_mbepd2d_fa80",
    )

    series_spec = series_spec.replace(
        "cmrr_mbep2d_bold_me4_sms4",
        "func-bold_task-qct__cmrr",
    )

    series_spec = series_spec.replace("AAHead_Scout", "anat-scout")

    # Parse the name according to our convention/specification

    # leading or trailing spaces do not matter
    series_spec = series_spec.strip(" ")

    # Strip off leading CAPITALS: prefix to accommodate some reported usecases:
    # https://github.com/ReproNim/reproin/issues/14
    # where PU: prefix is added by the scanner
    series_spec = re.sub("^[A-Z]*:", "", series_spec)
    series_spec = re.sub("^WIP ", "", series_spec)  # remove Philips WIP prefix

    # Remove possible suffix we don't care about after __
    series_spec = series_spec.split("__", 1)[0]

    bids = False  # we don't know yet for sure
    # We need to figure out if it is a valid bids
    split = series_spec.split("_")
    prefix = split[0]

    # Fixups
    if prefix == "scout":
        prefix = split[0] = "anat-scout"

    if prefix != "bids" and "-" in prefix:
        prefix, _ = prefix.split("-", 1)
    if prefix == "bids":
        bids = True  # for sure
        split = split[1:]

    def split2(s: str) -> tuple[str, Optional[str]]:
        # split on - if present, if not -- 2nd one returned None
        if "-" in s:
            a, _, b = s.partition("-")
            return a, b
        return s, None

    # Let's analyze first element which should tell us sequence type
    datatype, datatype_suffix = split2(split[0])
    if datatype not in KNOWN_DATATYPES:
        # It is not something we don't consume
        if bids:
            lgr.warning(
                "It was instructed to be BIDS datatype but unknown "
                "%s found. Known are: %s",
                datatype,
                ", ".join(KNOWN_DATATYPES),
            )
        return {}

    regd = dict(datatype=datatype)
    if datatype_suffix:
        regd["datatype_suffix"] = datatype_suffix
    # now go through each to see if one which we care
    bids_leftovers = []
    for s in split[1:]:
        key, value = split2(s)
        if value is None and key[-1] in "+=":
            value = key[-1]
            key = key[:-1]

        # sanitize values, which must not have _ and - is undesirable ATM as well
        # TODO: BIDSv2.0 -- allows "-" so replace with it instead
        value = (
            str(value)
            .replace("_", "X")
            .replace("-", "X")
            .replace("(", "{")
            .replace(")", "}")
        )  # for Philips

        if key in ["ses", "run", "task", "acq", "dir"]:
            # those we care about explicitly
            regd[{"ses": "session"}.get(key, key)] = sanitize_str(value)
        else:
            bids_leftovers.append(s)

    if bids_leftovers:
        regd["bids"] = "_".join(bids_leftovers)

    # TODO: might want to check for all known "standard" BIDS suffixes here
    # among bids_leftovers, thus serve some kind of BIDS validator

    # if not regd.get('datatype_suffix', None):
    #     # might need to assign a default label for each datatype if was not
    #     # given
    #     regd['datatype_suffix'] = {
    #         'func': 'bold'
    #     }.get(regd['datatype'], None)

    return regd
