

### Scheduling

#### One week BEFORE THE FIRST SESSION

- [x] Send a copy of the MRI Safety and screening form to the participant over email and confirm reception
- [x] Confirm that participant has read and understood the document, and in particular, double-check that they do not have any MRI contraindications
- [x] Remind participant that any jewelry should be removed prior to the scan 
- [x] Confirm clothing:
  - [ ] if allowed to wear street clothes, remind participant to avoid clothing with metal or that would uncomfortable to lie in for the duration of the scan; otherwise
  - [x] remark the participant they will be given a gown and they will need to change before every session.
- [x] If participant has indicated nervousness or history of claustrophobia, utilize mock scanner 

#### DAY OF SCAN, prior to participant arrival

- [x] Prepare consent documents (first session only)
- [x] Prepare an MRI safety screener 
- [x] Prepare scrubs and MR-compatible glasses if applicable
- [x] Setup scanner room and peripherals:
  - [x] prepare the 64-channel headcoil,
  - [x] prepare paddings: under-knee padding, neck padding, inflatable head-paddings
  - [x] prepare a blanket
  - [x] prepare a new pair of earplugs
  - [x] prepare the respiration belt, as well as the placeholder for the ECG and other physio sensors
  - [x] connect the cable from the RJ-45 output of the syncbox to the first filter (VNC connector; has a label "External signal") in the cupboard covering the access panel to the Faraday cage. The cable might be stored in the lower left cupboard of office 071. Make sure you will have access to the cable with sufficient time ahead.
    - [x] On the scanner console, checke the external signal input registers triggers from the syncbox
    - [x] prepare a thermometer
    - [x] prepare a blood preasure meter
  - [x] connect the USB cable from the syncbox to the PC HOS54938 (next to the DVD printer/burner)
  - [x] Set up the eye-tracking:
    - [x] 
  - [x] Open psychopy 3 and this protocol's files, make sure you have internet access to a Git repository and check files are up-to-date.
  - [x] Prepare the gas-analyzer:
    - [x] Prepare the canule tube, which is introduced through the tube in the access panel
    - [x] Prepare a new canule
- [x] Check stimulus display and response device:
  - [x] Check the movie to be displayed is ready
  - [x] Check the execution of the Breath holding task
  - [x] Check the execution of the finger tapping task

#### DAY OF SCAN, right when the participant arrives

- [x] Have participant fill out consent documents and MRI safety screener, and verbally confirm responses, paying attention to frequently forgotten devices and implants, like orthodontia
- [x] Have participant empty their pockets or change into scrubs, and remove all jewelry/hair accessories and check for any missed metallic objects with the scan center’s preferred method
- [x] Instruct participant on staying still and encourage them to request breaks if necessary
- [x] Describe the participant how the session will develop, with special attention to tasks. Answer all the questions that may arise.
- [x] Show the alarm button to the participant, instruct them to hold it on their hand throughout the session, with the exception of the finger tapping task for which they should leave it on their belly
- [x] Place participant on the scanner's bed:
  - [x] Accommodate the head inside the head coil
  - [x] Check again that it is the 64-channel head coil
  - [x] Check the scanner's screen that the three coils [SAY MORE SPECIFIC] are connected and active
  - [x] Solicit feedback on participant’s comfort while positioning them on the scanner bed and suggest ergonomic positioning of arms to avoid discomfort
  - [x] Make sure the speaker is audible (and not annoying) and confirm the participant's feedback

#### SCAN TIME

**Scan console checklist**

Parameters to double check

  - [x] MUX: 3
  - [x] TR: 1490
  - [x] TE: 3

Console instructions 

  - [x] 1. Run localizer
      - [x] SAVE Rx
      - [x] SCAN

  - [x] 2. Prescribe rest  
      - [x] Select `task-rest_bold` and click once on the localizer image that appears.
      - [x] Move the block of lines so that the whole brain is covered, with plenty of space in the front and back, top and bottom.
      - [x] **Do not run yet!**

  - [x] 3. Run shimming
      - [x] Select **GE HOS FOV28**
      - [x] SAVE Rx
      - [x] SCAN
      - [x] Adjust circle around the brain so that the red circle goes as tightly around the brain as possible
      - [x] CALCULATE
      - [x] **Done**
      - [x] Select the same scan again
      - [x] SCAN
      - [x] Add to Same Series
      - [x] CALCULATE
          - [x] If the difference between expected and actual is  < 1 continue; else repeat. 

  - [x] 4. Fieldmap
      - [x] Select fmap-fieldmap 
      - [x] Click the brain once, adjust the prescription so that it covers the whole brain. 
      - [x] SCAN 

  - [x] 5. Rest Scan 
      - [x] Select `task-rest_bold`
      - [x] Already prescribed from shim setup.  
      - [x] Put the fixation cross on the bore monitor, check in with the participant:

           > Hey [NAME], we are about to start our first scan run.
           > For this scan, all you have to do is stay still, and look at the screen.
           > Let us know when you’re ready to begin by pressing any button.

      - [x] PREP SCAN
      - [x] Physio setup 
          - [x] Click scan drop down menu 
          - [x] Research
          - [x] Phys_flag_record
              - [x] Change cv to 1
      - [x] SCAN

  - [x] 6. Task scans
      - [x] Select `task-[TASK NAME]_bold`
      - [x] Copy prescription from rest (GRx Toolbar -> Select scan to copy from -> Copy) 
      - [x] SAVE Rx
      - [x] Put the task window on the bore monitor
          - [x] check in with the participant.

	           > Hey [NAME], we are about to start our next scan run.
	           > For this scan, [TASK INSTRUCTIONS].
	           > Let us know when you’re ready to begin by pressing any button.

          - [x] Advance through practice trials, keeping an eye on the participant’s performance on the task if applicable.

      - [x] PREP SCAN
      - [x] Physio setup 
          - [x] Click scan drop down menu 
          - [x] Research
          - [x] Phys_flag_record
              - [x] Change cv to 1
      - [x] SCAN

  - [x] 7. Anatomical scans (T1w and T2w)
      - [x] Prescribe by clicking the localizer image once, and adjust the blue box with crosshairs so that the whole brain is covered, with plenty of space in the front and back, top and bottom.  
      - [x] SAVE Rx
      - [x] Put the fixation cross on the bore monitor, check in with the participant:

           > Hey, [NAME], we are about to start our next scan run.
           > For this scan, all you have to do is stay still.
           > Let us know when you’re ready to begin by pressing any button.

      - [x] SCAN 

**DURING SCAN**

- [x] Check in with participant frequently
- [x] Watch for motion if you can see the participant, or use motion monitoring equipment

**AFTER SCAN**

- [x] Solicit more feedback on participant’s comfort for future sessions
- [x] Run MRIQC to evaluate data

