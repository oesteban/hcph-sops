# QA/QC criteria for denoised data

## DOF distribution
- [ ] Check that the DOF for each session has a large positive value. If some DOF are close to zero or negative, revise the preprocessing to increase the motion censoring threshold, include less regressors or tweak/eliminate band-pass filtering.

## FC distributions
- [ ] Check that the FC distributions appear similar across sessions and are gaussians, centered approximately around zero with a small positive mean [Morfini et al. 2023]. If the FC distributions appear shifted towards positive values, skewed, flat or bimodal, the denoising was either too aggressive for the number of functional frames available or the BOLD signal is still contaminated with residual noise.
    - [ ] If the sessions with a non-conform distribution present a DOF close to zero or negative, revise the preprocessing to increase the motion censoring threshold, include less regressors or tweak/eliminate band-pass filtering.
    - [ ] If the DOF has a large positive value, exclude the sessions with the non-conform distribution.

## QC-FC distributions
- [ ] Check that the QC-FC distribution [Ciric et al. 2017] and the null distribution represented by the red dotted line are approximately equivalent and check the QC-FC% value which corresponds to the distance between the observed and the null distributions. 
    - [ ] If the QC-FC distribution do not meet the 95% cutoff, revise the preprocessing by lowering the motion censoring threshold, including more regressors or tweaking the band-pass filtering.
    - [ ] If the 95% cutoff is still not met after revising the preprocessing, eliminate all sessions associated with extreme IQM outliers.
    - [ ] If the 95% cutoff is still not met, iteratively exclude the session with the highest `fd_perc` until that cutoff is met.

## QC-FC versus euclidean distance
- [ ] Check that there is no significant correlation between QC-FC correlations and euclidean distance separating the nodes [Ciric et al. 2017].

# References

* Ciric, Rastko, Daniel H. Wolf, Jonathan D. Power, David R. Roalf, Graham L. Baum, Kosha Ruparel, Russell T. Shinohara, et al. “Benchmarking of Participant-Level Confound Regression Strategies for the Control of Motion Artifact in Studies of Functional Connectivity.” NeuroImage, Cleaning up the fMRI time series: Mitigating noise with advanced acquisition and correction strategies, 154 (juillet 2017): 174–87. <https://doi.org/10.1016/j>.neuroimage.2017.03.020.

* Morfini, Francesca, Susan Whitfield-Gabrieli, and Alfonso Nieto-Castañón. “Functional Connectivity MRI Quality Control Procedures in CONN.” Frontiers in Neuroscience 17 (2023). <https://doi.org/10.3389/fnins.2023.1092125>.


