import numpy as np
import scipy.signal
import skimage
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import ndimage
from matplotlib import cm
from scipy.optimize import curve_fit
from skimage.measure import regionprops

def supremum(I,J,shape):
    masquee=np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            masquee[i,j]=max(I[i,j],J[i,j])
    return masquee


def infimum(I,J,shape):
    masquee=np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            masquee[i,j]=min(I[i,j],J[i,j])
    return masquee

def cross_image(im1,im2):
    
    im1_gray=np.sum(im1.astype("float"),axis=2)
    im2_gray=np.sum(im2.astype("float"),axis=2)

    # soustraction de la moyenne pour améliorer les résultats de la corrélation
    im1_gray-=np.mean(im1_gray)
    im2_gray-=np.mean(im2_gray)

    # calcul de l'image de corrélation
    return scipy.signal.fftconvolve(im1_gray,im2_gray[::-1,::-1],mode='same')

def cross_image_gray(im1,im2):

    # soustraction de la moyenne pour améliorer les résultats de la corrélation
    im1-=np.mean(im1,dtype='uint8')
    im2-=np.mean(im2,dtype='uint8')

    # calcul de l'image de corrélation
    return scipy.signal.fftconvolve(im1,im2[::-1,::-1],mode='same')

def extractTexture(I, Z):
    """
    Extract texture from stack of images I, where Z is the index (altitude)
    I: stack of images, of shape (n, X, Y)
    Z: index of SFF maximum (of shape(X,Y)), values are between 0 and n-1
    returns basically I[Z(i,j)] for all (i,j)
    """

    m,n=I.shape[1:]
    ii,jj=np.ogrid[:m,:n]
    T=I[Z,ii,jj]
    return T

def sml(I, N):
    """
    SFF measure, sum of modified Laplacian
    I: image
    N: neighbourhood size
    returns: SFF measure for each pixel
    """

    h=np.array([[-1,2,-1]])
    ML=np.abs(ndimage.convolve(I,h))+np.abs(ndimage.convolve(I,np.transpose(h)))
    S=ndimage.uniform_filter(ML,N)
    return S

def variance(I,N):
    """
    SFF measure
    I: image
    N: neighbourhood size
    returns: SFF measure for each pixel, result is the same shape as I
    """

    M=ndimage.uniform_filter(I,N)
    D2=(I-M)**2
    V=ndimage.uniform_filter(D2,N)
    return V

def tenengrad(I,N):
    """
    SFF measure, variance of Tenengrad
    I: image
    N: neighborhood size
    returns: SFF measure for each pixel
    """
    Sx=ndimage.sobel(I,axis=0)
    Sy=ndimage.sobel(I,axis=1)
    S=np.hypot(Sx,Sy)
    vt=variance(S,N)
    return vt

def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


def gaussian_fit_column(column):
    """
    Gaussian fitting for data in the form of a N-by-1 matrix and returning the mean value for the computed gaussian curve
    """

    x=np.array(range(13))
    n=len(x)
    mu=sum(x*column)/n
    sigma=sum(column*(x-mu)**2)/n
    popt,pcov=curve_fit(gaus,x,column,p0=[1,mu,sigma])
    plt.plot(x,column,'b+:',label='data')
    plt.plot(x,gaus(x,*popt),'ro:',label='fit')
    plt.legend()
    plt.title('Fig 1 - Fit for True Elevation')
    plt.xlabel('Elevation')
    plt.ylabel('Sharpness')
    plt.show()

def calculate_diameter_average(mask):
    """
    
    Calcule le diamètre moyen des objets dans une image de masques
    
    mask : images de masques labellisés
    
    Retourne: diamètre moyen en pixels"""

    regions=regionprops(mask)
    if len(regions)==0:
        return 0
    diameters=[]
    for region in regions:
        area=region.area
        diameter=2*np.sqrt(area/np.pi)
        diameters.append(diameter)
    return np.mean(diameters)
    
def detect_difference_pile(image_sans,image_contaminee, numero_mise_au_point):
    """
    
    Annotation des images de contamination en les comparant au fond de gaine sans contamination
    image_sans: pile d'images .tif du fond de la gaine sans contamination particulaire
    image_contaminee: pile d'images .tif avec contamination particulaire
    numero_mise_au_point: indice dans la pile image_contaminee auquel la mise au point a été faite par le microscope

    Retourne: masque de l'annotation labelisée
    """
    img=image_contaminee[39,:,:]
    score_bef=0
    level_init=39
    level=39
    flag=True
    going_up=True
    increment=1
    incrementing=True
    decrementing=False
    decrement=-1
    while(flag):
        imgsans=image_sans[level,:,:]
        (score,diff)=skimage.metrics.structural_similarity(nvimgsans,nvimg,full=True)
        if(score>score_bef & incrementing):
            score_bef=score
            level+=1
        else:
            incrementing=False
            decrementing=True
            level=38
        if(score>score_bef & decrementing):
            score_bef=score
            level+=-1
        else:
            flag=False
    




