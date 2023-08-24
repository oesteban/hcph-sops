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

## Eye-Tracker Calibration Process

- [ ] Brief the participant about the calibration process. Refer to the [scanning protocol](scanning.md) for provided scripts.
- [ ] Start the experiment by pressing the green play button.
- [ ] On the eye-tracking (ET) computer, ensure that the appropriate calibration type is selected:
    - [ ] Click on `Set Options` located on the right side of the screen.
    - [ ] Under `Calibration type` in the top left corner, choose the image containing either 9 or 5 points.
      
![9-points_calibration](../assets/images/9-points_calibration.jpg)
      
- [ ] Two crosses should appear on the ET computer screen: one at the center of the pupil and the other at the center of the corneal reflection. If they're not visible, proceed sequentially with the following steps:
    - [ ] Adjust the focus of the ET camera and the pupil detection threshold. If the cross remains invisible,
    - [ ] Realign the mirror frame position by sliding it along the rails attached to the coil. If the cross still isn't visible,
    - [ ] Re-adjust the participant's head positioning inside the coil. If the cross is still not visible,
    - [ ] Make slight adjustments to the mirror's vertical position (be cautious as mentioned earlier). Even a small adjustment can impact calibration and eye positioning. If the cross remains invisible,
    - [ ] Repeat the previous steps as needed.
- [ ] Initiate the ET calibration by pressing <span class="keypress">C</span> on the laptop keyboard or by clicking on "Calibration" on the ET interface.
- [ ] Once the participant's gaze stabilizes on the first fixation point, the `Accept fixation` button turns green. Click it to confirm the initial position.

    ![accept_fixation](../assets/images/accept_fixation.jpg) 

- [ ] Subsequent positions should be automatically validated when the gaze remains stable. If not, manually click the validation button when it turns green.
- [ ] After the calibration, ensure that the fixation points' positions match the expected pattern for either the 9 or 5 points calibration. If the pattern appears too distorted, restart the calibration.
- [ ] Upon successful calibration, initiate validation by clicking "Validation" on the ET interface or pressing the 'V' key on the laptop keyboard. Follow the same instructions as in the calibration to validate positions.
- [ ] If validation fails, repeat previous steps and restart calibration. Otherwise, you can leave the calibration mode and proceed with the task program by pressing the <span class="keypress">Esc</span> key on the laptop (*{{ secrets.hosts.psychopy | default("███") }}*).
