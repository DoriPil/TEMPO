print("starting stack method ")

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


    read_dir_name_sane=os.path.join(data_folder,r"multi_focus\raw\clean")
    read_dir_name_contaminated=os.path.join(data_folder,r"multi_focus\raw\contaminated")
    read_dir_manual_segmentation=os.path.join(data_folder,r'multi_focus\ground_truth')
    write_dir_manual_segmentation_cropped=os.path.join(results_folder,r'stack_method\cropped_ground_truth')
    write_dir_name_difference_brute=os.path.join(results_folder,r'stack_method\raw_difference')
    write_dir_name_difference_ouverte=os.path.join(results_folder,r'stack_method\intermediate_difference')
    #write_dir_name_image_intermédiaire=os.oath.join(data_folder,r'C:\Users\PILLLARD-DOR\Documents\scripts_thèse\images_qualite\benchmark_images\masque_intermédiaire_pile')
    write_dir_name_image_reconstruite=os.path.join(results_folder,r'stack_method\automatic_segmentation')

    images=os.listdir(read_dir_name_sane)

    for filename in images:
        filename_png=filename[:-4]+".png"
        path_img_saine=os.path.join(read_dir_name_sane,filename)
        path_img_contaminee=os.path.join(read_dir_name_contaminated,filename)
        path_segmentation_manuelle=os.path.join(read_dir_manual_segmentation,filename_png)

        print("loading "+filename)

        save_path_difference_brute=os.path.join(write_dir_name_difference_brute,filename_png)
        save_path_difference_ouverte=os.path.join(write_dir_name_difference_ouverte,filename_png)
        save_path_manual_segmentation_cropped=os.path.join(write_dir_manual_segmentation_cropped,filename_png)
        #save_path_masque_intermédiaire=os.path.join(write_dir_name_image_intermédiaire,filename)
        save_path_masque_reconstruit=os.path.join(write_dir_name_image_reconstruite,filename)

        save_path_difference_brute=save_path_difference_brute[:-4]
        save_path_difference_ouverte=save_path_difference_ouverte[:-4]
        #save_path_masque_intermédiaire=save_path_masque_intermédiaire[:-4]
        save_path_masque_reconstruit=save_path_masque_reconstruit[:-4]
        save_path_masque_reconstruit=save_path_masque_reconstruit+".png"
        save_path_difference_ouverte=save_path_difference_ouverte+".png"

        flag=True
        score=0
        #index=39
        sens="Incrémentation"
        index_retenu=0
        for index in range(0,75):

            # Boucle permettant de faire le recalage vertical grâce au SSIM
            # Cette partie prend du temps et peut potentiellement être otpimisée en faisant des hypothèses appropriées sur l'évolution du SSIM sur l'ensemble de la pile

            img_saine_stack=io.imread(path_img_saine)
            img_contaminee_stack=io.imread(path_img_contaminee)
            img_contaminee_single=img_contaminee_stack[39,:,:]
            img_saine_single=img_saine_stack[index,:,:]
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

            (sim_score,diff)=skimage.metrics.structural_similarity(nvimgsans,nvimgavec,full=True)

            
            if(score==0):
                score=sim_score
            if(sim_score>score):
                score=sim_score
                index_retenu=index

            print("Image Similarity: {:.4f}%".format(score*100))
            print("Score calculé actuel: {:.4f}%".format(sim_score*100))

        print("score final retenu: {:.4f}%".format(score*100))
        print("index final retenu: {:.4f}".format(index_retenu))

        img_saine_stack=io.imread(path_img_saine)
        img_contaminee_stack=io.imread(path_img_contaminee)

        # Sélection de l'image contaminée au point et de l'image saine qui lui est le plus similaire comme calculé précédemment

        img_contaminee_single=img_contaminee_stack[39,:,:]
        img_saine_single=img_saine_stack[index_retenu,:,:]
        manual_segmentation=plt.imread(path_segmentation_manuelle)

        # Estimation du déplacement X et Y par corrélation croisée
        cross_correlation=utl.cross_image_gray(img_saine_single,img_contaminee_single)

        displacement=np.unravel_index(np.argmax(cross_correlation),cross_correlation.shape)

        # Croppage/recalage des images pour qu'elles se superposent le plus précisément possible
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

        difference=abs(nvimgsans-nvimgavec)

        # Calcul de l'image de différence

        (sim_score,diff)=skimage.metrics.structural_similarity(nvimgsans,nvimgavec,full=True)
        diff=(diff*255).astype("uint8")
        diff=255-diff
        print(diff.shape)
        segmentation_manuelle_croppee=manual_segmentation[ah0:ah1,aw0:aw1]
        matplotlib.image.imsave(save_path_manual_segmentation_cropped,segmentation_manuelle_croppee)
        
        matplotlib.image.imsave(save_path_difference_brute+".png",diff,cmap='gray')
        diff=skimage.morphology.opening(diff,skimage.morphology.disk(2))
        matplotlib.image.imsave(save_path_difference_ouverte,diff,cmap='gray')

        # Seuillage automatique de l'image

        thresh=skimage.filters.threshold_otsu(diff)
        binary=diff>thresh

        # Opérations morphologiques pour récupérer et corriger les masques binaires
        
        binary_opening=skimage.morphology.opening(binary,skimage.morphology.disk(4))
        binary_opening=skimage.morphology.area_opening(binary_opening,1000)
        binary_reconstruction=skimage.morphology.reconstruction(binary_opening,binary,"dilation")
        binary_reconstruction=skimage.morphology.closing(binary_reconstruction,skimage.morphology.disk(4))
        matplotlib.image.imsave(save_path_masque_reconstruit,binary_reconstruction,cmap="gray")
        """
        diff=(diff*255).astype("uint8")
        #diff=skimage.morphology.opening(diff, skimage.morphology.disk(2)) #revoir la ligne de code, car l'ouverture n'est pas prise en compte
        #matplotlib.image.imsave(save_path_difference_ouverte,diff+".png",cmap='gray')
        #diff=skimage.morphology.closing(diff, skimage.morphology.disk(2))

        print("saving mask as : "+save_path_masque_reconstruit+".png")
        #matplotlib.image.imsave(save_path_masque_reconstruit+".png",mask)
        diff=255-diff
        diff=skimage.morphology.closing(diff, skimage.morphology.disk(2))
        matplotlib.image.imsave(save_path_difference_ouverte,diff,cmap="gray")
        thresh=skimage.filters.threshold_otsu(diff)
        binary=diff>thresh
        binary_opening=skimage.morphology.opening(binary,skimage.morphology.disk(4))

        binary_opening=skimage.morphology.area_opening(binary_opening,1000)
        binary_reconstruction=skimage.morphology.reconstruction(binary_opening,binary,"dilation")
        binary_reconstruction=skimage.morphology.closing(binary_reconstruction,skimage.morphology.disk(4))

        seed = np.copy(binary_reconstruction)
        seed[1:-1, 1:-1] = binary_reconstruction.max()
        mask = binary_reconstruction
        
        filled = skimage.morphology.reconstruction(seed, mask, method='erosion')
        matplotlib.image.imsave(save_path_masque_reconstruit,binary)

        closed=skimage.morphology.closing(filled,skimage.morphology.disk(3))

        seed = np.copy(closed)
        seed[1:-1, 1:-1] = closed.max()
        mask = closed

        filled=skimage.morphology.reconstruction(seed,mask,method="erosion")

        #markers=np.zeros_like(nvimgavec,dtype=nvimgavec.dtype)
        #markers[binary_opening]=nvimgavec[binary_opening]

        #reconstruction=skimage.morphology.reconstruction(markers,nvimgavec,"dilation")

        
        print("saving mask as : "+save_path_masque_reconstruit)
        #matplotlib.image.imsave(save_path_masque_reconstruit,binary)
        """
        print("saving image as: "+save_path_masque_reconstruit)

if __name__=="__main__":
    main()

        