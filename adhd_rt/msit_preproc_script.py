import os
import sys
from numpy import array
import pandas as pd
from nilearn import image, masking
from nilearn.glm.first_level import FirstLevelModel
import tempfile
import nibabel as nib 
import datetime #for generating timestamps
from nilearn import image
import numpy as np
sys.path.append('/home/rt/rt-cloud/rtCommon/')
sys.path.append('/home/rt/rt-cloud/')
sys.path.append('/home/rt/rt-cloud/tests/')

tmpPath = tempfile.gettempdir() # specify directory for temporary files
currPath = os.path.dirname(os.path.realpath(__file__)) #'.../rt-cloud/projects/project_name'
rootPath = os.path.dirname(os.path.dirname(currPath)) #'.../rt-cloud' 
dicomParentPath = '/home/rt/sambashare/' #.../rt-cloud/projects/project_name/dicomDir/
outPath = rootPath+'/outDir' #'.../rt-cloud/outDir/'

# Get the list of directories
directories = [d for d in os.listdir(dicomParentPath) if os.path.isdir(os.path.join(dicomParentPath, d))]

# Get the name of the latest directory
latest_directory = max(directories, key=lambda d: os.path.getctime(os.path.join(dicomParentPath, d)))

# Ask the user if they want to use the latest directory
use_latest = input(f"Do you want to use the latest directory '{latest_directory}'? (yes/no): ").strip().lower()

if use_latest == 'yes':
    dicomPath = os.path.join(dicomParentPath, latest_directory)
else:
    # Ask the user to choose a directory from the list
    print("List of Directories:")
    for index, directory in enumerate(directories):
        print(f"{index + 1}. {directory}")
    
    choice = int(input("Enter the number of the directory to analyze: "))
    selected_directory = directories[choice - 1]
    dicomPath = os.path.join(dicomParentPath, selected_directory)

print("Location of subject's dicoms: \n" + dicomPath + "\n")

# add the path for the root directory to your python path
sys.path.append(rootPath)

# archive = BidsArchive(tmpPath+'/bidsDataset')
subjID = sys.argv[1]
print(f"\n----Starting MSIT----\n")

# Check if dicomPath exists before using it
if not os.path.exists(dicomPath):
    print(f"Error: Dicom path does not exist: {dicomPath}")
    sys.exit(1)

# load ACC template mask and subject's functional data for analysis
acc_mask = currPath+'/template_masks/acc_mni_bin.nii.gz'

# Check if the ACC template mask file exists before using it
if not os.path.exists(acc_mask):
    print(f"Error: ACC template mask file not found: {acc_mask}")
    sys.exit(1)

subj_data_func = image.load_img(os.path.join(dicomPath, '*_8.nii'))
# Check if the subject's functional data file exists before using it
if not subj_data_func:
    print("Error: No functional data found.")
    sys.exit(1)

# skull strip subject's func data
subj_skull_stripped = masking.compute_brain_mask(subj_data_func)

# GLM
events = pd.read_table('/home/rt/rt-cloud/projects/adhd_rt/MSIT_Design.csv')

print("starting GLM")
fmri_glm = FirstLevelModel(t_r=1.06, 
                            standardize=False, 
                            signal_scaling=0, 
                            smoothing_fwhm=6, 
                            hrf_model=None, 
                            drift_model='cosine', 
                            high_pass=0.01,
                            mask_img=acc_mask)

fmri_glm = fmri_glm.fit(subj_data_func, events)

design_matrix = fmri_glm.design_matrices_[0]
design_matrix
num_conditions = design_matrix.shape[1]
print('Number of conditions in the design matrix:', num_conditions)

# old conditions array
#conditions = {
#    'Control': array([1., -1., 0.]),
#    'Interference': array([-1., 1., 0.])
#}

#mw 10/27
conditions = {"Control": np.zeros(num_conditions), "Interference": np.zeros(num_conditions)}

conditions["Control"][0] = 1
conditions["Control"][1] = -1
conditions["Interference"][0] = -1
conditions["Interference"][1] = 1

# Looking for significantly greater activation during interference condition than control.
inter_minus_con = conditions['Interference'] - conditions['Control']
print("Length of inter_minus_con:",len(inter_minus_con))

z_map = fmri_glm.compute_contrast(inter_minus_con, output_type='z_score')

z_map_bin = image.binarize_img(z_map)

# Save to current subject's folder

# Generate a unique filename based on timestamp and a random value
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
unique_filename = f'acc_mask_{timestamp}.nii.gz'

# Construct the directory path
output_dir = os.path.join(currPath, 'subjects', subjID)

# Ensure the directory exists or create it if it doesn't
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the NIfTI image with the unique filename in the subject's folder
output_file_path = os.path.join(output_dir, unique_filename)
nib.save(z_map_bin, output_file_path)

try:
    nib.save(z_map_bin, output_file_path)
    print(f"Z-map saved successfully: {output_file_path}")
except Exception as e:
    print(f"Error: Unable to save Z-map: {e}")


