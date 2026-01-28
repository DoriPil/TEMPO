import subprocess
import sys

best_focus=True
compound_sharp=True
intern=True

ground_truth_path=r'C:\Users\PILLLARD-DOR\Documents\benchmark_data\results\best_focus_method\registered_ground_truth'
masks_path=r'C:\Users\PILLLARD-DOR\Documents\benchmark_data\results\best_focus_method\automatic_segmentation'
results_path=r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\results\best_focus_method"

annotations_path=r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\data\multi_focus\manual_annotations_independant\raw'
intern_ground_truth_path=r'C:\Users\PILLLARD-DOR\Documents\benchmark_data\data\multi_focus\ground_truth'
intern_results_path=r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\intern_annotations'



if best_focus:
    subprocess.run([sys.executable, r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\best_focus_method\evaluate.py',
                    "--annotationPath",masks_path,
                    "--groundTruthPath",ground_truth_path,
                    "--resultsPath",results_path])
    
if compound_sharp:
    subprocess.run([sys.executable, r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\compound_sharp_method\evaluate.py',
                    "--annotationPath",r'C:\Users\PILLLARD-DOR\Documents\benchmark_data\results\all_in_focus_method\automatic_segmentation',
                    "--groundTruthPath",r'C:\Users\PILLLARD-DOR\Documents\benchmark_data\results\all_in_focus_method\registered_ground_truth',
                    "--resultsPath",r"C:\Users\PILLLARD-DOR\Documents\benchmark_data\results\all_in_focus_method"])


#subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\stack_method\evaluate.py"])
#subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\compound_sharp_method\evaluate.py"])
#subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\depth_map_method\evaluate.py"])
#subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\mono_slice_method\evaluate.py"])
#subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\SAM_method\evaluate.py",
#                "--groundTruthPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\stack_method\cropped_ground_truth",
#                "--segmentationPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\SAM_method\SAM_cutouts",
#                "--cutoutsPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\SAM_method\binary_cutouts",
#                "--csvFileDestination",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\SAM_method\results.csv"])


if intern:
    subprocess.run([sys.executable, r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\intern_annotations\evaluate.py',
                    "--annotationPath",annotations_path,
                    "--groundTruthPath",intern_ground_truth_path,
                    "--resultsPath",intern_results_path])
