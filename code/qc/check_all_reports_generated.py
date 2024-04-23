import glob
import os
import re

# Set the paths
cprovins = "/home/data"
data_dir = os.path.join(cprovins, 'hcph')
derivatives_dir = os.path.join(cprovins,'hcph-derivatives', 'mriqc-24.0.0/')

# Use glob to find all folders matching the pattern ses-*
session_folders = glob.glob(os.path.join(data_dir, 'sub-001','ses-[0-9]*'))

# Extract session numbers from folder names
sessions = [folder.split('-')[-1] for folder in session_folders]

# Define the patterns you want to filter in filenames
patterns = ['acq-undistorted_T1w', 'acq-undistorted_T2w', 'acq-original_T2w',
            'task-qct_*_bold', 'task-bht_*_bold', 'task-rest_*_bold',
            'acq-highres_dir-*_dwi']

# Iterate over each session
missing_reports = {}
for session in sessions:

    # Initialize a list to store missing reports for this session
    missing_reports[session] = []

    # Iterate over each pattern
    for pattern in patterns:
        # Construct the regex pattern
        regex_pattern = f"sub-001_ses-{session}_{pattern}.html"

        # Use glob to check if any report files matching the pattern exist
        report_files = glob.glob(os.path.join(derivatives_dir, regex_pattern))

        if not report_files:
            missing_reports[session].append(pattern)

# Print sessions with missing reports
for session_name, missing_patterns in missing_reports.items():
    if missing_patterns:
        print(f"Session {session_name} is missing reports for the following patterns:")
        for pattern in missing_patterns:
            print(f" - {pattern}")
    else:
        print(f"All reports found for session {session_name}.")
