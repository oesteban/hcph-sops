import argparse
import logging

import os
import os.path as op

import matplotlib.pyplot as plt
import numpy as np

from bids import BIDSLayout
from bids.layout import parse_file_entities
from bids.layout.writing import build_path

from nilearn.datasets import fetch_atlas_difumo
from nilearn.maskers import MultiNiftiMapsMasker
from nilearn.interfaces.fmriprep import load_confounds

from nilearn.connectome import ConnectivityMeasure, vec_to_sym_matrix
from sklearn.covariance import GraphicalLassoCV, LedoitWolf

from nilearn.plotting import plot_design_matrix, plot_matrix

FC_PATTERN = [
    "sub-{subject}[/ses-{session}]/func/sub-{subject}"
    "[_ses-{session}][_task-{task}][_meas-{meas}]"
    "_{suffix}{extension}"
]
FC_FILLS = {"suffix": "relmat", "meas": "sparseinversecovariance",
            "extension": ".tsv"}
TIMESERIES_PATTERN = [
    "sub-{subject}[/ses-{session}]/func/sub-{subject}"
    "[_ses-{session}][_task-{task}][_desc-{desc}]"
    "_{suffix}{extension}"
]
TIMESERIES_FILLS = {"desc": "denoised", "extension": ".tsv"}
FIGURE_PATTERN = [
    "sub-{subject}/figures/sub-{subject}[_ses-{session}]"
    "[_task-{task}][_meas-{meas}][_desc-{desc}]"
    "_{suffix}{extension}",
    "sub-{subject}/figures/sub-{subject}[_ses-{session}]"
    "[_task-{task}][_desc-{desc}]_{suffix}{extension}",
]
# TS_FIGURE_PATTERN = ['sub-{subject}/figures/sub-{subject}[_ses-{session}]'
#                  '[_task-{task}][_desc-{desc}]_{suffix}{extension}']
FIGURE_FILLS = {"extension": "png"}

TS_FIGURE_SIZE = (50, 25)
FC_FIGURE_SIZE = (50, 40)


def get_arguments():
    parser = argparse.ArgumentParser(
        description="""Compute functional connectivity matrices from fmriprep
                    output directory.""",
        # formatter_class=argparse.RawTextHelpFormatter
    )

    # Input/Output arguments and options
    parser.add_argument("data_dir")
    parser.add_argument("-s", "--save", action="store_true", default=False)
    parser.add_argument("-o", "--output", default=None)

    # Script specific options
    parser.add_argument("--overwrite", default=False, action="store_true")
    parser.add_argument("--task", default=[], action="store", nargs="+")

    # fMRI and denoising specific options
    parser.add_argument("--denoise-only", default=False, action="store_true")
    parser.add_argument("--atlas-dimension", default=64, type=int)
    parser.add_argument("--low-pass", default=0.15, action="store", type=float)
    parser.add_argument("--FD-thresh", default=0.4, action="store", type=float)
    parser.add_argument("--SDVARS-thresh", default=3, action="store", type=float)
    parser.add_argument("--n-scrub-frames", default=5, action="store", type=int)
    parser.add_argument(
        "--fc-estimator", default="sparse inverse covariance", action="store", type=str
    )

    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=1,
        help="""increase output verbosity (-v: standard logging
                        infos; -vv: logging infos and NiLearn verbose; -vvv:
                        debug)""",
    )

    args = parser.parse_args()

    return args


def get_func_filenames_bids(paths_to_func_dir, task_filter=[]):
    logging.debug("Using BIDS to find functional files...")

    layout = BIDSLayout(
        paths_to_func_dir,
        validate=False,
    )

    all_derivatives = layout.get(
        scope="all",
        return_type="file",
        extension="nii.gz",
        session=[15],
        suffix="bold",
        task=task_filter,
    )

    t_rs = []
    for file in all_derivatives:
        t_rs.append(layout.get_metadata(file)["RepetitionTime"])

    unique_tr_s = set(t_rs)

    if len(unique_tr_s) > 1:
        logging.warning(
            "Multiple TR values found, temporal filtering may not" " work as intended !"
        )

    return all_derivatives, list(unique_tr_s)[0]


def get_bids_savename(filename, patterns=FC_PATTERN, **kwargs):
    entity = parse_file_entities(filename)

    for key, value in kwargs.items():
        entity[key] = value

    bids_savename = build_path(entity, patterns)
    logging.debug(f"BIDS filename is :\n\t{build_path(entity, patterns)}")

    return bids_savename


def get_atlas_data(atlas_name="DiFuMo", **kwargs):
    logging.info("Fetching the DiFuMo atlas ...")

    if kwargs["dimension"] not in [64, 128, 512]:
        logging.warning(
            "Dimension for DiFuMo atlas is different from 64, 128 or 512 !"
        )

    return fetch_atlas_difumo(legacy_format=False, **kwargs)


def find_derivative(path, derivatives_name="derivatives"):
    if op.split(path)[-1] == derivatives_name:
        return path
    if op.split(path)[0] == "":
        logging.error(f'"{derivatives_name}" could not be found on path !')
        return ""
    return find_derivative(path=op.split(path)[0])


def check_existing_output(output, func_filename, return_existing=False, **kwargs):
    logging.debug("\n\t".join(func_filename))

    missing_data_filter = [
        not op.exists(op.join(output, get_bids_savename(filename, **kwargs)))
        for filename in func_filename
    ]

    missing_data = np.array(func_filename)[missing_data_filter]
    logging.debug(f"\t{sum(missing_data_filter)} missing data found")
    logging.debug("\n\t".join(missing_data))

    if return_existing:
        existing_data = np.array(func_filename)[
            [not fltr for fltr in missing_data_filter]
        ]
        return missing_data.tolist(), existing_data.tolist()
    return missing_data.tolist()


def load_timeseries(func_filename, output):
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


def extract_timeseries(
    func_filename,
    atlas_filename,
    masker=None,
    verbose=2,
    interpolate=False,
    low_pass=None,
    t_r=None,
    **kwargs,
):
    if not len(func_filename):
        return [], []

    logging.info(f"Extracting and denoising timeseries for {len(func_filename)} files.")
    logging.debug(f"Denoising parameters are: {kwargs}")

    masker = MultiNiftiMapsMasker(
        maps_img=atlas_filename,
        low_pass=low_pass,
        t_r=t_r,
        standardize="zscore_sample",
        verbose=verbose,
        reports=True,
        n_jobs=2,
    )

    # TODO remove unnecessary entities from BIDS name to ensute "load_confounds"
    # is able to find the confounds file (due to a bug in NiLearn).

    confounds, sample_mask = load_confounds(
        func_filename,
        demean=False,
        strategy=["high_pass", "motion", "scrub"],
        motion="basic",
        **kwargs,
    )

    # The outputs of "load_confounds" will not be in a list if
    # "func_filename" is a list with one element.
    if not isinstance(confounds, list):
        confounds = [confounds]
    if not isinstance(sample_mask, list):
        sample_mask = [sample_mask]

    if interpolate:
        # TODO: implement cubicBspline interpolation independantly to
        # avoid censoring frames with high motion
        # use "signal._interpolate_volumes(volumes, sample_mask, t_r)"
        pass
    else:
        time_series = masker.fit_transform(
            func_filename, confounds=confounds, sample_mask=sample_mask
        )

    return time_series, confounds


def compute_connectivity(
    time_series, strategy="sparse inverse covariance", verbose=False
):
    n_ts = len(time_series)
    n_area = time_series[0].shape[-1]
    logging.info(
        f"Computing functional connectivity matrices for {n_ts} timeseries ..."
    )

    connectivity_kind = "correlation"
    FC_FILLS["meas"] = "correlation"
    FIGURE_FILLS["meas"] = "correlation"
    estimator = LedoitWolf(store_precision=False)

    if strategy not in ["cor", "corr", "correlation"]:
        connectivity_kind = "precision"
        FC_FILLS["meas"] = "sparseinversecovariance"
        FIGURE_FILLS["meas"] = "sparseinversecovariance"
        estimator = GraphicalLassoCV(alphas=6, max_iter=1000)  # , verbose=verbose)

        if strategy not in ["sparse", "sparse inverse covariance"]:
            connectivity_kind = "covariance"
            FC_FILLS["meas"] = "covariance"
            FIGURE_FILLS["meas"] = "covariance"

    logging.info(f'\tUsing the "{FIGURE_FILLS["meas"]}" measurement.')

    connectivity_estimator = ConnectivityMeasure(
        cov_estimator=estimator,
        kind=connectivity_kind,
        vectorize=True,
        discard_diagonal=True,
    )
    connectivity_measures = connectivity_estimator.fit_transform(time_series)
    return vec_to_sym_matrix(connectivity_measures, diagonal=np.zeros((n_ts, n_area)))


def plot_timeseries(
    timeseries,
    labels=None,
    normalize=False,
    plot_type="signal",
    vert_scale=5,
    margin_value=0.01,
):
    _, ax = plt.subplots(figsize=TS_FIGURE_SIZE)

    n_timepoints, n_area = timeseries.shape

    timeseries_to_show = timeseries.copy()
    if normalize:
        timeseries_to_show = (timeseries - timeseries.mean(axis=0)) / (
            timeseries.std(axis=0)
        )

    ax.set_xlabel("time")

    if "carpet" in plot_type.lower():
        ax.set_yticks(np.arange(n_area))
        ax.set_yticklabels(labels)
        image = ax.imshow(
            timeseries_to_show.T,
            cmap="binary_r",
            aspect="auto",
            interpolation="antialiased",
        )
        plt.colorbar(image, pad=0, aspect=40)

    if "signal" in plot_type.lower():
        x_plot = np.arange(n_timepoints)
        for i, roi_signal in enumerate(timeseries_to_show.T):
            ax.plot(x_plot, i * vert_scale + roi_signal, color="tab:blue", linewidth=2)

        # ax.set_xlabel('time')
        ax.set_yticks(np.arange(n_area) * vert_scale)
        ax.set_yticklabels(labels)
        ax.grid(visible=True, axis="y")
        ax.margins(x=margin_value, y=margin_value)


def visual_report_timeserie(timeseries, filename, output, confounds=None, **kwargs):
    # Plotting denoised and aggregated timeseries
    for plot_type, plot_desc in zip(["carpet", "signal"], ["carpetplot", "timeseries"]):
        ts_saveloc = get_bids_savename(
            filename, patterns=FIGURE_PATTERN, desc=plot_desc, **FIGURE_FILLS
        )
        plot_timeseries(timeseries, plot_type=plot_type, **kwargs)

        logging.debug("Saving timeseries visual report at:")
        logging.debug(f"\t{op.join(output, ts_saveloc)}")
        os.makedirs(op.join(output, op.dirname(ts_saveloc)), exist_ok=True)
        plt.savefig(op.join(output, ts_saveloc))

    # Plotting confounds as a design matrix
    if confounds is not None:
        conf_saveloc = get_bids_savename(
            filename, patterns=FIGURE_PATTERN, desc="designmatrix", **FIGURE_FILLS
        )

        _, ax = plt.subplots(figsize=TS_FIGURE_SIZE)
        plot_design_matrix(confounds, ax=ax)
        logging.debug("Saving confounds visual report at:")
        logging.debug(f"\t{op.join(output, conf_saveloc)}")

        plt.savefig(op.join(output, conf_saveloc))


def visual_report_fc(matrix, filename, output, labels=None):
    fc_saveloc = get_bids_savename(
        filename, patterns=FIGURE_PATTERN, desc="heatmap", **FIGURE_FILLS
    )
    fig, ax = plt.subplots(figsize=FC_FIGURE_SIZE)

    plot_matrix(matrix, labels=list(labels), axes=ax, vmin=-1, vmax=1)

    logging.debug("Saving functional connectivity matrices visual report at:")
    logging.debug(f"\t{op.join(output, fc_saveloc)}")

    plt.savefig(op.join(output, fc_saveloc))


def save_output(data_list, original_filenames, output=None, **kwargs):
    for data, filename in zip(data_list, original_filenames):
        path_to_save = get_bids_savename(filename, **kwargs)
        saveloc = op.join(output, path_to_save)
        logging.debug(f"Saving data of type {type(data)} to: {saveloc}")
        os.makedirs(op.dirname(saveloc), exist_ok=True)
        np.savetxt(saveloc, data, delimiter="\t")


def main():
    args = get_arguments()

    input_path = args.data_dir
    save = args.save
    output = args.output

    task_filter = args.task
    overwrite = args.overwrite

    # denoise_only = args.denoise_only
    atlas_dimension = args.atlas_dimension
    low_pass = args.low_pass
    fd_threshold = args.FD_thresh
    std_dvars_threshold = args.SDVARS_thresh
    scrub = args.n_scrub_frames
    fc_estimator = args.fc_estimator

    verbosity_level = args.verbosity
    nilearn_verbose = verbosity_level - 1

    logging_level_map = {
        0: logging.WARN,
        1: logging.INFO,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    logging.basicConfig(
        # filename='example.log',
        # format='%(asctime)s %(levelname)s:%(message)s',
        format="%(levelname)s: %(message)s",
        level=logging_level_map[min([verbosity_level, 3])],
    )

    logging.captureWarnings(True)

    func_filenames, t_r = get_func_filenames_bids(input_path, task_filter=task_filter)
    logging.info(f"Found {len(func_filenames)} functional file(s):")
    logging.info(
        "\t" + "\n\t".join([op.basename(filename) for filename in func_filenames])
    )

    atlas_data = get_atlas_data(dimension=atlas_dimension)
    atlas_filename = getattr(atlas_data, "maps")
    atlas_labels = getattr(atlas_data, "labels").loc[:, "difumo_names"]
    # atlas_net7 = getattr(atlas_data, "labels").loc[:, "yeo_networks7"]
    # atlas_net17 = getattr(atlas_data, "labels").loc[:, "yeo_networks17"]

    if output is None:
        output = op.join(find_derivative(input_path), "functional_connectivity")
    logging.info(f"Output will be save as derivatives in:\n\t{output}")

    # By default, the timeseries and FC of all filenames in input will be computed
    missing_ts = missing_output = func_filenames.copy()
    existing_timeseries = []
    if not overwrite:
        logging.debug("Looking for existing timeseries ...")
        missing_ts, existing_ts = check_existing_output(
            output,
            func_filenames,
            return_existing=True,
            patterns=TIMESERIES_PATTERN,
            **TIMESERIES_FILLS,
        )

        logging.info(f"{len(missing_ts)} files are missing timeseries.")
        logging.debug("Looking for existing fc matrices ...")
        missing_only_fc = check_existing_output(
            output, existing_ts, patterns=FC_PATTERN, **FC_FILLS
        )
        missing_output = missing_ts + missing_only_fc
        logging.info(f"{len(missing_output)} files are missing FC matrices.")
        existing_timeseries = load_timeseries(missing_only_fc, output)

    time_series, all_confounds = extract_timeseries(
        missing_ts,
        atlas_filename,
        verbose=nilearn_verbose,
        t_r=t_r,
        low_pass=low_pass,
        fd_threshold=fd_threshold,
        std_dvars_threshold=std_dvars_threshold,
        scrub=scrub,
    )

    if save and len(time_series):
        logging.info("Saving timeseries ...")
        os.makedirs(output, exist_ok=True)
        save_output(
            time_series,
            missing_ts,
            output,
            patterns=TIMESERIES_PATTERN,
            **TIMESERIES_FILLS,
        )

        for individual_time_serie, confounds, filename in zip(
            time_series, all_confounds, missing_ts
        ):
            visual_report_timeserie(
                individual_time_serie,
                filename=filename,
                output=output,
                confounds=confounds,
                labels=atlas_labels,
            )
    else:
        # TESTING VISUAL REPORTS
        for individual_time_serie, filename in zip(existing_timeseries, func_filenames):
            visual_report_timeserie(
                individual_time_serie,
                filename=filename,
                output=output,
                confounds=None,
                labels=atlas_labels,
            )

    fc_matrices = compute_connectivity(
        time_series + existing_timeseries, strategy=fc_estimator
    )

    if save:
        logging.info("Saving connectivity matrices ...")
        save_output(
            fc_matrices, missing_output, output, patterns=FC_PATTERN, **FC_FILLS
        )

        for individual_matrix, filename in zip(fc_matrices, missing_output):
            visual_report_fc(
                individual_matrix, filename=filename, output=output, labels=atlas_labels
            )
    else:
        # TESTING VISUAL REPORTS
        for individual_matrix, filename in zip(fc_matrices, missing_output):
            visual_report_fc(
                individual_matrix, filename=filename, output=output, labels=atlas_labels
            )

    logging.info(
        f"Computation is done for {len(missing_output)} files out of the "
        f"{len(func_filenames)} provided."
    )
    logging.info("Functional connectivity finished successfully !")


if __name__ == "__main__":
    main()
