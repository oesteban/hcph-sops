# QA/QC criteria

The following lists the pre-defined exclusion criteria for analyses of whole-brain structural and functional connectomes.

## Anatomical MRI

??? info "The exclusion criteria are tailored to how the anatomical images will be used."

    Given our planned analysis, the T1w image will be used for the spatial alignment with the standard MNI152NLin2009cAsym template.
    In addition, surface reconstructions from the T1w image will guide the co-registration of structural and functional (BOLD) images in fMRIPrep.
    Since the latter preprocessing steps are relatively robust to structural images with mild artifacts, the exclusion criteria for unprocessed T1w images are lenient.
    However, individual T1w images may be excluded without such a decision lead to exclusion of the whole session in which it belongs.
    We annotate subjects with visible artifacts in the T1w images in order to ensure rigorous scrutinizing of spatial normalization and surface reconstruction outputs from fMRIPrep (if both modalities passed the first QC checkpoint with MRIQC).

### Background-enhanced mosaic
- [ ] Check for signal *ripples* around the head typically caused by head motion.
    Exclude this T1w only if identifying these ripples leads to revising the decision on the brain mosaic.
- [ ] Check for signal interference leaked from the eyeballs across the PE direction.
    Exclude this T1w only if identifying these leakages leads to revising the decision on the brain mosaic.
- [ ] Check for ghosts outside the brain, and evaluate whether they may overlap with brain tissue:
        - [ ] Overlapping wrap-around.
        - [ ] Nyquist aliases (typically through PE direction).
        - [ ] Ghosts caused by external elements such as headsets or mirror frames.
    Exclude this T1w only if identifying these ghosts leads to revising the decision on the brain mosaic.

### Zoomed-in brain mosaic:
- [ ] Check that the brain is not presented upside down. 
    This indicates an issue of the header. 
    Either the header needs to be corrected manually or exclude the session.
- [ ] Check for potential incidental findings (e.g unusual black hole in the cortex). If you have a doubt about sth, you need to transfer the image to {{ secrets.people.medical_contact | default("███") }} for thorough inspection.
- [ ] Check for signal *ripples* around the frontal/prefrontal cortex typically caused by head motion.
    Exclude this particular T1w if ripples are clear and globally localized.
    These T1w images could degrade the quality of surface reconstruction. 
- [ ] Check for signal interference leaked from the eyeballs across the PE direction overlapping with brain tissue.
    Exclude this particular T1w if the leaked signal substantially overlaps cortical brain areas.
    These T1w images could degrade the quality of surface reconstruction. 
- [ ] Check for ghosts within the brain:
      - [ ] Overlapping wrap-around.
      - [ ] Nyquist aliases (typically through PE direction).
      - [ ] Ghosts caused by external elements such as headsets or mirror frames.
      
    Exclude this particular T1w if any of these ghosts overlap cortical gray matter.

- [ ] Check for other artifacts such as [fat shifts](https://mriquestions.com/chemical-shift-artifact.html) or RF spoiling within the brain.
   Exclude this particular T1w if any of these ghosts overlap cortical gray matter.
- [ ] Check for [zipper artifacts](https://mriquestions.com/zipper-artifact.html) and other EM interferences.
    Exclude this particular T1w if any of these ghosts overlap cortical gray matter.
- [ ] Check for excessive B<sub>1</sub> field inhomogeneity.
    Exclude only if it is evident that a coil failure happened.
- [ ] Check for inhomogeneous [*salt-and-pepper* noise patterns](https://en.wikipedia.org/wiki/Salt-and-pepper_noise).
    Generally, do not exclude this T1w image unless the noise pattern destroys cortical gray matter areas.
- [ ] Check for global [*salt-and-pepper* noise](https://en.wikipedia.org/wiki/Salt-and-pepper_noise) distribution.
    Generally, do not exclude this T1w image except evident imaging global failure.
- [ ] Check for low SNR characterized by a grainy picture. Generally, do not exclude this T1w image unless the noise pattern destroys cortical gray matter areas.

... continued ...

### Group report
- [ ] Check again the individual visual report of runs with outlying-low SNR, ensuring they do not fall into one of the [exclusion criteria](#functional-mri).


## Functional MRI

### Exclusion criteria applicable to all types of fMRI scans in our study

#### BOLD average mosaic
- [ ] Check that the brain is not presented upside down. 
    This indicates an issue of the header. 
    Either the header needs to be corrected manually or exclude the session.

- [ ] Check that the brain structure is clearly visible. Exclude the session if it is not.

- [ ] Check for signal *ripples* around the frontal/prefrontal cortex typically caused by head motion.
    Exclude the session if ripples are clear and globally localized.

- [ ] Check for ghosts within the brain:
      - [ ] Overlapping wrap-around.
      - [ ] Nyquist aliases or aliasing ghost (typically through PE direction).
      - [ ] Ghosts caused by external elements such as headsets or mirror frames.

      Exclude the session if any of these ghosts overlap cortical gray matter.

- [ ] Check for high standard deviation vertical strikes in the saggital plane of the standard deviation map.

- [ ] Check for low SNR characterized by a grainy picture. This dataset is specifically subject to this artifact, because multiband acceleration was used.

??? warning "Do not exclude subjects presenting susceptibility distortion artifacts yet!"

    For each session, we acquired fieldmaps that can be leveraged by fMRIPrep to perform susceptibility distortion correction. As such, those artifacts might be corrected by the preprocessing.

#### Standard deviation mosaic

- [ ] Check for ghosts within the brain:
      - [ ] Overlapping wrap-around.
      - [ ] Nyquist aliases or aliasing ghost (typically through PE direction).
      - [ ] Ghosts caused by external elements such as headsets or mirror frames.

      Exclude the session if any of these ghosts overlap cortical gray matter.

- [ ] Check for high-std vertical strikes in the saggital plane of the std map.

#### Background noise mosaic

- [ ] Check for ghosts within the brain:
      - [ ] Overlapping wrap-around.
      - [ ] Ghosts caused by external elements such as headsets or mirror frames.

      Exclude the session if any of these ghosts overlap cortical gray matter.

      - [ ] Nyquist aliases or aliasing ghost (typically through PE direction).
        Exclude the session if the intensity of the ghost is similar to the intensity of the inside of the brain.

#### FMRI Summary plot

- [ ] Check for periodic modulations of the signal, a sign that your signal is aliased by a regular and slow 
    motion, like respiration. 
    Exclude the session if the modulation is visible throughout the majority of the scan.
- [ ] Check for coil failures. They appear as abrupt changes in overall signal intensity not paired with motion 
    peaks. 
    Exclude the session if any coil failure is observed.
- [ ] Check for strong polarized structure in the crown. 
    Exclude the session if the polarized structure is prolonged throughout a majority of the scan and if the blocks 
    are particularly pronounced.
- [ ] Check for prolonged dark deflections accompanied by peaks in the FD trace as a sign for motion outbursts.
    Exclude the session in case the prolonged dark deflections cover more than half of the scan duration.

#### Group report
- [ ] If they are not excluded yet, re-inspect the individual visual report of the three scans with the highest mean FD and double-check that the data does not fall into one of the [exclusion criteria](#functional-mri).

- [ ] If they are not excluded yet, re-inspect the individual visual report of the three scans with the highest tSNR and double-check that the data does not fall into one of the [exclusion criteria](#functional-mri).

- [ ] If they are not excluded yet, re-inspect the individual visual report of the three scans with the lowest SNR and double-check that the data does not fall into one of the [exclusion criteria](#functional-mri).

### Resting-state

!!! info "The following exclusion criteria are tailored to how the RSfMRI will be used."

    The RSfMRI images will be used to construct and analyze whole-brain functional connectomes.
    As such the quality of all regions in the brain is important, i.e. there is not a region where we can be more lenient.

#### FMRI Summary plot
- [ ] Check for hyperintensity in single slices.
    Exclude the session if any single-slice hyperintensities are observed. Correlation analysis are likely to be biased by such peaks.

#### Group report
- [ ] Exclude sessions for which `fd_perc` > 75% which is the percentage of frames with a framewise displacement (FD) above the motion censoring threshold (by default 0.2mm in *MRIQC*). This corresponds to a QC cutoff of at least 5min of RSfMRI to accurately estimate functional connectivity (FC) [Van Dijk et al. 2010, Birn 2023].
- [ ] Re-examine the individual visual report of sessions for which `fd_perc` > 50% and double-check that the data does not fall into one of the [exclusion criteria](#functional-mri).

### Quality control task

!!! info "The following exclusion criteria are tailored to how the QCT fMRI will be used."

    Task activation maps will be extracted from the QCT fMRI images and compared across phase encoding directions.

### Breath-holding task

!!! info "The following exclusion criteria are tailored to how the BHT fMRI will be used."

??? important "For task fMRI, you should verify that your subjects are attempting to perform the instructed task."
    For accurate estimation of task activation, it is essential to check the quality of both the fMRI images and the task behavior [Etzel 2023]. As such, it is important to verify that the subjects were attempting to perform the instructed task (i.e not sleeping and not responding randomly). For QCT, this can be done by verifying that the subjects look at the fixation points and for BHT, you can use the respiration belt to verify that the subjects inhales, exhales and holds his breath when he is suppose to. We will however not spend time developing those QC methods, as we estimate that the participant, being the principal investigator of this project, has enough incentive to follow the tasks accurately.

## Diffusion MRI

## Physiological recordings

## Eye-tracking

# References

* Birn, Rasmus M. “Quality Control Procedures and Metrics for Resting-State Functional MRI.” Frontiers in Neuroimaging 2 (2023). <https://doi.org/10.3389/fnimg.2023.1072927>.

* Etzel, Joset A. “Efficient Evaluation of the Open QC Task fMRI Dataset.” Frontiers in Neuroimaging 2 (2023). https://www.frontiersin.org/articles/10.3389/fnimg.2023.1070274.

* Van Dijk, Koene R. A., Trey Hedden, Archana Venkataraman, Karleyton C. Evans, Sara W. Lazar, and Randy L. Buckner. “Intrinsic Functional Connectivity As a Tool For Human Connectomics: Theory, Properties, and Optimization.” Journal of Neurophysiology 103, no. 1 (January 2010): 297–321. <https://doi.org/10.1152/jn.00783.2009>.

