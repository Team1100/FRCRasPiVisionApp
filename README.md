# FRCRasPiVisionApp
Welcome to Inverse Polarity's tutorial on how to set up FRC vision on a Raspberry Pi. The instructions below can help anyone with limited programming experience set up a robot vision system for detecting [AprilTags](https://docs.wpilib.org/en/stable/docs/software/vision-processing/apriltag/apriltag-intro.html). Also included in the doc folder are two presentations. *AprilTag Vision Presentation* gives a general overview of AprilTags and briefly describes our solution. *Vision Distance Calculation* is an overview of how to calculate the distance to a target given several constants. 

## Instructions
1. Follow [these](https://docs.wpilib.org/en/stable/docs/software/vision-processing/wpilibpi/what-you-need-to-get-the-pi-image-running.html) instructions to set up the Raspberry PI
    1. Stop at the end of the *Installing the image to your MicroSD card* section.
2. Connect the pi to ethernet and power
3. Type http://wpilibpi.local/ into your browser to interface with the web dashboard.
    1. If the dashboard doesn't show up, you may need to connect a monitor and keyboard into the raspberry pi, and log in. However, if it did show up, skip to step 4.
        1. Username: `pi`
        2. Password: `raspberry`
    2. type `ifconfig` (prints out the IP address).
        1. The ip address should be after the word "inet"
        2. Ex: inet 192.168.0.196
    3. Type the ip address directly into your browser search bar.
4. Configure your Raspberry PI
    1. Read more about the web dashboard [here](https://docs.wpilib.org/en/stable/docs/software/vision-processing/wpilibpi/the-raspberry-pi-frc-console.html).
    2. Click *Writable* at the top: **MAKE SURE TO KEEP AS WRITABLE THE WHOLE PROCESS**
    3. Go to the Vision Settings tab of the web dashboard, type in your team number, and save.
5. Add the python application
    1. In the **Application** tab, select the *Uploaded Python file* option and upload the [pythonVisionApp.py](https://github.com/Team1100/FRCRasPiVisionApp/tree/master/src)
    2. In the upload file section of the **Application** tab, upload the [runCamera](https://github.com/Team1100/FRCRasPiVisionApp/tree/master/src) file.
6. Interface with the PI
    1. There are two ways you can interface with the pi. The easiest to set up is to follow the instructions listed in step 3. section i.
    2. The alternative is to download [Git Bash](https://gitforwindows.org/), which will allow for remote connection to the pi from your computer.
        1. Once downloaded, type in `ssh pi@wpilibpi.local` into the terminal to remotely connect to the pi.
        2. Log in with the same credentials listed in step 3) i.
7. Learn how to navigate a linux terminal
    1. Follow [this tutorial](https://linuxsurvival.com/) to learn how to use Linux
8. Make sure the system clock is up to date
    1. Type `date` into the pi or Git Bash to read out what the system thinks is the current date and time. If it's correct, you can skip to step 10. If it is incorrect, continue to step 9.
9. Update the system clock
    1. Type these instructions (insert the correct date for step C. "Year-Month-Day Hour:Minute:Second").
        1. `sudo bash`
        2. `timedatectl set-timezone America/New_York`
        3. `timedatectl set-time "2023-01-03 16:27:00"`
        4. `apt install ntpdate`
        5. `service ntp start`
10. Organize the file structure (REMEMBER: make sure the pi is set to Writable)
    1. Type these instructions.
        1. `mkdir python-app`
        2. `mv pythonVisionApp.py python-app/`
        3. `chmod 755 runCamera`
11. Download the AprilTag library
    1. Type these instructions.
        1. `apt update`
        2. `apt upgrade`
        3. `shutdown -r now`
    2. At this point, the pi will have shut down, so remove and re-insert the power cable to reboot.
    3. Log back in and set the system to *Writable* via the web app.
    4. Type these instructions.
        1. `sudo apt install git`
        2. `sudo apt install cmake`
        3. `sudo apt-get install python3-opencv`
        4. `mkdir apriltagCode`
        5. `cd apriltagCode`
        6. `git clone https://github.com/AprilRobotics/apriltag`
        7. `cd apriltag`
        8. `cmake .`
        9. `make`
        10. `sudo make install`
        11. `make apriltag_demo`
12. Configure the python application
    1. Read up on the [VI editor](https://www.redhat.com/sysadmin/introduction-vi-editor)
    2. ONLY IF you want to simulate the robot on a driver station, then you need to enter your computer ip address into the python program. However, if you plan on setting the pi up directly on the robot, skip to step 12) iii.
        1. Navigate into the python-app folder.
        2. Start editing the pythonVisionApp.py by typing `vi pythonVisionApp.py`
            1. On line 51, set `usingComputerIP` to `True`
            2. On line 112, set `ip` to your computer's ip address.
                1. On Windows, find your ip by opening Command Prompt and typing `ipconfig`
                2. On Mac, find your ip by opening Terminal and typing `ifconfig`
    3. To specify which variables you want published to NetworkTables, add additional lines to the code starting at line 172.
    4. If you wish to calculate the distance to a target, move onto step 13.
        1. Otherwise go to lines 59 through 71, set all five variables to 1, and skip to step 14.
13. Calculate the distance to a target
    1. Read up on calculating distance to a target.
    2. Go to lines 59 through 71 and fill in the five empty variables.
        1. *vertFOV* is the vertical field of view of the camera.
            1. Calulate *vertFOV* by facing the camera toward a wall (making sure it's flat).
            2. Measure the distance from the camera to the wall (We will call this `adjacentDistance`).
            3. Mark on the wall where the top and bottom of the camera feed ends (make sure they are along the same vertical line).
            4. Measure the distance between the two marks and devide that in half (We will call this `oppositeDistance`).
            5. Take the inverse tangent of the adjacentDistance divided by the oppositeDistance.
            6. That's your vertFOV! Plug that into the pythonVisionApp.
        2. *horizFOV* is the horizontal field of view of the camera.
            1. Calulate *horizFOV* by facing the camera toward a wall (making sure it's flat).
            2. Measure the distance from the camera to the wall (We will call this `adjacentDistance`).
            3. Mark on the wall where the left and right of the camera feed ends (make sure they are along the same horizontal line).
            4. Measure the distance between the two marks and devide that in half (We will call this `oppositeDistance`).
            5. Take the inverse tangent of the `adjacentDistance` divided by the `oppositeDistance`
            6. That's your horizFOV! Plug that into the pythonVisionApp.
        3. *elevationOfTarget* is the height of the target from the ground.
        4. *elevationOfCamera* is the height of the camera from the ground. NOTE: This will need to be updated if it ever changes.
        5. *angleFromHoriz* is the angle the camera makes from an imaginary horizontal line. If it is facing straight forwards, *angleFromHoriz* would be 0. NOTE: This will need to be updated if it ever changes.
14. View the video stream!
    1. Set up the pi on the robot.
        1. It requires a power input from the robot and an ethernet input from the radio.
        2. The camera needs to be plugged into one of the usb ports.
    2. Open Shuffleboard.
    3. In the top left corner, click on the two greater-than signs to expand the drawer.
    4. Click on the CameraServer menu.
    5. If *visionCam* shows up, right click and select *Show as: Camera Stream*. Wave an apriltag in front and see the program do its magic!!
    6. If it doesn't show up, restart the python program.
        1. Go to the **Vision Status** tab of the web dashboard (make sure you are connected to the robot's wifi).
        2. Toggle the switch on the far right of the Console Output to enble output.
        3. Press *Kill* to restart the program.
    7. If it still doesn't work, review the previous steps to make sure you followed directions exactly.






