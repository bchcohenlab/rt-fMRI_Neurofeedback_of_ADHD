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
from nilearn.glm.first_level import FirstLevelModel

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

# load motor template mask and subject's functional data for analysis
motor_mask = currPath+'/template_masks/thr_Precentral_Gyrus_fsl_atlas.nii.gz'
subj_data_func = image.load_img(os.path.join(dicomPath, '*_8.nii'))

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
                            mask_img=motor_mask)

fmri_glm = fmri_glm.fit(subj_data_func, events)

conditions = {
    'Control': array([1., -1., 0.]),
    'Interference': array([-1., 1., 0.])
}

# Define the contrast vector for overall activation (combining Control and Interference conditions)
overall_contrast = array([1., 1., 1.])

# Compute the contrast for overall activation
z_map = fmri_glm.compute_contrast(overall_contrast, output_type='z_score')

# Define the threshold value for activation (if needed)
threshold = 2.5  # z-score based threshold value, you can adjust this

# Apply threshold to the z-score map
thresholded_z_map = image.math_img('z_map >= {}'.format(threshold), z_map=z_map)

# Binarize the thresholded z-score map
z_map_bin = image.math_img('img > 0', img=thresholded_z_map)

# Save to current subject's folder

# Generate a unique filename based on timestamp and a random value
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
unique_filename = f'motor_mask_{timestamp}.nii.gz'

# Construct the directory path
output_dir = os.path.join(currPath, 'subjects', subjID)

# Ensure the directory exists or create it if it doesn't
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the NIfTI image with the unique filename in the subject's folder
output_file_path = os.path.join(output_dir, unique_filename)
nib.save(z_map_bin, output_file_path)

print("Length of conditions['Control']:", len(conditions['Control']))

