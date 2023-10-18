
### *Psychopy* installation
This block describes how to prepare an environment with a running *Psychopy 3* installation.

??? warning "Multiple screens"

    If you want to use multiple screens, install the corresponding libxcb extension:

    ``` shell
    sudo apt-get install libxcb-xinerama0
    ```

??? important "*Psychopy* should not be installed with *Conda*/*Anaconda*"

    If an anaconda environment is activated, run the following command to deactivate it:
    ``` shell
    conda deactivate
    ```

- [ ] Clone the [*Psychopy* repository](https://github.com/psychopy/psychopy):
    ``` shell
    git clone https://github.com/psychopy/psychopy.git
    ```
- [ ] Navigate to the *Psychopy* directory and check-out tag `{{ settings.psychopy.version }}`:
    ``` shell
    cd psychopy
    git checkout {{ settings.psychopy.version }}
    ```
- [ ] Update *Pypi* and *setuptools* to the latest version:
    ``` shell
    python3 -m pip install -U pip setuptools
    ```
- [ ] Update *Numpy* to the latest version:
    ``` shell
    python3 -m pip install -U numpy
    ```
- [ ] Install other necessary dependencies:
    ``` shell
    python3 -m pip install attrdict py2app bdist_mpkg
    ```
- [ ] Install *wxPython*.
    ``` shell
    python3 -m pip install -U \
        -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-$( lsb_release -r -s ) \
        wxPython
    ```
- [ ] Install *Psychopy* using the following command:
    ``` shell
    python3 -m pip install .[suggested]
    ```
- [ ] Install the *EyeLink* plugin for *Psychopy*:
    ``` shell
    python3 -m pip install git+https://github.com/oesteban/psychopy-eyetracker-eyelink.git
    ```

    ??? tip "On MacOSX or if you don't have access to pip directly, *Psychopy*'s package manager"

        Open *Psychopy* as mentioned immediately below.
        Click *Tools* ⤷ *Plugin/Packages manager...*, then go to the *Packages* tab and hit the <span class="keypress">Open PIP terminal</span> button (bottom left area).
        There, you can type:
        ``` shell
        pip install git+https://github.com/oesteban/psychopy-eyetracker-eyelink.git
        ```

- [ ] Try opening *Psychopy* by typing:
    ``` shell
    psychopy --no-splash -b
    ```

    ??? warning "Check that the *EyeLink* eye tracker is available in the dropdown under the experiment's options"

        If the *EyeLink* is not available, most likely the appropriate *Pylink* is missing.
        See the last checkbox in the [installation of the eye tracker](preliminary.md#preparing-the-stimuli-presentation-laptop-hos68752) to install it.
        Otherwise, make sure you installed the *EyeLink* plugin above.

    ??? important "The first time it runs, *Psychopy* will likely request some increased permissions"

        - [ ] Add a new `psychopy` group to your system.
            ``` shell
            sudo groupadd --force psychopy
            ```
        - [ ] Add your current user to the new group:
            ``` shell
            sudo usermod -a -G psychopy $USER
            ```
        - [ ] Raise security thresholds for *Psychopy*, by inserting the following into `/etc/security/limits.d/99-psychopylimits.conf`:
            ``` text
            @psychopy - nice -20
            @psychopy - rtprio 50
            @psychopy - memlock unlimited
            ```

??? bug "*Psychopy* crashes when trying to run a experiment: `pyglet.gl.ContextException: Could not create GL context`"

    This is likely related to your computer having a GPU and a nonfunctional configuration:

    ``` shell
    $ glxinfo | grep PyOpenGL
    X Error of failed request:  BadValue (integer parameter out of range for operation)
      Major opcode of failed request:  151 (GLX)
      Minor opcode of failed request:  24 (X_GLXCreateNewContext)
      Value in failed request:  0x0
      Serial number of failed request:  110
      Current serial number in output stream:  111
    ```

    A quick attempt to solve this would be adding our user to the `video` group.

    However, that is unlikely to work out so you'll need to take more actions (see [this](https://github.com/mmatl/pyrender/issues/13), and [this](https://askubuntu.com/questions/1255841/how-do-i-fix-the-glxinfo-badvalue-error-on-ubuntu-18-04))

??? bug "*Psychopy* crashes when trying to run a experiment: `qt.qpa.plugin: Could not load the Qt platform plugin 'xcb'`"

    If you installed `libxcb-xinerama0`, or you don't have multiple screens, first try:

    ``` shell
    python3 -m pip uninstall opencv-python
    python3 -m pip install opencv-python-headless
    ```

    If that doesn't work, try a brute force solution by installing libxcb fully:

    ``` shell
    sudo apt-get install libxcb-*
    ```

??? bug "*Psychopy* does not recognize the *SR Research* eye tracker"

    If the eye tracker does not appear in the corresponding dropdown menu or your experiments fail [as described in this issue](https://github.com/psychopy/psychopy/issues/5947), you almost certainly need to check the plugin is installed and available within *Psychopy*'s environment.

### Setting up the synchronization service as a daemon in the background

!!! important "It's fundamental to have a reliable means of communication with the BIOPAC digital inputs"

    The following guidelines set up a little service on a linux box that keeps listening for key presses (mainly, the <span class="keypress">s</span> trigger from the trigger box), and RPC (remote procedure calls) from typically *Psychopy* or similar software.

    The service is spun up automatically when you connect the MMBT-S modem interface that communicates with the BIOPAC (that is, the *N-shaped pink box*)

- [ ] To automatically start the program when the BIOPAC is connected, create a udev rule as follows:
    ``` shell
    sudo nano /etc/udev/rules.d/99-forward-trigger.rules
    ```
- [ ] Add the following rule to the file:
    ```
    ACTION=="add", KERNEL=="ttyACM0", SUBSYSTEM=="tty", TAG+="systemd", ENV{SYSTEMD_WANTS}="forward-trigger.service"
    ```
- [ ] Save the file and exit the editor.
- [ ] Run the following command to reload the udev rules:
    ``` shell
    sudo udevadm control --reload-rules
    ```
- [ ] Create a systemd service unit file:
    ``` shell
    sudo nano /etc/systemd/system/forward-trigger.service
    ```
- [ ] Add the following content to the file (Adapt the path to forward-trigger.py to the location on your computer):
    ```
    [Unit]
    Description=Forward Trigger Service
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /path/to/forward-trigger.py
    WorkingDirectory=/path/to/forward-trigger/directory
    StandardOutput=null

    [Install]
    WantedBy=multi-user.target
    ```
- [ ] Save the file and exit the text editor.
- [ ] Run the following command to enable the service to start at boot:
    ``` shell
    sudo systemctl enable forward-trigger
    ```
- [ ] Run the following command to reload the systemd daemon:
    ``` shell
    sudo systemctl daemon-reload
    ```
