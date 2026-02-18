import numpy as np
import matplotlib.pyplot as plt
from imageio.v2 import imread
from skimage.util import img_as_float
from skimage.filters import gaussian
from skimage.transform import resize


def creer_pyramides(image, nb_niveaux=5):

    image = img_as_float(image)
    c_axis = -1 if image.ndim == 3 else None
    taille_originale = image.shape[:2]  # taille normale

    pyramide_gaussienne = [image]
    img_courante = image
    for i in range(1, nb_niveaux):
        img_floue = gaussian(img_courante, sigma=2.0, channel_axis=c_axis)
        img_reduite = img_floue[::2, ::2]
        pyramide_gaussienne.append(img_reduite)
        img_courante = img_reduite

    pyramide_laplacienne = []
    for i in range(nb_niveaux - 1):
        taille_cible = pyramide_gaussienne[i].shape[:2]
        img_suivante_agrandie = resize(pyramide_gaussienne[i + 1], taille_cible, order=1, anti_aliasing=False)
        details = pyramide_gaussienne[i] - img_suivante_agrandie
        pyramide_laplacienne.append(details)

    pyramide_laplacienne.append(pyramide_gaussienne[-1])
    gauss_taille = [resize(img, taille_originale, order=1, anti_aliasing=False) for img in pyramide_gaussienne]
    laplace_taille = [resize(img, taille_originale, order=1, anti_aliasing=False) for img in
                             pyramide_laplacienne]

    return gauss_taille, laplace_taille


def creer_piles(image, nb_niveaux=5):

    image = img_as_float(image)

    pile_gaussienne = [image] # Première image de la pile

    c_axis = -1 if image.ndim == 3 else None
    for i in range(1, nb_niveaux): # pile gaussienne
        sigma = 2**i
        img_floue = gaussian(image, sigma=sigma, channel_axis=c_axis)
        pile_gaussienne.append(img_floue)

    pile_laplacienne = []
    for i in range(nb_niveaux - 1): # pile laplacienne
        details = pile_gaussienne[i] - pile_gaussienne[i + 1]
        pile_laplacienne.append(details)
    pile_laplacienne.append(pile_gaussienne[-1]) # dernière de la pile

    return pile_gaussienne, pile_laplacienne


def sauvegarder(pile_gauss, pile_laplace, nom_fichier_sortie):

    gauss_visuelle = [np.clip(img, 0, 1) for img in pile_gauss]
    laplace_visuelle = []
    for i in range(len(pile_laplace)):
        if i == len(pile_laplace) - 1:
            laplace_visuelle.append(np.clip(pile_laplace[i], 0, 1))
        else:
            laplace_visuelle.append(np.clip(pile_laplace[i] + 0.5, 0, 1)) # +0.5 pour le fond

    ligne_gauss = np.hstack(gauss_visuelle)
    ligne_laplace = np.hstack(laplace_visuelle)
    image_grille = np.vstack([ligne_gauss, ligne_laplace])

    if image_grille.ndim == 2:
        plt.imsave(nom_fichier_sortie, image_grille, cmap='gray')
    else:
        plt.imsave(nom_fichier_sortie, image_grille)


if __name__ == '__main__': # Test

    img_dali = imread('Dali.png') # Pile 1 avec Dali
    gauss_dali, laplace_dali = creer_piles(img_dali, nb_niveaux=5)
    #sauvegarder(gauss_dali, laplace_dali, 'Pile_Lincoln_Gala.png')

    img_hybride = imread('ImagePerso.png', mode='L') # Pile 2 avec ma photo hybride
    gauss_hybride, laplace_hybride = creer_piles(img_hybride, nb_niveaux=5)
    #sauvegarder(gauss_hybride, laplace_hybride, 'Pile_Protugal.png')

    gauss_pyr, laplace_pyr = creer_pyramides(img_dali, nb_niveaux=5)
    #sauvegarder(gauss_pyr, laplace_pyr, 'Pyramide_Lincoln_Gala.png')