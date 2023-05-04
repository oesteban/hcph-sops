## Scanning a participant

- [ ] Indicate the participant that the scanning will soon start:

    > Hey [NAME], we are about to start our first scan run.
    > For this scan, all you have to do is stay still, and look at the screen.
    > Are you ready?

- [ ] Start Exam
- [ ] Launch the AAhead_scout by pressing "Continue"
- [ ] Launch the T1w by pressing "Continue"
- [ ] Once the T1w is finished, you can drag the T1w into the scan viewing window by draging the three superposed squares next to the sequence name. This will allow to tweek the field-of-view (FOV) for the DWI and BOLD sequences
- [ ] Make sure that the FOV (yellow square) includes the whole brain. If the full brain, including the cerebellum, do not fit in the FOV, favorise making sure that the cortex is fully enclosed in the yellow square. Careful for reproduciblity do not tilt the FOV; just translate it.
- [ ] Once the FOV is well placed, launch the sequence by pressing "Go"
- [ ] If two sequences have the same resolution and the same number of slices, you can copy paste the FOV by clicking right clicking on the sequence for which the FOV was set, select "copy parameters>[WHAT WAS THE NAME]"
- [ ] You can set the worker icon on the left of the sequence if you want to pause before starting that sequence. If the worker is not present, the sequence will launch automatically.

- [ ] !!! Adapt the reproin name of the sequence according to its "Phase Encoding Dir." field !!!

**Scan console checklist**

Parameters to double check

  - [ ] MUX: 3
  - [ ] TR: 1490
  - [ ] TE: 3

Console instructions 

  - [ ] 1. Run localizer
      - [ ] SAVE Rx
      - [ ] SCAN

  - [ ] 2. Prescribe rest  
      - [ ] Select `task-rest_bold` and click once on the localizer image that appears.
      - [ ] Move the block of lines so that the whole brain is covered, with plenty of space in the front and back, top and bottom.
      - [ ] **Do not run yet!**

  - [ ] 3. Run shimming
      - [ ] Select **GE HOS FOV28**
      - [ ] SAVE Rx
      - [ ] SCAN
      - [ ] Adjust circle around the brain so that the red circle goes as tightly around the brain as possible
      - [ ] CALCULATE
      - [ ] **Done**
      - [ ] Select the same scan again
      - [ ] SCAN
      - [ ] Add to Same Series
      - [ ] CALCULATE
          - [ ] If the difference between expected and actual is  < 1 continue; else repeat. 

  - [ ] 4. Fieldmap
      - [ ] Select fmap-fieldmap 
      - [ ] Click the brain once, adjust the prescription so that it covers the whole brain. 
      - [ ] SCAN 

  - [ ] 5. Rest Scan 
      - [ ] Select `task-rest_bold`
      - [ ] Already prescribed from shim setup.  
      - [ ] Put the fixation cross on the bore monitor, check in with the participant:

           > Hey [NAME], we are about to start our first scan run.
           > For this scan, all you have to do is stay still, and look at the screen.
           > Let us know when you're ready to begin by pressing any button.

      - [ ] PREP SCAN
      - [ ] Physio setup 
          - [ ] Click scan drop down menu 
          - [ ] Research
          - [ ] Phys_flag_record
              - [ ] Change cv to 1
      - [ ] SCAN

  - [ ] 6. Task scans
      - [ ] Select `task-[TASK NAME]_bold`
      - [ ] Copy prescription from rest (GRx Toolbar -> Select scan to copy from -> Copy) 
      - [ ] SAVE Rx
      - [ ] Put the task window on the bore monitor
          - [ ] check in with the participant.

	           > Hey [NAME], we are about to start our next scan run.
	           > For this scan, [TASK INSTRUCTIONS].
	           > Let us know when you're ready to begin by pressing any button.

          - [ ] Advance through practice trials, keeping an eye on the participant's performance on the task if applicable.

      - [ ] PREP SCAN
      - [ ] Physio setup 
          - [ ] Click scan drop down menu 
          - [ ] Research
          - [ ] Phys_flag_record
              - [ ] Change cv to 1
      - [ ] SCAN

  - [ ] 7. Anatomical scans (T1w and T2w)
      - [ ] Prescribe by clicking the localizer image once, and adjust the blue box with crosshairs so that the whole brain is covered, with plenty of space in the front and back, top and bottom.  
      - [ ] SAVE Rx
      - [ ] Put the fixation cross on the bore monitor, check in with the participant:

           > Hey, [NAME], we are about to start our next scan run.
           > For this scan, all you have to do is stay still.
           > Let us know when you're ready to begin by pressing any button.

      - [ ] SCAN 
