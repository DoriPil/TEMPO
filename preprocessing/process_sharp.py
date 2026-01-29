import os, os.path
import skimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image
import argparse
import utils as utl
from scipy import ndimage

def main():

    # Parse arguments
    parser=argparse.ArgumentParser()
    parser.add_argument("--dataPath",required=True)
    parser.add_argument("--resultsPath",required=True)
    args=parser.parse_args()
    data_folder=args.dataPath
    results_folder=args.resultsPath

    # Read directories

    data_folder_clean=os.path.join(data_folder,r'multi_focus\raw\clean')
    data_folder_contaminated=os.path.join(data_folder,r'multi_focus\raw\contaminated')
    data_folder_ground_truth=os.path.join(data_folder,r'multi_focus\ground_truth')


    # Write directories
    sharp_folder_clean=os.path.join(results_folder,r'all_in_focus_method\clean')
    sharp_folder_contaminated=os.path.join(results_folder,r'all_in_focus_method\contaminated')
    raw_difference_folder=os.path.join(results_folder,r'all_in_focus_method\raw_difference')
    ssim_difference_folder=os.path.join(results_folder,r'all_in_focus_method\ssim_difference')
    registered_ground_truth_folder=os.path.join(results_folder,r'all_in_focus_method\registered_ground_truth')
    binary_masks=os.path.join(results_folder,r'all_in_focus_method\binary_masks')
    

    # Read image names in folder
    Z_stacks=[
        f for f in os.listdir(data_folder_clean)
        if f.lower().endswith(".tif")
        and os.path.isfile(os.path.join(data_folder_clean,f))
    ]

    # Iterate over all images
    for filename in Z_stacks:

        # Load images to be processed
        path_Z_stacks_clean=os.path.join(data_folder_clean,filename)
        path_Z_stacks_contaminated=os.path.join(data_folder_contaminated,filename)
        path_ground_truth=os.path.join(data_folder_ground_truth,filename[:-4]+'.png')

        Z_stack_clean=skimage.io.imread(path_Z_stacks_clean)
        Z_stack_contaminated=skimage.io.imread(path_Z_stacks_contaminated)
        ground_truth=skimage.io.imread(path_ground_truth)

        Z_stack_clean=Z_stack_clean.astype(float)
        Z_stack_contaminated=Z_stack_contaminated.astype(float)

        # Prepare variables
        F_clean=np.zeros(Z_stack_clean.shape)
        F_contaminated=np.zeros(Z_stack_contaminated.shape)
        N=10

        # Compute focus measures and in-focus images for clean images
        for i,im in enumerate(Z_stack_clean):
            F_clean[i]=utl.tenengrad(im,N)
        Z_clean=np.argmax(F_clean,axis=0)
        Z_clean=ndimage.minimum_filter(Z_clean,size=5)
        in_focus_clean=utl.extractTexture(Z_stack_clean,Z_clean)

        # Compute focus measures and in-focus images for contaminated images
        for i,im in enumerate(Z_stack_contaminated):
            F_contaminated[i]=utl.tenengrad(im,N)
        Z_contaminated=np.argmax(F_contaminated,axis=0)
        Z_contaminated=ndimage.minimum_filter(Z_contaminated,size=5)
        in_focus_contaminated=utl.extractTexture(Z_stack_contaminated,Z_contaminated)

        # Save all-in-focus images to folder
        path_in_focus_clean=os.path.join(sharp_folder_clean,filename)
        path_in_focus_contaminated=os.path.join(sharp_folder_contaminated,filename)

        matplotlib.image.imsave(path_in_focus_clean[:-4]+".png",in_focus_clean,cmap='gray')
        matplotlib.image.imsave(path_in_focus_contaminated[:-4]+".png",in_focus_contaminated,cmap='gray')

        print("image saved to "+path_in_focus_clean)


        # Compute displacement with cross-correlation in Fourrier domain
        cross_correlation=utl.cross_image_gray(in_focus_clean,in_focus_contaminated)
        displacement=np.unravel_index(np.argmax(cross_correlation),cross_correlation.shape)


        # Prepare variables for image registration
        s=in_focus_clean.shape
        midh=s[0]/2
        midw=s[1]/2

        sh0=0
        sh1=s[0]
        sw0=0
        sw1=s[1]
        ah0=0
        ah1=s[0]
        aw0=0
        aw1=s[1]

        if(displacement[0]<midh):
            sh1=s[0]-(midh-displacement[0])
            ah0=midh-displacement[0]
        else:
            sh0=displacement[0]-midh
            ah1=s[0]-(displacement[0]-midh)

        if(displacement[1]<midw):
            sw1=s[1]-(midw-displacement[1])
            aw0=midw-displacement[1]
        else:
            sw0=displacement[1]-midw
            aw1=s[1]-(displacement[1]-midw)

        sh0=int(sh0)
        sh1=int(sh1)
        sw0=int(sw0)
        sw1=int(sw1)
        ah0=int(ah0)
        ah1=int(ah1)
        aw0=int(aw0)
        aw1=int(aw1)


        # Perform image registration from cross_correlation computed values
        registered_focused_clean=in_focus_clean[sh0:sh1,sw0:sw1]
        registered_focused_contaminated=in_focus_contaminated[ah0:ah1,aw0:aw1]
        registered_ground_truth=ground_truth[ah0:ah1,aw0:aw1,:]

        # Compute and save raw difference images
        raw_difference=registered_focused_clean-registered_focused_contaminated
        raw_difference=abs(raw_difference)
        path_raw_difference=os.path.join(raw_difference_folder,filename)
        matplotlib.image.imsave(path_raw_difference[:-4]+'.png',raw_difference,cmap='gray')

        # Save registered ground truth
        path_registered_ground_truth=os.path.join(registered_ground_truth_folder,filename)
        matplotlib.image.imsave(path_registered_ground_truth[:-4]+'.png',registered_ground_truth)


        # Smooth images before applying SSIM function
        sigma=1.0
        registered_focused_clean=ndimage.gaussian_filter(registered_focused_clean,sigma)
        registered_focused_contaminated=ndimage.gaussian_filter(registered_focused_contaminated,sigma)

        # Apply SSIM function to compute difference between images
        data_range=registered_focused_clean.max()-registered_focused_clean.min()
        (sim_score,difference)=skimage.metrics.structural_similarity(registered_focused_clean,
                                                                     registered_focused_contaminated,
                                                                     data_range=data_range,
                                                                     full=True,
                                                                     gaussian_weights=True,
                                                                     sigma=1.5,
                                                                     use_sample_covariance=False)
        difference=abs(difference)
        difference=1-difference

        # Aggregate and suppress pixel noise
        difference=ndimage.median_filter(difference,size=5)

        # Save difference and binary images
        path_difference=os.path.join(ssim_difference_folder,filename)
        matplotlib.image.imsave(path_difference[:-4]+'.png',difference,cmap='gray')

        print("Saved image to " + path_difference[:-4]+'.png')


if __name__=="__main__":
    main()
    

