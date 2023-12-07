#!/bin/bash

# Prompt the user for a keyword
read -p "Enter the keyword to search for in directory names: " keyword

# Check if the user provided a keyword
if [ -z "$keyword" ]; then
  echo "Keyword cannot be empty. Exiting."
  exit 1
fi

parent_directory="/home/rt/sambashare"

# Navigate to the parent directory
cd "$parent_directory" || exit

# List directories containing the specified keyword
matching_directories=($(find . -type d -name "*$keyword*" -printf "%P\n"))

if [ ${#matching_directories[@]} -eq 0 ]; then
  echo "No directories found containing the keyword '$keyword'. Exiting."
  exit 1
else
  echo "Directories containing the keyword '$keyword':"
  for i in "${!matching_directories[@]}"; do
    echo "$((i + 1)). ${matching_directories[$i]}"
  done
fi

# Prompt the user to select a subdirectory
read -p "Enter the number corresponding to the subdirectory you want to process: " choice

# Validate the user's choice
if ! [[ "$choice" =~ ^[1-9][0-9]*$ ]] || [ "$choice" -gt "${#matching_directories[@]}" ]; then
  echo "Invalid selection. Exiting."
  exit 1
fi

selected_subdirectory="${matching_directories[$((choice - 1))]}"

# Create an output directory within the selected subdirectory
output_directory="$selected_subdirectory/process_msit_output_$(date +'%Y%m%d_%H%M%S')"
mkdir -p "$output_directory"

# Run dcm2niix with the output directory
dcm2niix -o "$output_directory" "$selected_subdirectory"

echo "----------------------------------------------------------------------------------------------"
echo "dcm2niix completed. Output nifti and json files are in: /home/rt/sambashare/$output_directory"
echo "----------------------------------------------------------------------------------------------"


cd "/home/rt/sambashare/$output_directory" 
echo "Please Enter the Subjects ID: " 
read pid

output_filename=""

dcacheDirIn="/home/rt/sambashare/$output_directory"

for file in "$dcacheDirIn"/*_8.nii
do
  # Get the parent folder name (output directory name)
  parent_folder=$(basename "$output_directory")

  # Append the parent folder name to the output filename
  output_filename="${pid}_3d_func_slice_$(date +'%Y%m%d_%H%M%S')"

  # Run fslroi with the modified output filename
  fslroi "$file" "$output_filename" 0 -1 0 -1 0 -1 0 1 
done


echo "---------------------------------------------------------------------------------------------------------------------------"
echo "fslroi completed. 3d Functional Slice is named: $output_filename and is located in /home/rt/sambashare/$output_directory"
echo "---------------------------------------------------------------------------------------------------------------------------"

# Capture the fslinfo of the output_filename
output_filename_header=$(fslinfo "$output_filename")
 
# Use $output_filename_header as needed
echo "FSL information for $output_filename:"
echo "$output_filename_header"

echo "Use IP Address: 192.168.2.6 to send functional data to MacBook? (y/n)"
read -r ip_yorn

if [ "$ip_yorn" == "y" ]; then 
    ip_ad="192.168.2.6"
else
    echo "Please enter IP Address (type 'privip' on mac to get a suitable ip for transfer): "
    read -r ip_ad
fi

scp -v "/home/rt/sambashare/${output_directory}/${output_filename}.nii.gz" meghan@"${ip_ad}":/Users/meghan/neurofeedback/3d_func_slices/

echo " -----------------------------------------------" 
echo "$output_filename has been sent to: /Users/meghan/neurofeedback/3d_func_slices"
echo "-------------------------------------------------"
