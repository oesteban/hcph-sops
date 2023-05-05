### Preliminary work

#### Once, at the beginning of the project
- [ ] [Fork the HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks/fork) under your user on GitHub.
- [ ] Prepare a laptop with a running Psychopy 3 installation AND the EyeTracker software. For these SOPs, the designated laptop for the experiments is *{{ secrets.hosts.psychopy }}*.
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
- [ ] Watch the gas analyzer (GA) video:
    <video id="wistia_simple_video_119" crossorigin="anonymous" style="background: transparent; display: block; height: 100%; max-height: none; max-width: none; position: static; visibility: visible; width: 100%; object-fit: fill;" aria-label="Video" src="https://embed-ssl.wistia.com/deliveries/5e08ccab25ab45382329671a82dfe5123f6e840e/file.mp4" playsinline="" preload="metadata" type="video/mp4" x-webkit-airplay="allow" controls>
      <source src="https://embed-ssl.wistia.com/deliveries/5e08ccab25ab45382329671a82dfe5123f6e840e/file.mp4" type="video/mp4" />
      Your browser does not support the video. <a href="./assets/files/GA_video.mp4">Click here to download it</a>
    </video>


**Install the BIOPAC**

- [ ] Set up the line frequency switches on the back of the BIOPAC amplifier depending on your country frequency to reduce noise. Both switches should be DOWN if your country's line frequency is 50Hz. Both switches should be UP if your country's line frequency line is 60Hz.
    ![biopack-frequency-switch](../assets/images/biopack-frequency-switch.jpg "BIOPAC frequency switch")
- [ ] Plug the different units of the BIOPAC together if it has not been done yet. We use the BIOPAC to synchronize and output in a single file all the physiological signals we record: cardiac pulsation, respiration and CO2 concentration.
- [ ] Install the BIOPAC recording software.
- [ ] Get familiar with the BIOPAC system:
    ![biopack-front](../assets/images/biopack-front.jpg "BIOPAC front side")
    - [ ] The AMI100C unit can receive up to 16 analog signals. 
    - [ ] The DA100C unit records the signal coming from the respiration belt. Plug the TSD160A unit on the DA100C.
    - [ ] The ECG100C MRI unit records the electrical signal coming from the heart via the ECG. Plug the MECMRI-2 unit on the ECG100C unit.
    - [ ] The SPT100 (solid state relay driver unit) is used to record triggers. A trigger appears as a vertical red line on your physiological recordings [INCLUDE IMAGE]. Plug the trigger to the TRIG entrance.
- [ ] Install the GA on the wooden platform behind the MRI consoles.

#### Every two months - calibrate the GA

- [ ] Get a gas bottle with a known CO<sub>2</sub> concentration between 5% and 10%.
- [ ] Connect the GA to the BIOPAC as described below and start recording signal.
- [ ] Edit the configuration of the inputs, making sure you update the voltage range for input 3 (the GA), estimated as described in [the GA's manual](../assets/files/GA_manual.pdf)

#### One week BEFORE THE FIRST SESSION

- [ ] Send a copy of the MRI Safety and screening form ([EN](../assets/files/safety_form_EN.pdf)|[FR](../assets/files/safety_form_FR.pdf)) to the participant over email and confirm reception.
- [ ] Confirm that the participant has read and understood the document, and in particular, double-check that they do not have any MRI contraindications.
- [ ] Remind the participant that any jewelry should be removed prior to the scan.
- [ ] Indicate that they MUST shave the upper area of their chest where the ECG electrodes will be placed, if there is hair. The ECG electrodes MUST directly contact the skin.
- [ ] Confirm clothing:
    - [ ] if allowed to wear street clothes, remind the participant to avoid clothing with metal or that would uncomfortable to lie in for the duration of the scan; otherwise
    - [ ] remark the participant they will be given a gown and they will need to change before every session.
- [ ] If participant has indicated nervousness or history of claustrophobia, use the mock scanner.

#### BEFORE DAY OF SCAN

- [ ] Make sure you have internet access, and update the [HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks) on *{{ secrets.hosts.psychopy }}*:
    ```
    git fetch upstream
    git checkout main
    git rebase upstream/main
    ```
- [ ] On the *{{ secrets.hosts.psychopy }}* laptop, open a terminal and execute `conda deactivate`.
- [ ] Open psychopy 3 by typing `psychopy`
- [ ] Load in the different experiments and check for proper functioning:
    - [ ] Resting-state fMRI (RSfMRI): open the file `resting_state.psyexp` and check that the movie is played.
    - [ ] Breath-holding task (BHT): open the file `breath_holding_task.psyexp` and check it properly runs, while timing it (total length should be 5 min 24 s).
    - [ ] Positive-control task (PCT): open the file `control_task.psyexp` and check it properly runs, while timing it (total length should be 2 min XX s)