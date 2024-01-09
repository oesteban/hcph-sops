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

    If some derivatives are missing, it is a sign that *fMRIPrep* encountered an error.
    
    - [ ] Check the "Errors" section of the visual report.
    - [ ] Check the `log/` folder corresponding to the *fMRIPrep* run, carefully ensuring no errors were missed out on the reports.
    - [ ] Search for associated keywords in the [issues on *fMRIPrep*'s GitHub repository](https://github.com/nipreps/fmriprep/issues) if the solution remains unclear after the first assessment; it is likely someone else experienced the same problem before you and reported it.
        The solution might be documented in the issue.
        Don't forget to check closed issues!
    - [ ] Search for the issue on [NeuroStars](https://neurostars.org/), if the solution remains unclear.
    - [ ] Open an issue in *fMRIPrep*'s GitHub repository to report the problem, if the solution remains elusive.
        Your description of the problem needs to be as complete and detailed as possible to help the maintainers identify the problem efficiently.
    - [ ] Re-run *fMRIPrep* on that particular subject and session after implementing a solution.
    
    !!! danger "If the error remains despite all efforts, the session MAY be excluded"

## Visualizing *fMRIPrep*'s individual reports

Following our protocols<sup>[1]</sup>, the quality of unprocessed images MUST be assessed before and after preprocessing to verify it did not go awry.

- [ ] Open each *fMRIPrep* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Visualize the first section entitled `Summary` and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#summary).

    !!! warning "Running through the visual report does not have to be executed in a fixed order"

        While we describe the run through the report as linear, often inspecting other reportlets can help make a decision about the exclusion criteria related to the reportlet at hand. 
        As such, we encourage you to jump back and forth between visualizations as much as needed.


### Anatomical preprocessing assessment

- [ ] Assess the "Anatomical conformation" section and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#anatomical-conformation).
- [ ] Assess the mosaic showing the calculated brain mask and brain tissue segmentation, and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#brain-mask-and-brain-tissue-segmentation-of-the-t1w).
- [ ] Visualize the spatial normalization flickering mosaic, and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#spatial-normalization-of-the-anatomical-t1w-reference).
- [ ] Assess the surface reconstruction mosaic, and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#surface-reconstruction).
### Assessment of fMRI Preprocessing

- [ ] Scrutinize the textual summary and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#textual-summary).
- [ ] Visualize the T2* map mosaic, and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#t2-map).
- [ ] Check the T2* gray-matter intensity histogram, and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#t2-gray-matter-values).
- [ ] Visualize the dynamic visualization of the co-registration, apply the [exclusion criteria](qaqc-criteria-preprocessed.md#alignment-of-functional-and-anatomical-mri-data).
    Flickering between T1w and BOLD images is active while hovering your mouse on the mosaic area.
- [ ] Visualize the next mosaic displaying regions of interest (ROIs) where nuisance series are estimated, and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#brain-mask-and-anatomicaltemporal-compcor-rois).
- [ ] Visualize the carpet plot and nuisance signals panel, and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#bold-summary).
- [ ] Visualize the confound correlation heatmap and use it to [choose the regressors](qaqc-criteria-preprocessed.md#correlations-among-nuisance-regressors) you will include in the nuisance regression model.
- [ ] Verify that no errors are reported within the "Errors" section. 

If errors or quality issues are encountered, find the issue corresponding to that session in the dataset's repository and report a comprehensive description of the problems.
In case of *fMRIPrep* failure, follow the procedure described above "Not all *fMRIPrep* derivatives were generated".

!!! warning "Immediately report images deemed *exclude*, as an issue in the dataset's repository"
