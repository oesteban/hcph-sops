## Executing *fMRIPrep*
Because *fMRIPrep* creates a single anatomical reference for all sessions, we generate such reference first by setting the `--anat-only` flag.
If that *fMRIPrep* execution finishes successfully, the anatomical processing outcomes will be stored in the output folder.
We will then run one *fMRIPrep* process for each dataset's session, which is the recommended way for datasets with a large number of sessions (e.g., more than six sessions).
We avert that session-wise *fMRIPrep*'s processes run into race conditions by pre-computing the anatomical reference.

- [ ] Submit the anatomical workflow:
    ``` bash title="Executing anatomical workflow of fMRIPrep"
    {% filter indent(width=4) %}
    {% include 'code/fmriprep/ss-fmriprep-anatonly.sh' %}
    {% endfilter %}
    ```

- [ ] Submit a *job array* with one scanning session each with the `--bids-filter-file` argument selecting the corresponding sessions, and point the `--fs-subjects-dir` argument to the folder where *FreeSurfer* results were stored.
    ``` bash title="Launch each session through fMRIPrep in parallel"
    cd code/fmriprep
    bash submit-fmriprep.sh
    ```

    ??? important "The sbatch file to run fMRIPrep session-wise"

        ``` bash title="Executing anatomical workflow of fMRIPrep"
        {% filter indent(width=8) %}
        {% include 'code/fmriprep/ss-fmriprep.sh' %}
        {% endfilter %}
        ```
