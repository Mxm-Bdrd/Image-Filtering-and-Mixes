import numpy as np
import matplotlib.pyplot as plt
import skimage.transform as sktr


def norm_image(image_array):
    return image_array.astype(np.float64) / 255.0


def translate_image(img, t, axis):
    # CORRECTION : S'adapte automatiquement (2D pour gris, 3D pour couleur)
    pad_width = [(0, 0)] * img.ndim
    if t > 0:
        pad_width[axis] = (t, 0)
    else:
        pad_width[axis] = (0, -t)
    pad_width = tuple(pad_width)
    return np.pad(img, pad_width, mode='constant')


def align_images(img1, img2):
    # CORRECTION : On ne prend que les 2 premières valeurs (hauteur, largeur) grâce à [:2]
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # gets two points from the user
    print('Select two points from each image define rotation, scale, translation')
    plt.imshow(img1, cmap='gray')
    x1, y1 = tuple(zip(*plt.ginput(2)))
    plt.close()
    cx1, cy1 = np.mean(x1), np.mean(y1)

    plt.imshow(img2, cmap='gray')
    x2, y2 = tuple(zip(*plt.ginput(2)))
    plt.close()
    cx2, cy2 = np.mean(x2), np.mean(y2)

    # translate first so that center of ref points is center of image
    tx = int(np.round((w1 / 2 - cx1) * 2))
    img1 = translate_image(img1, tx, axis=1)
    ty = int(np.round((h1 / 2 - cy1) * 2))
    img1 = translate_image(img1, ty, axis=0)

    tx = int(np.round((w2 / 2 - cx2) * 2))
    img2 = translate_image(img2, tx, axis=1)
    ty = int(np.round((h2 / 2 - cy2) * 2))
    img2 = translate_image(img2, ty, axis=0)

    # downscale larger image so that lengths between ref points are the same
    len1 = np.sqrt((y1[1] - y1[0]) ** 2 + (x1[1] - x1[0]) ** 2)
    len2 = np.sqrt((y2[1] - y2[0]) ** 2 + (x2[1] - x2[0]) ** 2)
    dscale = len2 / len1

    # CORRECTION : Empêche la fonction de redimensionner le canal de couleurs
    c_axis = -1 if img1.ndim == 3 else None

    if dscale < 1:
        img1 = sktr.rescale(img1, dscale, channel_axis=c_axis)
    else:
        img2 = sktr.rescale(img2, 1 / dscale, channel_axis=c_axis)

    # rotate im1 so that angle between points is the same
    theta1 = np.arctan2(-(y1[1] - y1[0]), x1[1] - x1[0])
    theta2 = np.arctan2(-(y2[1] - y2[0]), x2[1] - x2[0])
    dtheta = theta2 - theta1
    img1 = sktr.rotate(img1, dtheta * 180 / np.pi, preserve_range=True)

    # CORRECTION : Recadrage avec [:2]
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    minw = min(w1, w2)
    brd = (max(w1, w2) - minw) / 2

    if minw == w1:
        img2 = img2[:, int(np.ceil(brd)):-int(np.floor(brd))]
    else:
        img1 = img1[:, int(np.ceil(brd)):-int(np.floor(brd))]

    minh = min(h1, h2)
    brd = (max(h1, h2) - minh) / 2

    if minh == h1:
        img2 = img2[int(np.ceil(brd)):-int(np.floor(brd)), :]
    else:
        img1 = img1[int(np.ceil(brd)):-int(np.floor(brd)), :]

    return img1, img2