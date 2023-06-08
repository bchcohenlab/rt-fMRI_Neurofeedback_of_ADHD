# rt-fMRI Neurofeedback of ADHD
This manual describes the study protocol for neurofeedback on sustained attention in ADHD, conducted by Alexander Cohen's Lab of Translational Neuroimaging at Boston Children's Hospital. This study uses the rt-Cloud platform (https://github.com/brainiak/rt-cloud) and adapts stimulus presentation scripts from the multivariate and univariate real-time functional imaging (MURFI) program (https://github.com/cccbauer/MURFI-user-manual). 

 ![image](https://github.com/bchcohenlab/rt-fMRI_Neurofeedback_of_ADHD/assets/88854051/9b52c9eb-fd11-426f-ae58-616507b126d1)

**Initial Setup**

Source Documentation: https://rt-cloud.readthedocs.io/en/latest/index.html
**Note: every year security certificates expire on January 1. To share the renewed version with other machines, connect via ethernet cable and adapt the following code to your machine: scp -r certs username@ip.address:/certificates/folder
  •	 May need to edit permissions in web browser
    • Firefox instructions: https://support.mozilla.org/en-US/kb/Certificate-contains-the-same-serial-number-as-another-certificate
    • Chrome: settings → privacy and security → manage certificates → authorities → import → import 1000.pem
    •	If you get errors with certificate permissions, you can run your commands with the --test flag
        • Instead of logging in using the username rt, use "test" with password "test"


**Neurofeedback Components**

DATA_STREAMER: runs on machine that receives/sends DICOMs  (i.e., the MRI console)
•	Watches for new DICOM brain images and sends them to the machine analyzing the data

DATA_ANALYSER: runs on machine that analyses data in real-time (i.e., the Dell laptop)
•	Runs experimenter’s script to process DICOMs
•	Provides a web-based user interface for experimenter control

ANALYSIS_LISTENER: runs on machine that runs presentation software (i.e., personal laptop)
•	Listens for results from DATA_ANALYSER to inform experiment presentation (i.e., from PsychoPy)

**Starting a Neurofeedback Session**
1) Neurofeedback laptop: ``` sudo smbd nmbd start ```
3) Personal laptop (Mac): Finder → Go → Connect to server → type “smb://192.168.2.5/rtsambashare” and connect → click “guest”

 • shortcut: cmd + k 
 
 • since we are using an ethernet cord, the IP address shouldn’t change, but if you can’t connect, make sure you have the correct IP address by typing ifconfig on the Dell laptop
3) Start DATA_ANALYSER on Dell: 
  ``` 
  PROJ_DIR=/home/rt/rtcloud-projects/adhd_rt/
  docker run -it –rm –link-local-ip=192.168.2.5 -p 8888:8888 -v ~/certs:/rtcloud/certs -v $PROJ_DIR:/rt-cloud/projects/adhd_rt brainiak/rtcloud:latest scripts/data_analyser.sh -p  
  adhd_rt –subjectRemote –dataRemote
  ```
4) Start ANALYSIS_LISTENER on Macbook:
  ```
  WEB_IP=192.168.2.5
  conda activate rtcloud
  cd rt-cloud/
  bash scripts/analysis_listener.sh -s $WEB_IP:8888 -u rt
  ```
5) Start PsychoPy on Macbook:
• In a new terminal:
  ```
  Conda activate rtcloud
  psychopy
  ```
  •	run script from GUI

