
## Showing the participant out

- [ ] Extract the bed from the scanner's bore using the scanner's control wheel.
    The home (:fontawesome-solid-house:) button can alternatively be used to bring the bed out.

| ![take_table_down](../assets/images/take_table_down.png) |
|:--:|
| ![quick_return](../assets/images/quick_return.png) |

- [ ] Unplug the head coil from the bed connector, lift the lever that releases the upper part of the coil and put it aside (e.g., inside the bore or on a chair next to the scanner).
- [ ] Release the air from the inflatable padding by pushing the release valve of the pump and take them away. Remove the disposable covers and throw them away in the trash can.
- [ ] Help the participant sit down.
- [ ] Instruct the participant to remove the earplugs and dispose of them. Ask them about the experience:

    ???+ quote "Get feedback about the session from the participant"
        [NAME], how was your experience?
        Have you been able to feel comfortable throughout the session?
        What advice, indication do you feel we could've provided you for a better experience?

- [ ] Lift the nasal cannula and help the participant remove it from their head.
- [ ] Disconnect the tube from the RB and then lift the velcro attachment to remove the RB.
- [ ] Disconnect the ECG leads
- [ ] Help the participant step down and accompany them out to the control room.
- [ ] Help the participant recover their personal belongings and change clothes if necessary.
- [ ] Solicit more feedback on participant's comfort for future sessions.
- [ ] Solicit tickets and receipts for transportation.
- [ ] Give the participant the corresponding compensation for the participation and transportation.
- [ ] Ask the participant to sign the receipt of the amount of the financial compensation.

!!! important "To boost efficiency, two people can work simultaneously on the following steps — one inside the scanning room and the other outside. They can follow the designated sections [inside the scanning room](#after-scan-inside-the-scanner-room) and [outside the scanning room](#after-scan-outside-the-scanner-room) in parallel."

## AFTER SCAN, inside the scanner room

- [ ] Unplug the two cables connected to the ET (signal and power). Put those extremities aside far from the scanner.
- [ ] Disconnect the GA and RB tubes.

- [ ] **With someone outside in the control room**:
    - [ ] Carefully extract the cables (fiber and power of the ET) back through the access tube.
    - [ ] Extract the RB and the GA tubes from the room.

- [ ] **Carefully remove the infrared mirror**:
    - [ ] Enter again the scanner room with the plastic container of the mirror and leave it prepared on the bed.
    - [ ] Separate the mirror frame from the upper part of the head coil and lay it on the bed.
    - [ ] **PUT ON A NEW PAIR OF GLOVES**
    - [ ] Remove the scotch tape holding the infrared mirror and **IMMEDIATELY** insert the mirror in its plastic bag.
    - [ ] Take the mirror in its bag **OUT OF THE SCANNING ROOM** and place it back in the fMRI box, with extreme care.
    - [ ] Re-enter the scanning room and clean the standard mirror removing all residues of glue from the scotch tape. Re-attach the mirror to its coil's frame.

- [ ] Cleaning up instrumentation:
    - [ ] Take the projector's screen off and store it in its designated shelf.
    - [ ] Take the ET outside and put it in a stable place.
    - [ ] Disconnect the ECG leads from the filter of the access panel, fold the cable and leave it prepared with the RB to take out of the room with other equipment.
    - [ ] Disconnect the last section of the cannula and dispose of it in the trash can.

- [ ] **Clean-up of the scanning room**:
    - [ ] Put the sheet and the blanket inside the dirty linen bag (in the trash if used plastic sheets).
    - [ ] Dispose all single-use sanitary protections.
    - [ ] Put the pillows back in place.
    - [ ] Remove the head coil and put it in the scanner's bore.
    - [ ] Remove the back padding elements and put them back in their designated storage.
    - [ ] Reinstall the spine coil.
    - [ ] Plug back the head coil if you know the next exam will require that specific coil, or simply put it away with the other (head) coils on the shelf next to the scanner.
    - [ ] Take some cleaning napkins on the shelves in the MR room. Use them to clean the bed and the head coil (bottom and upper parts).
    - [ ] Lock the head coil back with its bottom part, do not plug the connectors.
    - [ ] Put the bed back in place = push the home (:fontawesome-solid-house:) button on the scanner
    - [ ] Everything that is removed for the experiment MUST be put back in place at the end of the experiment, i.e. position of the bed, coil, emergency button, ears padding.
    - [ ] Take the ECG electrodes, the RB, and the plexiglass outside to the control room.
    - [ ] Exit and close the external door.

## AFTER SCAN, outside the scanner room

- [ ] Help the person inside the scanning room to extract the cables and tubes.
- [ ] Carefully roll the fiber and power cable of the ET, and place them in the rolling table of the ET PC Tower.
- [ ] Carefully roll RB and the GA tubes and put them back in the GA and BIOPAC boxes.
- [ ] Unscrew the ET lens, while **ALWAYS** keeping one hand under the lens while screwing/unscrewing it and put it back into its cover.

  ![cover-mri-compatible-lens](../assets/images/cover-mri-compatible-lens.png "Cover MRI compatible lens")

- [ ] Put the cover, the ET base back in the fMRI box, **being extremely careful to not crush the mirror**.
- [ ] **Retrieve ET recordings** (from {{ secrets.hosts.psychopy | default("███") }}):
    - [ ] Insert a USB key into *{{ secrets.hosts.psychopy | default("███") }}* and save the experiment from AcqKnowledge.
    - [ ] Upload to a pre-designated drop-box (e.g., using Dropbox)
- [ ] Press <span class="keypress">Ctrl</span>+<span class="keypress">Alt</span>+<span class="keypress">Q</span> on the ET PC Tower to exit the EyeLink 1000 Plus Host PC application and click on the <span class="keypress">Shutdown</span> button from the **File Manager** toolbar.
- [ ] Switch off laptop and ET PC Tower. Plug back the sync box and the VGA projector where they were.
- [ ] Fix the rolled cable with the scotch on the ET PC Tower.
- [ ] Turn off the pump of the GA, then switch the GA off. **DO NOT PUT THE CAP IN WHILE THE PUMP IS ON.**
- [ ] Remove the cables connected to the BIOPAC and the GA and store them in the boxes in their original bags.
- [ ] Bring back the fMRI, BIOPAC and GA boxes in {{ secrets.rooms.et_camera| default("███") }}.
- [ ] Bring back the ET PC Tower and the plexiglas in {{ secrets.rooms.projector | default("███") }}
- [ ] Switch off the projector.

## Turn off the MRI system if no more sessions are scheduled afterward

!!! warning "It is critical to follow the steps in order, ensuring each step is completed before proceeding further"

![on-off-button](../assets/images/on-off-box.jpg)

- [ ] Turn off the satellite station ({{ secrets.hosts.console_left | default("███") }}, the computer on the left side of the control desk)
- [ ] Turn off the control station ({{ secrets.hosts.console_right | default("███") }}, the computer on the right side of the control desk)
- [ ] Push the blue button displaying an overdotted circle and the **SYSTEM OFF** label above, which is found right above the key
- [ ] Turn the key into the *closed lock* position (:fontawesome-solid-lock:)

