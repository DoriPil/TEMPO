import subprocess
import sys

subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\stack_method\method.py"])
subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\compound_sharp_method\method.py"])
subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\depth_map_method\method.py"])
subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\mono_slice_method\method.py"])
# Module pour faire fonctionner SAM pas encore installé sur la machine donc pas encore de script method.py associé, les images et masques obtenus sont tirés de l'outil en ligne pour le moment
#subprocess.run([sys.executable, r"C:\Users\PILLLARD-DOR\Documents\TEMPO\methods\SAM_method\method.py"])