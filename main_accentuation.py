import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.util import img_as_float
from skimage.filters import gaussian

# .\.venv\Scripts\activate

def sharpening(image, sigma, alpha):

    originale = img_as_float(image) # Conversion en float

    filtree = gaussian(originale, sigma, channel_axis=-1) # Création de l'image filtrée par un filtre gaussien

    details = originale - filtree # Extraction des hautes fréquences (Détails = Originale - Filtrée)

    accentuee = originale + (alpha * details) # Image finale accentuée

    accentuee = np.clip(accentuee, 0, 1) # Clipping pour corriger l'erreur dans le terminal...

    return accentuee


if __name__ == '__main__': # Test

    img1 = io.imread('Albert_Einstein.png')
    img2 = io.imread('Marilyn_Monroe.png')

    img1_sharp = sharpening(img1, 2.0, 3.0)
    img2_sharp = sharpening(img2, 1.0, 2.0)

    fig, axes = plt.subplots(2, 2) # Affichage

    # Affichage image 1
    axes[0, 0].imshow(img1)
    axes[0, 0].set_title("Image 1 : Originale")
    axes[0, 0].axis('off')

    axes[0, 1].imshow(img1_sharp)
    axes[0, 1].set_title(f"Image 1 : Accentuée (Sigma=2.0)")
    axes[0, 1].axis('off')

    # Affichage image 2
    axes[1, 0].imshow(img2)
    axes[1, 0].set_title("Image 2 : Originale")
    axes[1, 0].axis('off')

    axes[1, 1].imshow(img2_sharp)
    axes[1, 1].set_title(f"Image 2 : Accentuée (Sigma=1.0)")
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig('sharpening.png', bbox_inches='tight')
    plt.show()

    plt.imsave('Albert_Einstein_sharp.png', img1_sharp, cmap='gray')
    plt.imsave('Marilyn_Monroe_sharp.png', img2_sharp, cmap='gray')