import subprocess
import sys
import argparse
import os

# Path to data and results folders

benchmark_folder=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data" # Modifier ce chemin pour rendre compatible avec votre machine
data_folder=os.path.join(benchmark_folder,r'data')
results_folder=os.path.join(benchmark_folder,r'results')

# Booleans for choosing which data to process
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
                    "--dataPath",data_folder,
                    "--resultsPath",results_folder]])

# Process difference images from stack
if process_difference:
    subprocess.run([sys.executable,
                    r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\preprocessing\process_difference.py",
                    "--dataPath",data_folder,
                    "--resultsPath",results_folder])