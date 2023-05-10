
- [ ] Indicate the participant that the scanning will soon start:

    > Hey [NAME], we are about to start our first scan run.
    > For this scan, all you have to do is stay still, and look at the screen.
    > Are you ready?

- [ ] Start Exam
- [ ] Launch the AAhead_scout by pressing "Continue" [INSERT PICTURE].
- [ ] Once the scout is finished, you can drag the localizer into the scan viewing window by draging the three superposed squares next to the sequence name to check its quality. A localizer of bad quality will present noise in the background. If the localizer is not ok [WHAT?]
- [ ] Launch the T1w by pressing "Continue".
- [ ] While you run the T1w, there are a few important points to address:


    !!!warning "Important"
        - [ ] Adapt the reproin name of the sequence according to its "Phase Encoding Dir." field.

- [ ] Open the parameters of the sequence named "fmap-phasediff__gre" and ensure that under Contrast>resc. the option "Magnitude et phase" is selected. This is crucial so that both the magnitude and the phase difference field map images are saved.
- [ ] Similarly, once the T1w is finished, you can drag the T1w into the scan viewing window. This will allow to tweek the field-of-view (FOV) for the DWI and BOLD sequences.
    - [ ] Make sure that the FOV (yellow square) includes the whole brain. If the full brain, including the cerebellum, do not fit in the FOV, favorise making sure that the cortex is fully enclosed in the yellow square. Careful for reproduciblity do not tilt the FOV; just translate it.
    - [ ] If two sequences have the same resolution and the same number of slices, you can copy paste the FOV by clicking right clicking on the sequence for which the FOV was set, select "copy parameters>[WHAT WAS THE NAME]".
    - [ ] Once the FOV is well placed, launch the sequence by pressing "Go".

- [ ] You can set the worker icon on the left of the sequence if you want to pause before starting that sequence. If the worker is not present, the sequence will launch automatically.

- [ ] Check in with participant frequently.
- [ ] Watch for motion if you can see the participant, or use motion monitoring equipment.
