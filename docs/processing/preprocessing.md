## Executing *fMRIPrep*
Because *fMRIPrep* creates a single anatomical reference for all sessions, we generate such reference first by setting the `--anat-only` flag.
If that *fMRIPrep* execution finishes successfully, the anatomical processing outcomes will be stored in the output folder.
We will then run one *fMRIPrep* process for each dataset's session, which is the recommended way for datasets with a large number of sessions (e.g., more than six sessions).
We avert that session-wise *fMRIPrep*'s processes run into race conditions by pre-computing the anatomical reference.

- [ ] Submit the anatomical workflow:
    ``` bash title="Launch each session through fMRIPrep in parallel"
    cd code/fmriprep
    bash ss-fmriprep.sh
    ```

    ??? abstract "The sbatch file to run *fMRIPrep* with `--anat-only`"

        ``` bash
{% filter indent(width=8) %}
{% include 'code/fmriprep/ss-fmriprep-anatonly.sh' %}
{% endfilter %}
        ```

- [ ] Submit a *job array* with one scanning session each with the `--bids-filter-file` argument selecting the corresponding sessions, and point the `--fs-subjects-dir` argument to the folder where *FreeSurfer* results were stored.
    ``` bash title="Launch each session through fMRIPrep in parallel"
    cd code/fmriprep
    bash ss-fmriprep.sh
    ```

    ??? abstract "The sbatch file to run *fMRIPrep* session-wise"

        ``` bash
{% filter indent(width=8) %}
{% include 'code/fmriprep/ss-fmriprep.sh' %}
{% endfilter %}
        ```

??? warning "Not all *fMRIPrep* derivatives were generated"

    - [ ] If some derivatives are missing, it is a sign that *fMRIPrep* encountered an error. Identify what failed in the "Errors" section of the visual report or in the log of the *fMRIPrep* run.
    - [ ] If you could find the solution to the problem, re-run *fMRIPrep* on that particular subject implementing this solution.
    - [ ] In case you do not understand the error message, search for associated keywords in the [issues of the *fMRIPrep* github repository](https://github.com/nipreps/fmriprep/issues); it is likely someone else experienced the same problem before you and reported it. The solution might be documented in the issue. Don't forget to check closed issues!
    - [ ] If that did not help, you might find help on [NeuroStars](https://neurostars.org/).
    - [ ] If no issue has been opened regarding this error and you did not find answer in NeuroStars, then open an issue in the *fMRIPrep* github repository. Your description of the problem need to be as complete and detailed as possible to help the maintainers identify the problem efficiently.
    - [ ] In case *fMRIPrep* repeatedly fails on that particular session even with the help of the maintainers and even after trying several solutions, exclude that session.

## Visualizing *fMRIPrep*'s individual reports

Following our protocols<sup>[1]</sup>, the quality of unprocessed images MUST be assessed before after preprocessing to verify it did not go awry.

- [ ] Open each *fMRIPrep* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Visualize the first mosaic () and apply the [exclusion criteria](qaqc-criteria.md#background-enhanced-mosaic)
- [ ] Scroll down to the and apply the [exclusion criteria]()

!!! warning "Immediately report images deemed *exclude*, as an issue in the dataset's repository"
