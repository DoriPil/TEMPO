import subprocess
import sys
import argparse
import os

# Path to data and results folders
benchmark_folder=r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO" # Modifier ce chemin pour rendre compatible avec votre machine
data_folder=os.path.join(benchmark_folder,'data')
results_folder=os.path.join(benchmark_folder,'results')

# Define parameters for methods to apply
alternate_filters_depth=0
h_maximas=0
reconstruct=False
threshold_type="all" # Threshold arguments accepted: triangle, otsu, all or None

# Booleans for choosing which methods to benchmark
run_best_focus_method=False
run_sharp_method=True

# Compute masks using the best focused images
if run_best_focus_method:
    subprocess.run([sys.executable,
                    os.path.join(benchmark_folder,r'methods\best_focus_method\method.py'),
                    "--dataPath",data_folder,
                    "--resultsPath",results_folder,
                    "--alternateFiltersDepth",str(alternate_filters_depth),
                    "--h_maximas",str(h_maximas),
                    "--reconstruct",str(reconstruct),
                    "--thresholdOnly",threshold_type])
    
# Compute masks using all-in-one focus iamges (compound sharp images)
if run_sharp_method:
    subprocess.run([sys.executable,
                    os.path.join(benchmark_folder,r'methods\compound_sharp_method\method.py'),
                    "--dataPath",data_folder,
                    "--resultsPath",results_folder,
                    "--alternateFiltersDepth",str(alternate_filters_depth),
                    "--h_maximas",str(h_maximas),
                    "--reconstruct",str(reconstruct),
                    "--thresholdType",threshold_type])



#    subprocess.run([sys.executable, 
#                    r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\depth_map_method\method.py",
#                    "--dataPath",data_folder,
#                    "--resultsPath",results_folder])

#    subprocess.run([sys.executable, 
#                    r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\mono_slice_method\method.py",
#                    "--dataPath",data_folder,
#                    "--resultsPath",results_folder])
#     Module pour faire fonctionner SAM pas encore installé sur la machine donc pas encore de script method.py associé, les images et masques obtenus sont tirés de l'outil en ligne pour le moment
#    subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\SAM_method\method.py"])"""
