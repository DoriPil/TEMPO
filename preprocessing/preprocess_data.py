import subprocess
import sys
import argparse


# Liste des chemins de données brutes et intermédiaires
stack_data_folder_clean=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\raw\clean"
stack_data_folder_contaminated=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\raw\contaminated"

focused_single_slice_folder_clean=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\focused_single_slice\clean"
focused_single_slice_folder_contaminated=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\focused_single_slice\contaminated"

depth_map_folder_clean=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\depth_map\clean"
depth_map_folder_contaminated=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\depth_map\contaminated"


data_folder=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data"
results_folder=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\results"

difference_images_folder=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\difference"
best_focus_images_folder_clean=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\best_focus\clean"
best_focus_images_folder_contaminated=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\best_focus\contaminated"

process_sharp=True
process_depth=False
process_difference=False

# Process in-focus images from stack (focused single slice)

if process_sharp:
    subprocess.run([sys.executable,
                r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\preprocessing\process_sharp.py",
                    "--dataPath",data_folder,
                    "--resultsPath",results_folder])



# Process depth maps from stack

if process_depth:
    subprocess.run([sys.executable,
                    r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\preprocessing\process_depth.py",
                    "--cleanDataPath",stack_data_folder_clean,
                    "--contaminatedDataPath",stack_data_folder_contaminated,
                    "--depthDataPathClean",depth_map_folder_clean,
                    "--depthDataPathContaminated",depth_map_folder_contaminated])



# Process difference images from stack

if process_difference:
    subprocess.run([sys.executable,
                    r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\preprocessing\process_difference.py",
                    "--dataPath",data_folder,
                    "--resultsPath",results_folder])