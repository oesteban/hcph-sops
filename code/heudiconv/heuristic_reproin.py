"""Reproin heuristic."""

from __future__ import annotations

from warnings import warn
from collections import Counter
import logging
import re

import pydicom as dcm

from heudiconv.heuristics.reproin import *

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
    "testJB",  # dismiss a test trial of the cmrr sequence
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
    "": [
        ("t1_mprage_pre_Morpho", "anat-T1w__mprage_morpho"),
        (
            "micro_struct_137dir_BIPOLAR_b3000_1.6mm-iso",
            "dwi-dwi_acq-highres_dir-unknown__137dir_bipolar",
        ),
        (
            "micro_struct_137dir_BIPOLAR_b3000_1.6mm-iso",
            "dwi-dwi_acq-highres_dir-unknown__137dir_bipolar",
        ),
        (
            "micro_struct_137dir_BIPOLAR_b3000_2mm-iso",
            "dwi-dwi_acq-lowres_dir-unknown__137dir_bipolar",
        ),
        ("gre_field_mapping_1.6mmiso", "fmap-phasediff__gre"),
        (
            "cmrr_mbep2d_bold_me4_sms4_fa75_750meas",
            "func-bold_task-rest__750meas",
        ),
        (
            "cmrr_mbep2d_bold_me4_sms4_fa80",
            "func-bold_task-rest_acq-fa80__cmrr",
        ),
        (
            "cmrr_mbep2d_bold_me4_testJB",
            "func-bold_task-rest_acq-testJB__cmrr",
        ),
        (
            "cmrr_mbep2d_bold_fmap_fa80",
            "fmap-epi_acq-bold_dir-unknown__cmrr_mbepd2d_fa80",
        ),
        ("cmrr_mbep2d_bold_me4_sms4", "func-bold_task-qct__cmrr"),
        ("_task-qc_", "_task-qct_"),
        ("AAHead_Scout", "anat-scout"),
    ]
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
    "Acknowledgements": "See README.md.",
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
    t2w = create_key(
        "sub-{subject}/{session}/anat/sub-{subject}_{session}{run_entity}_T2w"
    )
    dwi = create_key(
        "sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_dir-{dir}{run_entity}_dwi"
    )
    mag = create_key(
        "sub-{subject}/{session}/fmap/sub-{subject}_{session}{run_entity}_magnitude"
    )
    phdiff = create_key(
        "sub-{subject}/{session}/fmap/sub-{subject}_{session}{run_entity}_phasediff"
    )
    epi = create_key(
        "sub-{subject}/{session}/fmap/sub-{subject}_{session}"
        "_acq-{acquisition}_dir-{dir}{part_entity}{run_entity}_epi"
    )
    func = create_key(
        "sub-{subject}/{session}/func/sub-{subject}_{session}"
        "_task-{task}{acq_entity}{part_entity}{run_entity}_bold"
    )
    sbref = create_key(
        "sub-{subject}/{session}/func/sub-{subject}_{session}_task-{task}{run_entity}_sbref"
    )

    info = {
        t1w: [],
        t2w: [],
        dwi: [],
        mag: [],
        phdiff: [],
        epi: [],
        func: [],
        sbref: [],
    }
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
            thisitem["acquisition"] = (
                "b0" if s.sequence_name.endswith("ep_b0") else "bold"
            )

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
                warn(
                    f"Dropping exceedingly short BOLD file with {s.series_files} time points."
                )
                continue

            thiskey = func

            # Some functional runs may come with acq
            func_acq = thisitem.pop("acq", None)
            thisitem["acq_entity"] = "" if not func_acq else f"_acq-{func_acq}"

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
        "_".join([f"{s[0]}-{s[1]}" for s in item.items() if s[0] != "item"])
        for item in modality_items
    ]
    strcount = Counter(str_patterns)

    for string, count in strcount.items():
        if count < 2:
            continue

        runid = 1

        for index, item_string in enumerate(str_patterns):
            if string == item_string:
                modality_items[index].update(
                    {
                        "run_entity": f"_run-{runid}",
                    }
                )
                runid += 1

    return modality_items
