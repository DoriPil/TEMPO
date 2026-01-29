import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.io import imread
from sklearn.metrics import jaccard_score
import skimage
from scipy.spatial import distance
import argparse



def main():
    

    # Parse arguments
    parser=argparse.ArgumentParser()
    parser.add_argument("--resultsPath",required=True)
    parser.add_argument("--algorithm",required=True)
    args=parser.parse_args()


    # Define support functions
    def dice_coefficient(y_true,y_pred):
        """Calcul du coefficient de Dice"""
        intersection=np.sum(y_true*y_pred)
        return (2.*intersection)/(np.sum(y_true)+np.sum(y_pred)+1e-8)

    def IoU(y_true,y_pred):
        """Calcul du coefficient Intersection Over Union"""
        intersection=np.sum(y_true*y_pred)
        return (intersection/(np.sum(y_true)+np.sum(y_pred)-intersection)+1e-8)

    def binary_labeling(ground_truth):
        binary_segmentation=(ground_truth[:,:,0]==68)*(ground_truth[:,:,1]==1)
        return 1-binary_segmentation

    def binarize_annotation(annotation):
        channeled_annotation=annotation[:,:,0]
        binary_annotation=channeled_annotation>0
        return binary_annotation


    # Read directories
    method_folder=os.path.join(args.resultsPath,r'all_in_focus_method')
    method_to_evaluate=args.algorithm

    
    results_folder=os.path.join(method_folder,r'automatic_segmentation')
    ground_truth_folder=os.path.join(method_folder,'registered_ground_truth')

    if method_to_evaluate=="raw_difference":
        masks_folder=os.path.join(results_folder,r'thresholds\raw_difference\triangle_threshold') # Changer 'otsu' en 'triangle' pour évaluer le seuillage triangle (changement pour rendre ça automatique/avec des arguments à venir)
    elif method_to_evaluate=="ssim_difference":
        masks_folder=os.path.join(results_folder,r'thresholds\ssim_difference\triangle_threshold')

    #masks_folder=os.path.join(masks_folder,r'h_maximas')
    #masks_folder=os.path.join(masks_folder,r'reconstruction')



    # Write directories
    results_destination=masks_folder


    # List files in folders
    filenames=sorted([
        f for f in os.listdir(ground_truth_folder)
        if f.lower().endswith(('.png','.jpg','.jpeg','.tif'))
    ])


    results=[]


    # Iterate over all images
    for filename in filenames:


        # Load images to be processed
        ground_truth_path=os.path.join(ground_truth_folder,filename)
        masks_path=os.path.join(masks_folder,filename)

        ground_truth_image=imread(ground_truth_path)
        mask_image=imread(masks_path)

        
        # Binarize mask and ground truth images
        binary_ground_truth=binary_labeling(ground_truth_image)
        binary_annotation=binarize_annotation(mask_image)


        # Verify that images are same shape
        if binary_ground_truth.shape != binary_annotation.shape:
            print(f"[ERREUR] Dimensions différentes pour {filename}: GT {binary_ground_truth.shape}, préd {binary_annotation.shape}")
            continue


        # Flatten data for jaccard_score
        ground_truth_flat=binary_ground_truth.flatten()
        annotation_flat=binary_annotation.flatten()


        # Compute performances according to metrics
        dice=dice_coefficient(binary_ground_truth,binary_annotation)
        intersection_over_union=IoU(binary_ground_truth,binary_annotation)


        # Fill results array
        results.append({
            "Filename": filename,
            "Dice": dice,
            "Intersection Over Union": intersection_over_union
        })
        

        # Create Dataframe and show results
        df=pd.DataFrame(results)
        df.loc["MOYENNE"]=df.mean(numeric_only=True)
        print(df)
        df.to_csv(os.path.join(results_destination,"results.csv"),sep=';',index=True)


if __name__=="__main__":
    main()