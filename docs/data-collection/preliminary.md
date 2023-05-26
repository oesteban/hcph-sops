### Preliminary work

#### Once, at the beginning of the project
- [ ] Prepare a laptop with a running Psychopy 3 installation AND the EyeTracker software. For these SOPs, the designated laptop for the experiments is *{{ secrets.hosts.psychopy | default("███") }}*.
- [ ] [Fork the HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks/fork) under your user on GitHub.
- [ ] Clone the [HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks):
    ```
    git clone git@github.com:<your-gh-username>/HCPh-fMRI-tasks.git
    ```
- [ ] Set-up the original repository as upstream remote:
    ```
    git remote add upstream git@github.com:theaxonlab/HCPh-fMRI-tasks.git
    ```
- [ ] Watch the gas analyzer (GA) video:
    <video id="wistia_simple_video_119" crossorigin="anonymous" style="background: transparent; display: block; height: 100%; max-height: none; max-width: none; position: static; visibility: visible; width: 100%; object-fit: fill;" aria-label="Video" src="https://embed-ssl.wistia.com/deliveries/5e08ccab25ab45382329671a82dfe5123f6e840e/file.mp4" playsinline="" preload="metadata" type="video/mp4" x-webkit-airplay="allow" controls>
      <source src="https://embed-ssl.wistia.com/deliveries/5e08ccab25ab45382329671a82dfe5123f6e840e/file.mp4" type="video/mp4" />
      Your browser does not support the video. <a href="./assets/files/GA_video.mp4">Click here to download it</a>
    </video>

**Set up the scanner protocol at the MR console**

!!!warning "Important: follow Reproin conventions"

    When assigning names to the MR sequences in the protocol, make sure to follow the [Reproin conventions](https://dbic-handbook.readthedocs.io/en/latest/mri/reproin.html) to maximally facilitate the conversion into BIDS.
- [ ] Once the protocol is decided upon, and after any updates, make sure of storing the protocol:
    - [ ] Select all the sequences in the sequence list and click right to copy.
    - [ ] Open the Dot-Cockpit
    - [ ] In `Browse`, find the right folder to save the protocol in (RESEARCH > Oscar).
    - [ ] Right click on the folder and select `New program`.
    - [ ] Paste the copied sequences in the empty program [INSERT PICTURE].
    - [ ] If desired, the protocol details can also be downloaded as a pdf on a peripherical USB key.
        - [ ] Click right on the protocol and select `Print`
        - [ ] Save the PDF in your USB key.
    - [ ] Repeat the operation after creating the four variants of the protocol, one per PE direction.

**Install the BIOPAC**

- [ ] Set up the line frequency switches on the back of the BIOPAC amplifier depending on your country frequency to reduce noise. Both switches should be DOWN if your country's line frequency is 50Hz. Both switches should be UP if your country's line frequency line is 60Hz.
    ![biopack-frequency-switch](../assets/images/biopack-frequency-switch.jpg "BIOPAC frequency switch")
- [ ] Plug the different units of the BIOPAC together if it has not been done yet.
- [ ] Get familiar with the BIOPAC system:
    - [ ] We use the BIOPAC to synchronize and output in a single file all the physiological recordings: cardiac pulsation, respiration and CO<sub>2</sub>  concentration.
    ![Biopac_setup](../assets/images/Biopac_setup.jpg "BIOPAC front side")
    - [ ] The AMI100C unit can receive up to 16 analog signals. 
    - [ ] The DA100C unit records the signal coming from the respiration belt. Plug the TSD160A unit on the DA100C.
    - [ ] The ECG100C MRI unit records the electrical signal coming from the heart via the ECG. Plug the MECMRI-2 unit on the ECG100C unit.
    - [ ] The SPT100 (solid state relay driver unit) is used to record triggers. A trigger appears as a vertical red line on your physiological recordings [INCLUDE IMAGE]. Plug the trigger to the TRIG entrance.

**Install the BIOPAC recording software AcqKnowledge.**
- [ ] You have to add each BIOPAC module individually in the system
    - [ ] Add the respiration belt (RB) module
        - [ ] Under the section `Analog`, click on `Add new module`.
        - [ ] Find the name of the BIOPAC unit corresponding to the RB `DA100C`.
        - [ ] Verify that channel on top of the unit and choose that channel. The RB has to be on **channel 1**.
        - [ ] Verify that the configurations in the front of the module matches the configuration on screen. You should correct the value of gain, mode, 35HzLPN and HP so it is matching.
        - [ ] When prompted to enter [calibration?], for the RB you should map the interval [-5,0] to [0,10]. You inverse the sign of the interval for the interpretation to be more clear.
    
    - [ ] Add the gaz analyzer module
        - [ ] After clicking on `Add new module`, find the BIOPAC module in which you plugged the GA `Ami-Hlt - in3`.
        - [ ] Verify thechannel in which you plugged the GA ethernet. The GA has to be on **channel 3**.
        - [ ] Verify that the configurations in the front of the module matches the configuration on screen. You should correct the value of gain, mode, 35HzLPN and HP so it is matching.
        - [ ] When prompted to enter [calibration?], for the GA you should map the interval [1,0.03] to [10,0]. 

    - [ ] Add the ECG module
        - [ ] After clicking on `Add new module`, find the BIOPAC module in which you plugged the GA `ECG100C`.
        - [ ] Verify thechannel in which you plugged the GA ethernet. The GA has to be on **channel 2**.
        - [ ] Verify that the configurations in the front of the module matches the configuration on screen. You should correct the value of gain, mode, 35HzLPN and HP so it is matching.
        - [ ] When prompted to enter [calibration?], for the GA you should map the interval ?? to ??.
    
    - [ ] Add the BIOPAC module
        - [ ] Under the section `Digital`, click on `Add new module`.
        - [ ] The parallel cable feeds into port D8-D15


#### Every two months - calibrate the GA

- [ ] Get a gas bottle with a known CO<sub>2</sub> concentration between 5% and 10%.
- [ ] Connect the GA to the BIOPAC as described below and start recording signal.
- [ ] Edit the configuration of the inputs, making sure you update the voltage range for input 3 (the GA), estimated as described in [the GA's manual](../assets/files/GA_manual.pdf)

#### Three days BEFORE THE FIRST SESSION

- [ ] Verify that as part of the [recruitement and screening procedure](../recruitment-scheduling-screening/recruitment.md), you have sent a copy of the MRI Safety and screening form ([EN](../assets/files/safety_form_EN.pdf)|[FR](../assets/files/safety_form_FR.pdf)) to the participant over email and confirm reception by checking the 'First contact email sent' column in [our recruits spreadsheet]({{ secrets.data.recruits_url | default("/redacted.html") }}).
- [ ] Verify also that you confirmed that the participant has read and understood the document, and in particular, you double-checked that they do not have any MRI contraindications, by checking the 'Phone interview done' and 'Participant volunteer and eligible' column in [our recruits spreadsheet]({{ secrets.data.recruits_url | default("/redacted.html") }}).
- [ ] If the phone call interview was more than three days before the first session, call the participant again to reconfirm the following informations: 
    - [ ] Remind the participant that any jewelry should be removed prior to the scan.
    - [ ] Indicate that they MUST shave the upper area of their chest where the ECG electrodes will be placed, if there is hair. The ECG electrodes MUST directly contact the skin.
    - [ ] Confirm clothing:
        - [ ] if allowed to wear street clothes, remind the participant to avoid clothing with metal or that would uncomfortable to lie in for the duration of the scan; otherwise
        - [ ] remark the participant they will be given a gown and they will need to change before every session.
    - [ ] Repeat at what time and where will you meet the participant.
    - [ ] Verify that the participant has your phone number {{ secrets.phones.study | default("███") }} to call you in case he gets lost.
- [ ] If participant has indicated nervousness or history of claustrophobia, organize a session to use the mock scanner.

#### BEFORE DAY OF SCAN

- [ ] Print [the informed consent form](../assets/files/icf_FR.pdf) (**first session only**), an MRI safety screener ([EN](../assets/files/safety_form_EN.pdf)|[FR](../assets/files/safety_form_FR.pdf)) and a receipt form for each participant that will get scanned.
- [ ] Make sure you have internet access, and update the [HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks) on *{{ secrets.hosts.psychopy | default("███") }}*:
    ```
    git fetch upstream
    git checkout main
    git rebase upstream/main
    ```
- [ ] On the *{{ secrets.hosts.psychopy | default("███") }}* laptop, open a terminal and execute `conda deactivate`.
- [ ] Open psychopy 3 by typing `psychopy`
- [ ] Load in the different experiments and check for proper functioning:
    - [ ] Resting-state fMRI (RSfMRI): open the file `resting_state.psyexp` and check that the movie is played.
    - [ ] Breath-holding task (BHT): open the file `breath_holding_task.psyexp` and check it properly runs, while timing it (total length should be 5 min 24 s).
    - [ ] Positive-control task (PCT): open the file `control_task.psyexp` and check it properly runs, while timing it (total length should be 2 min XX s)