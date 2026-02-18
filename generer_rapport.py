#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime


# =============================================================================
# CSS Styles
# =============================================================================

def obtenir_css(accent_color="#4fc3f7"):
    return f"""
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=Fira+Code:wght@400;500&display=swap');
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0; padding: 0;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh; color: #e8e8e8;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px 20px; }}
        header {{ text-align: center; padding: 40px 0; border-bottom: 2px solid rgba(255,255,255,0.1); margin-bottom: 40px; }}
        h1 {{ font-size: 2.5em; font-weight: 700; color: #fff; margin: 0 0 15px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
        .subtitle {{ font-size: 1.2em; color: #a0a0a0; margin: 0; line-height: 1.5; }}
        .date-badge {{ display: inline-block; background: rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 20px; margin-top: 20px; font-size: 0.9em; color: #b0b0b0; }}
        .image-section {{ background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius: 16px; padding: 30px; margin-bottom: 40px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.2); }}
        .image-section h2 {{ color: {accent_color}; font-size: 1.6em; margin: 0 0 25px 0; padding-bottom: 15px; border-bottom: 2px solid {accent_color}40; }}
        h3 {{ color: #e0e1dd; font-size: 1.3em; margin: 30px 0 20px 0; }}
        h3::before {{ content: ''; display: inline-block; width: 4px; height: 24px; background: {accent_color}; margin-right: 12px; border-radius: 2px; vertical-align: middle; }}
        .algorithm-box {{ background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin: 15px 0; border-left: 4px solid {accent_color}; }}
        .algorithm-box h4 {{ color: {accent_color}; margin: 0 0 10px 0; }}
        .algorithm-box p {{ margin: 5px 0; line-height: 1.6; }}

        .figure-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 20px 0; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 12px; }}
        .figure-container img {{ max-width: 80%; max-height: 500px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); cursor: zoom-in; transition: transform 0.2s; }}
        .figure-container img:hover {{ transform: scale(1.02); }}
        .figure-caption {{ margin-top: 10px; font-style: italic; color: #a0a0a0; font-size: 1em; text-align: center; }}

        .image-grid {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin: 30px 0; }}
        .image-grid-item {{ position: relative; border-radius: 12px; overflow: hidden; background: rgba(0,0,0,0.3); cursor: zoom-in; transition: transform 0.2s; flex: 0 1 400px; max-width: 100%; }}
        .image-grid-item:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.5); }}
        .image-grid-item img {{ width: 100%; height: auto; display: block; }}
        .image-grid-item .image-label {{ position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: #fff; padding: 15px 10px 10px; font-size: 0.9em; text-align: center; }}

        .lightbox {{ display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.9); animation: fadeIn 0.3s; overflow: auto; }}
        .lightbox.active {{ display: flex; align-items: center; justify-content: center; }}
        .lightbox-content {{ margin: auto; padding: 20px; display: flex; align-items: center; justify-content: center; }}
        
        .lightbox-content img {{ 
            max-width: 95vw; 
            max-height: 95vh; 
            object-fit: contain; 
            border-radius: 8px; 
            box-shadow: 0 0 30px rgba(0,0,0,0.8); 
            transition: transform 0.3s ease; 
            transform: scale(1.2); 
            cursor: zoom-out; 
        }}
        
        .lightbox-content img.fit-screen {{
            transform: scale(1);
            cursor: zoom-in;
        }}
        
        .lightbox-close {{ position: fixed; top: 20px; right: 40px; color: #fff; font-size: 40px; font-weight: bold; cursor: pointer; z-index: 10000; }}
        .lightbox-close:hover {{ color: {accent_color}; }}
        
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        footer {{ text-align: center; padding: 30px; color: #666; font-size: 0.9em; }}
    """


# =============================================================================
# Composants HTML
# =============================================================================

def document_html(titre, sous_titre, icone, contenu, accent_color="#4fc3f7"):
    date_str = datetime.now().strftime("%d %B %Y à %H:%M")
    css = obtenir_css(accent_color)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titre}</title>
    <style>{css}</style>
</head>
<body>
    <div id="lightbox" class="lightbox" onclick="closeLightbox(event)">
        <span class="lightbox-close">&times;</span>
        <div class="lightbox-content">
            <img id="lightbox-img" src="" alt="">
        </div>
    </div>

    <div class="container">
        <header>
            <h1>{icone} {titre}</h1>
            <p class="subtitle">{sous_titre}</p>
            <div class="date-badge">Généré le {date_str}</div>
        </header>

        {contenu}

        <footer></footer>
    </div>

    <script>
        function openLightbox(img) {{
            const lbImg = document.getElementById('lightbox-img');
            lbImg.src = img.src;
            lbImg.className = ''; 
            document.getElementById('lightbox').classList.add('active');
            document.body.style.overflow = 'hidden';
        }}
        
        function closeLightbox(event) {{
            const lightbox = document.getElementById('lightbox');
            if (event.target === lightbox || event.target.classList.contains('lightbox-close') || event.target.classList.contains('lightbox-content')) {{
                lightbox.classList.remove('active');
                document.body.style.overflow = 'auto';
            }}
        }}
        
        document.getElementById('lightbox-img').addEventListener('click', function(e) {{
            this.classList.toggle('fit-screen'); 
            e.stopPropagation(); 
        }});
        
        document.addEventListener('keydown', e => {{ 
            if (e.key === 'Escape') {{
                document.getElementById('lightbox').classList.remove('active');
                document.body.style.overflow = 'auto';
            }}
        }});
    </script>
</body>
</html>
"""


def section(titre, contenu, icone="📷"):
    return f'<div class="image-section"><h2><span class="icon">{icone}</span> {titre}</h2>{contenu}</div>'


def figure(chemin_img, legende="", alt=""):
    alt = alt or legende
    html_legende = f'<p class="figure-caption">{legende}</p>' if legende else ""
    return f'<div class="figure-container"><img src="{chemin_img}" alt="{alt}" onclick="openLightbox(this)">{html_legende}</div>'


def grille_images(images, titre=""):
    items = ""
    for img in images:
        items += f'<div class="image-grid-item" onclick="openLightbox(this.querySelector(\'img\'))"><img src="{img["src"]}" alt="{img["label"]}"><div class="image-label">{img["label"]}</div></div>'
    html_titre = f'<h3>{titre}</h3>' if titre else ""
    return f'{html_titre}<div class="image-grid">{items}</div>'


def boite_texte(titre, description):
    return f'<div class="algorithm-box"><h4>{titre}</h4><p>{description}</p></div>'


# =============================================================================
# Génération
# =============================================================================

def generer_rapport():
    contenu = ""


    contenu_sec0 = figure("sharpening.png", "Résultat de l'accentuation")
    contenu_sec0 += boite_texte("Explications", "Pour obtenir les images accentuées, on filtre l'image originale avec un filtre gaussien (basse fréquence). Ensuite, on soustrait l'image floue obtenue à l'originale pour obtenir les détails (hautes fréquences). Finalement, on additionne ces détails à l'originale. On peut modifier les paramètres alpha et sigma pour accentuée davantage ou flouter davantage respectivement (Accentuée = originale + alpha*détails)(Détails = originale - sigma*floue).")
    contenu += section("Sharpening", contenu_sec0, icone="📐")


    contenu_sec1 = ""
    contenu_sec2 = ""
    contenu_sec3 = ""


    images_hybrides = [
        {"src": "Hybride1.png", "label": "Albert et Marilyn"},
        {"src": "Hybride2.png", "label": "Le chien et le cheval"},
        {"src": "Hybride3.png", "label": "Mes photos du Portugal"}
    ]
    contenu_sec1 += grille_images(images_hybrides, titre="Résultats des images hybrides")

    contenu_sec1 += boite_texte("Explications",
                                "La photo hybride de Albert et Marilyn montre très bien l'effet désiré par l'algorithme. L'alignement par les yeux assurent aussi que les deux images de base soit unis. J'ai tenté de reproduire l'effet avec 2 animaux (un cheval et un chien, des images libres de droits de pexels.com). Malheureusement, l'alignement est plus compliqué pour des animaux aussi différent, mais c'est surtout le fond blanc qui gâche l'effet. Les hautes fréquences ne peuvent pas se fondent dans le décor et sont toujours visibles. J'ai réessayer avec mes propres photos de voyage pour reproduire l'effet sur deux personnes différentes prisent en photo pratiquement au même endroit. Le résultat est beaucoup mieux et l'effet est réussi (mon préféré). J'ai dû modifier plusieurs fois le sigma pour les images pour que le fondu se produise. L'analyse fréquentielle est basée sur cette image.")

    contenu_sec1 += figure("Hybride3_spectre.png", "Analyse fréquentielle de mes photos du Portugal")

    contenu_sec1 += boite_texte("Analyse fréquentielle",
                                "Dans la 1e image, l'intensité est très concentrée au centre. Les coins et les bords sont sombres, ce qui confirme que le filtre gaussien a coupé les hautes fréquences pour ne conserver que la structure globale de l'image. Dans la 2e image, le milieu est atténué par rapport au reste car on soustrait les basses fréquences. Le spectre s'étend aussi plus et je crois que c'est le cas car ma photo contient beaucoup de détails abruptes (motifs muraux). En additionnant les deux, on obtient la 3e photo où le centre est bien présent mais avec un spectre étendu également.")

    contenu_sec1 += figure("Hybride3_couleur.png", "Photos personnelles et en couleurs")

    contenu_sec1 += boite_texte("Effet de la couleur",
                                "J'ai tenté l'expérience avec mes photos en couleur. L'overlap de couleur rend l'effet beaucoup moins impressionnant. Il aurait fallu garder la couleur des basses fréquences, mais couper celles des hautes fréquences. L'effet est surtout dû au couleur des basses fréquences et la détails en nuances de gris aurait donné une bien meilleure image hybride (les couleurs des hautes fréquences sont bien moins perceptibles de toute façon).")
    contenu += section("Images hybrides", contenu_sec1, icone="🎭")


    contenu_sec2 += figure("Pile_Lincoln_Gala.png", "Piles de Gauss (haut) et de Laplace (bas) pour Lincoln et Gala")


    contenu_sec2 += boite_texte("Observations des piles de Lincoln et Gala",
                                "Dans la pile gaussienne, on voit qu'en augmentant le flou gaussien (les basses fréquences), la silhouette de Gala disparaît pour révéler le visage de Lincoln. La pile laplacienne du bas isole les hautes fréquences. On devrait donc voir seulement la silhouette de Gala dans les premières images, mais ce n'est pas le cas. Je vais réessayer avec mon image dans la Sé de Porto. ")
    contenu_sec2 += figure("Pile_Protugal.png", "Piles de Gauss et Laplace pour mon image hybride du Portugal")


    contenu_sec2 += boite_texte("Observations des piles de mon image hybride",
                                "La pile laplacienne isole mieux les détails de l'image vue de près que la pile précédente, mais on voit maintenant ce que la capsule du cours nous disait de nous méfier : du ghosting. Je devrai jouer avec les paramètres pour plus atténuer les basses fréquences dans le futur lorsqu'il y a des vêtements foncés.")

    contenu_sec2 += figure("Pyramide_Lincoln_Gala.png", "Pyramide de Gauss et Laplace pour Lincoln et Gala")

    contenu_sec2 += boite_texte("Observations des pyramides",
                                "La pyramide résultante de mon image hybride est extrêmement semblable à sa pile. J'en conclus qu'il est beaucoup plus avantageux d'utiliser un pyramide car les calculs de filtres gaussiens se font sur des images de plus en plus petites. On ne doit donc pas augmenter le sigma du filtre à chaque fois (et celui-ci augmente très très rapidement en 2^n). Je crois aussi que cela permet un meilleur stockage en mémoire à cause des images avec une résolution qui diminue au lieu de plusieurs images hautes résolution. Je ne vois pas de différence remarquable sur mes images, mais il est à noter que le sous-échantillonnage de la pyramide perd de l'information dans les hautes fréquences. En théorie, on devrait voir une petite perte de qualité (en théorie).")
    contenu += section("Piles Gaussiennes et Laplaciennes", contenu_sec2, icone="📚")


    contenu_sec3 += ''

    pommange_figures = [
        {"src": "pommange.png", "label": "La pommange"},
        {"src": "pommange_figure.png", "label": "Pile Laplacienne"}
    ]
    contenu_sec3 += grille_images(pommange_figures, titre="La pommange")

    contenu_sec3 += boite_texte("Approche",
                                "Pour reproduire l'exemple du cours, j'ai utilisé un masque vertical avec une transition nette au centre. "
                                "L'algorithme de mélange multirésolution sépare l'image en bandes de fréquences. "
                                "Dans les basses fréquences (haut de la pile), le masque devient très flou, ce qui mélange les couleurs de la pomme et de l'orange dans la zone. "
                                "Dans les hautes fréquences, la transition est plus apique."
                                "Je trouve que ça fait une fusion semi-naturelle.")

    creatif_figures = [
        {"src": "irregulier.png", "label": "Le bleuet planète"},
        {"src": "irregulier_masque.png", "label": "Masque"},
        {"src": "irregulier_figures.png", "label": "Pile Laplacienne"},
    ]
    contenu_sec3 += grille_images(creatif_figures, titre="Mélange avec masque irrégulier")

    contenu_sec3 += boite_texte("Explications",
                                "J'ai incrusté une image de la Terre à la place d'un bleuet en utilisant un masque en rond codé <strong>manuellement</strong> aux coordonnées du bleuet. "
                                "Grâce à la pile laplacienne, le contraste net du bord de la planète est semi-préservé, mais l'ajustement manuel n'est pas parfait. J'en conclus que les masques sont plus facilement fait sur Photoshop.")

    perso_figures = [
        {"src": "Perso.png", "label": "Fusion Portugal"},
        {"src": "Perso_masque.png", "label": "Masque"},
        {"src": "Perso_figure.png", "label": "Pile Laplacienne"},
    ]
    contenu_sec3 += grille_images(perso_figures, titre="Fusion de mes photos personnelles")

    contenu_sec3 += boite_texte("Explications",
                                "J'ai appliqué le procédé sur mes deux photo au Portugal."
                                "Je voulais fusionner 2 personnes verticalement dans le même décor."
                                "Les détails des deux photos sont additionnés couche par couche, mais il y a une coupure très laide à cause que les personnes ne sont pas parfaitement aligné par rapport au décors. Peut-être qu'un masque plus complexe aurait donné un meilleur résultat.")

    contenu += section("Mélange multirésolution", contenu_sec3, icone="🍄")


    sous_titre = "Photographie algorithmique<br> Maxime Bédard"

    html_final = document_html("<strong>On s'amuse en fréquences</strong> 📷", sous_titre, "📷", contenu)

    nom_fichier = "index.html"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(html_final)


if __name__ == '__main__':
    generer_rapport()