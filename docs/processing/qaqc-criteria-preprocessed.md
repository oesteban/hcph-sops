
## Summary

## Anatomical

### Anatomical conformation

### Brain mask and brain tissue segmentation of the T1w

- [ ] Check for residual intensity non-uniformity (INU).
  If the INU is clearly visible, tweak the INU correction and re-run *fMRIPrep*.
- [ ] Check that the brain mask does not cut off part of the brain and/or contain holes surrounding signal drop-out regions.
  If it is not the case, tweak the brain mask estimation and re-run *fMRIPrep*.
- [ ] Check that the brain mask does not include parts that are clearly NOT brain.
  Typically, this appears as bumps surrounding high-intensity areas of signal outside the brain (e.g dura or skull).
  If it is not the case, tweak skull-stripping and re-run *fMRIPrep*.
- [ ] Assess the quality of the segmentation:
    - [ ] Check that the blue line correctly outlines the boundary between GM and WM.
    - [ ] Check that the magenta line outlines ventricles.
    - [ ] Check that the contours do not exclude single voxels within piecewise-smooth regions (generally more identifiable in the WM and inside the ventricles).
      Careful if those single excluded voxels only appear close to tissue boundaries, they are likely misclassified because of partial volume effect, as such it does not consistitute an exclusion criteria.
    - [ ] Check that the contours do not include other tissues than the tissue of interest (GM; magenta, WM; blue). 
    - [ ] If you found any of the issues above, tweak the segmentation and re-run *fMRIPrep*.

### Spatial normalization of the anatomical T1w reference

- [ ] In order of importance, the following structures should be correctly aligned: 1. ventricles, 2. subcortical regions, 3. corpus callosum, 4. cerebellum, 5. cortical GM.
    Tweak the spatial normalization and re-run *fMRIPrep* in case of a misalignment of the ventricles, subcortical regions, or the corpus callosum.
    You can, however, be more lenient with GM alignment.
- [ ] Check for severe stretching or distortion of the T1w.
  If observed, tweak the normalization and re-run *fMRIPrep*.

### Surface reconstruction

!!! note "If you used the `--fs-no-reconall` flag to skip surface-based preprocessing, the section of the report will not exist"

- [ ] Check that the WM-GM boundary outlines (blue line) matches the boundary observed in the underlying image.
- [ ] Verify that the WM and pial surface do not cross or overlap each other.
- [ ] Verify that the pial surface (red line) does not extend past the actual pial boundary.

!!! Tip "Evaluating the quality of brain surfaces"

    As we will proceed with voxel-wise analysis, re-running *fMRIPrep* is necessary only when the reconstructed surfaces are extremely inacurate.
    That typically only happens in the presence of extreme artifacts that we should have captured previously in the step of [QA/QC for unprocessed data using *MRIQC*](../data-management/qaqc-criteria.md).

## Functional

### Textual summary

- [ ] Verify that in the field `Multi-echo EPI sequence` four echoes were detected.
  If not, check that four echoes were present in the unprocessed data and that they are no typos in their filename.
  Exclude the session if those issues cannot be fixed.

### T2* map

### T2* gray-matter values

### Alignment of functional and anatomical MRI data

- [ ] Check that the BOLD and the T1w image are well aligned:
    - [ ] Verify that the image boundaries as well as the anatomical landmarks, such as the ventricles and the corpus callosum, appear in the same place when toggling between images.
    - [ ] Verify that the white and pial surface outline (red and blue lines) correspond well to the tissues boundaries in the BOLD image.
- [ ] Check that no residual susceptibility distortion affects the BOLD image. Susceptibility distortion manifests as signal drop-outs or brain distortions.

### Brain mask and (anatomical/temporal) CompCor ROIs

- [ ] Verify that the brain mask does not clip GM areas out.
    Note that a hole in the middle of the brain mask is not a problem, as this will not disrupt co-registration.
    Note also that it is not a problem that the brain mask is loose around the brain.
- [ ] Verify that the temporal CompCor mask appears as a collection of points scattered around the brain (with typically higher density in the outer rim of the frontal lobe and close to the brainstem) and does not form suspiciously aggregated shapes (an indicator of an underlying artifact).

### BOLD summary

The carpet plot MUST appear homogeneous:

- [ ] Check that the carpet plot is unaffected by strong dark deflections (signal drops) associated with motion peaks (particularly in the brain edge).
- [ ] Check that no periodic modulation is visible throughout the plot.
- [ ] Check that the brain edge has no large black bands.
- [ ] Check for extensive signal drops that may reveal a coil failure.

### Correlations between nuisance regressors

- [ ] Note down the regressors that are highly correlated and take care of not including more than one per correlated group in the nuisance regression model.
