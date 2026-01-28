import os, os.path
import skimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image
from cellpose import plot, utils, io
import cv2
import skimage.morphology
import argparse
import utils as utl
from scipy import ndimage

def main():

    # Parse arguments
    parser=argparse.ArgumentParser()
    parser.add_argument("--cleanDataPath",required=True)
    parser.add_argument("--contaminatedDataPath",required=True)
    parser.add_argument("--depthDataPathClean",required=True)
    parser.add_argument("--depthDataPathContaminated",required=True)
    args=parser.parse_args()
    

    # Read directories
    data_folder_clean=args.cleanDataPath
    data_folder_contaminated=args.contaminatedDataPath


    # Write directories
    depth_folder_clean=args.depthDataPathClean
    depth_folder_contaminated=args.depthDataPathContaminated

    # Read image names in folder
    Z_stacks=os.listdir(data_folder_clean)

    # Iterate over all images
    for filename in Z_stacks:

        # Load images to be processed
        path_Z_stacks_clean=os.path.join(data_folder_clean,filename)
        path_Z_stacks_contaminated=os.path.join(data_folder_contaminated,filename)

        Z_stack_clean=io.imread(path_Z_stacks_clean)
        Z_stack_contaminated=io.imread(path_Z_stacks_contaminated)

        Z_stack_clean=Z_stack_clean.astype(float)
        Z_stack_contaminated=Z_stack_contaminated.astype(float)

        # Prepare variables
        F_clean=np.zeros(Z_stack_clean.shape)
        F_contaminated=np.zeros(Z_stack_contaminated.shape)
        N=10

        # Compute focus measures and depth map images for clean images
        for i,im in enumerate(Z_stack_clean):
            F_clean[i]=utl.tenengrad(im,N)
        Z_clean=np.argmax(F_clean,axis=0)
        Z_clean=ndimage.minimum_filter(Z_clean,size=5)
        depth_map_clean=76-Z_clean

        # Compute focus measures and depth map images for contaminated images
        for i,im in enumerate(Z_stack_contaminated):
            F_contaminated[i]=utl.tenengrad(im,N)
        Z_contaminated=np.argmax(F_contaminated,axis=0)
        Z_contaminated=ndimage.minimum_filter(Z_contaminated,size=5)
        depth_map_contaminated=76-Z_contaminated

        # Save images to folder
        path_depth_map_clean=os.path.join(depth_folder_clean,filename)
        path_depth_map_contaminated=os.path.join(depth_folder_contaminated,filename)

        matplotlib.image.imsave(path_depth_map_clean[:-4]+".png",depth_map_clean,cmap='viridis')
        matplotlib.image.imsave(path_depth_map_contaminated[:-4]+".png",depth_map_contaminated,cmap='viridis')

        print("image saved to "+path_depth_map_clean)
        
        



if __name__=="__main__":
    main()
    

