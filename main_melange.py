import numpy as np
import matplotlib.pyplot as plt
from imageio.v2 import imread
from skimage.metrics import mean_squared_error
from skimage.util import img_as_float, img_as_ubyte
from skimage.transform import resize
from main_pile import creer_piles
import os


def redimensionner(img_ref, img_a_changer):
    if img_ref.shape[:2] != img_a_changer.shape[:2]:
        return resize(img_a_changer, img_ref.shape[:2], anti_aliasing=True)
    return img_a_changer


def creer_m_rond(shape, centre=None, rayon=None):
    h, w = shape[:2]
    if centre is None: centre = (int(w / 2), int(h / 2))
    if rayon is None: rayon = min(centre[0], centre[1], w - centre[0], h - centre[1])
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - centre[0]) ** 2 + (Y - centre[1]) ** 2)
    masque = dist_from_center <= rayon
    return masque.astype(float)


def melange_multiresolution(img_A, img_B, masque, nb_niveaux=5):

    _, laplace_A = creer_piles(img_A, nb_niveaux) # juste Laplace
    _, laplace_B = creer_piles(img_B, nb_niveaux) # juste Laplace
    gauss_masque, _ = creer_piles(masque, nb_niveaux) # juste masque

    pile_melangee = []
    for i in range(nb_niveaux):
        m = gauss_masque[i]
        if img_A.ndim == 3 and m.ndim == 2:
            m = m[..., np.newaxis] # pour le masque noir et blanc

        niveau_fusionne = m*laplace_A[i] + (1-m)*laplace_B[i]
        pile_melangee.append(niveau_fusionne)

    image_finale = np.sum(pile_melangee, axis=0) # image complète
    image_finale = np.clip(image_finale, 0, 1)

    return image_finale, pile_melangee, gauss_masque, laplace_A, laplace_B


def sauvegarder_figures(laplace_A, laplace_B, gauss_masque, pile_melangee, nom_fichier):

    nb_niveaux = len(pile_melangee)
    fig, axes = plt.subplots(nb_niveaux, 3, figsize=(12, 3 * nb_niveaux))

    for i in range(nb_niveaux):
        m = gauss_masque[i]
        if laplace_A[i].ndim == 3 and m.ndim == 2:
            m = m[..., np.newaxis]
        comp_A = m * laplace_A[i]
        comp_B = (1 - m) * laplace_B[i]
        result = pile_melangee[i]
        if i < nb_niveaux - 1:
            comp_A = np.clip(comp_A + 0.5, 0, 1) #+0.5 pour pas d'image noire
            comp_B = np.clip(comp_B + 0.5, 0, 1)
            result = np.clip(result + 0.5, 0, 1)
        else:
            comp_A = np.clip(comp_A, 0, 1)
            comp_B = np.clip(comp_B, 0, 1)
            result = np.clip(result, 0, 1)

        axes[i, 0].imshow(comp_A, cmap='gray' if comp_A.ndim == 2 else None) # colonne 1
        axes[i, 0].axis('off')
        if i == 0: axes[i, 0].set_title("Masque * Laplace A")
        axes[i, 1].imshow(comp_B, cmap='gray' if comp_B.ndim == 2 else None) # colonne 2
        axes[i, 1].axis('off')
        if i == 0: axes[i, 1].set_title("(1 - Masque) * Laplace B")
        axes[i, 2].imshow(result, cmap='gray' if result.ndim == 2 else None) # colonne 3
        axes[i, 2].axis('off')
        if i == 0: axes[i, 2].set_title("Niveau Fusionné")

    plt.tight_layout()
    plt.savefig(nom_fichier, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':

    img1 = img_as_float(imread('apple.jpeg')) # Pommange
    img2 = img_as_float(imread('orange.jpeg'))
    masque = np.zeros(img1.shape[:2])
    masque[:, :img1.shape[1] // 2] = 1

    res_pom, piles_pom, mask_pom, lapA_pom, lapB_pom = melange_multiresolution(img1, img2, masque)
    plt.imsave('pommange.png', img_as_ubyte(res_pom))
    sauvegarder_figures(lapA_pom, lapB_pom, mask_pom, piles_pom, 'pommange_figure.png')


    img_fond = img_as_float(imread('bleuets.png')) # Planete remplace bleut
    img_objet = img_as_float(imread('planet.png'))
    h, w = img_fond.shape[:2]

    centre_x = int(w * 0.69)
    centre_y = int(h * 0.36)
    rayon_cercle = int(h * 0.22)
    h_p, w_p = img_objet.shape[:2]
    taille_carre = min(h_p, w_p)
    y_start, x_start = (h_p - taille_carre) // 2, (w_p - taille_carre) // 2
    planete_carree = img_objet[y_start:y_start + taille_carre, x_start:x_start + taille_carre]

    taille_finale = int(rayon_cercle * 2 * 1.15)
    img_objet_ready = resize(planete_carree, (taille_finale, taille_finale), anti_aliasing=True)
    img_incruste = np.zeros_like(img_fond)
    y1, x1 = centre_y - taille_finale // 2, centre_x - taille_finale // 2
    y2, x2 = y1 + taille_finale, x1 + taille_finale
    y1_safe, x1_safe = max(0, y1), max(0, x1)
    y2_safe, x2_safe = min(h, y2), min(w, x2)
    obj_y1, obj_x1 = y1_safe - y1, x1_safe - x1
    obj_y2, obj_x2 = obj_y1 + (y2_safe - y1_safe), obj_x1 + (x2_safe - x1_safe)
    img_incruste[y1_safe:y2_safe, x1_safe:x2_safe] = img_objet_ready[obj_y1:obj_y2, obj_x1:obj_x2]

    masque_rond = creer_m_rond(img_fond.shape, centre=(centre_x, centre_y), rayon=rayon_cercle)
    res_creatif, piles_creatif, mask_creatif, lapA_creatif, lapB_creatif = melange_multiresolution(img_incruste, img_fond, masque_rond, nb_niveaux=5)
    plt.imsave('irregulier.png', img_as_ubyte(res_creatif))
    plt.imsave('irregulier_masque.png', img_as_ubyte(masque_rond))
    sauvegarder_figures(lapA_creatif, lapB_creatif, mask_creatif, piles_creatif, 'irregulier_figures.png')


    p1 = img_as_float(imread('Portugal_maPhoto1.png')) # Portugal
    p2 = img_as_float(imread('Portugal_maPhoto2.png'))
    p2 = redimensionner(p1, p2)

    masque_p = np.zeros(p1.shape[:2])
    masque_p[:, :p1.shape[1] // 2] = 1
    res_perso, piles_perso, masque_perso, lapA_perso, lapB_perso = melange_multiresolution(p1, p2, masque_p)

    plt.imsave('Perso.png', img_as_ubyte(res_perso))
    plt.imsave('Perso_masque.png', img_as_ubyte(masque_p))
    sauvegarder_figures(lapA_perso, lapB_perso, masque_perso, piles_perso, 'Perso_figure.png')