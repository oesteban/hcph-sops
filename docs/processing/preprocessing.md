## Executing *fMRIPrep*

Because *fMRIPrep* creates a single anatomical reference for all sessions, we generate such reference first by setting the `--anat-only` flag.
If that *fMRIPrep* execution finishes successfully, the anatomical processing outcomes will be stored in the output folder.
We will then run one *fMRIPrep* process for each dataset's session, which is the recommended way for datasets with a large number of sessions (e.g., more than  six sessions).
We avert that session-wise *fMRIPrep*'s processes run into race conditions by pre-computing the anatomical reference.

- [ ] Submit the anatomical workflow:
    ``` bash title="Launch each session through fMRIPrep in parallel"
    cd code/fmriprep
    bash ss-fmriprep-anatonly.sh
    ```

    ??? abstract "The sbatch file to run *fMRIPrep* with `--anat-only`"

        ``` bash
{% filter indent(width=8) %}
{% include 'code/fmriprep/ss-fmriprep-anatonly.sh' %}
{% endfilter %}
        ```

- [ ] Once the anatomical workflow ran successfully, submit a *job array* with one scanning session each with the `--bids-filter-file` argument selecting the corresponding session, and point the `--fs-subjects-dir` argument to the folder where *FreeSurfer* results were stored.
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
<a id="fmriprep-failed"></a>
??? warning "Not all *fMRIPrep* derivatives were generated"

    If some derivatives are missing, it is a sign that *fMRIPrep* encountered an error.
    
    - [ ] Check the "Errors" section of the visual report.
    - [ ] Check the `log/` folder corresponding to the *fMRIPrep* run, carefully ensuring no errors were missed out on the reports.
    - [ ] Search for associated keywords in the [issues on *fMRIPrep*'s GitHub repository](https://github.com/nipreps/fmriprep/issues) if the solution remains unclear after the first assessment; it is likely someone else experienced the same problem before you and reported it.
        The solution might be documented in the issue.
        Don't forget to check closed issues!
    - [ ] Search for the issue on [NeuroStars](https://neurostars.org/), if the solution remains unclear.
    - [ ] If the solution remains elusive, open an issue in *fMRIPrep*'s GitHub repository to report the problem.
        Your description of the problem needs to be as complete and detailed as possible to help the maintainers identify the problem efficiently.
    - [ ] Re-run *fMRIPrep* on that particular subject and session after implementing a solution.
    
    !!! danger "If the error remains despite all efforts, the session MAY be excluded"

## Visualizing *fMRIPrep*'s individual reports

Following our protocols<sup>[1]</sup>, the quality of unprocessed images MUST be assessed [before](../data-management/mriqc.md#visualizing-mriqcs-individual-reports) and after preprocessing to verify it did not go awry.

### Anatomical preprocessing assessment

- [ ] Open the *fMRIPrep* anatomical report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Assess the "Summary" section and apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#summary).

!!! tip "Do not hesitate to jump back and forth through sections while screening the visual report."

- [ ] Assess the "Anatomical conformation" section and apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#anatomical-conformation).
- [ ] Assess the mosaic showing the calculated brain mask and brain tissue segmentation, and apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#brain-mask-and-brain-tissue-segmentation-of-the-t1w).
- [ ] Visualize the spatial normalization flickering mosaic, and apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#spatial-normalization-of-the-anatomical-t1w-reference).
    Flickering between the subject and the template space is active while your mouse pointer hovers the mosaic area.
- [ ] Assess the surface reconstruction mosaic, and apply the [exclusion criteria](qaqc-criteria-preprocessed.md#surface-reconstruction).
- [ ] Visualize the first section entitled *Summary* and apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#summary).

### Assessment of fMRI Preprocessing

- [ ] Open each *fMRIPrep* functional report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Go through the section of each fMRI run and proceed as follows:

    !!! note "Start with QCT to train your eye and anticipate quality issues that may affect BHT and RSfMRI as well, followed by BHT and then RSfMRI"

    - [ ] Scrutinize the textual summary
        - [ ] Apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#textual-summary).
        - [ ] Apply the [exclusion criteria](qaqc-criteria-preprocessed.md#textual-summary-1).
    - [ ] Visualize the T2* map mosaic, and apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#t2-map).
    - [ ] Check the T2* gray-matter intensity histogram, and apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#t2-gray-matter-values).
    - [ ] Visualize the co-registration flickering mosaic, apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#alignment-of-functional-and-anatomical-mri-data).
        Flickering between T1w and BOLD images is active while hovering your mouse on the mosaic area.
    - [ ] Visualize the next mosaic displaying regions of interest (ROIs) used to estimate the nuisance regressors, and apply the [QA/QC criteria](qaqc-criteria-preprocessed.md#brain-mask-and-anatomicaltemporal-compcor-rois).
    - [ ] Visualize the carpet plot and nuisance signals panel, 
        - [ ] Apply the [exclusion criteria](qaqc-criteria-preprocessed.md#bold-summary-1)
        - [ ] If you are visualizing the carpet plot corresponding to a RSfMRI run, apply [additional QA criteria](qaqc-criteria-preprocessed.md#qa-criteria-specifically-for-rsfmri).
    - [ ] Visualize the confound correlation heatmap and use it to [choose the regressors](qaqc-criteria-preprocessed.md#correlations-between-nuisance-regressors) 
        you will include in the nuisance regression model.
    - [ ] Finally, verify that no errors are reported within the "Errors" section. If there are, proceed as indicated in ["Not all *fMRIPrep* derivatives were generated"](#fmriprep-failed).
    - [ ] Continue with the next fMRI run section

!!! danger "Immediately report errors or quality issues encountered"
    If errors or quality issues are encountered, find the issue corresponding to that session in [the dataset's repository](https://github.com/{{ secrets.data.gh_repo | default('<organization>/<repo_name>') }}/issues) and report a comprehensive description of the problems.
    In case of *fMRIPrep* failure, follow the procedure described above in ["Not all *fMRIPrep* derivatives were generated"](#fmriprep-failed).

[1]: https://doi.org/10.3389/fnimg.2022.1073734 "Provins, C., … Esteban, O. (2023). Quality Control in functional MRI studies with MRIQC and fMRIPrep. Frontiers in Neuroimaging 1:1073734. doi:10.3389/fnimg.2022.1073734 (OA)."
