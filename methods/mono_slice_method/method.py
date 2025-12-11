import os, os.path
import skimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image
import matplotlib.pyplot as plt
from cellpose import plot, utils, io
import cv2
import utils as utl
import skimage.morphology
import argparse


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--dataPath",required=True)
    parser.add_argument("--resultsPath",required=True)
    args=parser.parse_args()
    data_folder=args.dataPath
    results_folder=args.resultsPath

    read_dir_name_sane=os.path.join(data_folder,r'mono_focus\clean')
    read_dir_name_contaminated=os.path.join(data_folder,r'mono_focus\contaminated')
    read_dir_manual_segmentation=os.path.join(data_folder,r'mono_focus\ground_truth')
    write_dir_manual_segmentation_cropped=os.path.join(results_folder,r'mono_slice_method\cropped_ground_truth')
    #write_dir_name_cropped_image=os.path.join(results_folder,r'C:\Users\PILLLARD-DOR\Documents\scripts_thèse\images_qualite\benchmark_images\image_cropee')
    write_dir_name_difference_brute=os.path.join(results_folder,r'mono_slice_method\raw_difference')
    write_dir_name_difference_ouverte=os.path.join(results_folder,r'mono_slice_method\intermediate_difference')
    write_dir_name_image_intermédiaire=os.path.join(results_folder,r'mono_slice_method\automatic_segmentation')
    write_dir_name_image_reconstruite=os.path.join(results_folder,r'mono_slice_method\automatic_segmentation')

    images=os.listdir(read_dir_name_sane)

    for filename in images:
        filename_png=filename[:-4]+".png"
        path_img_saine=os.path.join(read_dir_name_sane,filename)
        path_img_contaminee=os.path.join(read_dir_name_contaminated,filename)
        path_segmentation_manuelle=os.path.join(read_dir_manual_segmentation,filename_png)

        save_path_difference_brute=os.path.join(write_dir_name_difference_brute,filename)
        save_path_difference_ouverte=os.path.join(write_dir_name_difference_ouverte,filename)
        save_path_manual_segmentation_cropped=os.path.join(write_dir_manual_segmentation_cropped,filename_png)
        save_path_masque_intermédiaire=os.path.join(write_dir_name_image_intermédiaire,filename)
        save_path_masque_reconstruit=os.path.join(write_dir_name_image_reconstruite,filename)

        save_path_difference_brute=save_path_difference_brute[:-4]
        save_path_difference_ouverte=save_path_difference_ouverte[:-4]
        save_path_masque_intermédiaire=save_path_masque_intermédiaire[:-4]
        save_path_masque_reconstruit=save_path_masque_reconstruit[:-4]
        

        img_saine=io.imread(path_img_saine)
        img_contaminee=io.imread(path_img_contaminee)
        manual_segmentation=plt.imread(path_segmentation_manuelle)

        print(manual_segmentation.shape)

        cross_correlation=utl.cross_image(img_saine,img_contaminee)

        displacement=np.unravel_index(np.argmax(cross_correlation),cross_correlation.shape)

        s=img_contaminee.shape

        midh=s[0]/2
        midw=s[1]/2

        shifth=displacement[0]
        shiftw=displacement[1]

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


        nvimgsans=img_saine[sh0:sh1,sw0:sw1]
        nvimgavec=img_contaminee[ah0:ah1,aw0:aw1]
        segmentation_manuelle_croppee=manual_segmentation[ah0:ah1,aw0:aw1]
        matplotlib.image.imsave(save_path_manual_segmentation_cropped,segmentation_manuelle_croppee)


        imgsansgris=cv2.cvtColor(nvimgsans, cv2.COLOR_BGR2GRAY)
        imgavecgris=cv2.cvtColor(nvimgavec, cv2.COLOR_BGR2GRAY)

        difference=abs(imgsansgris-imgavecgris)
        

        matplotlib.image.imsave(save_path_difference_brute+".png", difference)

        SE=skimage.morphology.disk(5)
        opened_image=skimage.morphology.opening(difference,SE)
        closed_image=skimage.morphology.closing(opened_image,SE)
        matplotlib.image.imsave(save_path_difference_ouverte+".png",closed_image)
        
        thresh=skimage.filters.threshold_triangle(closed_image)
        binary=closed_image>thresh
        area_opened_image=skimage.morphology.area_opening(binary,1000)
        matplotlib.image.imsave(save_path_masque_intermédiaire+".png",area_opened_image)


        SE=skimage.morphology.disk(10)
        imopen=skimage.morphology.closing(area_opened_image,SE)
        seed=np.copy(imopen)
        mask=imopen
        seed[1:-1,1:-1]=imopen.max()
        imopen_filled=skimage.morphology.reconstruction(seed,mask,method="erosion")

if __name__=="__main__":
    main()
