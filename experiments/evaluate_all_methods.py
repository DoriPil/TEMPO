import subprocess
import sys
import os

# Path to data and results folders
benchmark_folder=r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO" # Modifier ce chemin pour rendre compatible avec votre machine
results_folder=os.path.join(benchmark_folder,'results')

ground_truth_path=os.path.join(benchmark_folder,r'results\best_focus_method\registered_ground_truth')
masks_path=os.path.join(benchmark_folder,r'results\best_focus_method\automatic_segmentation')
results_path=os.path.join(benchmark_folder,r'results\best_focus_method')

annotations_path=r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\data\multi_focus\manual_annotations_independant\raw'
intern_ground_truth_path=r'C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\ground_truth'
intern_results_path=r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\intern_annotations'

# Booleans to choose which methods to evaluate
best_focus=False
compound_sharp=True
intern=False

# String to choose specific algorithm to evaluate
algorithm="ssim_difference" # Options: raw_difference, ssim_difference, gaussian_filter, median_filter, asf, h_maximas, reconstruction

# Evaluate the results obtained using best-focused images
if best_focus:
    subprocess.run([sys.executable, 
                    os.path.join(benchmark_folder,r'methods\best_focus_method\evaluate.py'),
                    "--resultsPath",results_folder,
                    "--algorithm",algorithm])
    
# Evaluate the results obtained using all-in-one-focused images
if compound_sharp:
    subprocess.run([sys.executable, 
                    os.path.join(benchmark_folder,r'methods\compound_sharp_method\evaluate.py'),
                    "--resultsPath",results_folder,
                    "--algorithm",algorithm])

# Evaluate the independantly annotated images 
if intern:
    subprocess.run([sys.executable, r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\intern_annotations\evaluate.py',
                    "--annotationPath",annotations_path,
                    "--groundTruthPath",intern_ground_truth_path,
                    "--resultsPath",intern_results_path])
