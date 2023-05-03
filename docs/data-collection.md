### Scheduling

#### Once, at the beginning of the project
- [ ] [Fork the HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks/fork) under your user on GitHub.
- [ ] Prepare a laptop with a running Psychopy 3 installation AND the EyeTracker software. For these SOPs, the designated laptop for the experiments is *HOS68752*.
- [ ] Clone the [HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks):
    ```
    git clone git@github.com:<your-gh-username>/HCPh-fMRI-tasks.git
    ```
- [ ] Set-up the original repository as upstream remote:
    ```
    git remote add upstream git@github.com:theaxonlab/HCPh-fMRI-tasks.git
    ```
- [ ] Once the protocol is decided upon, and after any updates, make sure of storing the protocol:
    - [ ] Save the protocol by selecting all the sequences in the sequence list, click right to copy.
    - [ ] Open the Dot-Cockpit, paste the sequences and save.
    - [ ] Repeat the operation after creating the four variants of the protocol, one per PE direction.

**Install the BIOPAC**

- [ ] Set up the line frequency switches on the back of the BIOPAC amplifier depending on your country frequency to reduce noise. Both switches should be DOWN if your country's line frequency is 50Hz. Both switches should be UP if your country's line frequency line is 60Hz.
    ![biopack-frequency-switch](./assets/images/biopack-frequency-switch.jpg "BIOPAC frequency switch")
- [ ] Plug the different units of the BIOPAC together if it has not been done yet. We use the BIOPAC to synchronize and output in a single file all the physiological signals we record: cardiac pulsation, respiration and CO2 concentration.
- [ ] Install the BIOPAC recording software.
- [ ] Get familiar with the BIOPAC system:
    ![biopack-front](./assets/images/biopack-front.jpg "BIOPAC front side")
    - [ ] The AMI100C unit can receive up to 16 analog signals. 
    - [ ] The DA100C unit records the signal coming from the respiration belt. Plug the TSD160A unit on the DA100C.
    - [ ] The ECG100C MRI unit records the electrical signal coming from the heart via the ECG. Plug the MECMRI-2 unit on the ECG100C unit.
    - [ ] The SPT100 (solid state relay driver unit) is used to record triggers. A trigger appears as a vertical red line on your physiological recordings [INCLUDE IMAGE]. Plug the trigger to the TRIG entrance.
- [ ] Install the gas analyzer (GA) on the wooden platform behind the MRI consoles.

#### Every two months - calibrate the GA

- [ ] Get a gas bottle with a known CO<sub>2</sub> concentration between 5% and 10%.
- [ ] Connect the GA to the BIOPAC as described below and start recording signal.
- [ ] Edit the configuration of the inputs, making sure you update the voltage range for input 3 (the GA), estimated as described in [the GA's manual](./assets/files/GA_manual.pdf)

#### One week BEFORE THE FIRST SESSION

- [ ] Send a copy of the MRI Safety and screening form ([EN](./assets/files/safety_form_EN.pdf)|[FR](./assets/files/safety_form_FR.pdf)) to the participant over email and confirm reception.
- [ ] Confirm that the participant has read and understood the document, and in particular, double-check that they do not have any MRI contraindications.
- [ ] Remind the participant that any jewelry should be removed prior to the scan.
- [ ] Indicate that they MUST shave the upper area of their chest where the ECG electrodes will be placed, if there is hair. The ECG electrodes MUST directly contact the skin.
- [ ] Confirm clothing:
    - [ ] if allowed to wear street clothes, remind the participant to avoid clothing with metal or that would uncomfortable to lie in for the duration of the scan; otherwise
    - [ ] remark the participant they will be given a gown and they will need to change before every session.
- [ ] If participant has indicated nervousness or history of claustrophobia, use the mock scanner.

#### BEFORE DAY OF SCAN

- [ ] Make sure you have internet access, and update the [HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks) on *HOS68752*:
    ```
    git fetch upstream
    git checkout main
    git rebase upstream/main
    ```
- [ ] On the *HOS68752* laptop, open a terminal and execute `conda deactivate`.
- [ ] Open psychopy 3 by typing `psychopy`
- [ ] Load in the different experiments and check for proper functioning:
    - [ ] Resting-state fMRI (RSfMRI): open the file `resting_state.psyexp` and check that the movie is played.
    - [ ] Breath-holding task (BHT): open the file `breath_holding_task.psyexp` and check it properly runs, while timing it (total length should be 5 min 24 s).
    - [ ] Positive-control task (PCT): open the file `control_task.psyexp` and check it properly runs, while timing it (total length should be 2 min XX s)

#### DAY OF SCAN, prior to participant arrival
- [ ] If the scanner is shut down, boot it up.
- [ ] Remove the head coil that is currently installed.
    - [ ] If it is the 64-channel, you can just temporarily move it into the scanner's bore.
    - [ ] Otherwise, store it on the shelf where the other coils are and bring the 64-channel one in the proximity of the bed (e.g., inside the scanner's bore). Make sure to remove other coil's fitting element.
- [ ] Remove the spine coil by lifting the corresponding latch, then sliding it toward the head of the bed, lift it from the bed, and place it on the floor ensuring it is not obstructing any passage or unstable.
- [ ] Place the two back padding elements filling the spine coil socket.
- [ ] Fix the 64-channel head-and-neck coil onto the head end of the bed and connect the coil's terminal cable. Check that the head-and-neck coils are now detected by the scanner, as indicated in the scanner's monitor screen.

**Setting up the BIOPAC system and physiological recording sensors**

- [ ] Ensure you have the USB key with the BIOPAC software license.
    - [ ] Plug the USB key to the computer [WHICH COMPUTER]. It needs to stay plug at all times during the acquisition. [INSERT PHOTO]
- [ ] Plug the power cord of the BIOPAC and of the GA into suitable power sockets.
- [ ] Plug in the Ethernet (the plug is in the back) to the Ethernet port of [WHICH COMPUTER].
    ![biopack-back](./assets/images/biopack-back.jpg "BIOPAC back side")
- [ ] Go inside the scanning room, unscrew the wood cap that covers the hole in front of the MR.
- [ ] Delicately pass a long tube that will be connected to the nasal cannula through the front access tube. Connect the tube and the cannula and leave it ready on the bed ready for the participant.
- [ ] Pass the respiration-belt (RB) tube through the same hole. Again, connect the end inside of the scanning room to the respiration belt and leave it on the bed.
- [ ] Connect the end of the control room to the TSD160A BIOPAC unit, using the the plug marked negative (**-** symbol).
- [ ] Connect the coaxial end of the cable to the CO<sub>2</sub> output in the back of the GA, the other end of the cable should be a jack plug (similar to headphones).
- [ ] Connect the other end (jack plug) into the input end of the INISO/A filter.
- [ ] Connect one end (RJ-45/Ethernet to RJ-45/Ethernet) into **channel 3** of the AMI100D BIOPAC module, and the other end to the output of the INISO/A filter.
- [ ] Check that the exhaust pipe (back of the GA) is free of obstruction.
- [ ] The **pump switch MUST BE OFF** (front of the GA).
- [ ] Turn the GA on using the on/off switch located at the back of the GA.
    ![gaz-analyser-back](./assets/images/gaz-analyser-back.jpg "Gas Analyzer back")
- [ ] Remove the cap of the gas input and connect the end of the tubing to the cannula with a no-return filter set.
    ![gaz-analyser-front](./assets/images/gaz-analyser-front.jpg "Gas Analyzer front")
- [ ] Connect the end of the control room to the corresponding designated gas intake plug in front of the GA.
    ![gaz-analyser](./assets/images/gaz-analyser.jpg "Gas Analyzer")

**Setting up the eye-tracker**

!!! info "Thanks"
    All the documentation about the eye-tracker is derived from Benedetta Franceschiello's user guide.

- [ ] The eye-tracker (ET) computer is kept on its designated rolling table, which is stored under the projector in room BH07/075. Behind the rolling table, there is a transparent panel (the *plexiglas* in the following) where the ET camera will stand inside the scanner bore.
- [ ] Verify that the monitor and the cable, as well as the ET over the PC tower are fixed to the rolling table with scotch tape.
- [ ] Bring the table with the ET computer to the control room, and place it next to the access closet. Be very attentive during the displacement and lift the front wheels when passing steps or cables. The plexiglas panel can also be brought to the scanning room simultaneously, if done with care.
- [ ] From room BH07/071 (first cabinet on the left), take the box labeled *fMRI usage*, containing the ET camera, lenses, and the special infrared mirror. 
- [ ] Take the MR-compatible lens out of the lenses box. It is easy to recognize it as it is the only one with two golden screws.
    ![cover-mri-compatible-lens](./assets/images/cover-mri-compatible-lens.png "Cover MRI compatible lens")
    ![mri-compatible-lens](./assets/images/mri-compatible-lens.png "MRI compatible lens")
- [ ] For the ET, you should remove the ventilation and the light inside the scanner bore [TO DO : INSERT PICTURE]
- [ ] Install the MR-compatible lens, after removing any other present lens. If other lens is present, put it back to its plastic bag inside the lenses box after unscrewing and removal. To avoid accidentally dropping a lens, one hand MUST be under the lens at all times while screwing/unscrewing it. **The lens MUST BE INSTALLED before bringing the ET inside the Scanner Room**.

    ![screw-mri-compatible-lens](./assets/images/screw-lens.png "Screw the MRI compatible lens")

**INSIDE the scanner room**

- [ ] Place the plexiglas standing panel inside the scanner bore, following the indications stuck on the panel (a sign notes the top side that faces up, and to tape markers designate the position of the ET). **DON'T PUSH IT inside**, it MUST be adjusted once the participant is placed inside the scanner to ensure the repeatible positioning of the ET.
- [ ] Bring the ET inside the scanner room, and put it on top of the plexiglas panel. The two posterior feet of the ET stand have to be within the two corner signs made of scotch tape. **HOLD THE ET STAND STRONGLY, BECAUSE THE MAGNETIC FIELD GENERATES RESISTANCES.**
- [ ] Open the door of the cable section between the recording room and the scanner room.
- [ ] First, pass the optic fiber (orange wire) and the power cable (the one with a fabric sheet) through the access point (TODO: ATTACH PICTURE). This operation requires two people, one handling the cables from outside the scanner, and the other gently pulling them from inside. Both people will lift the cable to avoid its abrasion with the edges of the metallic cylinder, which is the passage between exterior and interior of the scanner room. Once the sliding of the cable is finished, leave the extremities inside the scanner room in the left-top corner, far from the scanner. These parts are magnetic.
- [ ] Connect the cables (two plugs for the black, one plug for the orange).
- [ ] Take the half-circle one-direction screen from the table behind the scanner and put it on the back of the scanner, behind the ET system (don't push the plexiglas yet)
- [ ] Place the infrared mirror:
    - [ ] Detach the mirror frame from the head coil, if it is placed there. Remove unnecessary items from the scanning bed, and prepare the mirror to attach the infrared mirror of the ET at a later step.
    - [ ] Prepare two long strips of scotch tape and leave them in a convenient place to attach the ET mirror later. E.g., attach the corner of each strip to the back part of the mirror frame.
    - [ ] Go back to the control room and take the infrared mirror out of the «fMRI usage» box. **<span style="color:red">DO NOT EXTRACT THE MIRROR OUT FROM ITS BOX YET</span>**. The mirror's box is labeled as [*RELIQUIA DI SAN GENNARO*](https://it.wikipedia.org/wiki/San_Gennaro#La_reliquia) to emphasize that **THIS IS THE MOST DELICATE PART, BECAUSE THE MIRROR CANNOT BE REPLACED <span style="color:red">NOR CLEANED</span>**. This mirror is **EXTREMELY EXPENSIVE**. 
        ![infrared-mirror](./assets/images/infrared-mirror.png)
    - [ ] Get two gloves (e.g., from the box hanging at the entrance of the scanner room), then approach the scanner bed. Put the gloves on, and **DON'T TOUCH ANYTHING**. You MUST have the standard mirror dismounted and in front of you at this point. **WITH THE GLOVES** proceed to extract the infra-red mirror from its box, being extremely careful. **YOU CAN ONLY TOUCH THE MIRROR WITH GLOVES**, because it cannot be cleaned up. Watch out for **FINGERPRINTS** and once taken out of its box, **IMMEDIATELY PROCEED TO ATTACH IT** to the standard coil mirror. The mirror MUST NOT be placed anywhere else if not in its box.
    - [ ] **WITH YOUR GLOVES ON**, attach the ET mirror to the standard coil mirror (the larger mirror that points toward projector's screen at the back of the scanning room) using the scotch tape strips you prepared before. Put it more or less in the center, although <span style="color:red">this position may need to be adjusted</span> (being careful and with the same precautions explained before). **Do not touch the surface of the ET mirror.**
    - [ ] Place the mirror frame back on the head coil. As always, **DO NOT TOUCH THE MIRROR**. 

**Back OUTSIDE THE SCANNER ROOM (control room)**

- [ ] Connect the Power cable to the metallic extremity belonging to the PC-tower
    ![connect-power-cable](./assets/images/connect-power-cable.png "Connect power cable")
- [ ] Plug in the Power strip containing the ET Power Cable, the PC-tower power, etc
    ![powerstrip](./assets/images/powerstrip.png)
    ![plug-powerstrip](./assets/images/plug-powerstrip.png)

- [ ] Switch on the PC-tower, as well as the laptop. Select "Eyelink" when given the option of which operating system to launch.
    ![pctower](./assets/images/pctower.png)
- [ ] This is the sync box of the scanner, allowing a synchronization of the triggers between the scanner sequence and the ET recordings.
    ![syncbox](./assets/images/syncbox.png)
- [ ] Connect to the ET to the laptop with the ethernet cable (blue color).
- [ ] Connect the USB sync box to the laptop with the USB cable. It is normally plugged into the sync box, it must be re-plugged in after usage.
    ![connect-ethernet-to-laptop](./assets/images/connect-ethernet-to-laptop.png)
    ![ubs-syncbox](./assets/images/ubs-syncbox.png)
- [ ] Connect the **hos68752** laptop to the screen switch box (see picture below) with the corresponding HDMI cable. This should project your screen on the second screen.
    ![switchbox_hdmi](./assets/images/switchbox_hdmi.png)
- [ ] Configure the display settings of the laptop to mirror outputs and set a resolution of 800x600 for both screens.
- [ ] Double check that the IP address corresponding to the ethernet interface of the *HOS68752* laptop is correct. You can either run `ifconfig -a` or use the GUI. Make sure the IP/mask is **100.1.1.2/24**, and the protocol is IP version 4. Execute `ping 100.1.1.1` to see if the ET is responding to echoes.
- [ ] Check that you can send trigger events manually:
    - [ ] Enter the "Synchronization" menu by selecting it and pushing the enter button (&#x25CF;).
    - [ ] Hit the down arrow button (&#x25BC;) until you find "Send trigger"
    - [ ] Push the enter button (&#x25CF;) every time you want to send an `s` character.
    - [ ] Check that the *HOS68752* laptop types those triggers (e.g., on an open editor receiving keypresses, or the shell prompt).
    - [ ] Check that the BIOPAC is properly registering the trigger too. Every trigger sent should be seen in the *AcqKnowledge* GUI.
- [ ] Start the syncbox session:
    - [ ] Push the up arrow button (&#x25B2;) until you find "Start session"
    - [ ] Push the enter button (&#x25CF;) and the syncbox will be now waiting for the scanner's trigger signal to forward it.
    
    | ![choose-synchronisation-syncbox](./assets/images/choose-synchronisation-syncbox.png) | 
    |:--:|
    | ![start-session-syncbox](./assets/images/start-session-syncbox.png) |
    | ![run-session-syncbox](./assets/images/run-session-syncbox.png) |
    
- [ ] Switch the projector on by hitting the power button on on its right side. The projector is found in room BH07/075. Adjust the projector tilt and centering if the projection does not properly aim the panel inside the scanner's bore. E.g., change the height of the paper pile that supports it (see images, FENS papers).

    | ![projector](./assets/images/projector.png) | ![paper-projector](./assets/images/paper-projector.png) | ![adjust-projector](./assets/images/adjust-projector.png) |
    |:--:|:--:|:--:|
    | *The hole is the part through which we should check the quality of the projection* {: colspan=3} | | |

- [ ] Go back to the *HOS68752* laptop, open a terminal and execute `conda deactivate`.
- [ ] Open psychopy 3 by typing `psychopy`
- [ ] Open the PCT experiment in *Psychopy* (`control_task.psyexp` file) and leave the streaming mode on (*camera setup mode*) so that the adjustment of the ET can be quickly done later as the infrared camera is providing feedback inside the scanning room through the projector.
    - [ ] Verify that the calibration chosen is in the options [VERIFY EXACT BUTTON NAME] the 6-points one 
    - [ ] Run the experiment by pressing the green play button. 
    - [ ] Enter the session and participant number in the pop up window. The Eyelink system setup page opens.
    - [ ] Press enter to begin the *camera setup mode*.
    - [ ] The camera setup mode contains a view of one eye, and you can switch that view between two modes: one is the field-of-view of the ET, the second is an automatic zoom on the eye itself (or a random part if the eye is not visible).
    - [ ] To ease the setup of the ET, switch to the full view in the camera setup mode by pressing the left or right arrow.

**Set-up of documents and equipment**

- [ ] Prepare consent documents (first session only)
- [ ] Prepare an MRI safety screener 
- [ ] Prepare scrubs and MR-compatible glasses if applicable
- [ ] Setup scanner room and peripherals:
    - [ ] prepare the 64-channel headcoil,
    - [ ] prepare padding: under-knee padding, neck padding, inflatable head-padding
    - [ ] prepare a blanket
    - [ ] prepare a new pair of earplugs
    - [ ] check the RB is prepared
    - [ ] connect the three cables corresponding to the ECG leads to the filter in the access cupboard
    - [ ] connect the cable from the RJ-45 output of the syncbox to the first filter (VNC connector; has a label "External signal") in the cupboard covering the access panel to the Faraday cage. The cable might be stored in the lower left cupboard of office 071. Make sure you will have access to the cable with sufficient time ahead.
        - [ ] On the scanner console, check the external signal input registers triggers from the syncbox
        - [ ] prepare a thermometer
        - [ ] prepare a blood pressure meter
    - [ ] Prepare the GA:
        - [ ] Prepare the cannula tube, which is introduced through the tube in the access panel
        - [ ] Prepare a new cannula


#### DAY OF SCAN, right after the participant arrives

- [ ] Have participant fill out consent documents and MRI safety screener, and verbally confirm responses, paying attention to frequently forgotten devices and implants, like orthodontia
- [ ] Have participant empty their pockets or change into scrubs, and remove all jewelry/hair accessories and check for any missed metallic objects with the scan center's preferred method
- [ ] Instruct participant on staying still and encourage them to request breaks if necessary
- [ ] Describe the participant how the session will develop, with special attention to tasks. Answer all the questions that may arise.
- [ ] Tell the participant they will be holding an alarm button to the participant throughout the session, and that they may use it any time whenever they need to stop the experiment.
    - [ ] Tell the participant that they MUST leave the alarm button, e.g., on their belly, during the positive control task. Indicate that you will remind them of this before starting the task.
- [ ] Indicate the participant where the door to the changing room is, and ask them to change clothes if necessary.
- [ ] Ask the participant to place the ECG electrodes on the location indicated by the picture below.
    - [ ] Clean the skin with [WHAT?]
    - [ ] Remove the protective film from the electrode
    - [ ] Stick the electrode on your skin by starting in one side and ironing the rest of the electrode. This procedure ensures that no air is trapped between the electrode and your skin and that no wrinkles from at the edges. Repeat for the three electrodes
        ![prep-ecg-electrodes](./assets/images/prep-ecg-electrodes.png)

**Preparing the scanning protocol**

- [ ] Close open patients discarding changes.
- [ ] Search the participant by clicking on the "Patient Browser" in the top left corner
    - [ ] Search for "Oscar esteban"
- [ ] Check the head coil **is not** plugged before initiating a "New examination" to ensure good SNR of the localizer sequence.
- [ ] Right click and select "New examination"
    - [ ] Enter the weight and height of the participant
    - [ ] Select the right protocol under "Oscar" 
    - [ ] Select Brain as the organ
    - [ ] Select the Position as "Head supine"
    - [ ] Click the "Exam" button (red background, rightmost-bottom)
- [ ] Load the adequate protocol, making sure of loading the right phase-encoding (PE) direction corresponding to the session.
    - [ ] Double-check that all PE prescriptions are correct.
- [ ] Open the parameters of the sequence named "fmap-phasediff__gre" and ensure that under Contrast>resc. the option "Magnitude et phase" is selected. This is crucial so that both the magnitude and the phase difference field map images are saved.


#### DAY OF SCAN, participant setup

- [ ] Bring the participant inside the room, and give them the ear-plugs to protect the hearing during acquisition.
- [ ] Connect the ECG leads on the three electrodes. The electrodes MUST be connected following the color scheme [ADD DETAILS]
- [ ] Install the respiration belt below the participant's chest and connect it to the tube [INSERT PHOTO]. The respiration belt measure the displacement of the stomach induced by breathing, it thus needs to surround the stomach comfortably. [GIVE MORE PRECISE INFO WHERE SHOULD IT BE PLACED]
- [ ] Place the nasal cannula in the nose of the participant making sure the two protrusion are aligned with the nostrils of the participant. Place the tube behind the ears and tighten behind the head for comfort and stability by sliding the ring.
- [ ] Give to the participant the emergency button. Make the participant try it, so they can see it works. To switch off the alarm, there's a button on the scanner (circular, both on the left and on the right of the hole) 
- [ ] Adjust the participant inside. With the paddings, their head position MUST be adjusted and elevated so that the nose and the forehead of the participant are both close to the upper coil. This procedure ensures the ET has the clearest possible view of eye.
- [ ] This part must be repeated taking out and putting back the upper part of the head-coil, adjusting the pillow at every step, until the head is fixed and the nose and forehead of the participant almost touch the coil. In case of need, ask the participant to "say yes" with the head (chin on neck) and keep this position, place the pillows, place the coil and check that the participants' front touches the coil. Now the nose can also be a bit far from the coil. Tell the participant to relax the neck, so the nose should go a bit up and touch the coil.  
    ![two_pillows](./assets/images/two_pillows.png)
    ![superpose_pillows](./assets/images/superpose_pillows.png)
- [ ] Take the Ears -protection pillow, stick it on top of the ears of the participant, one by one. Once they are settled, you can pump it, until the participant is comfortable, the head is fixed and the ears are protected.
- [ ] Ask the participant if they are feeling cold. Cover them with a blanket if necessary.
- [ ] Solicit feedback on participant's comfort while positioning them on the scanner bed and suggest ergonomic positioning of arms to avoid discomfort. Remind the participant not to create closed loops by crossing their legs or holding their hands together.
- [ ] Gently move the participant with the manual regulation. Stop when the head is under the head-localizer. Ask the participant to close their eyes, press the laser alignment button and align the head-coil markers with the red light.
- [ ] Switch off the alignment light, now the participant can open their eyes. You can move the participant (always gently as before) inside the scanner, until the mm counter marks "Isometric".
- [ ] Go behind the scanner, push the plexiglas panel until it touches the bed.
- [ ] You should see the projection of the calibration mode as you left it open before.
- [ ] Regulate the ET position until you see from the projector screen the eye. In case of need, you can adjust the strength of the infrared light (emitter). This is the black box on the other side with respect to the lens. Under the emitter there are two little screws. Unscrew, move the emitter front/back, check the contrast of the face image, re-screw. Once the eye is well seen, the image is zoomed (externally by the operator in front of the PC-tower) to the pupil. The right lens MUST be manipulated rotating the roller, like what you would do with your reflex to obtain the focus. If the position of the ET is not satisfying, you can move the base.
    ![base-eye-tracker](./assets/images/base-eye-tracker.png)
- [ ] If the pupil is correctly seen, as well as the eye, you can go out.
    - [ ] Inform the participant that you are leaving the room, and that you are going to first check with them whether the speaker works well, immediately
- [ ] Make sure the speaker is audible (and not annoying) and confirm the participant's feedback:
    > Hey [NAME], we are about to start our first scan run.
    > For this scan, all you have to do is stay still, and look at the screen.
    > Let us know when you're ready to begin by pressing any button.
- [ ] Switch the ET camera back to zoomed mode, and exit the camera mode.
- [ ] Inform the participant about the calibration process.
    - [ ] Ask the participant to follow a fixation point with their gaze, without moving their head.
    - [ ] Tell the participant to move the eyes ONLY after the point moves (do not anticipate).
    - [ ] When the gaze is stable and the validate button [VERIFY THE EXACT NAME] appears green, you can manually click on it to validate the first position.
    - [ ] The following positions should be validated automatically when the gase is stable enough. If it is not the case, manually click on the validate button when it turns green
- [ ] The ET software MUST show a cross during the calibration. If it does not, try sequentially the following:
    - [ ] readjust the focus of the ET; and if it still doesn't show the cross,
    - [ ] readjust the mirror frame position sliding it throught the rails attached to the coil; and if it still doesn't show the cross,
    - [ ] readjust the participant's head positioning inside the coil; and if it still doesn't show the cross,
    - [ ] move the mirror up or down (being careful as mentioned before). Just a few mm can ruin the calibration and the eye-position; and if it still doesn't show the cross,
    - [ ] iterate over the previous steps.
- [ ] When the calibration is successful, launch the validation by clicking on validation on the ET interface or clicking V on the keyboard of the laptop. Follow the same instructions as in the calibration to validate the positions.
- [ ] <span style="color:red"> Turn the pump of the GA on </span> and make sure the flow control is set on maximum.

#### SCAN TIME

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

#### DURING SCAN

- [ ] Check in with participant frequently
- [ ] Watch for motion if you can see the participant, or use motion monitoring equipment

#### END OF RECORDING

- [ ] Everything that is removed for the experiment MUST be put back in place and the end of the experiment, i.e. position of the bed, coil, emergency button, ears cover.
- [ ] Before doing anything else, put the plastic base far from the bed, again. Do not remove the projector screen yet, otherwise the participant would be flashed by the lights.
- [ ] Take out the participant gently as before. 
- [ ] Remove the upper part of the coil
- [ ] Remove the ear-pillow.
- [ ] Let him go. 
- [ ] Switch off the projector.

#### AFTER SCAN, inside scanner room

- [ ] Take the upper part of the coil. Take the plastic container of the infrared mirror. Take the gloves. Put them on.
- [ ] Remove the scotch. Put the mirror back in its custody. Then back in its plastic bag.
- [ ] Place it back in the fMRI external box, with extreme care.
- [ ] Clean the coil mirror from the scotch. Clean the coil.
- [ ] Remove it and put it back in place.
- [ ] Put the pillows back in place.
- [ ] Put the projector screen back in place.
- [ ] Unplug the Eye tracker from the Optic Fiber and the Power. Put those extremities aside far from the scanner. Take the Eye-Tracker back outside. Put it in a stable place.
- [ ] Remove the plastic base, put that outside next to the box.
- [ ] With someone from the other side, pass being extremely careful the cables (fiber and power of the ET) back thought the hole. Roll them around their support being extremely careful. 
- [ ] Put the bed back in place = push the "home" button on the scanner
- [ ] Take a glove, on the right there is some cleaning napkins. Use them to clean the bed. 
- [ ] exit and Close the External door.

#### AFTER SCAN, outside scanner room

- [ ] Solicit more feedback on participant's comfort for future sessions
- [ ] Switch off laptop and ET PC Tower. Plug back the sync box and the VGA projector where they were. 
- [ ] Fix the rolled cable with the scotch on the PC Tower base.
- [ ] Take the ET, Remove (always with and hand under the lens) the MRI compatible LENS. Put it back to its contained inside the box. 
- [ ] Put back the regular Lens. 
- [ ] Bring back the box and the base at CIBM EEG lab. Put the keys back under old Nora's desk.
- [ ] Fix the ET with the scotch at the chariot.
- [ ] Bring back the chariot and the TMS laptop at the TMS lab
- [ ] If you are the last person to scan for the day, turn off the MRI machine. First, turn off the left computer, then the right one and finally push the button shut down on the MRI console that lies on the wall and turn the key to close the cover of the console. ! The order is important and the next element needs to be shut down only when the previous is completely off!


