# QA/QC criteria for denoised data

## DOF distribution

- [ ] Check that the effective DOF for each session has a large positive value.
    If some DOFs are near zero or negative, revise the preprocessing to increase the motion censoring threshold, include fewer regressors, or tweak/eliminate band-pass filtering.

## FC distributions

- [ ] Check that the FC distributions appear similar across sessions and are gaussian, centered approximately around zero with a small positive mean <sup>[1]</sup>.
    If the FC distributions appear shifted towards positive values, skewed, flat, or bimodal, the denoising was either too aggressive for the number of functional frames available, or the BOLD signal is still contaminated with residual noise.
    If the sessions with a non-conform distribution present a DOF close to zero or negative:
    
        - [ ] Revise the denoising strategy to include fewer regressors, and/or tweak/eliminate band-pass filtering.
        - [ ] Revise the preprocessing to increase the motion censoring threshold.
    - [ ] Exclude the sessions with the non-conform distribution if DOFs is a large positive value.

## QC-FC distributions

- [ ] Check that the QC-FC distribution<sup>[2]</sup> and the null distribution represented by the red dotted line are approximately equivalent by assessing the QC-FC% value corresponding to the distance between the observed and the null distributions. 
    - [ ] Revise the preprocessing by lowering the motion censoring threshold, including more regressors, or tweaking the band-pass filtering if the QC-FC distribution does not meet the 95% cutoff.
    - [ ] Exclude sessions associated with extreme IQM outliers if the 95% cutoff is still not met after revising the preprocessing.
    - [ ] Iteratively exclude the session with the highest `fd_perc` until that cutoff is met if the 95% cutoff is still not met.

## QC-FC versus Euclidean distance

- [ ] Check that there is no significant correlation between QC-FC correlations and Euclidean distance separating the nodes<sup>[2]</sup>.

# References

[1]: https://doi.org/10.3389/fnins.2023.1092125 "Morfini, F., Whitfield-Gabrieli, S., and Nieto-Castañón, A. “Functional Connectivity MRI Quality Control Procedures in CONN.” Front Neurosci 17 (2023). doi:10.3389/fnins.2023.1092125"
[2]: https://doi.org/10.1016/j.neuroimage.2017.03.020 "Ciric, R. et al. “Benchmarking of Participant-Level Confound Regression Strategies for the Control of Motion Artifact in Studies of Functional Connectivity. (2017)” NeuroImage, doi:10.1016/j.neuroimage.2017.03.020"
[3]: https://doi.org/10.1016/j.neuroimage.2017.03.056 "Bright, M. & Murphy, K., Cleaning up the fMRI time series: Mitigating noise with advanced acquisition and correction strategies. (2017) NeuroImage. doi:10.1016/j.neuroimage.2017.03.056"


