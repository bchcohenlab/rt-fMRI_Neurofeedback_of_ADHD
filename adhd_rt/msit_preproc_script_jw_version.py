import os
import sys
from numpy import array
import pandas as pd
from nilearn import image, masking
from nilearn.glm.first_level import FirstLevelModel
import tempfile
import nibabel as nib 

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

directories = []
for entry in os.scandir(dicomParentPath):
    if entry.is_dir():
        directories.append(entry.path)
        
latest_directory = max(directories, key=os.path.getctime)

dicomPath = os.path.join(dicomParentPath, latest_directory)
print("Location of subject's dicoms: \n" + dicomPath + "\n")

# add the path for the root directory to your python path
sys.path.append(rootPath)

# archive = BidsArchive(tmpPath+'/bidsDataset')
subjID = sys.argv[1]
print(f"\n----Starting MSIT----\n")

# load ACC template mask and subject's functional data for analysis
acc_mask = currPath+'/template_masks/acc_mni_bin.nii.gz'
subj_data_func = image.load_img(os.path.join(dicomPath, '*.nii'))

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

conditions = {
    'Control': array([1., -1., 0.]),
    'Interference': array([-1., 1., 0.])
}

# Looking for significantly greater activation during interference condition than control.
inter_minus_con = conditions['Interference'] - conditions['Control']

z_map = fmri_glm.compute_contrast(inter_minus_con, output_type='z_score')

z_map_bin = image.binarize_img(z_map)

# Save to current subject's folder
nib.save(z_map_bin, os.path.join(currPath, 'subjects', subjID, 'acc_mask_subj_space.nii.gz'))
