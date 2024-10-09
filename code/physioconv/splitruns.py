# Copyright 2024 The Axon Lab <theaxonlab@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#

from __future__ import annotations

import argparse
from pathlib import Path
from json import loads
from sys import exit
import numpy as np
import nibabel as nb
import pandas as pd
from datetime import timezone
import h5py

from bioread import read_file

# Default paths
DATA_PATH = Path("/data/datasets/hcph-pilot-sourcedata/recordings/BIOPAC")
BIDS_PATH = Path("/data/datasets/hcph")


def _get_length(filepath: Path) -> float:
    """
    Calculate the length of the run based on the metadata and file size.

    Parameters
    ----------
    filepath : Path
        The path to the NIfTI file.

    Returns
    -------
    float
        The length of the scan in seconds.

    """

    sidecar_fname = filepath.name.replace(".nii.gz", ".json").replace("_part-mag", "")
    sidecar = filepath.parent / sidecar_fname
    meta = loads(sidecar.read_text())
    if "RepetitionTime" not in meta:
        global_name = sidecar.name.split("_", 2)[-1]
        meta |= loads((sidecar.parents[3] / global_name).read_text())

    size = nb.load(filepath).shape[-1]
    return size * meta["RepetitionTime"]


def main(
    participant: str,
    session: str,
    data_path: Path = DATA_PATH,
    bids_path: Path = BIDS_PATH,
) -> list[Path]:
    """
    Process the scan and physiological data for the given participant and session.

    Parameters
    ----------
    participant : str
        The participant identifier (subject id).
    session : int
        The session number.
    data_path : Path, optional
        The path to the data files (default is DATA_PATH).
    bids_path : Path, optional
        The path to the BIDS dataset (default is BIDS_PATH).

    Returns
    -------
    Path
        The path to the generated HDF5 file.

    """
    scans_lookup = pd.read_csv(
        bids_path / "code" / "scans.tsv", sep="\t", na_values="n/a"
    )
    scans_lookup["acq_time"] = pd.to_datetime(scans_lookup.acq_time)
    scans_row = scans_lookup[
        scans_lookup.filename.str.startswith(f"sub-{participant}/ses-{session}/dwi")
    ]

    run_names = scans_lookup[
        (
            scans_lookup.filename.str.startswith(f"sub-{participant}/ses-{session}/dwi")
            | (
                scans_lookup.filename.str.startswith(
                    f"sub-{participant}/ses-{session}/func"
                )
                & scans_lookup.filename.str.contains("_echo-1_part-mag")
            )
        )
    ].filename.values.tolist()

    # BIDS: get onset and length for runs
    bids_start = np.array(
        [
            scans_lookup[scans_lookup.filename.str.contains(_rn)].acq_time.values[0]
            for _rn in run_names
        ],
        dtype=np.datetime64,
    )
    bids_lengths = np.array(
        [int(round(_get_length(bids_path / p) * 1e9)) for p in run_names],
        dtype="timedelta64[ns]",
    )

    # Extract AcqKnowledge metadata
    physio_path = scans_row.physio_files.values[0].split(",")[0]
    session_data = read_file(str(data_path / physio_path))
    recording_start = np.datetime64(
        str(
            session_data.event_markers[0]
            .date_created_utc.replace(tzinfo=timezone.utc)
            .astimezone(tz=None)
        ).split("+")[0]
    )

    # Calculate onsets and offsets
    run_onsets = (bids_start - recording_start) / np.timedelta64(1, "s")
    run_offsets = (bids_start - recording_start + bids_lengths) / np.timedelta64(1, "s")

    channels = session_data.channels

    clip_onsets = [0] + (run_onsets[1:] - 5.0).tolist()
    clip_offsets = (run_onsets[1:] - 1.0).tolist() + [-1]

    out_files = []
    for run_id, (clip_on, clip_off) in enumerate(zip(clip_onsets, clip_offsets)):
        run_name = (
            Path(run_names[run_id])
            .name.replace("_echo-1_part-mag", "")
            .rsplit("_", 1)[0]
        )
        h5_filename = data_path / f"{run_name}_physio.hdf5"
        with h5py.File(h5_filename, "w") as h5f:
            h5f.attrs["start_recording"] = np.datetime_as_string(
                recording_start,
                timezone="local",
            ).astype("S30")
            h5f.attrs["start_run"] = run_onsets[run_id]
            h5f.attrs["stop_run"] = run_offsets[run_id]

            for i, ch in enumerate(channels):
                onset_index = (
                    0 if clip_on == 0 else np.abs(ch.time_index - clip_on).argmin()
                )
                offset_index = (
                    -1 if clip_off == -1 else np.abs(ch.time_index - clip_off).argmin()
                )

                ch_group = h5f.create_group(f"channel_{i}")
                ch_group.attrs["name"] = ch.name
                ch_group.attrs["units"] = ch.units
                ch_group.attrs["frequency"] = ch.samples_per_second
                ch_group.attrs["start_time"] = round(ch.time_index[onset_index], 6)
                ch_group.create_dataset(
                    "data",
                    data=ch.data[onset_index:offset_index],
                    compression="gzip",
                    compression_opts=9,
                )

        print(f"Generated: {h5_filename}")
        out_files.append(h5_filename)

    return out_files


def parse_session(session: str | int) -> str:
    """
    Parse the session argument to allow integers or strings.
    If the session argument starts with 'ses-', the prefix is removed.

    Parameters:
    -----------
    session : str
        The session identifier (could be an integer or string).

    Returns:
    --------
    str
        The cleaned session identifier without 'ses-' prefix.
    """
    if isinstance(session, int):
        return f"{session:03d}"

    # Remove 'ses-' prefix if present
    return session[4:] if session.startswith("ses-") else session


def parse_args():
    """
    Parse command line arguments.

    Returns:
    --------
    argparse.Namespace
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process physiological data for a BIDS dataset."
    )
    parser.add_argument("participant", type=str, help="Participant ID")
    parser.add_argument(
        "session",
        type=parse_session,
        help="Session identifier (can be an integer or string).",
    )
    parser.add_argument(
        "--data_path",
        type=Path,
        default=DATA_PATH,
        help="Path to BIOPAC .acq files (default: %(default)s)",
    )
    parser.add_argument(
        "--bids_path",
        type=Path,
        default=BIDS_PATH,
        help="Path to BIDS dataset (default: %(default)s)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if not (
        session_path := args.bids_path
        / f"sub-{args.participant}"
        / f"ses-{args.session}"
    ).exists():
        print(f"Skipping {session_path} (missing).")
        exit(1)

    main(args.participant, args.session, args.data_path, args.bids_path)
