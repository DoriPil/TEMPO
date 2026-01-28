import subprocess
import sys
import argparse

"""def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--dataPath",required=True)
    parser.add_argument("--resultsPath",required=True)
    args=parser.parse_args()
    data_folder=args.dataPath
    results_folder=args.resultsPath"""

    
    # Passer en argument "--dataPath" le chemin vers le dossier des données de travail, et en script le chemin vers le script à exécuter
data_folder=r'C:\Users\PILLLARD-DOR\Documents\benchmark_data\data'
results_folder=r'C:\Users\PILLLARD-DOR\Documents\benchmark_data\results'
alternate_filters_depth=5
h_maximas=10
reconstruct=True

run_best_focus_method=True
run_sharp_method=True

if run_best_focus_method:
    subprocess.run([sys.executable,
                    r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\best_focus_method\method.py',
                    "--dataPath",data_folder,
                    "--resultsPath",results_folder,
                    "--alternateFiltersDepth",str(alternate_filters_depth),
                    "--h_maximas",str(h_maximas),
                    "--reconstruct",str(reconstruct)])
    
if run_sharp_method:
    subprocess.run([sys.executable,
                    r'C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\compound_sharp_method\method.py',
                    "--dataPath",data_folder,
                    "--resultsPath",results_folder,
                    "--alternateFiltersDepth",str(alternate_filters_depth),
                    "--h_maximas",str(h_maximas),
                    "--reconstruct",str(reconstruct)]) 


#subprocess.run([sys.executable, 
 #               r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\stack_method\method.py",
 #               "--dataPath",data_folder,
 #               "--resultsPath",results_folder])

#    subprocess.run([sys.executable,
#                    r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\compound_sharp_method\method.py",
#                    "--dataPath",data_folder,
#                    "--resultsPath",results_folder])

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

"""if __name__=="__main__":
    main()"""