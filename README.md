# rt-fMRI Neurofeedback of ADHD
This manual describes the study protocol for neurofeedback on sustained attention in ADHD, conducted by Alexander Cohen's Lab of Translational Neuroimaging at Boston Children's Hospital. This study uses the rt-Cloud platform (https://github.com/brainiak/rt-cloud) and adapts stimulus presentation scripts from the multivariate and univariate real-time functional imaging (MURFI) program (https://github.com/cccbauer/MURFI-user-manual). For more detailed instructions on how to use the rt-Cloud platform, see: https://rt-cloud.readthedocs.io/en/latest/index.html. 

 ![image](https://github.com/bchcohenlab/rt-fMRI_Neurofeedback_of_ADHD/assets/88854051/9b52c9eb-fd11-426f-ae58-616507b126d1)

# Initial Setup

Source Documentation: https://rt-cloud.readthedocs.io/en/latest/index.html
**Note: every year security certificates expire on January 1. To share the renewed version with other machines, connect via ethernet cable and adapt the following code to your machine: ``` scp -r certs username@ip.address:/certificates/folder ```
  •	 May need to edit permissions in web browser
    • Firefox instructions: https://support.mozilla.org/en-US/kb/Certificate-contains-the-same-serial-number-as-another-certificate
    • Chrome: settings → privacy and security → manage certificates → authorities → import → import 1000.pem
    •	If you get errors with certificate permissions, you can run your commands with the --test flag
        • Instead of logging in using the username rt, use "test" with password "test"

 # Neurofeedback Components

DATA_STREAMER: runs on machine that receives/sends DICOMs  (i.e., the MRI console)
•	Watches for new DICOM brain images and sends them to the machine analyzing the data

DATA_ANALYSER: runs on machine that analyses data in real-time (i.e., the Dell laptop)
•	Runs experimenter’s script to process DICOMs
•	Provides a web-based user interface for experimenter control

ANALYSIS_LISTENER: runs on machine that runs presentation software (i.e., personal laptop)
•	Listens for results from DATA_ANALYSER to inform experiment presentation (i.e., from PsychoPy)

 # Short Instructions 
 ## Remember to do the MRI Screening form and symptom screening form
 # NOTE: Restart Computer after plugging in
 ## Test Connection
  1. type ```pingdell``` from the Macbook
  2. type ```pingmac``` from the Dell computer
  3. to test the connection with the scanner, type ```ping 192.168.2.1``` from the neurofeedback laptop.

 ## LCD Monitor Setup
  1. Attach C2G extension cable to the research PC cord
  2. Attach cord to Macbook
  3. Click Research PC Button (Push down 1-2 seconds, wait a few seconds), make sure all three lights (keyboard, audio, cable) transfer.
    - The top button can be yellow, the bottom two must be green.
    
 ## Button Box Setup 
  1. slices = 1, Trigger = 1, volumes = 364, USB Mode = "HID"
  2. everything is ‘1’
  3. works for MSIT and NF
  NOTE: quit after each run and restart, as number of volumes is higher than needed

 ## Dell Computer Setup: 
  1. Open Terminal
  2. Type ```start``` and put in the password
  3. Type ```analyse``` and click the link to open Docker

 ## Mac Computer Setup: 
  1. Open Terminal
  2. After setting up Dell Computer, type ```listener```
  3. In a new terminal, type ```psychopy```

 ## Pre-MSIT 
  1. Open ```msit_neurofeedback.py```
  2. click play

 ## Rest 
  1. Quit button box and start again
  2. start ```rest.py``` from PsychoPy app
  3. during the first resting state, run the MSIT ACC localizer script on the neurofeedback laptop
    a. type ``` nifti ``` into a terminal to convert the dicoms to nifti
    b. type ```localize_acc```, ```localize_motor```, ```localize_motor_hotspot``` or any other localizer alias created

 ## Neurofeedback
  1. Quit button box and start again
  2. Run the ```rt_feedback_single_roi.py``` script from the PsychoPy app.
   - This script will begin as soon as it receives the first pulse from the scanner, and it will begin sending feedback as soon as it receives a  json file with the neurofeedback score.
  3. Click 'run' in the web interface on the neurofeedback laptop. The script will start when it sees the first DICOM image.
    
  - NOTE: Change the run number from 1 to 2 to 3 depending on which run it is
  - NOTE: Quit button box and start again after every run

 ## Post-MSIT 
  1. Open ```msit_neurofeedback.py```
  2. click play
      
## Ending a session
After all 3 runs are finished for the session, click "finalize session" in the web browser.

# ------------------------------------------
# Longer Instructions 
# ------------------------------------------
# Equipment Setup

## Set up necessary connections
1) Connect the neurofeedback and stimulus laptops to the two ethernet cables that are at the scanner. If you haven't set up the ethernet connections in the past, configure them manually in your laptop's settings, making sure the IP address is set to 192.168.2.6 and the net mask is 255.255.255.240.
2) Make sure the IP addresses are 192.168.2.5 for the neurofeedback laptop and 192.168.2.6 for the stimulus laptop. The scanner's IP address should always be 192.168.2.1. To check the IP address on Ubuntu, type: ```ifconfig``` and to check on Mac, type: ```ipconfig```.
 NOTE: To Ping Dell and Mac: type ping 192.168.2.5 from your laptop and ping 192.168.2.6 from the Dell 
4) Have the MR tech connect the scanner to the neurofeedback laptop's samba share. From File Explorer, right-click on This PC, then select Add A Network Location. Follow the directions to enter the samba share address: //192.168.2.5/sambashare. When it asks for credentials, click on guest.
• After it is set up once, you should be able to click on it in the left sidebar, but you may have to go through this setup again if it gets deleted from the scanner console.
5) To test the connection with the scanner, type ```ping 192.168.2.1``` from the neurofeedback laptop.

## Set up stimulus presentation
## Button Box Setup
1) Plug the "Research Computer" LCD Monitor Cord into the computer and click the "Research Computer" Button on the Box next to the Cord.
2) Click Research PC Button (Push down 1-2 seconds, wait a few seconds), make sure all three lights (keyboard, audio, cable) transfer. The top button can be yellow, the bottom two must be green. 
3) Make sure that NNL (Button Box): go to Options-> slices = 1, Trigger = 1, volumes = 364, USB Mode = "HID"
4) Hit Start, should see screen with brain

NOTE: Once you plug the laptop into the LCD monitor, you should be able to use the laptop screen while projecting the stimuli onto the LCD. However, this has posed some problems. If it does, set your display to 'mirror'. The script should work now, but the participant will be able to see anything you are seeing on the laptop screen.

# Scanning Protocol
### Sequence of Events: Task-Based Scans
![Picture1](https://github.com/bchcohenlab/rt-fMRI_Neurofeedback_of_ADHD/assets/88854051/2569af92-8cf1-4a7e-9022-3bb343de786e)

## Preparing rt-Cloud and PsychoPy 

You can set up the rt-cloud connections while the MR tech is running the anatomical scans. To do this:
1) On the Neurofeedback (Dell) laptop, type ``` start ``` in Terminal. If this alias doesn't work, type: ``` sudo smbd nmbd start ```

2) Start DATA_ANALYSER on Neurofeedback laptop:
You should only have to type ```analyse```. However, if this command doesn't work, try typing:
   ``` 
   PROJ_DIR=/home/rt/rtcloud-projects/adhd_rt/
   docker run -it --rm --link-local-ip=192.168.2.5 -p 8888:8888 --cap-add=SYS_ADMIN -v ~/certs:/rt-cloud/certs -v /home/rt/rt-cloud/projects/adhd_rt:/rt-cloud/projects/adhd_rt -v /home/rt/sambashare:/home/rt/sambashare julianawall/adhd_rtcloud scripts/data_analyser.sh -p adhd_rt --subjectRemote
   ```
   or
   ```
      PROJ_DIR=/home/rt/rtcloud-projects/adhd_rt/
      docker run -it –rm –link-local-ip=192.168.2.5 -p 8888:8888 -v ~/certs:/rtcloud/certs -v $PROJ_DIR:/rt-cloud/projects/adhd_rt brainiak/rtcloud:latest scripts/data_analyser.sh -p adhd_rt –subjectRemote –dataRemote
   ```
   If you get errors around this step or a little later, it would be good to check what is going on in this step and look for errors here.

• This should pop up a link that you can click on, which will bring you to the login page. Enter username and password, then, in the second tab, click "initialize session". 

3) Start ANALYSIS_LISTENER on stimulus laptop:

  ``` listener ``` 
  
  if that doesn't work, do these four commands in order: 

  ```
  WEB_IP=192.168.2.5
  conda activate rtcloud
  cd rt-cloud/
  bash scripts/analysis_listener.sh -s $WEB_IP:8888 -u rt
  ```
Once the stimulus and neurofeedback laptops are connected, this message will pop up on the stimulus laptop's terminal:
```
INFO:root:Connected to: wss://192.168.2.5:8888/wsSubject
Connected to: wss://192.168.2.5:8888/wsSubject
```
Also, in the righthand corner of the web interface, you should see 'subjConn: connected'

4) Start PsychoPy on Macbook:
• In a new terminal:

 ``` psychopy ```
 
if this alias doesnt work, do:
  ```
  conda activate rtcloud
  psychopy
  ```
**Note: Make sure to stay in Psychopy window, do not navigate away from screen**
## Running fMRI Scans (MSIT, resting-state, and neurofeedback)
**1. start psychopy, 2. participant reads instructions and presses button, 3. then scanner can be started**
Right Thumb = volume up (regardless of keyboard)
Right Index Finger = c, 3 
Left Thumb = a, 2
Left Index Finger = b, 1
<img width="1004" alt="Screenshot 2024-04-29 at 8 07 16 AM" src="https://github.com/bchcohenlab/rt-fMRI_Neurofeedback_of_ADHD/assets/89412811/d786267f-69f1-4d37-aa12-6fb33f56d4c8">



1) The first task-based scan is the multi-source interference task (MSIT). The stimuli for this task will be presented using PsychoPy.
To start the task, type:

```
psychopy
```
if the above alias doesn't work, do:
``` 
conda activate rtcloud
psychopy 
```
and start MSIT_neurofeedback.py from the app. Make sure to check which monitor is selected. 

**Note: Have every component / machine listening and ready for the scanner before having the MRI Tech start the scanner.** 

2) After the MSIT is a resting-state scan. **Press "a" to end instructions screen, and have it wait for scanner** Make sure to repeat this step for each resting-state scan throughout the session. 
 - start rest.py from PsychoPy app

3) During the first resting state, run the MSIT ACC localizer script on the neurofeedback laptop.

Start by converting the DICOMs to nifti:
- type ``` nifti ``` into a terminal. It will ask you to either choose from a list of directories in the sambashare folder (most recent first) or provide the name of the directory yourself.
- If this doesn't work:
  Copy the name of the directory with the DICOMs, then type this command:
   ```
   conda activate rtcloud
   dcm2niix /home/rt/sambashare/{DICOM directory}
   ```

To localize the subject's anterior cingulate cortex, type ``` localize_acc ```.
if the acc localizer doesn't work, try: 
   ```
   python3 /home/rt/rt-fMRI_Neurofeedback_of_ADHD/adhd_rt/msit_preproc_script.py {subject id}
   ```

To localize the subject's motor cortex, type ``` localize_motor ```. 
if the motor localizer doesn't work, try: 
   ```
   python3 /home/rt/rt-fMRI_Neurofeedback_of_ADHD/adhd_rt/msit_preproc_script_motor_cortex.py {subject id}
   ```


 - Before moving on, it is a good idea to check that the mask looks okay. Pull up the new mask in FSLeyes with the functional data as the background.
   
** Note: The MSIT will be repeated at the end, but you don't need to run this script the second time. 

4) Neurofeedback runs
   1) Run the rt_feedback_single_roi.py script from the PsychoPy app. This script will begin as soon as it receives the first pulse from the scanner, and it will begin sending feedback as soon as it   receives a json file with the neurofeedback score. 

   2) Click 'run' in the web interface on the neurofeedback laptop. The script will start when it sees the first DICOM image.

   NOTE: Change the run number from 1 to 2 to 3 depending on which run it is

## Ending a session
After all 3 runs are finished for the session, click "finalize session" in the web browser.

## Helpful definitions to keep everything straight
- neurofeedback laptop: the Dell laptop running the data_analyser script
- stimulus laptop: laptop that is running  PsychoPy scripts
- session: entire scan, each time a participant visits 2BP (participants will come for 3-8 sessions)
- run: single neurofeedback scan within a session (there are 3 during each session)
- block: single round of neurofeedback during a run (there are 2 blocks in each run)

