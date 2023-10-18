## Once, at the beginning of the project

### Setting up the scanner protocol at the MR console

The pilot phase will conclude when the protocol is decided upon.
Once finalized the protocol design, it will be *frozen* and it cannot be changed anymore.

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

### Install the BIOPAC

- [ ] Make sure you understand the components and settings of the BIOPAC, described in the [introduction section](intro.md#biopac-documentation-and-devices).
- [ ] Set up the line frequency switches on the back of the BIOPAC amplifier depending on your country frequency to reduce noise. Both switches should be DOWN if your country's line frequency is 50Hz. Both switches should be UP if your country's line frequency line is 60Hz.
    ![biopack-frequency-switch](../assets/images/biopack-frequency-switch.jpg "BIOPAC frequency switch")
- [ ] Plug the different units of the BIOPAC together if it has not been done yet.
- [ ] Ensure that the *Mode* switch of the [MMBT-S Trigger Interface Box adapter (pink color box)](../assets/files/MMBT-S_instruction_manual_v2.2.pdf) is set on the **P** position.
- [ ] Install the BIOPAC recording software (*AcqKnowledge*).
- [ ] Create a template *graph file* ([`EXP_BASE.gtl`](../assets/files/EXP_BASE.gtl))

    !!! important "Creating the *AcqKnowledge*'s template graph file"

        - [ ] Creating a graph file requires the BIOPAC system powered up and connected to the *{{ secrets.hosts.acqknowledge | default("███") }}* computer.
        - [ ] Add the RB module
            - [ ] Check the channel on top switch of the unit: the <mark>DA100C</mark> MUST be set on **channel 1**.
            - [ ] Under the tab *Analog*, click on *Add new module*.
            - [ ] Find the name of the BIOPAC unit corresponding to the <mark>DA100C</mark>.
            - [ ] Set the module settings (gain, filters, etc.) corresponding to those of the configuration switches in the front of the module.
            - [ ] When prompted to enter the calibration points, map the interval [-5, 0] to [0, 10]. You invert the sign of the interval for the interpretation to be more clear.
        - [ ] Add the ECG module
            - [ ] Check the channel on top switch of the unit: the <mark>ECG100C MRI</mark> MUST be set on **channel 2**.
            - [ ] Under the tab *Analog*, click on *Add new module*.
            - [ ] Find the name of the BIOPAC unit corresponding to the <mark>ECG100C</mark>.
            - [ ] Set the module settings (gain, filters, etc.) corresponding to those of the configuration switches in the front of the module.
            - [ ] When prompted to enter [calibration?], for the ECG you should map the interval ?? to ??.
        - [ ] Add the GA module
            - [ ] Confirm that the CO<sub>2</sub> output of the GA is connected through the ANISO filter to the **channel 3** of the AMI100C module.
            - [ ] Under the tab *Analog*, click on *Add new module*.
            - [ ] Select *Custom* and then indicate it is connected to **channel 3** by selecting *AMI/HLT - in3*.
            - [ ] When prompted to enter the calibration points, map the interval [0.03, 1.0] to [0, 10.0].
        - [ ] Add the Digital inputs
            - [ ] Under the tab *Digital*, click on *Add new module*.
            - [ ] The parallel cable feeds into ports <mark>D8-D15</mark>.
        - [ ] Configure the sampling frequency
        - [ ] Configure the experiment length (at least 2.5 hours)
        - [ ] Configure whether you want to collect directly to hard disk and autosave settings
        - [ ] Save the experiment, making sure you choose a "graph template file" (with extension `.gtl`)

### Install the gas analyzer (GA)


### Preparing the *Stimuli presentation laptop* ({{ secrets.hosts.psychopy | default("███") }})

The stimuli presentation laptop and any other box you want to use for debugging and development will require a few additional software packages to be available.

#### Installing *EyeLink* (eye tracker software)

!!! warning "The *EyeLink* software MUST be installed BEFORE *Pychopy*"

- [ ] Log on *{{ secrets.hosts.psychopy | default("███") }}* with the username *{{ secrets.login.username_psychopy | default("███") }}* and password `{{ secrets.login.password_psychopy | default("*****") }}`.

- [ ] Enable Canonical's universe repository with the following command:
    ``` shell
    sudo add-apt-repository universe
    sudo apt update
    ```
- [ ] Install and update the ca-certificates package:
    ``` shell
    sudo apt update
    sudo apt install ca-certificates
    ```
- [ ] Add the SR Research Software Repository signing key:
    ``` shell
    curl -sS https://apt.sr-research.com/SRResearch_key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/sr-research.gpg
    ```
- [ ] Add the SR Research Software Repository as an *Aptitude* source:
    ``` shell
    sudo add-apt-repository 'deb [arch=amd64] https://apt.sr-research.com SRResearch main'
    ```
- [ ] Install the EyeLink Developers Kit:
    ``` shell
    sudo apt install eyelink-display-software
    ```
- [ ] Install the EyeLink Data Viewer:
    ``` shell
    sudo apt install eyelink-dataviewer
    ```
- [ ] Install the *Pylink* module made by *SR Research*, it is prepared with the installation of the `eyelink-display-software`:

    ``` shell
    python3 -m pip install /usr/share/EyeLink/SampleExperiments/Python/wheels/sr_research_pylink-2.1.762.0-cp310-cp310-linux_x86_64.whl
    ```

    ??? warning "Find the appropriate version for your *Python* distribution"

        The example above is for *cPython* 3.10, alternative installations are:

        ```
        /usr/share/EyeLink/SampleExperiments/Python/wheels/sr_research_pylink-2.1.762.0-cp27-cp27mu-linux_x86_64.whl
        /usr/share/EyeLink/SampleExperiments/Python/wheels/sr_research_pylink-2.1.762.0-cp310-cp310-linux_x86_64.whl
        /usr/share/EyeLink/SampleExperiments/Python/wheels/sr_research_pylink-2.1.762.0-cp311-cp311-linux_x86_64.whl
        /usr/share/EyeLink/SampleExperiments/Python/wheels/sr_research_pylink-2.1.762.0-cp36-cp36m-linux_x86_64.whl
        /usr/share/EyeLink/SampleExperiments/Python/wheels/sr_research_pylink-2.1.762.0-cp37-cp37m-linux_x86_64.whl
        /usr/share/EyeLink/SampleExperiments/Python/wheels/sr_research_pylink-2.1.762.0-cp38-cp38-linux_x86_64.whl
        /usr/share/EyeLink/SampleExperiments/Python/wheels/sr_research_pylink-2.1.762.0-cp39-cp39-linux_x86_64.whl
        ```

#### Installing our synchronization server

During the session, we run a synchronization server that acts as a hub for the signals (triggers, task events, etc.) that define the experiment.
For the best experience, we *daemonize* the synchronization service (meaning, we make it a service of the operative system that runs in the background).
To install it as a service, please follow [the documentation in the appendix](software.md#setting-up-the-synchronization-service-as-a-daemon-in-the-background)

- [ ] Locate the latest version of the synchronization service on your system.
    It is within the SOPs repository, at ``{{ secrets.data.sops_clone_path | default('<path>') }}/code/synchronization/forward-trigger-service.py``.
- [ ] Install the necessary libraries <mark>as root</mark>:
    ``` shell
    sudo python3 -m pip install -r {{ secrets.data.sops_clone_path | default('<path>') }}/code/synchronization/requirements.txt
    ```
- [ ] Test the service is properly installed:
    ``` shell
    sudo python3 code/synchronization/forward-trigger-service.py --disable-mmbt-check
    ```

    !!! important "Use the `--disable-mmbt-check` flag only if you do not plan to connect the MMBT-S trigger box"

- [ ] Test operation with our test client:

    !!! tip "Check the server's log file at `/var/log/forward-trigger-service.log`"

    Open a separate terminal on a separate window
    Then, open and follow the log file:
    ``` shell
    less +F /var/log/forward-trigger-service.log
    ```

    Return to the original terminal, keeping the other window visible and execute:
    ``` shell
    python code/synchronization/forward-trigger-client.py
    ```

    The log file should now have added two lines like:
    ```
    2023-10-12 14:44:31.788 - INFO - Data received: <b'\x02'>
    2023-10-12 14:44:31.788 - INFO - Forwarded <b'\x02'>
    ```

??? important "Testing the service without the MMBT-S connected"

    Testing the service without the MMBT-S trigger box connected requires emmulating `/dev/ttyACM0`:

      - [ ] Ensure `socat` and `screen` are installed (if not already):
          ``` shell
          sudo apt-get update
          sudo apt-get install socat screen
          ```
      - [ ] Create a virtual serial port and establish a symbolic link to `/dev/ttyACM0` using the following command:
          ``` shell
          sudo socat PTY,link=/tmp/virtual_serial_port PTY,link=/dev/ttyACM0,group-late=dialout,mode=666,b9600
          ```
      - [ ] With `screen`, listen to the new virtual serial port:
          ``` shell
          screen /dev/ttyACM0
          ```

          !!! tip "Alternatively, you can check the server's log file at `/var/log/forward-trigger-service.log`"

      - [ ] Press <span class="keypress">s</span> and verify that `^A` appears in the screen terminal.

#### Prepare the *Psychopy* experiments

!!! tip "The appendix has some guides on [how to install *Psychopy*](software.md#psychopy-installation)."

- [ ] Log on *{{ secrets.hosts.psychopy | default("███") }}* with the username *{{ secrets.login.username_psychopy| default("███") }}* and password `{{ secrets.login.password_psychopy| default("*****") }}`.
- [ ] Deactivate conda environment (if needed):
    ``` shell
    conda deactivate
    ```
- [ ] Install our *HCPh-signals* package (assumes these SOPs are checked out at `{{ secrets.data.sops_clone_path | default('<path>') }}`:
    ``` shell
    cd {{ secrets.data.sops_clone_path | default('<path>') }}/code/signals
    python3 -m pip install .
    ```
- [ ] [Fork the HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks/fork) under your user on GitHub.
- [ ] Clone the [HCPh-fMRI-tasks repository](https://github.com/TheAxonLab/HCPh-fMRI-tasks):
    ```
    git clone git@github.com:<your-gh-username>/HCPh-fMRI-tasks.git
    ```
- [ ] Set-up the original repository as upstream remote:
    ```
    git remote add upstream git@github.com:theaxonlab/HCPh-fMRI-tasks.git
    ```
- [ ] Open *Psychopy* and (optionally) a experiment file corresponding to a task by typing the following command in the terminal:
    ```
    psychopy {{ settings.psychopy.tasks.func_qct }}
    ```
- [ ] For each task, check the following:
    - [ ] `{{ settings.psychopy.tasks.func_qct }}` (positive-control task, QCT) :
        - [ ] time it to [confirm the length](intro.md#task-timing), and
        - [ ] check the task runs properly.
    - [ ] `{{ settings.psychopy.tasks.func_rest }}` (resting-state fMRI):
        - [ ] time it to confirm the length, and
        - [ ] check that the movie is played.
    - [ ] `{{ settings.psychopy.tasks.func_bht }}` (breath-holding task, BHT):
        - [ ] time it to confirm the length, and
        - [ ] check the task runs properly.

## Every two months

### Calibrate the GA

??? important "A gas mixture bottle with a known CO<sub>2</sub> and O<sub>2</sub> concentrations is necessary"

    CO<sub>2</sub> concentration must be between 5% and 10%, while O<sub>2</sub> within 5% and 21%.
    A second reference mixture is necessary, and room air can be used, knowing that atmospheric contents by volume are 0.039 ±0.001%
    for CO<sub>2</sub> and 20.946 ±0.003% for O<sub>2</sub>.

- [ ] Connect the GA to the BIOPAC as described in [this section](pre-session.md#setting-up-the-biopac-system-and-physiological-recording-sensors).
- [ ] Connect the BIOPAC to the *Physiology recording laptop* ({{ secrets.hosts.acqknowledge | default("███") }}) as described in [this section](pre-session.md#setting-up-the-biopac-system-and-physiological-recording-sensors).
- [ ] Connect the *AcqKnowledge* License Key into a USB Port of the *Physiology recording laptop* ({{ secrets.hosts.acqknowledge | default("███") }}).
- [ ] Open *AcqKnowledge* software on the *Physiology recording laptop* ({{ secrets.hosts.acqknowledge | default("███") }}).
- [ ] Open the template *graph file* ([`EXP_BASE.gtl`](../assets/files/EXP_BASE.gtl))
- [ ] Edit the configuration of the inputs 3 (connected to the CO<sub>2</sub> output of the GA) and 4 (connected to the O<sub>2</sub> output of the GA).
    Lower and upper calibration points can be set by sampling the input a number of times with the *AcqKnowledge* utility.
- [ ] Overwrite the template *graph file* `EXP_BASE.gtl`.
