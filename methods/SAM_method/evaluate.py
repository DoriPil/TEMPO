import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from skimage.io import imread
from sklearn.metrics import jaccard_score
import skimage
from scipy.spatial import distance
import argparse
import cv2 as cv

def dice_coefficient(y_true, y_pred):
    """Calcul du coefficient de Dice"""
    intersection = np.sum(y_true * y_pred)
    return (2. * intersection) / (np.sum(y_true) + np.sum(y_pred) + 1e-8)

def IoU(y_true,y_pred):
    """Calcul du coefficient Intersection Over Union"""
    intersection=np.sum(y_true*y_pred)
    return (intersection/(np.sum(y_true)+np.sum(y_pred)-intersection)+1e-8)

def binarize(image, threshold=128):
    #revoir la fonction de binarisation car elle ne fonctionne probablement    

    """Convertir une image en masque binaire (valeurs 0 ou 1)"""
    #imageb=image.sum(axis=2)

    #imageb=1.0*(imageb>0)
    
    
    #return imageb

    image=image[:,:,0:3]


    gray_image=skimage.color.rgb2gray(image)

    thresh=skimage.filters.threshold_triangle(gray_image)
    binary=gray_image>thresh
    return binary.astype(np.uint8)

def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--groundTruthPath",required=True)
    parser.add_argument("--segmentationPath",required=True)
    parser.add_argument("--cutoutsPath",required=True)
    parser.add_argument("--csvFileDestination",required=True)
    args=parser.parse_args()
    ground_truth_dir=args.groundTruthPath
    predicted_mask_dir=args.segmentationPath
    save_dir=args.cutoutsPath
    results_path=args.csvFileDestination



    # Lister les fichiers de ground truth (on suppose qu’ils sont tous présents dans les deux dossiers)
    filenames = sorted([
        f for f in os.listdir(ground_truth_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif'))
    ])

    results = []

    for filename in filenames:
        gt_path = os.path.join(ground_truth_dir, filename)
        pred_path = os.path.join(predicted_mask_dir, filename)
        save_path = os.path.join(save_dir,filename)

        if not os.path.exists(pred_path):
            print(f"[AVERTISSEMENT] Masque prédit manquant pour {filename}")
            continue

        # Charger l’image labellisée (ground truth)
        gt_img = binarize(imread(gt_path))
        
        plt.imshow(gt_img)

        pred_img = binarize(imread(pred_path))

        matplotlib.image.imsave(save_path,pred_img)

        pred_img = cv.resize(
            pred_img,
            (gt_img.shape[1], gt_img.shape[0]),
            interpolation=cv.INTER_NEAREST
        )

        pred_img = pred_img.astype(np.uint8)


        matplotlib.image.imsave(save_path,pred_img)

        #calculer les intersections/union entre images pour vérifier la véracité des scores IoU et Dice

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
    df.to_csv(results_path,sep=';',decimal=',',index=True)

if __name__=="__main__":
    main()