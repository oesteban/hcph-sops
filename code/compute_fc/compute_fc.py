import argparse
import logging

import os
import os.path as op

from bids import BIDSLayout

from nilearn.datasets import fetch_atlas_difumo
from nilearn.maskers import NiftiMapsMasker
from nilearn.interfaces.fmriprep import load_confounds

from nilearn.connectome import ConnectivityMeasure
from sklearn.covariance import GraphicalLassoCV

def get_arguments():
    parser = argparse.ArgumentParser(
        description="""Compute functional connectivity matrices from fmriprep
                    output directory.""",
        #formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('data_dir')
    parser.add_argument('-v', '--verbosity', action="count", default=1,
                        help="""increase output verbosity (-v: standard logging infos; 
                        -vv: logging infos and NiLearn verbose; -vvv: debug)""")
    parser.add_argument('--no-bids', action='store_true', default=False)
    parser.add_argument('--atlas-dimension', default=64)

    args = parser.parse_args()

    return args

def get_folders_w_prefix(path, prefix, stop_at_first=True):
    subfolders = os.walk(path)

    matching_dirs = []
    for root, dirs, files in subfolders:
        #logging.debug(f'Looking for "{prefix}" in {root}')
        has_sub = [subdir for subdir in dirs  if subdir.startswith(prefix)]
        if len(has_sub) > 0:
            logging.debug(f'Found {len(has_sub)} "{prefix}" folder(s) in {root}')
            matching_dirs += [op.join(root, target_dir) for target_dir in has_sub]
            if stop_at_first:
                return matching_dirs

    if len(matching_dirs) == 0:
        logging.warning(f'No folder found containing "{prefix}"')
    return matching_dirs

def find_func_files(paths_to_func_dir, suffix):
    paths_to_func_dir = list(paths_to_func_dir)

    matching_files = []
    for path in paths_to_func_dir:
        files_in_func = os.listdir(path)

        # Find filename that matches prefix
        matching_files += [op.join(path, filename) for filename in files_in_func if suffix in filename]
    
    # Filter matching files keeping only neuroimaging formats (e.g. .nii.gz)
    matching_ni = [filename for filename in matching_files if '.nii' in filename]

    logging.debug(f'Found {len(matching_ni)} matching functional file(s):')
    logging.debug('\t'+'\n\t'.join(matching_ni))
    return matching_ni

def get_func_filenames(input_path):
    logging.info(f'Manually scan the folders to find functional files...')
    logging.debug(f'Scanning for data in {input_path} subfolders')
    path_to_subs = get_folders_w_prefix(input_path, prefix='sub-')
    path_to_sessions = []

    for path_to_individual_sub in path_to_subs:
        path_to_sessions += get_folders_w_prefix(path_to_individual_sub, prefix='ses-')

    logging.debug(f'Pipeline will continue with {len(path_to_sessions)} sessions at:')
    logging.debug('\t'+'\n\t'.join(path_to_sessions))

    path_to_func = [op.join(ses, 'func') for ses in path_to_sessions]

    func_filenames = find_func_files(path_to_func, suffix='MNI152NLin2009cAsym_desc-preproc_bold')

    return func_filenames

def get_func_filenames_bids(paths_to_func_dir):
    logging.info(f'Using BIDS to find functional files...')

    layout = BIDSLayout(
        paths_to_func_dir,
        validate=False,
        )

    all_derivatives = layout.get(
        scope='all',
        return_type='file',
        extension='nii.gz',
        session=[15],
        suffix='bold'
        )

    return all_derivatives

def get_atlas_data(atlas_name='DiFuMo', **kwargs):
    logging.info(f'Fetching the DiFuMo atlas ...')
    
    if kwargs['dimension'] not in [64, 128, 512]:
        logging.warning(f'Dimension for DiFuMo atlas is different from 64, 128 or 512 !')

    return fetch_atlas_difumo(legacy_format=False, **kwargs)
    
def extract_timeseries(func_filename, atlas_filename, masker=None, verbose=2):
    if masker is None:
        masker = NiftiMapsMasker(
            maps_img=atlas_filename,
            #standardize="zscore_sample",
            #memory="nilearn_cache",
            verbose=verbose,
            )
    
    if type(func_filename) == list:
        time_serie = []
        for file_id, individual_filename in enumerate(func_filename):
            logging.info(f'Extraction of timeseries from list: {file_id+1}/{len(func_filename)} ...')
            time_serie.append(extract_timeseries(individual_filename, atlas_filename,
                                                 masker=masker, verbose=verbose))
        return time_serie

    confounds, sample_mask = load_confounds(
        func_filename,
        strategy=["high_pass", "motion", "scrub"],
        motion="basic",
        scrub=4,
        fd_threshold=0.4,
        std_dvars_threshold=10,
        )
    
    time_serie = masker.fit_transform(
        func_filename,
        confounds=confounds,
        sample_mask=sample_mask
        )
    
    return time_serie

def compute_connectivity(time_series, strategy='sparse inverse covariance'):

    if type(time_series) == list:
        fc_matrices = []
        for ts_id, individual_ts in enumerate(time_series):
            logging.info(f'Computing FC from list: {ts_id+1}/{len(time_series)} ...')
            fc_matrices.append(compute_connectivity(individual_ts, strategy=strategy))

        return fc_matrices

    estimator = GraphicalLassoCV(tol=1e-3)
    estimator.fit(time_series)
    
    if 'sparse' not in strategy.lower():
        return estimator.covariance_

    return estimator.precision_

def main():
    args = get_arguments()

    input_path = args.data_dir
    no_bids = args.no_bids
    atlas_dimension = args.atlas_dimension
    verbosity_level = args.verbosity
    nilearn_verbose = verbosity_level-1

    logging_level_map = {0:logging.WARN,
                         1:logging.INFO,
                         2:logging.INFO,
                         3:logging.DEBUG}

    logging.basicConfig(
        #filename='example.log',
        #format='%(asctime)s %(levelname)s:%(message)s',
        format='%(levelname)s: %(message)s',
        level=logging_level_map[min([verbosity_level, 3])]
    )

    if no_bids:
        func_filenames = get_func_filenames(input_path)
    else:
        func_filenames = get_func_filenames_bids(input_path)

    logging.info(f'Found {len(func_filenames)} functional file(s):')
    logging.info('\t'+'\n\t'.join([op.basename(filename) for filename in func_filenames]))

    atlas_data = get_atlas_data(dimension=atlas_dimension)
    atlas_filename = getattr(atlas_data, 'maps')
        
    #all_time_series = extract_timeseries(func_filenames, atlas_filename,
    #                                     verbose=nilearn_verbose)
    
    all_time_series = []
    for individual_time_serie in all_time_series:
        print(individual_time_serie.shape)

    #all_fc_matrices = compute_connectivity(all_time_series)
    
    all_fc_matrices = []
    for individual_matrix in all_fc_matrices:
        print(individual_matrix.shape)
    
if __name__ == "__main__":
    main()