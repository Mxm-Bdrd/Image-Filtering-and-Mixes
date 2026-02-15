import numpy as np
import matplotlib.pyplot as plt
from imageio.v2 import imread
from skimage.util import img_as_float
from skimage.filters import gaussian
from skimage.color import rgb2gray

from align_images import align_images
from crop_image import crop_image


def hybrid_image(img1, img2, sigma1, sigma2):
    img1 = img_as_float(img1)
    img2 = img_as_float(img2)

    b_frequences = gaussian(img1, sigma1, channel_axis=-1)
    h_frequences = img2 - gaussian(img2, sigma2, channel_axis=-1)

    hybride = b_frequences + h_frequences
    hybride = np.clip(hybride, 0, 1)

    return b_frequences, h_frequences, hybride


def fourier(image):
    if image.ndim == 3:
        image = rgb2gray(image)
    return np.log(np.abs(np.fft.fftshift(np.fft.fft2(image))) + 1e-9) # Pour le rapport


if __name__ == '__main__': # Test

    img1 = imread('Portugal_maPhoto1.png', mode='RGB')
    img2 = imread('Portugal_maPhoto2.png', mode='RGB')
    img1, img2 = align_images(img2, img1) # Alignement

    coupure_low = 4.0
    coupure_high = 10.0

    b_freq, h_freq, hybride = hybrid_image(img1, img2, coupure_low, coupure_high)
    hybride_cropped = crop_image(hybride) # Crop

    plt.figure(figsize=(10, 5)) # Images
    plt.subplot(1, 3, 1)
    plt.imshow(b_freq)
    plt.title('Basses Fréquences')
    plt.subplot(1, 3, 2)
    plt.imshow(h_freq + 0.5)
    plt.title('Hautes Fréquences')
    plt.subplot(1, 3, 3)
    plt.imshow(hybride_cropped)
    plt.title('Image Hybride Recadrée')
    #plt.savefig('Hybride3_couleur.png', bbox_inches='tight')
    plt.show()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5)) # Spectres
    axes[0].imshow(fourier(b_freq), cmap='viridis')
    axes[0].set_title('Spectre Passe-Bas')
    axes[1].imshow(fourier(h_freq), cmap='viridis')
    axes[1].set_title('Spectre Passe-Haut')
    axes[2].imshow(fourier(hybride), cmap='viridis')
    axes[2].set_title('Spectre Hybride')
    plt.tight_layout()
    #plt.savefig('Hybride3_spectre.png', bbox_inches='tight')
    plt.show()