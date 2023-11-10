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
- [ ] Visualize the first mosaic (zoomed into brain mask) and apply the [exclusion criteria](qaqc-criteria.md#zoomed-in-brain-mosaic)
- [ ] Scroll down to the background-enhanced mosaic and apply the [exclusion criteria](qaqc-criteria.md#background-enhanced-mosaic)
- [ ] Assign a quality rating and indicate artifacts with the *Rating widget*.
    To assign a quality rating, follow the [QA/QC criteria]() stated below.
- [ ] Download the rating file as a JSON and add it to the derivatives dataset.

!!! warning "Immediately report images deemed *exclude*, as an issue in the dataset's repository"

### Assessing functional images

!!! danger "Insufficient quality of an fMRI run requires recalling the session"

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

### Assessing diffusion images


!!! danger "Insufficient quality of a dMRI run requires recalling the session"

    - [ ] Immediately report images deemed *exclude*, as an issue in the dataset's repository.
    - [ ] Proceed to scheduling an extra session after the initially-planned scanning period.


[1]: https://doi.org/10.3389/fnimg.2022.1073734 "Provins, C., … Esteban, O. (2023). Quality Control in functional MRI studies with MRIQC and fMRIPrep. Frontiers in Neuroimaging 1:1073734. doi:10.3389/fnimg.2022.1073734 (OA)."
[2]: https://rr.peercommunityin.org/articles/rec?id=346 "Provins, C., … Esteban, O. (2023). Defacing biases in manual and automated quality assessments of structural MRI with MRIQC, Stage 1 IPA (in principle acceptance) of Version 3 by Peer Community in Registered Reports."
