# rt-fMRI Neurofeedback of ADHD
This manual describes the study protocol for neurofeedback on sustained attention in ADHD, conducted by Alexander Cohen's Lab of Translational Neuroimaging at Boston Children's Hospital. This study uses the rt-Cloud platform (https://github.com/brainiak/rt-cloud) and adapts stimulus presentation scripts from the multivariate and univariate real-time functional imaging (MURFI) program (https://github.com/cccbauer/MURFI-user-manual). 

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

# Equipment Setup
## Set up necessary connections
1) Connect the neurofeedback and PsychoPy laptops to the two ethernet cables that are at the scanner. 
2) Make sure the IP addresses are 192.168.2.5 for the neurofeedback laptop and 192.168.2.6 for the PsychoPy laptop. The scanner's IP address should always be 192.168.2.1. To check the IP address on Ubuntu, type: ```ifconfig``` and to check on Mac, type: ```ipconfig```.
3) Have the MR tech connect the scanner to the neurofeedback laptop's samba share. From File Explorer, right-click on This PC, then select Add A Network Location. Follow the directions to enter the samba share address: //192.168.2.5/sambashare. When it asks for credentials, click on guest.
• After it is set up once, you should be able to click on it in the left sidebar, but you may have to go through this setup again if it gets deleted from the scanner console. 

## Set up stimulus presentation
1) Once you plug the laptop into the LCD monitor, you should be able to use the laptop screen while projecting the stimuli onto the LCD. However, this has posed some problems. If it does, set your display to 'mirror'. The script should work now, but the participant will be able to see anything you are seeing on the laptop screen.

# Scanning Protocol
### Sequence of Events: Task-Based Scans
![Picture1](https://github.com/bchcohenlab/rt-fMRI_Neurofeedback_of_ADHD/assets/88854051/2569af92-8cf1-4a7e-9022-3bb343de786e)

1) The first task-based scan is the multi-source interference task (MSIT). The stimuli for this task will be presented using PsychoPy.
To start the task:
``` 
conda activate rtcloud
psychopy #start the task from the GUI
```
2) After the MSIT is a resting-state scan. During this time, run the MSIT ACC localizer script on the neurofeedback laptop:
 - Start by running converting the DICOMs to nifti:
   ```
   dcm2niix /home/rt/sambashare/{DICOM directory}
   ```
 - Then type the following command to run the localizer script on this data.   
   ```
   python3 msit_acc_localizer.py {subject id}
   ```
 - Before moving on, it is a good idea to check that the mask looks okay. Pull up the new mask in FSLeyes with the functional data as the background.
   
** Note: The MSIT will be repeated at the end, but you don't need to run this script the second time. 

3) Neurofeedback scans (described below) 

## Starting a Neurofeedback Session
1) Neurofeedback laptop: ``` sudo smbd nmbd start ```

2) Start DATA_ANALYSER on neurofeedback laptop:
   - The neurofeedback laptop has an alias set up to run this step, so you should only have to type ```analyse```. However, if this command doesn't work, type:
   ``` 
   PROJ_DIR=/home/rt/rtcloud-projects/adhd_rt/
   docker run -it –rm –link-local-ip=192.168.2.5 -p 8888:8888 -v ~/certs:/rtcloud/certs -v $PROJ_DIR:/rt-cloud/projects/adhd_rt brainiak/rtcloud:latest scripts/data_analyser.sh -p  
   adhd_rt –subjectRemote –dataRemote
   ```
• This should pop up a link that you can click on, which will bring you to the login page. Enter username and password, then, in the second tab, click "initialize session". 

4) Start ANALYSIS_LISTENER on PsychoPy laptop:
  ```
  WEB_IP=192.168.2.5
  conda activate rtcloud
  cd rt-cloud/
  bash scripts/analysis_listener.sh -s $WEB_IP:8888 -u rt
  ```

5) Start PsychoPy on Macbook:
• In a new terminal:
  ```
  conda activate rtcloud
  psychopy
  ```
•	Run the rt_feedback_single_roi.py script from the GUI. This script will begin as soon as it receives the first pulse from the scanner, and it should begin sending feedback as soon as it receives a json file with the neurofeedback score. 

6) Click 'run' in the web interface on the neurofeedback laptop. The script will start when it sees the first DICOM image.

7) After all 3 runs are finished for the session, click "finalize session" in the web browser.

