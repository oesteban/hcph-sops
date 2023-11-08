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
- [ ] Visualize the first mosaic (zoomed into brain mask):
    - [ ] Check for signal *ripples* around the frontal/prefrontal cortex typically caused by head motion
    - [ ] Check for signal interference leaked from the eyeballs across the PE direction overlapping with brain tissue.
    - [ ] Check for ghosts within the brain:
        - [ ] Overlapping wrap-around.
        - [ ] Nyquist aliases (typically through PE direction).
        - [ ] Ghosts caused by external elements such as headsets or mirror frames.
    - [ ] Check for other artifacts such as fat shifts or RF spoiling within the brain.
    - [ ] Check for zipper artifacts and other EM interferences.
    - [ ] Check for excessive B<sub>1</sub> field inhomogeneity.
    - [ ] Check for inhomogeneous *salt-and-pepper* noise patterns.
    - [ ] Check for global *salt-and-pepper* noise distribution.
- [ ] Scroll down to the background-enhanced mosaic:
    - [ ] Check for signal *ripples* around the head typically caused by head motion.
    - [ ] Check for signal interference leaked from the eyeballs across the PE direction.
        If present, go back to the brain mosaic to confirm whether they overlap with the brain tissue.
    - [ ] Check for ghosts outside the brain, and evaluate whether they may overlap with brain tissue:
        - [ ] Overlapping wrap-around.
        - [ ] Nyquist aliases (typically through PE direction).
        - [ ] Ghosts caused by external elements such as headsets or mirror frames.
    - [ ] Check for other artifacts such as RF spoiling or objects outside the head.
    - [ ] Check for zipper artifacts and other EM interferences.
    - [ ] Check for global *salt-and-pepper* noise distribution in the background.
    - [ ] Check for anomalous noise distribution in the background.
- [ ] Assign a quality rating and indicate artifacts with the *Rating widget*.
    To assign a quality rating, follow the [QA/QC criteria]() stated below.
- [ ] Download the rating file as a JSON and add it to the derivatives dataset.

!!! warning "Immediately report images deemed *exclude*, as an issue in the dataset's repository"

### Assessing functional images


!!! danger "Insufficient quality of an fMRI run requires recalling the session"

    - [ ] Immediately report images deemed *exclude*, as an issue in the dataset's repository.
    - [ ] Proceed to scheduling an extra session after the initially-planned scanning period.

### Assessing diffusion images


!!! danger "Insufficient quality of a dMRI run requires recalling the session"

    - [ ] Immediately report images deemed *exclude*, as an issue in the dataset's repository.
    - [ ] Proceed to scheduling an extra session after the initially-planned scanning period.


[1]: https://doi.org/10.3389/fnimg.2022.1073734 "Provins, C., … Esteban, O. (2023). Quality Control in functional MRI studies with MRIQC and fMRIPrep. Frontiers in Neuroimaging 1:1073734. doi:10.3389/fnimg.2022.1073734 (OA)."
[2]: https://rr.peercommunityin.org/articles/rec?id=346 "Provins, C., … Esteban, O. (2023). Defacing biases in manual and automated quality assessments of structural MRI with MRIQC, Stage 1 IPA (in principle acceptance) of Version 3 by Peer Community in Registered Reports."
