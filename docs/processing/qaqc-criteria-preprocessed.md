# QA criteria for preprocessed data

## Summary
- [ ] Check that the anatomical processing is based on the number of T1w images you expected and that no excluded T1w was mistakenly included in the processing.
  If that is not the case, use the *fMRIPrep* `--bids-filter-file` flag to exclude unwanted T1w from the processing and re-run *fMRIPrep*.
- [ ] Verify that the standard output space corresponds to the one you want.
  If that is not the case, assign the correct output space to the `--output-spaces` flag of *fMRIPrep* and re-run *fMRIPrep*.

## Anatomical

### Anatomical conformation

### Brain mask and brain tissue segmentation of the T1w
- [ ] Assess the quality of the segmentation:
    - [ ] Check that the blue line correctly outlines the boundary between GM and WM.
    - [ ] Check that the magenta line outlines ventricles.
    - [ ] Check that the contours do not exclude single voxels within piecewise-smooth regions (generally more identifiable in the WM and inside the ventricles).
      Careful if those single excluded voxels only appear close to tissue boundaries, they are likely misclassified because of partial volume effect, as such it does not constitute an exclusion criteria.
    - [ ] Check that the contours do not include other tissues than the tissue of interest (GM; magenta, WM; blue). 
    - [ ] If you found any of the issues above, do not use the CompCor confounds for nuisance regression.

### Spatial normalization of the anatomical T1w reference

- [ ] In order of importance, the following structures should be correctly aligned: 1. ventricles, 2. subcortical regions, 3. corpus callosum, 4. cerebellum, 5. cortical GM.
    Tweak the spatial normalization and re-run *fMRIPrep* in case of a misalignment of the ventricles, subcortical regions, or the corpus callosum.
    You can, however, be more lenient with GM alignment.
- [ ] Check for severe stretching or distortion of the T1w.
  If observed, use the preprocessed BOLD images in subject space for the analysis rather than MNI.

  !!! note "We can afford to work in subject space because our study is based on a single subject"

## Functional

### Textual summary

- [ ] Check that the repetition time is the expected 1.6s. 
  If not:
    - [ ] Investigate whether the TR has been mistakenly reported in the Nifti header, fix it and re-run *fMRIPrep*.
    - [ ] If the session has been acquired with the wrong TR, [exclude that session](#textual-summary-1).
- [ ] Verify that slice timing correction was applied. 
  If not, fix the problem and re-run *fMRIPrep*.
- [ ] Verify that susceptibility distortion correction was applied. 
  If not, check that fieldmaps were present in the unprocessed data, that they are no typos in their filename and that the field `B0FieldSource` and `B0FieldIdentifier` have been correctly setup in the JSON sidecars.
- [ ] Verify that registration was applied. 
  If not, fix the problem and re-run *fMRIPrep*.
- [ ] Check that four echoes are detected in the field `Multi-echo EPI sequence`.
  If not, check that four echoes were present in the unprocessed data and that they are no typos in their filename.
  [Exclude the session if those issues cannot be fixed](#textual-summary-1).

### T2* map

### T2* gray-matter values

### Alignment of functional and anatomical MRI data

- [ ] Check that the BOLD and the T1w image are well aligned:
    - [ ] Verify that the image boundaries as well as the anatomical landmarks, such as the ventricles and the corpus callosum, appear in the same place when toggling between images.
    - [ ] Verify that the white and pial surface outline (red and blue lines) correspond well to the tissues boundaries in the BOLD image.
    - [ ] If issues are observed in the points above, tweak the co-registration by increasing its degrees of freedom using the `--bold2t1w-dof 9` flag of *fMRIPrep* and re-run *fMRIPrep*.
    - [ ] If that did not solve co-registration problem, assign the fMRIPrep flag `--bold2t1w-init header` and re-run *fMRIPrep*.
    - [ ] If co-registration is still faulty, [exclude this session](#alignment-of-functional-and-anatomical-mri-data).

- [ ] Check that no large residual susceptibility distortion affects the BOLD image. Susceptibility distortion manifests as signal drop-outs or brain distortions.
    - [ ] If large susceptibility distortion remains, double-check that [susceptibility distortion correction was applied correctly by *fMRIPrep*](#textual-summary).
    - [ ] If this issue cannot be fixed, [exclude the session](#alignment-of-functional-and-anatomical-mri-data-1).

### Brain mask and (anatomical/temporal) CompCor ROIs

- [ ] Verify that the brain mask does not clip GM areas out.
    Note that a hole in the middle of the brain mask is not a problem, as this will not disrupt co-registration.
    Note also that it is not a problem that the brain mask is loose around the brain.
    If the brain mask does not appear as it should, make sure you should not 
- [ ] Verify that the temporal CompCor mask appears as a collection of points scattered around the brain (with typically higher density in the outer rim of the 
    frontal lobe and close to the brainstem) and does not form suspiciously aggregated shapes (an indicator of an underlying artifact).
    If the mask does not appear as it should, make sure to not use temporal CompCor confounds in the nuisance regression.

### BOLD summary

The carpet plot MUST appear homogeneous:

- [ ] Check that the carpet plot is unaffected by strong dark deflections (signal drops) associated with motion peaks (particularly in the brain edge).
- [ ] Check that no periodic modulation is visible throughout the plot.
- [ ] Check that the brain edge has no large black bands.

If any of the latter patterns is observed, flag the session and double check that the carpetplot appears homogeneous after denoising. 

### Correlations between nuisance regressors

- [ ] Note down the regressors that are highly correlated and take care of not including more than one per correlated group in the nuisance regression model.

# Exclusion criteria for fMRIPrep anatomical processing

## Anatomical

### Brain mask and brain tissue segmentation of the T1w

- [ ] Check for residual intensity non-uniformity (INU).
  If the INU is clearly visible, tweak the INU correction and re-run *fMRIPrep*.
- [ ] Check that the brain mask does not cut off part of the brain and/or contain holes surrounding signal drop-out regions.
  If it is not the case, exclude the data.
- [ ] Check that the brain mask does not include parts that are clearly NOT brain.
  Typically, this appears as bumps surrounding high-intensity areas of signal outside the brain (e.g dura or skull).
  If it is not the case, exclude the data.

### Surface reconstruction

!!! note "If you used the `--fs-no-reconall` flag to skip surface-based preprocessing, the section of the report will not exist"

- [ ] Check that the WM-GM boundary outlines (blue line) matches the boundary observed in the underlying image.
- [ ] Verify that the WM and pial surface do not cross or overlap each other.
- [ ] Verify that the pial surface (red line) does not extend past the actual pial boundary.

!!! Tip "Evaluating the quality of brain surfaces"

    As we will proceed with voxel-wise analysis, re-running *fMRIPrep* is necessary only when the reconstructed surfaces are extremely inaccurate.
    That typically only happens in the presence of extreme artifacts that we should have captured previously in the step of [QA/QC for unprocessed data using *MRIQC*](../data-management/qaqc-criteria.md).

# Exclusion criteria for preprocessed task fMRI

!!! important "We do not put together exclusion criteria for preprocessed task fMRI"

    Our QC protocol is very lenient for task fMRI as those scans have been primarily acquired for QC purposes or to aid in methodological development, rather than holding scientific significance. 
    Task fMRI are excluded only in case of extreme distortion of the image, however such cases would have been already captured by [the first QC checkpoint](../data-management/mriqc.md#visualizing-mriqcs-individual-reports).

# Exclusion criteria for preprocessed RSfMRI

## Functional

### Textual summary

- [ ] If the RSfMRI has been acquired with a TR different from 1.6s, exclude that scan. It is likely the other fMRI scans have been mistakenly acquired with the  
  wrong TR, so double-check the task fMRI.

- [ ] If the four echoes are not detected in the field `Multi-echo EPI sequence` even after checking their presence in the unprocessed data and that they are no 
  typos in their filename, exclude the session.

### Alignment of functional and anatomical MRI data

- [ ] If the BOLD to T1w image alignment cannot be fixed by [tweaking the co-registration](#alignment-of-functional-and-anatomical-mri-data), the RSfMRI scan has 
  to be excluded.
- [ ] If large susceptibility distortion remains [despite previous measures](#alignment-of-functional-and-anatomical-mri-data), exclude the RSfMRI scan.

### BOLD summary

- [ ] Check for extensive signal drops that may reveal a coil failure. If such pattern is observed, exclude the RSfMRI scan.
