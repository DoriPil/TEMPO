import os, os.path
import skimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image
import utils as utl
import skimage.morphology
import argparse

def main():

    # Parse arguments
    parser=argparse.ArgumentParser()
    parser.add_argument("--dataPath",required=True)
    parser.add_argument("--resultsPath",required=True)
    parser.add_argument("--alternateFiltersDepth",type=int,required=True)
    parser.add_argument("--h_maximas",type=int,required=True)
    parser.add_argument("--reconstruct",type=bool,required=True)
    args=parser.parse_args()
    
    data_folder=args.dataPath
    results_folder=args.resultsPath
    alternate_filter_depth=args.alternateFiltersDepth
    h_maximas=args.h_maximas
    reconstruct=args.reconstruct


    # Read directories
    difference_folder=os.path.join(results_folder,r'all_in_focus_method\raw_difference')


    # Write directories
    automatic_segmentation_folder_alternate_filters=os.path.join(results_folder,r"all_in_focus_method\automatic_segmentation\alternate_filters\masks")
    intermediate_difference_folder_alternate_filters=os.path.join(results_folder,r'all_in_focus_method\automatic_segmentation\alternate_filters\intermediate_difference')
    automatic_segmentation_folder_h_maximas=os.path.join(results_folder,r'all_in_focus_method\automatic_segmentation\h_maximas\masks')
    gaussian_filtered_image_folder=os.path.join(results_folder,r'all_in_focus_method\automatic_segmentation\h_maximas\filtered_difference')
    intermediate_difference_folder_h_maximas=os.path.join(results_folder,r'all_in_focus_method\automatic_segmentation\h_maximas\intermediate_difference')
    automatic_segmentation_folder_reconstruction=os.path.join(results_folder,r'all_in_focus_method\automatic_segmentation\reconstruction\masks')
    intermediate_difference_folder_reconstruction=os.path.join(results_folder,r'all_in_focus_method\automatic_segmentation\reconstruction\intermediate_difference')
    reconstruction_folder=os.path.join(results_folder,r'all_in_focus_method\reconstructed_image')
    full_reconstruction_folder=os.path.join(results_folder,r'all_in_focus_method\full_reconstruction')

    
    # Read image names in folder
    images=os.listdir(difference_folder)


    # Iterate over all images
    for filename in images:

        # Load images to be processed
        path_raw_difference_images=os.path.join(difference_folder,filename)
        difference=skimage.io.imread(path_raw_difference_images)
        difference=difference.astype(float)


        # Extract grayscale image from 4-channel RGBA image
        difference=difference[:,:,0]
                              

        
        # Open difference to get rid of "constellation noise"
#Essayer:
#- filtres alternés séquencés
#- reconstruction sous l'image de différence
#- essayer avec les maximas

        #opened_difference=skimage.morphology.opening(difference,skimage.morphology.disk(5))
        #opened_difference=skimage.morphology.area_opening(difference,500)
        #closed_difference=skimage.morphology.closing(opened_difference,skimage.morphology.disk(4))
        #closed_difference=opened_difference

        # Alternate filtering method

        if alternate_filter_depth>0:

            difference_alternate=difference
            for size in range(alternate_filter_depth-1):
                difference_alternate=skimage.morphology.opening(difference_alternate,skimage.morphology.disk(alternate_filter_depth))
                difference_alternate=skimage.morphology.closing(difference_alternate,skimage.morphology.disk(alternate_filter_depth))
            
            
            # Save opened difference
            save_path_intermediate_difference=os.path.join(intermediate_difference_folder_alternate_filters,filename)
            matplotlib.image.imsave(save_path_intermediate_difference,difference_alternate,cmap='gray')

            # Binarize and save image
            threshold=skimage.filters.threshold_otsu(difference_alternate)
            binary=difference_alternate>threshold

            save_path_binary_image=os.path.join(automatic_segmentation_folder_alternate_filters,filename)
            matplotlib.image.imsave(save_path_binary_image,binary,cmap='gray')


        # H_maximas method

        if h_maximas>0:

            difference_h_max=difference
            difference_h_max=skimage.filters.gaussian(difference_h_max,sigma=1.0)

            # Save gaussian filtered image

            save_path_filtered_image=os.path.join(gaussian_filtered_image_folder,filename)
            matplotlib.image.imsave(save_path_filtered_image,difference_h_max,cmap='gray')


            maximas=skimage.morphology.h_maxima(difference_h_max,h_maximas)
            filtered=difference*maximas


            # Save maximas filtering

            save_path_intermediate_difference=os.path.join(intermediate_difference_folder_h_maximas,filename)
            matplotlib.image.imsave(save_path_intermediate_difference,filtered,cmap='gray')

        
            # Reconstruct objetcs from maximas markers under original image

            # Combining H_maximas and alternate filtering method

        # Reconstruction of opened difference under raw difference

        if reconstruct:
            opened_difference=skimage.morphology.opening(difference,skimage.morphology.disk(5))
            opened_difference=skimage.morphology.area_opening(difference,500)
            closed_difference=skimage.morphology.closing(opened_difference,skimage.morphology.disk(4))
            reconstruction=skimage.morphology.reconstruction(opened_difference,difference,method='dilation')

            # Save image reconstruction under original difference 

            save_path_reconstruction=os.path.join(reconstruction_folder,filename)
            matplotlib.image.imsave(save_path_reconstruction[:-4]+'.png',reconstruction,cmap='gray')
            print('save reconstructed image!')

            # Binarize image
            threshold=skimage.filters.threshold_otsu(reconstruction)
            binary_image=reconstruction>threshold


            # Reconstruct image from binary segmentation under original raw difference

            markers=binary_image*reconstruction
            full_reconstruction=skimage.morphology.reconstruction(markers,difference,method='dilation')

            # Fill holes in reconstruction before saving

            seed=np.copy(full_reconstruction)
            seed[1:-1, 1:-1]=full_reconstruction.max()
            mask=full_reconstruction

            filled_reconstruction=skimage.morphology.reconstruction(seed, mask, method='erosion')

            # Save binary image and full reconstruction

            save_path_mask=os.path.join(automatic_segmentation_folder_reconstruction,filename)
            save_path_full_reconstruction=os.path.join(full_reconstruction_folder,filename)
            matplotlib.image.imsave(save_path_mask,binary_image,cmap='gray')
            matplotlib.image.imsave(save_path_full_reconstruction,filled_reconstruction,cmap='gray')
        




        # Binarize the image to obtain mask
        #threshold=skimage.filters.threshold_otsu(closed_difference)
        #binary=closed_difference>threshold

        #seed = np.copy(binary)
        #seed[1:-1, 1:-1] = binary.min()
        #reconstruction = skimage.morphology.reconstruction(seed, binary, method='dilation')


        # Save mask
        #save_path_mask=os.path.join(automatic_segmentation_folder_alternate_filters,filename)
        #matplotlib.image.imsave(save_path_mask,binary,cmap='gray')


if __name__=="__main__":
    main()