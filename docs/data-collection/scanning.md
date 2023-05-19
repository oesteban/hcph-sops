
!!!danger "BE REACTIVE in case the alarm rings"
    If at any point the participant rings the alarm, it is crucial to enter the scanning room and check on the participant IMMEDIATELY.

    - [ ] Enter the scanning room 
    - [ ] Only then turn off the alarm using the circular button either on the left or on the right of the bore.
        ![alarm_button](../assets/images/alarm_button.png)
    - [ ] Ask to the participant what's wrong. 
        - [ ] If he needs reassurance or information, provide it and confirm he can continue the scanning session. However, if you cannot communicate efficiently, take the participant out of the scanner.
        - [ ] If the participant does not feel well, provide assistance or call [WHO?] if it is really serious or if you have any doubts.

- [ ] Indicate the participant that the scanning will soon start:

    > Hey [NAME], we are about to start our first scan run.
    > For this scan, all you have to do is stay still, and look at the screen.
    > Are you ready?

- [ ] Start Exam
- [ ] Launch the AAhead_scout by pressing `Go`.

![launch_sequence.jpg](../assets/images/launch_sequence.jpg)

- [ ] Once the scout is finished, you can drag the localizer into the scan viewing window by draging the three superposed squares next to the sequence name to check its quality. A localizer of bad quality will present noise in the background. If the localizer is not ok, unplug and replug the head coil and reacquire the AAhead_scout sequence.

![drag_t1w.jpg](../assets/images/drag_t1w.jpg)

- [ ] Launch the T1w by pressing `Go`.
- [ ] While you run the T1w, there are a few important points to address:


    !!!warning "Important"
        - [ ] Adapt the reproin name of the sequence according to its "Phase Encoding Dir." field.
        - [ ] Open the parameters of the sequence named "fmap-phasediff__gre" and ensure that under Contrast>resc. the option "Magnitude et phase" is selected. This is crucial so that both the magnitude and the phase difference field map images are saved.
        - [ ] Open the DWI sequence and under the section [WHAT?], uncheck all the derivatives except `Diffusion weighted image`.

!!!note "Essentials for running an MRI session"
    Once the T1w is finished, you can drag the T1w into the scan viewing window. This will allow to tweek the field-of-view (FOV) for the DWI and BOLD sequences.
        
    - [ ] Open the next sequence by double clicking on it.
    - [ ] Make sure that the FOV (yellow square) includes the whole brain by tilting or translating the FOV. If the full brain, including the cerebellum, do not fit in the FOV, favorise making sure that the cortex is fully enclosed in the yellow square. For reproduciblity, it is better if the FOV across sequences have a similar center and a similar tilt. However, if it is not possible, the priority remains to include the whole brain in the FOV. 
    - [ ] If two sequences have the same resolution and the same number of slices, you can copy paste the FOV
        - [ ] Right click on the sequence for which the FOV was set
        - [ ] Select `Copy Parameters`
        - [ ] `Center [WHAT WAS THE NAME]`
    - [ ] Once the FOV is well placed, launch the sequence by pressing `Go`.

    ![adjustFOV.jpg](../assets/images/adjustFOV.jpg)

    - [ ] You can set the worker icon on the left of the sequence by clicking on it if you want to pause before starting that sequence. If the worker is not present, the sequence will launch automatically.

        ![worker_icon.jpg](../assets/images/worker_icon.jpg)

        - [ ] Note that the bloc with `__x__` introduces break. The scanner will warn you `Exam Paused`, just click `Continue`. Always leave the `Patient has Contrast Agent` checkbox empty as this protocol do not involve contrast agent.

        ![exam_paused.jpg](../assets/images/exam_paused.jpg)

    - [ ] Check in with participant frequently.
    - [ ] Watch for motion if you can see the participant, or use motion monitoring equipment.

- [ ] Launch the fieldmap `fmap-epi_dir-PA` sequence.
- [ ] While the fieldmap sequence is running,
    - [ ] check the FOV for the resting-state functional MRI (rsfMRI) sequence following the steps explained above.
    - [ ] Verify that the resting-state task `resting_state.psyexp` is open in psychopy, that you calibrated the ET and that the task is ready to receive the scanner trigger to start. 
- [ ] Inform the participant that the next sequence is rsfMRI.

    > Hey [NAME], we are about to start resting-state fMRI.
    > For this scan, all you have to do is stay still, and look at the movie.
    > Please do not close your eyes.
    > Are you ready?

- [ ] Launch the rsfMRI `func-bold_task-rest_dir-AP` sequence.
- [ ] While it is running, tweek the FOV for the next sequence.
- [ ] Once the sequence is over, close the resting-state task and open the breath-holding one `breath_holding_task.psyexp`.
    - [ ] Run the experiment by pressing the green play button. 
    - [ ] Enter the session and participant number in the pop up window. The Eyelink system setup page opens.
    - [ ] [DO WE HAVE TO DO THE CALIBRATION EVERYTIME OR NOT?]
    - [ ] Verify that the task is ready to receive input trigger to start.

- [ ] Inform the participant that the next sequence is breath-holding task fMRI. Repeat the instructions for the task.
    > Hey [NAME], we will proceed with the breath holding task.
    > I remind you that you have to breath following the rectangle color.
    > Green means inhale, orange means exhale and red means hold.
    > Remember to not follow the breathing instructions during the first block and to exhale the small amount of air you have remaining at the end of the hold.
    > Are you ready?

- [ ] Launch the `func-bold_task-bht_dir-AP` sequence.
- [ ] While it is running, 
    - [ ] Tweek the FOV for the next sequence.
    - [ ] Verify that in the next sequence parameters under Contrast>resc. the option `Magnitude et phase` is selected!
- [ ] Once the sequence is over, you need to stop manually the psychopy task by clicking on `t` (as fast as possible to avoid collecting more data than needed).
- [ ] Launch the fieldmap `fmap_phasediff_gre` sequence.
- [ ] While it is running, 
    - [ ] Tweek the FOV for the next sequence.
    - [ ] Verify that in the next sequence parameters under [WHERE?] that all the derivatives are unchecked except `Diffusion weighted image`.
- [ ] Inform the participant that the diffusion scan will follow.

    > Hey [NAME], the next sequence is diffusion. You can close your eyes if you want and just relax.
    > It will last XX minutes.

- [ ] Launch the diffusion `dwi-dwi_dir-PA` sequence.
- [ ] While it is running, tweek the FOV for the next sequence.
- [ ] Launch the fieldmap `fmap-epi_acq-highres_dir-AP` sequence.
- [ ] While it is running, 
    - [ ] Tweek the FOV for the next sequence.
    - [ ] Prepare the the quality control task 
        - [ ] Open `control_task.psyexp` in psychopy
        - [ ] Run the experiment by pressing the green play button. 
        - [ ] Enter the session and participant number in the pop up window. The Eyelink system setup page opens.
        - [ ] [DO WE HAVE TO DO THE CALIBRATION EVERYTIME OR NOT?]
        - [ ] Verify that the task is ready to receive input trigger to start.
- [ ] Inform the participant that we will proceed with the quality control task. Repeat task instructions.

    > Hey [NAME], the next scan is the quality control task.
    > I remind you that this task is composed of different subtasks.
    > In the first subtask, you must fix the cross.
    > In the second subtask, you must follow the points with your eyes. 
    > In the third subtask, tap the finger of your left or right hand depending on the word that flashes.
    > I remind you that during the finger tapping you MUST leave the alarm button, e.g., on your belly.

- [ ] Launch the control task fMRI `func-bold_task-qc_dir-AP` sequence.
- [ ] While it is running, tweek the FOV for the next sequence.
- [ ] [SINGLE_ECHO BOLD ?]
- [ ] Launch the T2w sequence.
- [ ] The exam is over, you can proceed with the [tear-down protocol](./tear-down.md).
