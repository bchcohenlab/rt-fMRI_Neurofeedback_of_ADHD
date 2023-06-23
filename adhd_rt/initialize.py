"""-----------------------------------------------------------------------------

initialize.py (Last Updated: 01/26/2021)

The purpose of this script is to initialize the rt-cloud session. Specifically,
it will initiate any variables that need to be initiated (e.g., configuration
file) and upload any necessary files to the cloud.

-----------------------------------------------------------------------------"""

# print a short introduction on the internet window
print(""
    "-----------------------------------------------------------------------------\n"
    "This script initializes the rt-cloud session. Specifically,\n"
    "it will initiate the configuration file, load the ACC mask,\n"
    "and create subject and session directories.\n"
    "-----------------------------------------------------------------------------")

import os
import sys
import time
import pandas as pd
import argparse
import struct
import logging
import argparse

# obtain full path for current directory: '.../rt-cloud/projects/adhd_rt/'
currPath = os.path.dirname(os.path.realpath(__file__))
# obtain full path for root directory: '.../rt-cloud'
rootPath = os.path.dirname(os.path.dirname(currPath))

# add the path for the root directory to your python path so that you can import
#   project modules from rt-cloud
sys.path.append(rootPath)
# import project modules from rt-cloud
import rtCommon.utils as utils
from rtCommon.clientInterface import ClientInterface
from rtCommon.dataInterface import uploadFilesToCloud, uploadFolderToCloud, uploadFilesFromList

# obtain the full path for the configuration toml file
defaultConfig = os.path.join(currPath, 'conf/adhd_rt.toml')

def initialize(cfg, dataInterface):
    """ purpose: load information and add to config """
    """
    This function is called by 'main()' below. Here, we will do a demo of the
    types of things you can do in this 'initialize.py' script. For instance,
    let's say that you need to upload mask files that you are planning to
    use during your real-time experiment or a registration file that is integral
    for the analysis of your task. The point of this script is to upload files
    to the cloud that you will need for your entire scanning session.

    In this demo, we will show how you can move files (e.g., such as those 
    needed for registration) from the local (non-cloud) stimulus computer to the 
    cloud directory. Here, everything will be on the same computer but in different 
    folders to show how this will happen when you run your own experiment!

    INPUT:
        [1] cfg (configuration file with important variables)
        [2] dataInterface (this will allow a script from the cloud to access files 
                   from the stimulus computer)
    OUTPUT:
        None.
    """
        # before we get ahead of ourselves, we need to make sure that the necessary file
    #   types are allowed (meaning, we are able to read them in)... in this example,
    #   at the very least we need to have access to dicom and txt file types.
    #   INPUT: None
    #   OUTPUT:
    #       [1] allowedFileTypes (list of allowed file types)
    
    allowedFileTypes = dataInterface.getAllowedFileTypes()
    #print(""
    "-----------------------------------------------------------------------------\n"
    "Before continuing, we should check to see the file types that are allowed.\n"
    "To verify, we will use 'allowedFileTypes'. Only these files will be uploaded\n"
    "to the cloud in the next step!! If you need to add a file type that is missing\n"
    "here, you will have to stop and restart the fileServer on the stimulus computer\n"
    "specifying the necessary file types in the command line parameters.\n"
    "Allowed file types: %s"# %allowedFileTypes)" "
    
    if cfg.sessionId in (None, '') or cfg.useSessionTimestamp is True:
        cfg.useSessionTimestamp = True
        cfg.sessionId = utils.dateStr30(time.localtime())
    else:
        cfg.useSessionTimeStamp = False
        
    # get DICOM directory
    if cfg.buildImgPath:
        imgDirDate = datetime.now()
        dateStr = cfg.date.lower()
        if dateStr != 'now' and dateStr != 'today':
            try:
                imgDirDate = parser.parse(cfg.date)
            except ValueError as err:
                raise RequestError('Unable to parse date string {} {}'.format(cfg.date, err))
        datestr = imgDirDate.strftime("%Y%m%d")
        imgDirName = "{}.{}".format(datestr, cfg.subjectName)
        cfg.dicomDir = os.path.join(cfg.dicomDir,imgDirName)
    else:
        cfg.dicomDir = cfg.dicomDir # then the whole path was supplied
    
    cfg.bids_id = 'sub-{0:03d}'.format(cfg.subjectNum)
    cfg.ses_id = 'ses-{0:02d}'.format(cfg.subjectDay)
    
    # make local directories
    print(cfg.rtcloudDir)
    cfg.projectDir = os.path.join(cfg.rtcloudDir, 'projects', cfg.projectName)
    if not os.path.exists(cfg.projectDir):
        os.makedirs(cfg.projectDir)
    cfg.subjectDir = os.path.join(cfg.projectDir, 'subjects', cfg.bids_id)
    if not os.path.exists(cfg.subjectDir):
        os.makedirs(cfg.subjectDir)
    cfg.sesDir = os.path.join(cfg.subjectDir, cfg.ses_id)
    if not os.path.exists(cfg.sesDir):
        os.makedirs(cfg.sesDir)
    cfg.logDir = os.path.join(cfg.sesDir, 'log')
    if not os.path.exists(cfg.logDir):
        os.makedirs(cfg.logDir) 
    cfg.imgDir = os.path.join(cfg.sesDir, 'img')
    if not os.path.exists(cfg.imgDir):
        os.makedirs(cfg.imgDir)
    cfg.maskDir = os.path.join(cfg.sesDir, 'mask')
    if not os.path.exists(cfg.maskDir):
        os.makedirs(cfg.maskDir)
    cfg.localizerDir = os.path.join(cfg.sesDir, 'ses-localizer', 'func')
    if not os.path.exists(cfg.localizerDir):
        os.makedirs(cfg.localizerDir)
    cfg.nfDir = os.path.join(cfg.sesDir, 'real_NF', 'func')
    if not os.path.exists(cfg.nfDir):
        os.makedirs(cfg.nfDir)
    cfg.shamDir = os.path.join(cfg.sesDir, 'sham_NF', 'func')
    if not os.path.exists(cfg.shamDir):
        os.makedirs(cfg.shamDir)
    cfg.restDir = os.path.join(cfg.sesDir, 'rest')
    if not os.path.exists(cfg.restDir):
        os.makedirs(cfg.restDir)
    print("Created all directories for participant {}".format(cfg.bids_id))
        
    # copy mask files to registration directory
    #import shutil

    # Load the source and destination paths from the TOML configuration file
    # Use the shutil module's copytree function to copy the folder from the source to destination path
    
    #shutil.copytree(cfg.projectDir, cfg.maskDir)

    os.system(f'cp {cfg.projectDir}/template_masks/acc_mni_bin.nii.gz {cfg.maskDir}')
    print("Copied MNI masks to subject folder")
        
    # get conversion to flip dicom to nifti files
    ##cfg.axesTransform = getTransform(('L', 'A', 'S'),('P', 'L', 'S'))
    
    cfg.acc_mask_mni = os.path.join(cfg.maskDir, 'acc_mni_bin.nii.gz')
    cfg.run_design = pd.read_csv(currPath+'/study_design/events.csv')
    
    return cfg


####################################################################################
# from initialize import *
# defaultConfig = 'conf/amygActivation.toml'
# args = StructDict({'config':defaultConfig, 'runs': '1', 'scans': '9'})
####################################################################################

def main(argv=None):
    """
    This is the main function that is called when you run 'intialize.py'.

    Here, you will load the configuration settings specified in the toml configuration 
    file, initiate the class dataInterface, and set up some directories and other 
    important things through 'initialize()'
    """

    # define the parameters that will be recognized later on to set up fileIterface
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--config', '-c', default=defaultConfig, type=str,
                            help='experiment config file (.json or .toml)')
    argParser.add_argument('--runs', '-r', default='', type=str,
                        help='Comma separated list of run numbers')
    argParser.add_argument('--scans', '-s', default='', type=str,
                        help='Comma separated list of scan number')
    args = argParser.parse_args(argv)

    print('Initializing directories and configurations')

    # establish the RPC connection to the projectInterface
    clientInterface = ClientInterface()
    dataInterface = clientInterface.dataInterface
    args.dataRemote = clientInterface.isDataRemote()

    # load the experiment configuration file
    cfg = utils.loadConfigFile(args.config)
    #cfg = initialize(cfg, args)
    initialize(cfg, clientInterface.dataInterface)
    
    return 0

    print(""
    "-----------------------------------------------------------------------------\n"
    "INITIALIZATION COMPLETE!")


# def main(argv=None):
    """
    This is the main function that is called when you run 'intialize.py'.
    
    Here, you will load the configuration settings specified in the toml configuration 
    file, initiate the class dataInterface, and set up some directories and other 
    important things through 'initialize()'
    """

    # define the parameters that will be recognized later on to set up fileIterface
    # argParser = argparse.ArgumentParser()
    # argParser.add_argument('--config', '-c', default=defaultConfig, type=str,
                        #    help='experiment config file (.json or .toml)')
    # args = argParser.parse_args(argv)

    # load the experiment configuration file
    # cfg = utils.loadConfigFile(args.config)

    # establish the RPC connection to the projectInterface
    # clientInterface = ClientInterface()

    # now that we have the necessary variables, call the function 'initialize' in
    #   order to actually start reading dicoms and doing your analyses of interest!
    #   INPUT:
    #       [1] cfg (configuration file with important variables)
    #       [2] dataInterface (this will allow a script from the cloud to access files 
    #               from the stimulus computer)
    # initialize(cfg, clientInterface.dataInterface)
    # return 0


if __name__ == "__main__":
    """
    If 'initalize.py' is invoked as a program, then actually go through all of the 
    portions of this script. This statement is not satisfied if functions are called 
    from another script using "from initalize.py import FUNCTION"
    """
    main()
    sys.exit(0)
