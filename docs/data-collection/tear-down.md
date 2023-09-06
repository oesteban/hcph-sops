
## Showing the participant out

- [ ] Enter the scanner room, and announce yourself to the participant:

    !!! quote "Hi [NAME], thanks a lot for your collaboration. We will get you out in a second."

- [ ] Extract the participant [following the standard procedure](scanning-notes.md#standard-extraction-of-the-participant).
- [ ] Unplug the head coil from the bed connector, lift the lever that releases the upper part of the coil and put it aside (e.g., inside the bore or on a chair next to the scanner).
- [ ] Remove the tape band across the coil and touching the participants forehead.
- [ ] Lift the nasal cannula and put it away so the participant does not get tangled.
- [ ] Assist the participant to remove the padding elements around their head.
- [ ] Help the participant sit down.
- [ ] Instruct the participant to remove the earplugs and dispose of them.
- [ ] Ask them about the experience:

    ???+ quote "Get feedback about the session from the participant"
        [NAME], how was your experience?
        Have you been able to feel comfortable throughout the session?
        What advice, indication do you feel we could've provided you for a better experience?

- [ ] Disconnect the tube from the RB and then lift the velcro attachment to remove the RB.
- [ ] Prepare the belt on the bed to be removed from the room when you show the participant out.
- [ ] Help the participant carefully remove the ECG leads.
- [ ] Disconnect the three ECG terminals from the cable and put them in their pouch.
- [ ] Disconnect the last section of the cannula and dispose of it in the trash can.
- [ ] Help the participant step down and accompany them out to the control room.
- [ ] Help the participant recover their personal belongings and change clothes if necessary.
- [ ] Solicit more feedback on participant's comfort for future sessions.
- [ ] Solicit tickets and receipts for transportation.
- [ ] Give the participant the corresponding compensation for the participation and transportation.
- [ ] Ask the participant to sign the receipt of the amount of the financial compensation.


## Clearing up the Scanning Room

### ET arm, ET cables, infrared mirror and stimuli screen

- [ ] Unplug the two cables (signal and power) connected to the ET arm.
    Put their extremities aside far from the scanner.
- [ ] Agree with another experimenter, who will exit the room, sit on the other side of the access tubes in the Control Room, and pull cables (fiber and power of the ET) and tubes (RB and GA) out of the room.
    At the same time, you carefully feed them so they do not suffer abrasion from touching the edges of the tube.

    !!! warning "Extracting the cables and tubes requires two experimenters"

- [ ] The experimenter currently outside in the Control Room will re-enter the Scanner Room with the plastic bag of the mirror and a fresh pair of gloves and will leave them prepared on the bed.
- [ ] Remove the mirror frame from its rails mounted on the head coil and lay it on the bed.
- [ ] Put the gloves on and detach the infrared mirror from the standard mirror.

    !!! danger "The infrared mirror MUST be manipulated with clean gloves at all times."

- [ ] Immediately insert the infrared mirror back into its plastic pouch.
- [ ] Take the pouch containing the infrared mirror outside to the Control Room and place it back in its designated box, with extreme care.
- [ ] Clean the standard mirror removing all residues of glue from the scotch tape.
- [ ] Re-attach the mirror to the coil's frame.
- [ ] Take the projector's screen off and store it in its designated shelf.
- [ ] Disconnect the ECG cable from the filter of the access panel, roll the cable.

### Readying the scanner for the next session

!!! warning "Every setting altered for the experiment MUST be put back to its original status at the end of the experiment (e.g., position of the bed, coil, emergency button, padding elements, etc.)"

- [ ] Put the used bed-sheet and the blanket inside the soiled linen bag.

    !!! important "Put them away in the trash if they are disposable"

- [ ] Dispose all single-use sanitary protections.
- [ ] Put the pillows back in their designated storage places.
- [ ] Remove the head coil and put it in the scanner's bore.
- [ ] Remove the back padding elements and put them back in their designated storage.
- [ ] Reinstall the spine coil.
- [ ] Wipe the bed and the head coil (bottom and upper parts).

    !!! info "Cleaning wipes are available on shelf in the Scanning Room."

- [ ] Lock the head coil back with its bottom part without plugging the connectors.
- [ ] Put the head coil away with the other head-coils on the shelf next to the scanner.

    !!! important "If the next user is already there or you know the current coil will be also used in the next session, plug it back into the bed socket."

- [ ] Return the bed to its *Home* position by pressing the :fontawesome-solid-house: button ([more info](scanning-notes.md#standard-extraction-of-the-participant)).
- [ ] Take the ET arm outside to the Control Room and place it in a stable place.
- [ ] Take the ECG electrodes, ECG cable, the RB, and the plexiglass panel outside to the control room.
- [ ] Exit and close the external door.

## Clearing up the Control Room

### Finalize the *boxing* of the ET elements
- [ ] Put the lens cover.
- [ ] Unscrew the ET lens, while **ALWAYS** keeping one hand under the lens while screwing/unscrewing it and put it back into its pouch.
    ![cover-mri-compatible-lens](../assets/images/cover-mri-compatible-lens.png "Cover MRI compatible lens")
- [ ] Store the ET arm in its designated box.

    !!! danger "REMEMBER | the infrared mirror is inside that box already: DO NOT crush the mirror."

### Finalize the *boxing* of other physiological recording instruments

- [ ] Store the ECG cable and the pouch with the ECG leads in its designated box / storage.
- [ ] Carefully roll the fiber and power cable of the ET, and place them in the rolling table of the ET PC.
- [ ] Carefully roll the GA tube and put it in its designated bag.
- [ ] Carefully roll the RB tube and put it in its designated bag.
- [ ] Disconnect the MMBT-S Interface, and the two corresponding cables (pink USB, 25-pin parallel), and insert them in their designated bags.
- [ ] Remove the cable connecting the GA to the AMI100D module of the BIOPAC, roll it and put it in its designated bag.
- [ ] Put the GA and the corresponding cables in the designated box.
- [ ] Disconnect and bag the remaining cables connected to the BIOPAC:
    - [ ] Ethernet to the *{{ secrets.hosts.acqknowledge | default("███") }}* computer.
    - [ ] Power cord.
- [ ] Retrieve and bag the *AcqKnowledge USB License Key* from the *{{ secrets.hosts.acqknowledge | default("███") }}* computer.
- [ ] Store the *fMRI box*, BIOPAC and GA boxes back in room {{ secrets.rooms.et_camera| default("███") }}.

### Finalizing with the ET's PC

- [ ] Exit the EyeLink 1000 Plus Host PC application by pressing <span class="keypress">Ctrl</span>+<span class="keypress">Alt</span>+<span class="keypress">Q</span> on the ET PC and next click on the <span class="keypress">Shutdown</span> button from the **File Manager** toolbar.
- [ ] Secure the rolled cable with the scotch tape on the ET PC Tower.
- [ ] Take the ET PC Tower and the plexiglass back into room {{ secrets.rooms.projector | default("███") }}.
- [ ] Switch the projector off before exiting room {{ secrets.rooms.projector | default("███") }}.

### Finalizing the support laptops
- [ ] Unplug from {{ secrets.hosts.psychopy | default("███") }} the USB cable coming from the SyncBox.
- [ ] Switch the SyncBox off, and make sure you leave it connected exactly as you found it.
- [ ] Unplug from {{ secrets.hosts.psychopy | default("███") }} the HDMI cable from the display switch.
- [ ] Check that you leave the display switch as you found it.
- [ ] Switch off the {{ secrets.hosts.psychopy | default("███") }} computer.
- [ ] Exit the *Amphetamine* session and lock the screen of the {{ secrets.hosts.acqknowledge | default("███") }} computer.

## Turn off the MRI system if no more sessions are scheduled afterward

!!! warning "It is critical to follow the steps in order, ensuring each step is completed before proceeding further"

![on-off-button](../assets/images/on-off-box.jpg)

- [ ] Turn off the satellite station ({{ secrets.hosts.console_left | default("███") }}, the computer on the left side of the control desk)
- [ ] Turn off the control station ({{ secrets.hosts.console_right | default("███") }}, the computer on the right side of the control desk)
- [ ] Push the blue button displaying an overdotted circle and the **SYSTEM OFF** label above, which is found right above the key
- [ ] Turn the key into the *closed lock* position (:fontawesome-solid-lock:)
