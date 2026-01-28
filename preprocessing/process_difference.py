import os, os.path
import skimage
import numpy as np
import matplotlib.image
import utils as utl
import argparse
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
    difference_folder=os.path.join(results_folder,r'best_focus_method\raw_difference')
    best_focus_images_folder_clean=os.path.join(data_folder,r'multi_focus\best_focus\clean')
    best_focus_images_folder_contaminated=os.path.join(data_folder,r'multi_focus\best_focus\contaminated')
    registered_ground_truth_folder=os.path.join(results_folder,r'best_focus_method\registered_ground_truth')
    registered_best_focus_clean_folder=os.path.join(results_folder,r'best_focus_method\registered_clean')
    registered_best_focus_contaminated_folder=os.path.join(results_folder,r'best_focus_method\registered_contaminated')



    # Read image names in folder
    images=os.listdir(data_folder_clean)


    # Iterate over all images
    for filename in images:


        # Load images to be processed
        path_images_clean=os.path.join(data_folder_clean,filename)
        path_images_contaminated=os.path.join(data_folder_contaminated,filename)
        path_ground_truth=os.path.join(data_folder_ground_truth,filename[:-4]+'.png')

        image_stack_clean=skimage.io.imread(path_images_clean)
        image_stack_contaminated=skimage.io.imread(path_images_contaminated)
        ground_truth=skimage.io.imread(path_ground_truth)

        image_stack_clean=image_stack_clean.astype(float)
        image_stack_contaminated=image_stack_contaminated.astype(float)


        # Prepare variables
        flag=True
        score=0
        sens="Incrémentation"
        index_retenu=0


        # Iterate over all images
        for index in range(0,75):


            # Determine best focus for image registration (this process can be improved by making certain hypotheses on the focus measures of images)
            # Extract single slices from stack 
            image_contaminated=image_stack_contaminated[39,:,:]
            image_clean=image_stack_clean[index,:,:]


            # Compute displacement with cross-correlation in Fourrier domain
            cross_correlation=utl.cross_image_gray(image_clean,image_contaminated)
            displacement=np.unravel_index(np.argmax(cross_correlation),cross_correlation.shape)


            # Prepare variables for image registration
            s=image_contaminated.shape
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
            registered_image_clean=image_clean[sh0:sh1,sw0:sw1]
            registered_image_contaminated=image_contaminated[ah0:ah1,aw0:aw1]

            data_range=registered_image_clean.max()-registered_image_clean.min()

            # Compute SSIM between registered images
            (sim_score,difference)=skimage.metrics.structural_similarity(registered_image_clean,registered_image_contaminated,data_range=data_range,full=True)


            # Save index if similarity is greater than previous best focus
            if(score==0):
                score=sim_score
            if(sim_score>score):
                score=sim_score
                index_retenu=index
            
            print("Image Similarity: {:.4f}%".format(score*100))
            print("Score calculé actuel: {:.4f}%".format(sim_score*100))

        print("Score final retenu: {:.4f}%".format(score*100))
        print("Index final retenu: {:.4f}%".format(index_retenu))

        # Read the images with the best focus from the stack
        image_contaminated_best_focus=image_stack_contaminated[39,:,:]
        image_clean_best_focus=image_stack_clean[index_retenu,:,:]

        # Save the images with the best focus/most similarity from the stack
        path_best_focus_clean=os.path.join(best_focus_images_folder_clean,filename)
        path_best_focus_contaminated=os.path.join(best_focus_images_folder_contaminated,filename)

        matplotlib.image.imsave(path_best_focus_clean[:-4]+".png",image_clean_best_focus,cmap='gray')
        matplotlib.image.imsave(path_best_focus_contaminated[:-4]+".png",image_contaminated_best_focus,cmap='gray')


        # Compute displacement with cross-correlation in Fourrier domain
        cross_correlation=utl.cross_image_gray(image_clean_best_focus,image_contaminated_best_focus)
        displacement=np.unravel_index(np.argmax(cross_correlation),cross_correlation.shape)


        # Prepare variables for image registration
        s=image_clean_best_focus.shape
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
        registered_image_clean=image_clean_best_focus[sh0:sh1,sw0:sw1]
        registered_image_contaminated=image_contaminated_best_focus[ah0:ah1,aw0:aw1]
        registered_ground_truth=ground_truth[ah0:ah1,aw0:aw1,:]

        # Save registered ground truth
        path_registered_ground_truth=os.path.join(registered_ground_truth_folder,filename)
        matplotlib.image.imsave(path_registered_ground_truth[:-4]+'.png',registered_ground_truth)


        # Smooth images before applying SSIM function
        sigma=1.0
        registered_image_clean=ndimage.gaussian_filter(registered_image_clean,sigma)
        registered_image_contaminated=ndimage.gaussian_filter(registered_image_contaminated,sigma)


        # Apply SSIM function to compute difference between images
        data_range=registered_image_clean.max()-registered_image_contaminated.min()
        (sim_score, difference)=skimage.metrics.structural_similarity(registered_image_clean,
                                                                      registered_image_contaminated,
                                                                      data_range=data_range,
                                                                      full=True,
                                                                      gaussian_weights=True,
                                                                      sigma=1.5,
                                                                      use_sample_covariance=False)
        difference=abs(difference)
        difference=1-difference

        # Aggregate and suppress pixel noise
        difference=ndimage.median_filter(difference,size=5)


        # Save difference image and registered best focus images
        path_registered_clean_focus=os.path.join(registered_best_focus_clean_folder,filename)
        path_registered_contaminated_focus=os.path.join(registered_best_focus_contaminated_folder,filename)
        path_difference=os.path.join(difference_folder,filename)
        matplotlib.image.imsave(path_difference[:-4]+'.png',difference,cmap='gray')
        matplotlib.image.imsave(path_registered_clean_focus[:-4]+'.png',registered_image_clean,cmap='gray')
        matplotlib.image.imsave(path_registered_contaminated_focus[:-4]+'.png',registered_image_contaminated,cmap='gray')



if __name__=="__main__":
    main()