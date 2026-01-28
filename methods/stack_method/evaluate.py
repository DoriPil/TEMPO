import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.io import imread
from sklearn.metrics import jaccard_score
import skimage
from scipy.spatial import distance
















def dice_coefficient(y_true, y_pred):
    """Calcul du coefficient de Dice"""
    intersection = np.sum(y_true * y_pred)
    return (2. * intersection) / (np.sum(y_true) + np.sum(y_pred) + 1e-8)

def IoU(y_true,y_pred):
    """Calcul du coefficient Intersection Over Union"""
    intersection=np.sum(y_true*y_pred)
    return (intersection/(np.sum(y_true)+np.sum(y_pred)-intersection)+1e-8)

def binarize(image, threshold=128):
    """Convertir une image en masque binaire (valeurs 0 ou 1)"""

    image=image[:,:,0:3]


    gray_image=skimage.color.rgb2gray(image)

    thresh=skimage.filters.threshold_triangle(gray_image)
    binary=gray_image>thresh
    return binary.astype(np.uint8)

# === PARAMÈTRES pour les masques issus de piles d'images===
ground_truth_dir = r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\stack_method\cropped_ground_truth"
predicted_mask_dir = r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\stack_method\automatic_segmentation"
output_dir= r"C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\stack_method\


# Lister les fichiers de ground truth (on suppose qu’ils sont tous présents dans les deux dossiers)
filenames = sorted([
    f for f in os.listdir(ground_truth_dir)
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif'))
])

results = []

for filename in filenames:
    gt_path = os.path.join(ground_truth_dir, filename)
    pred_path = os.path.join(predicted_mask_dir, filename)

    if not os.path.exists(pred_path):
        print(f"[AVERTISSEMENT] Masque prédit manquant pour {filename}")
        continue

    # Charger l’image labellisée (ground truth)
    gt_img = binarize(imread(gt_path))

    pred_img = binarize(imread(pred_path))
    plt.imshow(gt_img)

    # Vérification des dimensions
    if gt_img.shape != pred_img.shape:
        print(f"[ERREUR] Dimensions différentes pour {filename}: GT {gt_img.shape}, préd {pred_img.shape}")
        continue

    # Aplatir les images pour jaccard_score
    gt_flat = gt_img.flatten()
    pred_flat = pred_img.flatten()

    dice = dice_coefficient(gt_img, pred_img)
    #jaccard = jaccard_score(gt_img, pred_img, average=None)
    intersection_over_union=IoU(gt_img, pred_img)

    results.append({
        "Nom du fichier": filename,
        "Dice": dice,
    #    "Jaccard": jaccard
        "Intersection over Union": intersection_over_union
    })

# Créer un DataFrame et afficher les résultats
df = pd.DataFrame(results)
df.loc["MOYENNE"] = df.mean(numeric_only=True)
print(df)
df.to_csv(os.path.join(output_dir, "results.csv"),index=True)
