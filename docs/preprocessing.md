## Executing *fMRIPrep*
Because *fMRIPrep* creates a single anatomical reference for all sessions, we will need first to run with ``--anat-only`` so that the results get cached and *fMRIPrep* processes do not run into race conditions.

Similarly, when running *fMRIPrep* on a dataset with many sessions, the safest approach is to submit one job per session.

- [ ] Submit the anatomical workflow:
    ``` bash title="Executing anatomical workflow of fMRIPrep"
    {% include 'code/fmriprep/ss-fmriprep-anatonly.sh' %}
    ```

- [ ] Submit a *job array* with one scanning session each with the `--bids-filter-file` argument selecting the corresponding sessions, and point the `--fs-subjects-dir` argument to the folder where *FreeSurfer* results were stored.
    ``` bash title="Launch each session through fMRIPrep in parallel"
    cd code/fmriprep
    bash submit-fmriprep.sh
    ```