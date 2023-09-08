import argparse
import logging

import os
import os.path as op

import matplotlib.pyplot as plt

from bids import BIDSLayout
from bids.layout import parse_file_entities
from bids.layout.writing import build_path

from nilearn.datasets import fetch_atlas_difumo
from nilearn.maskers import NiftiMapsMasker
from nilearn.interfaces.fmriprep import load_confounds

from nilearn.connectome import ConnectivityMeasure
from sklearn.covariance import GraphicalLassoCV

#from nilearn.plotting import plot_design_matrix, plot_matrix

def get_arguments():
    parser = argparse.ArgumentParser(
        description="""Compute functional connectivity matrices from fmriprep
                    output directory.""",
        #formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('data_dir')
    parser.add_argument('-s', '--save', action='store_true', default=False)
    parser.add_argument('-o', '--output', default=None)
    parser.add_argument('-v', '--verbosity', action="count", default=1,
                        help="""increase output verbosity (-v: standard logging infos; 
                        -vv: logging infos and NiLearn verbose; -vvv: debug)""")
    parser.add_argument('--task', default=[], action='store', nargs='+')
    parser.add_argument('--atlas-dimension', default=64)

    args = parser.parse_args()

    return args

def get_func_filenames_bids(paths_to_func_dir, task_filter=[]):
    logging.debug(f'Using BIDS to find functional files...')

    layout = BIDSLayout(
        paths_to_func_dir,
        validate=False,
        )
    
    all_derivatives = layout.get(
        scope='all',
        return_type='file',
        extension='nii.gz',
        session=[15],
        suffix='bold',
        task=task_filter
        )

    return all_derivatives

def get_bids_savename(filename,
                      patterns=None, **kwargs):
    if patterns is None:
        patterns = ['sub-{subject}[/ses-{session}]/func/sub-{subject}'
                    '[_ses-{session}][_task-{task}][_meas-{meas}]'
                    '_{suffix}{extension}']
    entity = parse_file_entities(filename)

    for key, value in kwargs.items():
        entity[key] = value

    bids_savename = build_path(entity, patterns)
    logging.debug(f'save filename will be:\n\t{build_path(entity, patterns)}')

    return bids_savename

def get_atlas_data(atlas_name='DiFuMo', **kwargs):
    logging.info(f'Fetching the DiFuMo atlas ...')
    
    if kwargs['dimension'] not in [64, 128, 512]:
        logging.warning(f'Dimension for DiFuMo atlas is different from 64, 128 or 512 !')

    return fetch_atlas_difumo(legacy_format=False, **kwargs)

def find_derivative(path, derivatives_name='derivatives'):
    if op.split(path)[-1] == derivatives_name:
        return path
    if op.split(path)[0]=='':
        logging.error(f'"{derivatives_name}" could not be found on path !')
        return ''
    return find_derivative(path=op.split(path)[0])

def extract_timeseries(func_filename, atlas_filename, masker=None, verbose=2):
    if masker is None:
        masker = NiftiMapsMasker(
            maps_img=atlas_filename,
            #standardize="zscore_sample",
            #memory="nilearn_cache",
            verbose=verbose,
            )
    
    if type(func_filename) == list:
        time_series = []
        confounds = []
        for file_id, individual_filename in enumerate(func_filename):
            logging.info(f'Extraction of timeseries from list: {file_id+1}/{len(func_filename)} ...')
            ts, conf = extract_timeseries(individual_filename, atlas_filename,
                                          masker=masker, verbose=verbose)
            time_series.append(ts)
            confounds.append(conf)
        return time_series, confounds

    confounds, sample_mask = load_confounds(
        func_filename,
        strategy=["high_pass", "motion", "scrub"],
        motion="basic",
        scrub=4,
        fd_threshold=0.4,
        std_dvars_threshold=10,
        )
    
    time_series = masker.fit_transform(
        func_filename,
        confounds=confounds,
        sample_mask=sample_mask
        )
    
    return time_series, confounds

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

def visual_report_timeserie(timeseries, confounds=None, save=False, output=None):

    plt.imshow(timeseries, cmap='binary')

    if save is not None:
        plt.savefig(output)

    return

def visual_report_fc(matrix, save=False, output=None):
    return

def save_output(data_list, original_filenames, output=None):
    return

def main():
    args = get_arguments()

    input_path = args.data_dir
    save = args.save
    output = args.output
    task_filter = args.task
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

    func_filenames = get_func_filenames_bids(input_path, task_filter=task_filter)

    logging.info(f'Found {len(func_filenames)} functional file(s):')
    logging.info('\t'+'\n\t'.join([op.basename(filename) for filename in func_filenames]))

    atlas_data = get_atlas_data(dimension=atlas_dimension)
    atlas_filename = getattr(atlas_data, 'maps')

    if save:
        if output is None:
            output = op.join(find_derivative(input_path), 'functional_connectivity')
        logging.info(f'Output will be save at:\n\t{output}')
        #os.makedirs(output, exist_ok=True)
        
    #all_time_series, all_confounds = extract_timeseries(func_filenames,
    #                                                    atlas_filename,
    #                                                    verbose=nilearn_verbose)
    #
    #for individual_time_serie, confounds in zip(all_time_series, all_confounds):
    #    visual_report_timeserie(individual_time_serie, confounds=confounds,
    #                            save=save, output=output)
    #    print(individual_time_serie.shape)

    #all_fc_matrices = compute_connectivity(all_time_series)
    
    all_fc_matrices = []
    for individual_matrix, individual_file in zip(all_fc_matrices, func_filenames):
        print(f'matrix has shape {individual_matrix.shape} and will be saved at:')
        print(get_bids_savename(filename=individual_file, suffix='relmat',
                                meas='sparseinversecovariance',
                                extension='.tsv'))
    
if __name__ == "__main__":
    main()