import subprocess
import sys

# Passer en argument "--dataPath" le chemin vers le dossier des données de travail, et en script le chemin vers le script à exécuter

subprocess.run([sys.executable, 
                r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\stack_method\method.py",
                "--dataPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\data",
                "--resultsPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate"])

subprocess.run([sys.executable,
                r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\compound_sharp_method\method.py",
                "--dataPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\data",
                "--resultsPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate"])

subprocess.run([sys.executable, 
                r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\depth_map_method\method.py",
                "--dataPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\data",
                "--resultsPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate"])

subprocess.run([sys.executable, 
                r"C:\Users\PILLLARD-DOR\Documents\GitHub\TEMPO\methods\mono_slice_method\method.py",
                "--dataPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\data",
                "--resultsPath",r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate"])
# Module pour faire fonctionner SAM pas encore installé sur la machine donc pas encore de script method.py associé, les images et masques obtenus sont tirés de l'outil en ligne pour le moment
#subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\SAM_method\method.py"])"""