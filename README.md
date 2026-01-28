Répertoire listant les scripts permettant de faire l'annotation automatique des données liées à la thèse TEMPO.

# PRÉ-TRAITEMENTS
Le dossier "preprocess" contient les scripts permettant de faire le pré-traitement des piles d'images afin d'obtenir:
- les cartes de profondeur de chaque pile d'image
- les images nettes virtuelles de chaque pile
- faire le recalage vertical entre les deux piles (procédé décrit ci-dessous)
- les différénces entre chaque paire d'image contaminée/saine

Le script "preprocess_data.py" permet de lancer tous les pré-traitements; des booléens pour chaque pré-traitement permettent d'activer/désactiver quels prétraitement appliquer.

RECALAGE VERTICAL:
Le recalage vertical est réalisé en sélectionnant l'image contaminée pour laquelle le microscope a fait la mise au point (39ème image de la pile contaminée), pour appliquer ensuite la fonction Structural Similarity Index Measure et comparer l'image contaminée au point à chaque autre image de la pile saine; l'image de la pile saine permettant d'obtenir le meilleur score SSIM est alors retenue pour la suite des traitements.

DIFFÉRENCES D'IMAGES:
La différénce entre image contaminée et image saine peut être réalisée de deux façons, après les avoir recalées horizontalement grâce au produit d'intercorrélation:
- différence brute (image 1 - image 2)
- différence SSIM (image retournée en mettant l'argument "full" à "True" dans la fonction SSIM)


# MÉTHODES
Chaque méthode peut être lancée individuellement ou collectivement en lançant le script "run_all_benchmarks" dans le dossier "experiments". Des booléens à l'intérieur de ce script permettent de sélectionner les méthodes à lancer. En outre, chaque méthode possède des paramètres à optimiser qui permettent de sauter le calcul d'une méthode en particulier si les paramètres sont mis à 0.

# RÉSULTATS
Chaque méthode peut être évaluée grâce au script "evaluate_all_methods" dans le dossier "experiments". Des booléens permettent de choisir les résultats de quelle méthode évaluer.

# DONNÉES
Les segmentations obtenues par le logiciel d'annotation Cellpose sont disponibles au format "Position_XXXX_seg.npy". Le script "convert_seg_to_png.py" permet de générer des images png pour les visualiser avec la labelisation. Les autres données (images au format .tif) sont disponibles selon un lien de téléchargement séparé.

Le chemin vers les données doit être précisé dans les scripts "run_all_benchmarks", "preprocess_data" et "evaluate_all_methods". A partir de là les dossiers sont créés automatiquement avec les images et résultats générés.


