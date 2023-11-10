# QA/QC criteria

The following lists the pre-defined exclusion criteria for analyses of whole-brain structural and functional connectomes.

## Anatomical MRI

??? info "The exclusion criteria are tailored to how the anatomical images will be used."

    Given our planned analysis, the T1w image will be used for the spatial alignment with the standard MNI152NLin2009cAsym template.
    In addition, surface reconstructions from the T1w image will guide the co-registration of structural and functional (BOLD) images in fMRIPrep.
    Since the latter preprocessing steps are relatively robust to structural images with mild artifacts, the exclusion criteria for unprocessed T1w images are lenient.
    However, individual T1w images may be excluded without such a decision lead to exclusion of the whole session in which it belongs.
    We annotate subjects with visible artifacts in the T1w images in order to ensure rigorous scrutinizing of spatial normalization and surface reconstruction outputs from fMRIPrep (if both modalities passed the first QC checkpoint with MRIQC).
    The explanation and the description of the flagging criteria 1 to 7 are the same as their counterpart in the previous section.



## Anatomical

### Zoomed-in brain mosaic:
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

- [ ] Check for other artifacts such as fat shifts or RF spoiling within the brain.
   Exclude this particular T1w if any of these ghosts overlap cortical gray matter.
- [ ] Check for zipper artifacts and other EM interferences.
    Exclude this particular T1w if any of these ghosts overlap cortical gray matter.
- [ ] Check for excessive B<sub>1</sub> field inhomogeneity.
    Exclude only if it is evident that a coil failure happened.
- [ ] Check for inhomogeneous *salt-and-pepper* noise patterns.
    Generally, do not exclude this T1w image unless the noise pattern destroys cortical gray matter areas.
- [ ] Check for global *salt-and-pepper* noise distribution.
    Generally, do not exclude this T1w image except evident imaging global failure.

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

... continued ...


## Functional MRI

### Resting-state
### Quality control task
### Breath-holding task

## Diffusion MRI

## Physiological recordings

## Eye-tracking

# References

* Aquino, Kevin M., Ben D. Fulcher, Linden Parkes, Kristina Sabaroedin, and Alex Fornito. 2020. “Identifying and Removing Widespread Signal Deflections from FMRI Data: Rethinking the Global Signal Regression Problem.” NeuroImage 212 (May): 116614. <https://doi.org/10.1016/j.neuroimage.2020.116614>.

* Behzadi, Yashar, Khaled Restom, Joy Liau, and Thomas T. Liu. 2007. “A Component Based Noise Correction Method (CompCor) for BOLD and Perfusion Based FMRI.” NeuroImage 37 (1): 90–101. <https://doi.org/10.1016/j.neuroimage.2007.04.042>.

* Ciric, Rastko, Daniel H. Wolf, Jonathan D. Power, David R. Roalf, Graham L. Baum, Kosha Ruparel, Russell T. Shinohara, et al. 2017. “Benchmarking of Participant-Level Confound Regression Strategies for the Control of Motion Artifact in Studies of Functional Connectivity.” NeuroImage, Cleaning up the fMRI time series: Mitigating noise with advanced acquisition and correction strategies, 154: 174–87. <https://doi.org/10.1016/j.neuroimage.2017.03.020>.

* Cox, R.W., J. Ashbruner, H. Breman, K. Fissell, C. Haselgrove, and C. J. Holmes. 2004. “A (Sort of) New Image Data Format Standard: NIfTI-1.” In the 10th Annual Meeting of the Organization for Human Brain Mapping in Budapest.

* Cusack, Rhodri. 2006. “CommonArtefacts - MRC CBU Imaging Wiki.” March 2006. <https://imaging.mrc-cbu.cam.ac.uk/imaging/CommonArtefacts>.

* Esteban, Oscar, Azeez Adebimpe, Christopher J. Markiewicz, Mathias Goncalves, Ross W. Blair, Matthew Cieslak, Mikaël Naveau, et al. 2021. “The Bermuda Triangle of D- and f-MRI Sailors - Software for Susceptibility Distortions (SDCFlows).” OSF Preprints. <https://doi.org/10.31219/osf.io/gy8nt>.

* Fischl, Bruce. 2012. “FreeSurfer.” NeuroImage 62 (2): 774–81. https://doi.org/10.1016/j.neuroimage.2012.01.021.

* Glen, Daniel R., Paul A. Taylor, Bradley R. Buchsbaum, Robert W. Cox, and Richard C. Reynolds. 2020. “Beware (Surprisingly Common) Left-Right Flips in Your MRI Data: An Efficient and Robust Method to Check MRI Dataset Consistency Using AFNI.” Frontiers in Neuroinformatics 14. <https://www.frontiersin.org/articles/10.3389/fninf.2020.00018>.

* Hutton, Chloe, Andreas Bork, Oliver Josephs, Ralf Deichmann, John Ashburner, and Robert Turner. 2002. “Image Distortion Correction in FMRI: A Quantitative Evaluation.” NeuroImage 16 (1): 217–40. <https://doi.org/10.1006/nimg.2001.1054>.

* Klapwijk, Eduard T., Ferdi van de Kamp, Mara van der Meulen, Sabine Peters, and Lara M. Wierenga. 2019. “Qoala-T: A Supervised-Learning Tool for Quality Control of FreeSurfer Segmented MRI Data.” NeuroImage 189 (April): 116–29. <https://doi.org/10.1016/j.neuroimage.2019.01.014>.

* Power, Jonathan D. 2017. “A Simple but Useful Way to Assess FMRI Scan Qualities.” NeuroImage, Cleaning up the fMRI time series: Mitigating noise with advanced acquisition and correction strategies, 154 (July): 150–58. <https://doi.org/10.1016/j.neuroimage.2016.08.009>.

* Provins, Céline, Yasser Alemán-Gómez, Martine Cleusix, Raoul Jenni, Jonas Richiardi, Patric Hagmann, and Oscar Esteban. 2022. “Defacing Biases Manual and Automated Quality Assessments of Structural MRI with MRIQC.” OSF Preprints. <https://doi.org/10.31219/osf.io/8mcyz>.

* Provins, Céline, Christopher J. Markiewicz, Rastko Ciric, Mathias Goncalves, César Caballero-Gaudes, Russell Poldrack, Patric Hagmann, and Oscar Esteban. 2022. “Quality Control and Nuisance Regression of FMRI, Looking out Where Signal Should Not Be Found.” OSF Preprints. <https://doi.org/10.31219/osf.io/hz52v>.

* White, Tonya, Philip R. Jansen, Ryan L. Muetzel, Gustavo Sudre, Hanan El Marroun, Henning Tiemeier, Anqi Qiu, Philip Shaw, Andrew M. Michael, and Frank C. Verhulst. 2018. “Automated Quality Assessment of Structural Magnetic Resonance Images in Children: Comparison with Visual Inspection and Surface-Based Reconstruction.” Human Brain Mapping 39 (3): 1218–31. <https://doi.org/10.1002/hbm.23911>.

