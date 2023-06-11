# import necessary libraries
import sys  # for error handling
import os  # for file handling
import subprocess  # for running shell commands

# define paths
raw_data_folder = "data/raw"
convert_data_folder = "data/mzML_files"

# parse and convert raw data files to mzML using proteowizard
for file in os.listdir(raw_data_folder):
    if file.endswith(".d"): # check raw data file extension .d for bruker raw data
        # get file name
        file_name = file.split(".")[0]
        # define paths
        raw_file_path = os.path.join(raw_data_folder, file)
        convert_file_path = os.path.join(convert_data_folder, file_name + ".mzML")
        # convert raw file to mzML using proteowizard
        subprocess.run(["msconvert", raw_file_path, "-o", convert_data_folder, "--mzML", "--filter", "peakPicking true 1-"], 
                       shell=True)
    else:
        print("Error: No .d data files found in data/raw folder, check file extension and file path")
        sys.exit(1)
    
##############################################################################################################
# to do: install and config proteowizard to run msconvert from command line