# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2023 The Axon Lab <theaxonlab@gmail.com>
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
""" Python module for loading and saving fMRI related data"""


def separate_by_similar_values(
    input_list: list, external_value: Optional[list] = None
) -> dict:
    """This returns elements of `input_list` with similar values (optionally set by
    `external_value`) separated into sub-lists.

    Parameters
    ----------
    input_list : list
        List to be separated.
    external_value : Optional[list], optional
        Values corresponding to the elements of `input_list`, by default None

    Returns
    -------
    dict
        Dictionnary where each entry is a list of elements that have similar values and
        the keys are the value for each list.
    """
    if external_value is None:
        external_value = input_list

    data_by_value = defaultdict(list)

    for val, data in zip(external_value, input_list):
        data_by_value[val].append(data)
    return data_by_value


def get_func_filenames_bids(
    paths_to_func_dir: str,
    task_filter: list = [],
    ses_filter: list = [],
    run_filter: list = [],
) -> tuple[list[list[str]], list[float]]:
    """Return the BIDS functional imaging files matching the specified task and session
    filters as well as the first (if multiple) unique repetition time (TR).

    Parameters
    ----------
    paths_to_func_dir : str
        Path to the BIDS (usually derivatives) directory
    task_filter : list, optional
        List of task name(s) to consider, by default []
    ses_filter : list, optional
        List of session name(s) to consider, by default []
    run_filter : list, optional
        List of run(s) to consider, by default []

    Returns
    -------
    tuple[list[list[str]], list[float]]
        Returns two lists with: a list of sorted filenames and a list of TRs.
    """
    logging.debug("Using BIDS to find functional files...")

    layout = BIDSLayout(
        paths_to_func_dir,
        validate=False,
    )

    all_derivatives = layout.get(
        scope="all",
        return_type="file",
        extension=["nii.gz", "gz"],
        suffix="bold",
        task=task_filter,
        session=ses_filter,
        run=run_filter,
    )

    affines = []
    for file in all_derivatives:
        affines.append(loadsave.load(file).affine)

    similar_fov_dict = separate_by_similar_values(
        all_derivatives, np.array(affines)[:, 0, 0]
    )
    if len(similar_fov_dict) > 1:
        logging.warning(
            f"{len(similar_fov_dict)} different FoV found ! "
            "Files with similar FoV will be computed together. "
            "Computation time may increase."
        )

    separated_files = []
    separated_trs = []
    for file_group in similar_fov_dict.values():
        t_rs = []
        for file in file_group:
            t_rs.append(layout.get_metadata(file)["RepetitionTime"])

        similar_tr_dict = separate_by_similar_values(file_group, t_rs)
        separated_files += list(similar_tr_dict.values())
        separated_trs += list(similar_tr_dict.keys())

        if len(similar_tr_dict) > 1:
            logging.warning(
                "Multiple TR values found ! "
                "Files with similar TR will be computed together. "
                "Computation time may increase."
            )

    return separated_files, separated_trs


def get_bids_savename(filename: str, patterns: list = FC_PATTERN, **kwargs) -> str:
    """Return the BIDS filename following the specified patterns and modifying the
    entities from the keywords arguments.

    Parameters
    ----------
    filename : str
        Name of the original BIDS file
    patterns : list, optional
        Patterns for the output file, by default FC_PATTERN

    Returns
    -------
    str
        BIDS output filename.
    """
    entity = parse_file_entities(filename)

    for key, value in kwargs.items():
        entity[key] = value

    bids_savename = build_path(entity, patterns)

    return bids_savename


def get_atlas_data(atlas_name: str = "DiFuMo", **kwargs) -> dict:
    """Fetch the specifies atlas filename and data.

    Parameters
    ----------
    atlas_name : str, optional
        Name of the atlas to fetch, by default "DiFuMo"

    Returns
    -------
    dict
        Dictionnary with keys "maps" (filename) and "labels" (ROI labels).
    """
    logging.info("Fetching the DiFuMo atlas ...")

    if kwargs["dimension"] not in [64, 128, 512]:
        logging.warning(
            "Dimension for DiFuMo atlas is different from 64, 128 or 512 ! Are you"
            "certain you want to deviate from those optimized modes? "
        )

    return fetch_atlas_difumo(legacy_format=False, **kwargs)


def find_derivative(path: str, derivatives_name: str = "derivatives") -> str:
    """Find the corresponding BIDS derivative folder (if existing, otherwise it will be
    created).

    Parameters
    ----------
    path : str
        Path to the BIDS (usually derivatives) dataset.
    derivatives_name : str, optional
        Name of the derivatives folder, by default "derivatives"

    Returns
    -------
    str
        Absolute path to the derivative folder.
    """
    splitted_path = path.split("/")
    if derivatives_name in splitted_path:
        while splitted_path[-1] != derivatives_name:
            splitted_path.pop()
        return "/".join(splitted_path)
    logging.warning(
        f'"{derivatives_name}" could not be found on path - '
        f'creating at: {op.join(path, derivatives_name)}"'
    )
    return op.join(path, derivatives_name)


def check_existing_output(
    output: str, func_filename: list[str], return_existing: bool = False, **kwargs
) -> tuple[list[str], list[str]]:
    """Check for existing output.

    Parameters
    ----------
    output : str
        Path to the output directory
    func_filename : list[str]
        Original file to be computed in the futur
    return_existing : bool, optional
        Condition to return a boolean filter with True for existing data, by default
        False

    Returns
    -------
    tuple[list[str], list[str]]
        Boolean filter with True for missing data (optionally, a second filter with
        existing data)
    """

    missing_data_filter = [
        not op.exists(op.join(output, get_bids_savename(filename, **kwargs)))
        for filename in func_filename
    ]

    missing_data = np.array(func_filename)[missing_data_filter]
    logging.debug(
        f"\t{sum(missing_data_filter)} missing data found for files:"
        "\n\t" + "\n\t".join(missing_data)
    )

    if return_existing:
        existing_data = np.array(func_filename)[
            [not fltr for fltr in missing_data_filter]
        ]
        return missing_data.tolist(), existing_data.tolist()
    return missing_data.tolist()


def load_timeseries(func_filename: list[str], output: str) -> list[np.ndarray]:
    """Load existing timeseries from .csv files.

    Parameters
    ----------
    func_filename : list[str]
        List of timeseries filenames.
    output : str
        Path to the output folder.

    Returns
    -------
    list[np.ndarray]
        List of loaded timeseries.
    """
    if len(func_filename):
        logging.info(f"Loading existing timeseries for {len(func_filename)} files ...")

    loaded_ts = []
    for filename in func_filename:
        path_to_ts = get_bids_savename(
            filename, patterns=TIMESERIES_PATTERN, **TIMESERIES_FILLS
        )
        logging.debug(f"\t{op.join(output, path_to_ts)}")
        loaded_ts.append(
            np.genfromtxt(op.join(output, path_to_ts), float, delimiter="\t")
        )

    return loaded_ts
