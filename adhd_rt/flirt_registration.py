import os
import subprocess
from datetime import datetime
def create_output_directory(directory):
    try:
        os.makedirs(directory)
        print("---------------------------------------------")
        print(f"Directory '{directory}' created successfully.")
        print("---------------------------------------------")
    except FileExistsError:
        print("---------------------------------------")
        print(f"Directory '{directory}' already exists.")
        print("---------------------------------------")

def choose_subdirectory_from_directory(directory):
    print("Directories in Sambashare:")
    subdirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    for i, subdirectory in enumerate(subdirectories):
        print(f"{i + 1}. {subdirectory}")
    
    while True:
        try:
            choice = int(input("Enter the number of the DICOM Directory you want to use: "))
            if 1 <= choice <= len(subdirectories):
                return os.path.join(directory, subdirectories[choice - 1])
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def choose_nifti_file_from_directory(directory):
    print("Files in the directory:")
    files = os.listdir(directory)
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    
    while True:
        try:
            choice = int(input("Enter the number of the Functional Nifti File you want to use: "))
            if 1 <= choice <= len(files):
                return os.path.join(directory, files[choice - 1])
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def choose_mask_file_from_directory(directory):
    print("Files in the directory:")
    files = os.listdir(directory)
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    
    while True:
        try:
            choice = int(input("Enter the number of the MNI-space Template Mask you want to use: "))
            if 1 <= choice <= len(files):
                return os.path.join(directory, files[choice - 1])
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def register_template_mask():
    
    output_directory = input("Enter the name of the output directory: ")
    output_directory_path = os.path.join('/home/rt/rt-fMRI_Neurofeedback_of_ADHD/adhd_rt/registration_folder', output_directory)
    create_output_directory(output_directory_path)

    subdirectory = choose_subdirectory_from_directory('/home/rt/sambashare')
    subdirectory_path = os.path.join('/home/rt/sambashare', subdirectory)
    subject_nifti_file = choose_nifti_file_from_directory(subdirectory_path)

    template_mask = choose_mask_file_from_directory('/home/rt/rt-fMRI_Neurofeedback_of_ADHD/adhd_rt/template_masks')

    subject_filename = os.path.basename(subject_nifti_file)

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    skull_stripped_subject_nifti_file = os.path.join(output_directory_path, f"skull_stripped_{current_datetime}_{subject_filename}")
    registered_mask_output = os.path.join(output_directory_path, f"template_mask_registered_{current_datetime}.nii.gz")
    registered_non_bin_mask_output = os.path.join(output_directory_path, f"registered_bin_mask_{current_datetime}.nii.gz")
    final_registered_bin_mask_output = os.path.join(output_directory_path, f"final_registered_bin_mask_{current_datetime}.nii.gz")


    # Step 1: Skull stripping
    subprocess.run(["bet", subject_nifti_file, skull_stripped_subject_nifti_file])

    # Step 2: FLIRT registration
    subprocess.run(["flirt", "-in", template_mask, "-ref", skull_stripped_subject_nifti_file, "-out", registered_mask_output, "-applyxfm", "-usesqform"])

    # Step 3: Apply the mask to the subject brain 
    subprocess.run(["fslmaths", skull_stripped_subject_nifti_file, "-mas", registered_mask_output, registered_non_bin_mask_output])

    # Step 4: Thresholding
    subprocess.run(["fslmaths", registered_non_bin_mask_output, "-thr", "0.5", "-bin", final_registered_bin_mask_output])

    print("Final registered binary mask created: ", final_registered_bin_mask_output)

# Call the function to execute the script
register_template_mask()
