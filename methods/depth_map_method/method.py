import os, os.path
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.image
import skimage
import numpy as np
import matplotlib.pyplot as plt
from cellpose import plot, utils, io
import cv2
import utils as utl
import skimage.morphology



read_dir_name_sane=r'C:\Users\PILLLARD-DOR\Documents\TEMPO\data\multi_focus\depth_map\clean'
read_dir_name_contaminated=r'C:\Users\PILLLARD-DOR\Documents\TEMPO\data\multi_focus\depth_map\contaminated'
read_dir_manual_segmentation=r'C:\Users\PILLLARD-DOR\Documents\TEMPO\data\multi_focus\ground_truth'
write_dir_name_sane=r'C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\depth_map_method\cropped_ground_truth'
write_dir_name_contaminated=r'C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\depth_map_method\automatic_segmentation'
write_dir_name_difference_brute=r'C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\depth_map_method\raw_difference'
write_dir_name_difference_ouverte=r'C:\Users\PILLLARD-DOR\Documents\TEMPO\results_and_intermediate\depth_map_method\intermediate_difference'

images=os.listdir(read_dir_name_sane)

for filename in images:
    path_img_saine=os.path.join(read_dir_name_sane,filename)
    path_img_contaminee=os.path.join(read_dir_name_contaminated,filename)
    path_segmentation_manuelle=os.path.join(read_dir_manual_segmentation,filename)

    save_path_manual_segmentation_cropped=os.path.join(write_dir_name_sane,filename)
    save_path_masque_reconstruit=os.path.join(write_dir_name_contaminated,filename)
    save_path_difference_brute=os.path.join(write_dir_name_difference_brute,filename)
    save_path_difference_ouverte=os.path.join(write_dir_name_difference_ouverte,filename)

    img_saine_single=skimage.io.imread(path_img_saine)
    img_contaminee_single=skimage.io.imread(path_img_contaminee)

    img_saine_single=img_saine_single[:,:,0:3]
    img_contaminee_single=img_contaminee_single[:,:,0:3]


    img_saine_single=skimage.color.rgb2gray(img_saine_single)
    img_contaminee_single=skimage.color.rgb2gray(img_contaminee_single)

    manual_segmentation=plt.imread(path_segmentation_manuelle)
    cross_correlation=utl.cross_image_gray(img_saine_single,img_contaminee_single)

    displacement=np.unravel_index(np.argmax(cross_correlation),cross_correlation.shape)

    s=img_contaminee_single.shape

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


    nvimgsans=img_saine_single[sh0:sh1,sw0:sw1]
    nvimgavec=img_contaminee_single[ah0:ah1,aw0:aw1]
    

    segmentation_manuelle_croppee=manual_segmentation[ah0:ah1,aw0:aw1]
    

    difference=abs(nvimgsans-nvimgavec)
    matplotlib.image.imsave(save_path_manual_segmentation_cropped,difference)
    matplotlib.image.imsave(save_path_difference_brute,difference)
    difference=skimage.morphology.opening(difference, skimage.morphology.disk(2))
    #diff=skimage.morphology.closing(diff, skimage.morphology.disk(2))
    thresh=skimage.filters.threshold_otsu(difference)
    binary=difference>thresh    
    
    print("saving mask as : "+save_path_masque_reconstruit)
    matplotlib.image.imsave(save_path_masque_reconstruit,binary)
    matplotlib.image.imsave(save_path_difference_ouverte,difference)