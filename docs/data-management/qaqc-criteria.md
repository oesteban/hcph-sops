# QA/QC criteria

The following lists the pre-defined exclusion criteria for analyses of whole-brain structural and functional connectomes.

## Anatomical MRI

??? info "The exclusion criteria are tailored to how the anatomical images will be used."

    Given our planned analysis, the T1w image will be used for the spatial alignment with the standard `MNI152NLin2009cAsym` template.
    In addition, surface reconstructions from the T1w image will guide the co-registration of structural and functional (BOLD) images in fMRIPrep.
    Since the latter preprocessing steps are relatively robust to structural images with mild artifacts, the exclusion criteria for unprocessed T1w images are lenient.
    However, individual T1w images may be excluded without such a decision lead to exclusion of the whole session in which it belongs.
    We annotate subjects with visible artifacts in the T1w images in order to ensure rigorous scrutinizing of spatial normalization and surface reconstruction outputs from fMRIPrep (if both modalities passed the first QC checkpoint with MRIQC).

### View of the background of the anatomical image
- [ ] Check for signal *ripples* around the head typically caused by head motion.
    Exclude this T1w only if identifying these ripples leads to revising the decision on the brain mosaic.
- [ ] Check for signal interference leaked from the eyeballs across the PE direction.
    Exclude this T1w only if identifying these leakages leads to revising the decision on the brain mosaic.
- [ ] Check for ghosts outside the brain, and evaluate whether they may overlap with brain tissue:
    - [ ] Overlapping wrap-around.
    - [ ] Nyquist aliases (typically through PE direction).
    - [ ] Ghosts caused by external elements such as headsets or mirror frames.
    Exclude this T1w only if identifying these ghosts leads to revising the decision on the brain mosaic.

### Zoomed-in mosaic view of the brain:
- [ ] Check that the brain is not presented upside down. 
    This indicates a mistake in the header. 
    Either the header needs to be corrected manually or exclude the session.
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
   Exclude this particular T1w if any of these artifacts overlap cortical gray matter.
- [ ] Check for [zipper artifacts](https://mriquestions.com/zipper-artifact.html) and other EM interferences.
    Exclude this particular T1w if any of these artifacts overlap cortical gray matter.
- [ ] Check for excessive B<sub>1</sub> field inhomogeneity.
    Exclude only if it is evident that a coil failure happened.
- [ ] Check for inhomogeneous [*salt-and-pepper* noise patterns](https://en.wikipedia.org/wiki/Salt-and-pepper_noise).
    Generally, do not exclude this T1w image unless the noise pattern destroys cortical gray matter areas.
- [ ] Check for global [*salt-and-pepper* noise](https://en.wikipedia.org/wiki/Salt-and-pepper_noise) distribution.
    Generally, do not exclude this T1w image except evident imaging global failure.
- [ ] Check for low SNR characterized by a grainy picture. Generally, do not exclude this T1w image unless the noise pattern destroys cortical gray matter areas.

### Group report
- [ ] Check again the individual visual report of runs with outlying-low SNR, ensuring they do not fall into one of the [exclusion criteria](#anatomical-mri).

## Task behavior

For accurate estimation of task activation, it is essential to check the quality of both the fMRI images and the task behavior [Etzel 2023]. As such, it is important to verify that the subjects were attempting to perform the instructed task (i.e not sleeping and not responding randomly). One particularity of this project is that our single participant is the principal investigator of the project. As such, we trust that the participant, when actively awake, has enough incentive to follow the tasks accurately, even more so that the tasks are simple paradigms. We will however verify that the participant did not inadvertently fell asleep during one of the fMRI scans. 

- [ ] Leveraging the eye-tracking data, verify that the subject did not close his eyes for an extended period.

## Functional MRI

### Task fMRI exclusion criteria

!!! important "Our QC protocol is very lenient for task fMRI as those scans have been primarily acquired for QC purposes or to aid in methodological development, rather than holding scientific significance."

- [ ] Exclude the QCT fMRI scan only in case of extreme distortion of the image. Potential causes can be e.g. failure in the image reconstruction, mistake in the header leading to the image being in the wrong orientation, extreme noise...
- [ ] Exclude the BHT fMRI scan only in case of extreme distortion of the image. Potential causes can be e.g. failure in the image reconstruction, mistake in the header leading to the image being in the wrong orientation, extreme noise...

### RSfMRI exclusion criteria

!!! important "The following exclusion criteria are tailored to how the RSfMRI will be used."

    The RSfMRI images will be used to construct and analyze whole-brain functional connectomes.
    As such the quality of all regions in the brain is important, i.e. there is not a region where we can be more lenient.
    Additionally, a stringent QC is required for RSfMRI as noise sources that are highly correlated in different regions presents a high risk of spuriously inflation correlation estimation. 

#### Standard deviation of signal through time

- [ ] Check for ghosts within the brain:
      - [ ] Overlapping wrap-around.
      - [ ] Nyquist aliases or aliasing ghost (typically through PE direction).
      - [ ] Ghosts caused by external elements such as headsets or mirror frames.

      Exclude the session if any of these ghosts overlap cortical gray matter.

- [ ] Check for high-standard-deviation vertical strikes in the saggital plane of the standard deviation map.

#### Carpetplot and nuisance signals

- [ ] Check for periodic modulations of the signal, which is a sign that your signal is aliased by a regular and slow 
    motion, like respiration. 
    Exclude the session if the modulation is visible throughout the majority of the scan.
- [ ] Check for coil failures. They appear as abrupt changes in overall signal intensity not paired with motion 
    peaks. 
    Exclude the session if any coil failure is observed.
- [ ] Check for strong polarized structure in the crown. 
    Exclude the session if the polarized structure is prolonged throughout the majority of the scan and if the blocks 
    are particularly pronounced.
- [ ] Check for prolonged dark deflections accompanied by peaks in the FD trace as a sign for motion outbursts.
    Exclude the session in case the prolonged dark deflections cover more than half of the scan duration.
- [ ] Check for hyperintensity in single slices.
    Exclude the session if any single-slice hyperintensities are observed. Correlation analysis are likely to be biased by such peaks.

#### View of the background of the voxel-wise average of the BOLD timeseries

- [ ] Check for ghosts within the brain:
      - [ ] Overlapping wrap-around.
      - [ ] Ghosts caused by external elements such as headsets or mirror frames.

      Exclude the session if any of these ghosts overlap cortical gray matter.

      - [ ] Nyquist aliases or aliasing ghost (typically through PE direction).
        Exclude the session if the intensity of the ghost is similar to the intensity of the inside of the brain.

#### Average signal through time
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

- [ ] Check for low SNR characterized by a grainy picture. This dataset is specifically subject to this artifact, because we used multiband acceleration.

??? warning "Do not exclude subjects presenting susceptibility distortion artifacts yet!"

    For each session, we acquired fieldmaps that can be leveraged by fMRIPrep to perform susceptibility distortion correction. As such, those artifacts might be corrected by the preprocessing.

#### Group report
- [ ] Check again the individual visual report of runs with outlying-high FD, ensuring they do not fall into one of the [exclusion criteria](#function-mri).

- [ ] Check again the individual visual report of runs with outlying-high tSNR, ensuring they do not fall into one of the [exclusion criteria](#function-mri).

- [ ] Check again the individual visual report of runs with outlying-low SNR, ensuring they do not fall into one of the [exclusion criteria](#function-mri).

- [ ] Re-examine the individual visual report of sessions for which `fd_perc` > 50% and double-check that the data does not fall into one of the [exclusion criteria](#functional-mri).

## Diffusion MRI

## Physiological recordings

## Eye-tracking

# References

* Birn, Rasmus M. “Quality Control Procedures and Metrics for Resting-State Functional MRI.” Frontiers in Neuroimaging 2 (2023). <https://doi.org/10.3389/fnimg.2023.1072927>.

* Etzel, Joset A. “Efficient Evaluation of the Open QC Task fMRI Dataset.” Frontiers in Neuroimaging 2 (2023). https://www.frontiersin.org/articles/10.3389/fnimg.2023.1070274.

* Van Dijk, Koene R. A., Trey Hedden, Archana Venkataraman, Karleyton C. Evans, Sara W. Lazar, and Randy L. Buckner. “Intrinsic Functional Connectivity As a Tool For Human Connectomics: Theory, Properties, and Optimization.” Journal of Neurophysiology 103, no. 1 (January 2010): 297–321. <https://doi.org/10.1152/jn.00783.2009>.

