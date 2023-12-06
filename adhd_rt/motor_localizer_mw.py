import nibabel as nib
import numpy as np

def create_peak_activation_mask(functional_file, motor_mask_file, percentile_threshold=90):
    # Load functional and motor mask NIfTI files
    functional_img = nib.load(functional_file)
    motor_mask_img = nib.load(motor_mask_file)

    # Get data arrays from the images
    functional_data = functional_img.get_fdata()
    motor_mask_data = motor_mask_img.get_fdata()

    # Apply the motor mask to the functional data
    masked_data = functional_data * motor_mask_data

    # Get the activation values within the mask
    activation_values = masked_data[motor_mask_data > 0]

    # Calculate the intensity threshold based on the given percentile
    intensity_threshold = np.percentile(activation_values, percentile_threshold)

    # Create a binary mask where points above the intensity threshold are set to 1
    peak_activation_mask = np.zeros_like(masked_data)
    peak_activation_mask[masked_data > intensity_threshold] = 1

    # Save the binary mask as a NIfTI file
    peak_activation_mask_img = nib.Nifti1Image(peak_activation_mask, motor_mask_img.affine)
    nib.save(peak_activation_mask_img, 'peak_activation_mask.nii.gz')

# Example usage
functional_file = '/home/rt/rt-fMRI_Neurofeedback_of_ADHD/adhd_rt/registration_folder/P001_motor_mask_20231102111749/P001_skull_stripped_20231102111749_20231010.STEEBY_CLARA.6021246_func-bold_task-preMSIT_20231010131715_8.nii.gz'
motor_mask_file = '/home/rt/rt-fMRI_Neurofeedback_of_ADHD/adhd_rt/registration_folder/P001_motor_mask_20231102111749/P001_final_registered_bin_mask_20231102111749.nii.gz'
percentile_threshold = 60  # Specify the percentile threshold here

create_peak_activation_mask(functional_file, motor_mask_file, percentile_threshold)




