import skimage.io
import matplotlib.pyplot as plt

def binarize(image, threshold=128):
    #revoir la fonction de binarisation car elle ne fonctionne probablement    
    
    
    return imageb

image_label=skimage.io.imread(r'C:\Users\PILLLARD-DOR\Documents\TEMPO\data\multi_focus\ground_truth\Position_0001.png')
image_binaire=binarize(image_label)
print(image_binaire.max())
print(image_binaire.min())
print(image_label[:,:,3].max())
print(image_label[:,:,3].min())
print(image_label.shape)
plt.imshow(image_binaire,cmap='gray')
plt.show()



