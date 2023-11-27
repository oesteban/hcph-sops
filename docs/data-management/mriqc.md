## Executing *MRIQC*

- [ ] Create a dataset to host the *MRIQC* derivatives.
    Remember to set the correct version of the container (in our case {{ settings.versions.mriqc }}).
    ``` shell
    mkdir -p /data/datasets/hcph-derivatives
    cd /data/datasets/hcph-derivatives
    datalad create -c bids mriqc_{{ settings.versions.mriqc }}
    ```
??? warning "We are not yet registering the *MRIQC* derivatives dataset as a sub-dataset."

    To avoid complication at run time, the *MRIQC* derivatives dataset will be added as a sub-dataset to the unprocessed dataset only after *MRIQC* run is completed. As such, note that we are **NOT** using the `-d` flag

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

- [ ] Visualize the first mosaic (background mosaic) and apply the [exclusion criteria](qaqc-criteria.md#view-of-the-background-of-the-anatomical-image).
- [ ] Scroll down to the zoom in the zoomed-in brain mosaic and apply the [exclusion criteria](qaqc-criteria.md#zoomed-in-mosaic-view-of-the-brain).
- [ ] Assign a quality rating and indicate artifacts with the *Rating widget*.
    To assign a quality rating, follow the .
    - [ ] Open the *Rating widget* by clicking on it in the upper right corner of the *MRIQC* visual report.
    - [ ] Open up the "Record specific artifacts" menu and select the artifacts that you spotted according to the [QA/QC criteria](qaqc-criteria.md).
    - [ ] Assign a quality grade that reflects the number of artifacts you spotted and their severity, using the slider
    - [ ] Optionally, you can write down any extra comment you might have about the data and indicate your level of confidence regarding your ratings in the "Extra details" menu.
- [ ] Download the rating file as a JSON and add it to the derivatives dataset.

!!! warning "Immediately report images deemed *exclude*, as an issue in the dataset's repository"

### Assessing functional images

#### QCT

!!! note "We are checking QCT fMRI first and in principle not excluding QCT scans"
    Except if the image is [extremely distorted](qaqc-criteria.md#task-fmri-exclusion-criteria), we are not excluding QCT scans because we will leverage those images to evaluate the quality of fMRI scans and derived constructs throughout the whole analysis pipeline. We are however going through the *MRIQC* reports to train our eye, anticipate issues that might be affecting RSfMRI and flag the corresponding sessions.

- [ ] Open each *MRIQC* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Repeat the following two steps for each echo:
    - [ ] Visualize the first mosaic (standard-deviation) and search for [artifacts](qaqc-criteria.md#standard-deviation-of-signal-through-time)
    - [ ] Scroll down to the carpetplot and search for [artifacts](qaqc-criteria.md#carpetplot-and-nuisance-signals).
- [ ] Once you went through all the echo-wise visualization of the base report, scroll down to the "Extended echo-wise reports" section, inspect the background view and search for [artifacts](qaqc-criteria.md#view-of-the-background-of-the-voxel-wise-average-of-the-bold-timeseries).
- [ ] Scroll down to the average BOLD mosaic and search for [artifacts](qaqc-criteria.md#average-signal-through-time)
- [ ] Inspect the zoomed-in view of the average BOLD mosaic as well and search for the same [artifacts](qaqc-criteria.md#average-signal-through-time).


#### BHT

!!! note "Following the same reasoning as described in QCT, we are in principle not excluding BHT scans."

- [ ] Open each *MRIQC* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Repeat the following two steps for each echo:
    - [ ] Visualize the first mosaic (standard-deviation) and apply the [exclusion criteria](qaqc-criteria.md#standard-deviation-of-signal-through-time)
    - [ ] Scroll down to the carpetplot and apply the [exclusion criteria](qaqc-criteria.md#carpetplot-and-nuisance-signals).
- [ ] Once you went through all the echo-wise visualization of the base report, scroll down to the "Extended echo-wise reports" section, inspect the background view and apply the [exclusion criteria](qaqc-criteria.md#view-of-the-background-of-the-voxel-wise-average-of-the-bold-timeseries).
- [ ] Scroll down to the average BOLD mosaic and apply the [exclusion criteria](qaqc-criteria.md#average-signal-through-time)
- [ ] Inspect the zoomed-in view of the average BOLD mosaic as well and apply the same [exclusion criteria](qaqc-criteria.md#average-signal-through-time).

#### RSfMRI

!!! danger "Insufficient quality of an RSfMRI run requires recalling the session"

    - [ ] Immediately report images deemed *exclude*, as an issue in the dataset's repository.
    - [ ] Proceed to [scheduling an extra session](../recruitment-scheduling-screening/scheduling.md) after the initially-planned scanning period.

- [ ] Open each *MRIQC* report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Repeat the following two steps for each echo:
    - [ ] Visualize the first mosaic (standard-deviation) and apply the [exclusion criteria](qaqc-criteria.md#standard-deviation-of-signal-through-time)
    - [ ] Scroll down to the carpetplot and apply the [exclusion criteria](qaqc-criteria.md#carpetplot-and-nuisance-signals). 
- [ ] Once you went through all the echo-wise visualization of the base report, scroll down to the "Extended echo-wise reports" section, inspect the background view and apply the [exclusion criteria](qaqc-criteria.md#view-of-the-background-of-the-voxel-wise-average-of-the-bold-timeseries).
- [ ] Scroll down to the average BOLD mosaic and apply the [exclusion criteria](qaqc-criteria.md#average-signal-through-time)
- [ ] Inspect the zoomed-in view of the average BOLD mosaic as well and apply the same [exclusion criteria](qaqc-criteria.md#average-signal-through-time).

## Visualizing *MRIQC*'s group reports

### Assessing anatomical images
- [ ] Open the *MRIQC* group report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Visualize the IQMs distributions and apply the [exclusion critera](qaqc-criteria.md#group-report).

### Assessing functional images
- [ ] Open the *MRIQC* group report on a current Web Browser (*Google Chrome* is preferred).
- [ ] Visualize the IQMs distributions and apply the [exclusion critera](qaqc-criteria.md#group-report-1).


[1]: https://doi.org/10.3389/fnimg.2022.1073734 "Provins, C., … Esteban, O. (2023). Quality Control in functional MRI studies with MRIQC and fMRIPrep. Frontiers in Neuroimaging 1:1073734. doi:10.3389/fnimg.2022.1073734 (OA)."
[2]: https://rr.peercommunityin.org/articles/rec?id=346 "Provins, C., … Esteban, O. (2023). Defacing biases in manual and automated quality assessments of structural MRI with MRIQC, Stage 1 IPA (in principle acceptance) of Version 3 by Peer Community in Registered Reports."
