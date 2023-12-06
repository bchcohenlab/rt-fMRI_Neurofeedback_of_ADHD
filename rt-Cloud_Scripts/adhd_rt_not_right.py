
"""-----------------------------------------------------------------------------
--- IMAGING SEQUENCE -- 2 BROOKLINE PLACE, BCH---
Scanning was acquired with a 3T Siemens Prisma MRI scanner. 

--- STUDY DESIGN ---
Each session begins with the Multi Scale Interference Task (MSIT), a measure of 
sustained attention, which serves both as a baseline for the participation's
neural activity and behavior and as a localizer for the anterior cingulate
cortex (ACC). Each of the two feedback runs included in this project contains 
5 blocks alternating rest and neurofeedback: (1) rest, (2) neurofeedback, 
(3) rest, (4) neurofeedback, (5) rest. During rest blocks, participants view 
a fixation cross, and during the neurofeedback blocks, they try to move a white 
ball on the screen into a target circle. The better they pay attention, and the
greater the activity in the ACC (compared to a predicted value), the closer the ball
gets to the circle. If they can keep the ball in the circle for 5 seconds, the ball
resets to its starting position and the target circle shrinks, making the task 
more challenging. Participants are not given explicit instructions or strategies 
for increasing their attention, but rather are encouraged to identify a strategy
that works best for them. After the second run, participants complete the MSIT once
more to evaluate neural and behavioral changes within the session. After each session,
participants are asked to list the attention strategies they used and to evaluate
the efficacy of each.

--- REAL-TIME PROCESSING PIPELINE ---

PRIOR To START OF SCAN: Task instruction. Scan starts once participant hits
a button to continue.
PRIOR TO FIRST REST BLOCK: 
- load MNI ACC mask
- 10 discarded TRs (disdaqs)

REST BLOCK PIPELINE (first and third blocks):
TRs 1-19 and 160-179:
    1. Transform DICOM to Nifti 
    2. Concatenate all TRs
    3. Generate average baseline image from TR list
    4. Resample ACC mask to the average baseline image 
    (converting it to subject space)
    5. Create and fit masker with subject space ACC mask
    
REST BLOCK PIPELINE (fifth block):
TRs 300-319:
    1. Transform DICOM to Nifti
    2. Skull strip Nifti
    3. Motion correct Nifti
    4. Concatenate all TRs
    5. Generate average baseline image
    
NEUROFEEDBACK BLOCK PIPELINE (second and fourth blocks):
TRs 20-159 and 180-299:
    1. Create GLM with smoothing, hemodynamic response function,
       slice timing reference, and ACC mask.
    2. Transform DICOM to Nifti 
    3. Concatenate Nifti to list of TRs (which starts 
       with the average baseline of the preceding rest block)
    4. Fit GLM to the concatenated list
    5. Calculate real and predicted activation values for 
       the list of TRs using masker.fit_transform()
    6. Take the average of real and predicted values (this is
       the neurofeedback score)
    7. Create a JSON file with this score and send it to the
       presentation laptop

-----------------------------------------------------------------------------"""

"""-----------------------------------------------------------------------------
The below portion of code simply imports modules and sets up path directories.
-----------------------------------------------------------------------------"""
# Importing modules and setting up path directories
import os
import sys
import numpy as np
import pandas as pd
import nibabel as nib
import argparse
from subprocess import call, Popen
import tempfile
from pathlib import Path
from datetime import datetime
    
from nilearn import image, masking
from nilearn.maskers import NiftiMasker
from nilearn.glm.first_level import FirstLevelModel
from nilearn.image import high_variance_confounds

sys.path.append('/home/rt/rt-cloud/rtCommon/')
sys.path.append('/home/rt/rt-cloud/')
sys.path.append('/home/rt/rt-cloud/tests/')

tmpPath = tempfile.gettempdir() # specify directory for temporary files
currPath = os.path.dirname(os.path.realpath(__file__)) #'.../rt-cloud/projects/project_name'
rootPath = os.path.dirname(os.path.dirname(currPath)) #'.../rt-cloud' 
dicomParentPath = '/home/rt/sambashare/' #.../rt-cloud/projects/project_name/dicomDir/
outPath = rootPath+'/outDir' #'.../rt-cloud/outDir/'

directories = []
for entry in os.scandir(dicomParentPath):
    if entry.is_dir():
        directories.append(entry.path)

# Looks for the most recently created directory
latest_directory = max(directories, key=os.path.getctime)

dicomPath = os.path.join(dicomParentPath, latest_directory)
print("Location of subject's dicoms: \n" + dicomPath + "\n")

# add the path for the root directory to your python path
sys.path.append(rootPath)

# import rtCommon modules
from rtCommon.utils import loadConfigFile, stringPartialFormat, findNewestFile
from rtCommon.clientInterface import ClientInterface
from rtCommon.bidsArchive import BidsArchive
from rtCommon.bidsRun import BidsRun
from bidsInterface import BidsInterface
from bidsArchive import BidsArchive

BidsInterface = BidsInterface()
archive = BidsArchive('/home/rt/rt-cloud/projects/adhd_rt/dicomBidsStream')
BidsInterface.allowedDirs = dicomPath

defaultConfig = os.path.join(currPath, f'conf/{Path(__file__).stem}.toml')
argParser = argparse.ArgumentParser()
argParser.add_argument('--config', '-c', default=defaultConfig, type=str,
                        help='experiment config file (.json or .toml)')
args = argParser.parse_args(None)
cfg = loadConfigFile(args.config)

print(f"\n----Starting project: {cfg.title}----\n")
# Load variables from config file
# Prep starting run and scan number 
# These are 1-indexed because that's how the DICOM file names are written
# Note: cfg variables altered in web interface will be strings!
startRun = int(cfg.runNum[0])
startBlock = 1
numRuns = int(cfg.numRuns)
num_TRs_per_run = int(cfg.num_total_TRs)
num_TRs_per_block = int(cfg.num_TRs_per_block)
rest_onset_TR = 1
nf_onset_TR = int(cfg.nf_onset_TR)
numBlocks = int(cfg.numBlocks)
disdaqs = cfg.disdaqs # num volumes at start of run to discard for MRI to reach steady state
origScanNamePattern = cfg.origScanNamePattern
sub_id = cfg.subjectNum

# Load experimental design for participant. To start, only the initial rest block is included. The design matrix will be updated after each TR after the first block. 
dict = {'trial_type': ['rest'], 'onset': [1], 'duration': [19]}
design = pd.DataFrame(dict)
    
# If skipping localizer, load ACC template mask for analysis
#acc_mask = currPath+'/template_masks/acc_mni_bin.nii.gz'

# If using MSIT localizer, load ACC mask in subject space 
acc_mask = currPath+'subjects'+f'sub-{sub_id}'+'acc_mask_subj_space.nii.gz'
"""-----------------------------------------------------------------------------
The below section initiates the clientInterface that enables communication 
between the three RTCloud components, which may be running on different 
machines.
-----------------------------------------------------------------------------"""
# Initialize the remote procedure call (RPC) for the data_analyser
# (aka projectInferface). This will give us a dataInterface for retrieving 
# files, a subjectInterface for giving feedback, a webInterface
# for updating what is displayed on the experimenter's webpage,
# and enable BIDS functionality
clientInterfaces = ClientInterface()
dataInterface = clientInterfaces.dataInterface
subjInterface = clientInterfaces.subjInterface
webInterface  = clientInterfaces.webInterface
bidsInterface = clientInterfaces.bidsInterface

"""====================REAL-TIME ANALYSIS GOES BELOW===================="""

# clear existing web browser plots if there are any
try:
    webInterface.clearAllPlots()
except:
    pass

# VNC Viewer: if on cloud server, use VNC to show GUIs in web interface (cannot use "--test" mode)
Popen("DISPLAY=:1 fsleyes",shell=True) 

class ImageProcessor:
    def __init__(self):
        self.dicomPath = dicomPath
        self.tmpPath = tmpPath
    
    def rename_file(self, dicom_path):
        current_file = findNewestFile(dicomPath, origScanNamePattern) 
        new_filename = f"001_{curRun:06d}_{TR:06d}.dcm"
        source_file = os.path.join(dicomPath, current_file)
        dest_file = os.path.join(dicom_path, new_filename)
        os.rename(current_file, dest_file)
        
    def image_prep(self, TR, streamID):
        currentBidsRun.appendIncremental(bidsIncremental)
        niftiObject = bidsIncremental.image
        single_tr_data = niftiObject.get_fdata()
        return single_tr_data, niftiObject
    
    def get_bl_results(self, nifti, img_data):
        bl_imgs.append(img_data)
        bl_concat_data = np.concatenate(bl_imgs, axis=3)
        bl_concat_nifti = image.new_img_like(nifti, bl_concat_data)
        print(bl_concat_data.shape) # check to make sure the images are being appended properly
        return bl_concat_data, bl_concat_nifti
    
    def incremental_GLM(self, TR,  design_matrix, img_data, baseline, mask_subj_space, previous_nii_data):
        masker = NiftiMasker(
            mask_img=mask_subj_space,
            smoothing_fwhm=None,
            high_variance_confounds=True, # regress out things like WM and CSF
        )
        masker.fit()
        concatenated_data = np.concatenate([previous_nii_data, img_data], axis=3)
        concatenated_nifti = image.new_img_like(mask_subj_space, concatenated_data)
        print(concatenated_nifti.shape) # check to make sure the images are being appended properly
        confounds = pd.DataFrame(high_variance_confounds(concatenated_nifti, percentile=1)) # regress out things like WM and CSF
        fmri_glm = FirstLevelModel(
            t_r=1.06,
            hrf_model='spm + derivative',
            mask_img=masker,
            smoothing_fwhm=6,
            high_pass=1/240, 
            noise_model='ols',
            verbose=3,
            n_jobs=-2,
            signal_scaling=False,
            minimize_memory=False,
        )
        fmri_glm.fit(concatenated_nifti, design_matrix, confounds=confounds)
        current_resid = masker.fit_transform(fmri_glm.residuals[-1]) # residual for all voxels
        current_resid_mean = current_resid.mean() # residual across entire ACC
        resid_list.append(current_resid_mean)
        nf_score_raw = np.mean(resid_list)
        nf_scores.append(nf_score_raw)
        min_score = np.min(nf_scores)
        max_score = np.max(nf_scores)
        if nf_score_raw < min_score:
            min_score = nf_score_raw 
        elif nf_score_raw > max_score:
            max_score = nf_score_raw
        nf_score_norm = ((nf_score_raw - min_score) / (max_score - min_score)) * 2 - 1 # norm nf_score_raw so that it is between -1 and 1
        print(f'Raw nf score at TR {TR}: {nf_score_raw}')
        print(f'Final NF score at TR {TR}: {nf_score_norm}')       
        webInterface.plotDataPoint(runId=curRun,trId=TR, value=nf_score_norm) #plot data point on web
        # Send the model outputs back to the computer running analysis_listener. 
        subjInterface.setResultDict(name=f'run{curRun}_TR{TR}',
                        values={'values': str(nf_score_norm)})
        return concatenated_nifti, concatenated_data

bl_imgs = []
nf_scores = []
resid_list = []
for curRun in range(startRun,numRuns):
    # prep stream of DICOMS -> BIDS 
    # "anonymize" removes participant specific fields from each DICOM header.
    if cfg.dsAccessionNumber=='None': 
        dicomScanNamePattern = stringPartialFormat(cfg.dicomNamePattern, 'RUN', curRun)
        streamId = bidsInterface.initDicomBidsStream(dicomPath,dicomScanNamePattern,
                                                    cfg.minExpectedDicomSize, 
                                                    anonymize=True,
                                                     **{'subject':cfg.subjectNum,
                                                     'run':curRun,
                                                     'task':cfg.taskName}
                                                    )
    else:
        # For OpenNeuro replay, initialize a BIDS stream using the dataset's Accession Number
        streamId = bidsInterface.initOpenNeuroStream(cfg.dsAccessionNumber,
                                                        **{'subject':cfg.subjectNum,
                                                        'run':f"0{curRun}",
                                                        'task':cfg.taskName})

    # prep BIDS-Run, which will store each BIDS-Incremental in the current run
    currentBidsRun = BidsRun()

    # reset the first x-axis plot location for Data Plot
    point_idx=-1 
    
    for curBlock in range(startBlock, numBlocks):
        
        for TR in range(1,num_TRs_per_block+1):
            print(f'--- Run {curRun} | Block {curBlock} | TR {TR} ---')
            processor = ImageProcessor()
            current_img = processor.rename_file(dicomPath)
            
            bidsIncremental = bidsInterface.getIncremental(streamId=streamId,volIdx=TR,
                    demoStep=cfg.demoStep)
            
            preprocessed_data, preprocessed_img = processor.image_prep(current_img, streamId)
            
            # rest block
            if rest_onset_TR<=TR<nf_onset_TR:
                bl_data, bl_nifti = processor.get_bl_results(preprocessed_img, preprocessed_data)
                # Make sure mask is in same space as baseline images (you should be able to skip this if using a subject-space mask to begin with)
                if TR==nf_onset_TR-1:
                    acc_mask_subj_space = image.resample_to_img(acc_mask, bl_nifti, interpolation='nearest') 
                
            # neurofeedback block
            elif nf_onset_TR<=TR:
                if nf_onset_TR == TR:
                    design.loc[1] = ['nf', nf_onset_TR, 1] # adds new row to design data frame
                    nf_design_matrix = design
                    concatenated_nifti, concatenated_data = processor.incremental_GLM(TR, nf_design_matrix, preprocessed_data, bl_data, acc_mask_subj_space, previous_nii_data=bl_data)
                else:
                    design.at[1, 'duration'] = TR - num_rest_TRs # updates duration value to match current TR
                    nf_design_matrix = design
                    concatenated_nifti, concatenated_data = processor.incremental_GLM(TR, nf_design_matrix, preprocessed_data, bl_data, acc_mask_subj_space, previous_nii_data=concatenated_data)
                    
                if TR==nf_onset_TR:
                    concatenated_nifti, concatenated_data = processor.incremental_GLM(TR, nf_design_matrix, preprocessed_data, bl_data, acc_mask_subj_space, previous_nii_data=bl_data)
                else:
                    concatenated_nifti, concatenated_data = processor.incremental_GLM(TR, nf_design_matrix, preprocessed_data, bl_data, acc_mask_subj_space, previous_nii_data=concatenated_data)
        
    print(f"==END OF RUN {curRun}!==\n")
    archive.appendBidsRun(currentBidsRun)
    bidsInterface.closeStream(streamId)

print("-----------------------------------------------------------------------\n"
"REAL-TIME EXPERIMENT COMPLETE!\n"
"-----------------------------------------------------------------------")
sys.exit(0)

"""-----------------------------------------------------------------------------
Additional note: you can create an "initialize.py" and/or "finalize.py" file, which
are scripts that can run by clicking the respective buttons on the RT-Cloud web 
browser (under the Session tab). This can be helpful when needing to run specific 
code at the beginning or end of your experiment.
-----------------------------------------------------------------------------"""
