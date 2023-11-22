## Executing *MRIQC*

- [ ] Run *MRIQC*.
    ```shell
    #Assign the variable to the last session ID
    lastsession=01
    datalad containers-run \
        --container-name mriqc \
        --input sourcedata \
        --output ./derivatives/mriqc-23.1.0 \
        "{inputs} {outputs} participant --session-id ${lastsession} -w ${HOME}/tmp/hcph-derivatives/mriqc-23.1.0 --mem 40G"
    ```
- [ ] Check that *MRIQC* generated all expected individual reports.
    For each session, the following files must be generated:
    ``` text
    derivatives
        ├── mriqc_23.2.0
        │   ├── dataset_description.json
        │   ├── logs
        │   ├── sub-001
        │   ├── sub-001_ses-001_acq-highres_dir-AP_dwi.html
        │   ├── sub-001_ses-001_acq-original_T2w.html
        │   ├── sub-001_ses-001_acq-undistorted_T1w.html
        │   ├── sub-001_ses-001_acq-undistorted_T2w.html
        │   ├── sub-001_ses-001_task-bht_dir-AP_bold.html
        │   ├── sub-001_ses-001_task-qct_dir-AP_bold.html
        │   ├── sub-001_ses-001_task-rest_dir-AP_bold.html
    ```

    ??? bug "*MRIQC* failed to produce all the expected visual reports"

        Depending on the specific error condition hit by *MRIQC*, some visual reports may not be generated at all.
        
        - [ ] Check for corresponding *crash files* under the `logs/` directory under the output folder.
        - [ ] Address the issue (e.g., insufficient disk space) and re-run *MRIQC*.
            If the issue is unclear, search for similar problems reported previously in the [issues of the *MRIQC* GitHub repository](https://github.com/nipreps/mriqc/issues).
            The solution could be documented in some existing issue opened by a user who experienced the same problem before you and reported it.
            Don't forget to check closed issues!
            If that did not help, you might find help on [NeuroStars](https://neurostars.org/).
        - [ ] Open a new issue in the *MRIQC* GitHub repository if all the above fails.

- [ ] Check that the `group_{T1w,T2w,bold,dwi}.tsv` file contains the image quality metrics (IQMs) for all the expected inputs (one row per individual run at the input).
- [ ] Push the new derivatives to the remote storage.
    ```shell
    datalad push --to ria-storage
    datalad push --to origin
    ```

## Visualizing *MRIQC*'s individual reports

Following our protocols<sup>[1]</sup>, the quality of unprocessed images MUST be assessed before executing any processing (e.g., *fMRIPrep* or *dMRIPrep* for preprocessing).
In addition, *MRIQC* is executed prior any further processing step considering our preliminary findings regarding *defacing*<sup>[2]</sup>.

### Assessing anatomical images (T<sub>1</sub>-weighted and T<sub>2</sub>-weighted)
- [ ] Open each *MRIQC* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Check that the visual report is complete when you open it.

    ??? bug "A visual report is incomplete"

        - [ ] Identify what failed in the "About > Errors" section of the visual report.
        - [ ] Address the issue (e.g., out-of-memory when running a container) and re-run *MRIQC*.
            Proceed as in the previous case by finding documentation on the *MRIQC* repository or NeuroStars.

- [ ] Visualize the first mosaic (background-enhanced mosaic) and apply the [exclusion criteria](qaqc-criteria.md#background-enhanced-mosaic)
- [ ] Scroll down to the zoom in the brain mask mosaic and apply the [exclusion criteria](qaqc-criteria.md#zoomed-in-brain-mosaic)
- [ ] Assign a quality rating and indicate artifacts with the *Rating widget*.
    To assign a quality rating, follow the [QA/QC criteria]() stated below.
- [ ] Download the rating file as a JSON and add it to the derivatives dataset.

!!! warning "Immediately report images deemed *exclude*, as an issue in the dataset's repository"

### Assessing functional images

!!! danger "Insufficient quality of an RSfMRI run requires recalling the session"

    - [ ] Immediately report images deemed *exclude*, as an issue in the dataset's repository.
    - [ ] Proceed to scheduling an extra session after the initially-planned scanning period.

#### RSfMRI
- [ ] Open each *MRIQC* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Visualize the first mosaic (BOLD average) and apply the [exclusion criteria](qaqc-criteria.md#bold-average)
- [ ] Scroll down to the standard-deviation (std) mosaic and apply the [exclusion criteria](qaqc-criteria.md#standard-deviation-mosaic)
- [ ] Scroll down to the background noise mosaic and apply the [exclusion criteria](qaqc-criteria.md#background-noise-mosaic)
- [ ] Scroll down to the fMRI summary plot and apply the [exclusion criteria](qaqc-criteria.md#fmri-summary-plot) as well as [the exclusion criteria specific to the BHT](qaqc-criteria.md#resting-state).

#### QCT
- [ ] Open each *MRIQC* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Visualize the first mosaic (BOLD average) and apply the [exclusion criteria](qaqc-criteria.md#bold-average)
- [ ] Scroll down to the standard-deviation (std) mosaic and apply the [exclusion criteria](qaqc-criteria.md#standard-deviation-mosaic)
- [ ] Scroll down to the background noise mosaic and apply the [exclusion criteria](qaqc-criteria.md#background-noise-mosaic)
- [ ] Scroll down to the fMRI summary plot and apply the [exclusion criteria](qaqc-criteria.md#fmri-summary-plot) as well as [the exclusion criteria specific to the BHT](qaqc-criteria.md#quality-control-task) 

#### BHT
- [ ] Open each *MRIQC* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Visualize the first mosaic (BOLD average) and apply the [exclusion criteria](qaqc-criteria.md#bold-average)
- [ ] Scroll down to the standard-deviation (std) mosaic and apply the [exclusion criteria](qaqc-criteria.md#standard-deviation-mosaic)
- [ ] Scroll down to the background noise mosaic and apply the [exclusion criteria](qaqc-criteria.md#background-noise-mosaic)
- [ ] Scroll down to the fMRI summary plot and apply the [exclusion criteria](qaqc-criteria.md#fmri-summary-plot) as well as [the exclusion criteria specific to the BHT](qaqc-criteria.md#breath-holding-task) 

## Visualizing *MRIQC*'s group reports

### Assessing functional images
- [ ] Open the *MRIQC* group report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Visualize the IQMs distributions and apply the [exclusion critera](qaqc-criteria.md#group-report) for all BOLD scans and apply [these exclusion criteria](qaqc-criteria.md#group-report-1) to RSfMRI.

### Assessing diffusion images

!!! danger "Insufficient quality of a dMRI run requires recalling the session"

    - [ ] Immediately report images deemed *exclude*, as an issue in the dataset's repository.
    - [ ] Proceed to scheduling an extra session after the initially-planned scanning period.


[1]: https://doi.org/10.3389/fnimg.2022.1073734 "Provins, C., … Esteban, O. (2023). Quality Control in functional MRI studies with MRIQC and fMRIPrep. Frontiers in Neuroimaging 1:1073734. doi:10.3389/fnimg.2022.1073734 (OA)."
[2]: https://rr.peercommunityin.org/articles/rec?id=346 "Provins, C., … Esteban, O. (2023). Defacing biases in manual and automated quality assessments of structural MRI with MRIQC, Stage 1 IPA (in principle acceptance) of Version 3 by Peer Community in Registered Reports."
