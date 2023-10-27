## Quick guide to the protocol settings and configuration

### Editing a sequence
- [ ] Double click on the sequence name.
- [ ] After editing the sequence, you MUST store the changes if you want them to be kept by clicking on the <span class="consolebutton red">Go</span> button:

    ![launch_sequence.jpg](../assets/images/launch_sequence.jpg)

### Setting sequences for automatic start
- [ ] You can set the worker icon on the left of the sequence by clicking on it if you want to pause before starting that sequence. If the worker is not present, the sequence will launch automatically.

    ![worker_icon.jpg](../assets/images/worker_icon.jpg)

- [ ] Blocks with a name between double underscores `__*__` introduce an *Exam Paused* break.
    Such breaks prompt a modal dialog with the *Exam Paused* title like this:

    ![exam_paused.jpg](../assets/images/exam_paused.jpg)

    !!! warning "The *Patient has Contrast Agent* checkbox MUST always be unchecked, as this protocol does not involve a contrast agent""

- [ ] Click <span class="consolebutton red">Continue</span> when you are ready to proceed.

### Setting the FoV
!!! warning "Using the anatomical image to adjust the field-of-view (FoV) is RECOMMENDED"

    - [ ] Drag and drop the protocol's stack icon (🗇) corresponding to the `anat-T1w__mprage` sequence into the image viewer.
        The icon will appear AFTER the image has been acquired.

- [ ] Make sure that the FOV (yellow square) includes the whole brain by tilting or translating the FOV. If the full brain, including the cerebellum, do not fit in the FOV, favorise making sure that the cortex is fully enclosed in the yellow square. For reproducibility, it is better if the FOV across sequences have a similar center and a similar tilt. However, if it is not possible, the priority remains to include the whole brain in the FOV.
- [ ] If two sequences have the same resolution and the same number of slices, you can copy paste the FOV
    - [ ] Open the sequence for which you want to adjust the FOV/geometry
    - [ ] Right click on the sequence for which the FOV has already been carefully positioned
    - [ ] Select `Copy Parameters`
    - [ ] `Center of slice groups and saturation regions`
- [ ] Once the FOV is well placed, store the new settings of the sequence by pressing <span class="consolebutton red">Go</span>.

    ![adjustFOV.jpg](../assets/images/adjustFOV.jpg)

### Repeat scan
- [ ] If you have to interrupt a sequence because a problem occurred (e.g., the participant fell asleep, the stimuli were not adequately started, etc.), or you have to repeat a sequence because the image was of low quality, right click on the sequence that needs to be restarted and click on *Repeat* to restart the scan **without changing anything in its name!**

    ![repeat_scan.png](../assets/images/repeat_scan.png)


### Managing protocols

- [ ] (Optional) Load an existing protocol
- [ ] Edit the protocol as needed

    !!! important "Follow Reproin conventions"

        When assigning names to the MR sequences in the protocol, make sure to follow the [Reproin conventions](https://dbic-handbook.readthedocs.io/en/latest/mri/reproin.html) to maximally facilitate the conversion into BIDS.

- [ ] Update the *Number of measurements* in all `func-bold_task-*` sequences, according to the [previously recorded timings](intro.md#task-timing):

    $$N_\text{measurements} = L_t / \text{TR}, \quad t \in \{\text{bht}, \text{qct}, \text{rest}\},$$

    where $L_t$ is the length of a particular task $t$ (either BHT, QCT, or resting state) in seconds as timed before, and
    $\text{TR}$ is the **repetition time** of the BOLD sequence, in seconds.

- [ ] Save the protocol

    !!! warning "Logging in as an advanced user is required before saving the protocol"

        As a good practice, always work as the standard user `{{ secrets.login.username_scanner | default("janedoe") }}`.
        However, you MUST change into *advanced user mode* before saving the protocol.

        Simultaneously press the <span class="keypress">Tab</span> + <span class="keypress">Delete</span> + <span class="keypress">:octicons-sign-out-16:</span> on the control-computer's keyboard:

        > Username: `{{ secrets.login.superusername_scanner | default("superjanedoe") }}`
        >
        > Password: `{{ secrets.login.superuserpass_scanner | default("******") }}`

        !!! danger "After three wrong password entries, access will be denied, and only a Siemens engineer will be able to unlock the MR scanner."

    - [ ] Open the Dot-Cockpit window
        ![](../assets/images/save_protocol1.jpg)
    - [ ] In `Browse`, find the right folder to save the protocol in (*RESEARCH* ⤷ *Oscar*).
    - [ ] Right click on the folder and select *New* ⤷ *Program*. This opens an empty page in the program editor
        ![](../assets/images/save_protocol2.jpg)
        ![](../assets/images/save_protocol3.jpg)
    - [ ] Select all the sequences you want to run from the sequence list and click right to copy.
        ![](../assets/images/save_protocol4.jpg)
    - [ ] Drag or paste the copied sequences in the program editor.
        ![](../assets/images/save_protocol5.jpg)
    - [ ] Once finished, click on the floppy disk icon (:fontawesome-solid-floppy-disk:) in the upper left to save.
    - [ ] Give the protocol a relevant name starting with the date of acquisition in the format YYYYMMDD and click <span class="consolebutton">Save</span>.
        ![](../assets/images/save_protocol6.jpg)
    - [ ] If desired, the protocol details can also be downloaded as a pdf on a peripherical USB key.
        - [ ] Right-click on the protocol and select *Print*
        - [ ] Save the PDF in your USB key.
- [ ] Make sure you save a different protocol for each of the four PE directions (i.e., AP, PA, LR, RL).

### Scanner boot-up protocol

!!! warning "Please wait for all systems to finalize their boot-up (about 10 minutes), even if only the satellite station (*{{ secrets.hosts.console_lef | default('██████')}}*) is to be used."

![on-off-button](../assets/images/on-off-box.jpg)

- [ ] Turn the key of the **System ON/OFF Station Box** into the *open lock* position (:fontawesome-solid-unlock:)
- [ ] Push the blue button with the sun symbol :octicons-issue-opened-16: and the **SYSTEM ON** label above, which is found right above the key

## Scanner interface
The picture below shows you the scanner interface as you will see it when you operate the MR machine. The arrow points to the screen and the red circles indicate the control buttons.
![alarm_button](../assets/images/alarm_button.png)


### Scanner's settings buttons

Adjust settings by pressing the respective button and then turning the central knob (1) to adjust the setting to the desired level:

![ventilation_button](../assets/images/ventilation_button.png)

- [ ] Use the headphones :fontawesome-solid-headphones: button (2) to adjust the volume of the earphones.
- [ ] Use the speaker :fontawesome-solid-volume-off: button (3) to adjust the volume of the air speaker in the scanning room.
- [ ] Use the light :fontawesome-solid-lightbulb: button (4) to adjust the intensity of the illumination inside the scanning room.
- [ ] Use the fan :fontawesome-solid-fan: button (5) to adjust the ventilation in the scanning room.

!!! warning "The central knob (button 1) will turn off the alarm if pushed when the alarm is on"

### Standard extraction of the participant

There are two options to extract the participant, when the session has concluded or within the session if the participant needs to be extracted and there is no emergency (e.g., in case of technical error the scanner does not permit continuing the session and it needs to be aborted).

| ![take_table_down](../assets/images/take_table_down.png) | ![quick_return](../assets/images/quick_return.png) |
|:--:|:--:|
| *The participant can be extracted by pressing the extraction button (bottom arrow in the leftmost picture) and then genly rolling the central knob. Alternatively, you can just press the* Home :fontawesome-solid-house: *button (rightmost picture).* {: colspan=2} |

---

## Eye-Tracker Calibration Process

- [ ] On the eye-tracking (ET) computer, ensure that the appropriate calibration type is selected (9-point for QCT and 5-point for resting state and breath-holding tasks):
    - [ ] Click on <span class="keypress">Set Options</span> located on the right side of ET computer screen.
    - [ ] Under **Calibration type** in the top left corner, choose the image containing either 9 or 5 points.

        ![9-points_calibration](../assets/images/9-points_calibration.jpg)

- [ ] Two crosses should appear on the ET computer screen: one at the center of the pupil and the other at the center of the corneal reflection.

    !!! warning "If the two crosses do not appear, the coverage, focus and intensity of the ET are incorrect"

        - [ ] Repeat the steps for their setting up given in [the participant's preparation section](participant-prep.md#final-preparatory-steps-of-the-et)

- [ ] Initiate the ET calibration by pressing <span class="keypress">C</span> on the laptop keyboard or by clicking on <span class="keypress">Calibration</span> on the ET interface.
- [ ] Once the participant's gaze stabilizes on the first fixation point, the <span class="keypress">Accept Fixation</span> button turns green.
    Click on it to confirm the initial position.

    ![accept_fixation](../assets/images/accept_fixation.jpg)

- [ ] Subsequent positions should be automatically validated when the gaze remains stable.
    If not, manually click the <span class="keypress">Accept Fixation</span> button when it turns green.
- [ ] After the calibration, ensure that the fixation points' positions match the expected pattern corresponding to the 9- or 5-point calibration.
    If the pattern appears too distorted, restart the calibration.
- [ ] Upon successful calibration, initiate validation by clicking <span class="keypress">Validation</span> on the ET interface or pressing the <span class="keypress">V</span> key on the laptop keyboard. Follow the same instructions as in the calibration to validate positions.
- [ ] If validation fails, repeat previous steps and restart calibration. Otherwise, you can leave the calibration mode and proceed with the task program by pressing the <span class="keypress">Esc</span> key on the laptop (*{{ secrets.hosts.psychopy | default("███") }}*).
