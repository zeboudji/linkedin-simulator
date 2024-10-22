from PIL import Image
import streamlit as st
import base64
from io import BytesIO
import pandas as pd
import requests

# --- Configuration de la page ---
st.set_page_config(
    page_title="Simulateur de Performance LinkedIn",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# --- Fonction pour encoder l'image en base64 ---
def get_image_base64(image_path):
    try:
        img = Image.open(image_path)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str
    except Exception as e:
        st.error(f"Erreur lors du chargement du logo : {e}")
        return ""

# --- Fonction pour gérer le compteur de visiteurs avec CountAPI ---
def increment_counter(namespace, key):
    url = f"https://api.countapi.xyz/hit/{namespace}/{key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['value']
        else:
            st.error(f"Erreur {response.status_code} lors de l'incrémentation du compteur de visiteurs.")
            st.error(f"Réponse de l'API : {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la connexion à CountAPI : {e}")
        return None

def get_counter(namespace, key):
    url = f"https://api.countapi.xyz/get/{namespace}/{key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('value', 0)
        else:
            st.error(f"Erreur {response.status_code} lors de la récupération du compteur de visiteurs.")
            st.error(f"Réponse de l'API : {response.text}")
            return 0
    except Exception as e:
        st.error(f"Erreur lors de la connexion à CountAPI : {e}")
        return 0

# --- Chargement et encodage du logo ---
logo_base64 = get_image_base64('linkedin_logo.png')  # Assurez-vous que le chemin vers votre logo est correct

# --- Incrémentation du compteur ---
namespace = "linkedin_simulator_unique123"  # Remplacez par votre propre namespace unique
key_counter = "visitors_unique123"  # Remplacez par votre propre clé unique
visitor_count = increment_counter(namespace, key_counter)

# --- Affichage du logo et du titre ---
st.markdown(
    f"""
    <div style='display: flex; align-items: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='100' style='margin-right: 20px;'/>
        <h1 style='color: var(--textColor);'>Simulateur de Performance LinkedIn</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Affichage du compteur de visiteurs ---
if visitor_count is not None:
    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h4>🔍 Nombre de visiteurs : {visitor_count}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Description de l'application ---
st.markdown("""
Bienvenue dans votre simulateur de performance LinkedIn.  
Ajustez les valeurs pour obtenir des résultats précis et des conseils personnalisés.
""")

# --- Initialisation des variables dans st.session_state ---
default_values = {
    'followers': 5000,
    'likes': 0,
    'comments': 0,
    'shares': 0,
    'views': 0,
    'hours_since_posted': 10
}

for key_state, value in default_values.items():
    if key_state not in st.session_state:
        st.session_state[key_state] = value

# --- Fonctions de synchronisation des widgets ---
def sync_input_with_slider(input_key, slider_key):
    st.session_state[slider_key] = st.session_state[input_key]

def sync_slider_with_input(slider_key, input_key):
    st.session_state[input_key] = st.session_state[slider_key]

# --- Fonction pour déterminer la performance et retourner l'indice ---
def determine_performance_index(value, thresholds):
    for i, threshold in enumerate(thresholds):
        if value < threshold:
            return i
    return len(thresholds)

# --- Définition des seuils et labels pour les vues ---
views_thresholds = [500, 1000, 3000]  # Médiocre, Correct, Bon, Excellent
views_labels = ["😟", "👍", "😊", "🔥"]

# --- Définition des seuils et labels pour les réactions ---
reactions_thresholds = [100, 200, 400, 500]  # Faible, Moyen, Bon, Excellent
reactions_labels = ["😟", "😐", "🙂", "🚀"]

# --- Définition des seuils, labels et icônes pour la performance globale ---
global_performance_thresholds = [500, 1000, 3000]  # Basés sur les vues
global_performance_labels = ["Médiocre", "Correct", "Bon", "Excellent"]
performance_icons_dict = {
    "Médiocre": "😟",
    "Correct": "👍",
    "Bon": "😊",
    "Excellent": "🔥"
}

# --- Couleurs associées à chaque catégorie de performance ---
performance_colors = {
    "Médiocre": "#FF4B4B",  # Rouge vif
    "Correct": "#FFA500",    # Orange
    "Bon": "#32CD32",        # Vert lime
    "Excellent": "#1E90FF"   # Bleu dodger
}

# --- Mise en page en colonnes ---
col1, col2 = st.columns([1, 1])

# --- Saisie des paramètres dans la première colonne ---
with col1:
    st.header("Paramètres")

    # Nombre d'abonnés
    st.subheader("Nombre d'abonnés")
    st.number_input(
        "Entrez le nombre d'abonnés",
        min_value=0,
        max_value=20_000,  # Ajusté pour accommoder plus d'abonnés
        value=st.session_state.followers,
        step=200,
        key='followers_input',
        on_change=sync_input_with_slider,
        args=('followers_input', 'followers_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=20_000,
        value=st.session_state.followers,
        step=200,
        key='followers_slider',
        on_change=sync_slider_with_input,
        args=('followers_slider', 'followers_input')
    )
    st.divider()

    # Nombre de vues générées
    st.subheader("Nombre de vues générées")
    st.number_input(
        "Entrez le nombre de vues",
        min_value=0,
        max_value=10_000,  # Ajusté pour accommoder plus de vues
        value=st.session_state.views,
        step=200,
        key='views_input',
        on_change=sync_input_with_slider,
        args=('views_input', 'views_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=10_000,
        value=st.session_state.views,
        step=500,
        key='views_slider',
        on_change=sync_slider_with_input,
        args=('views_slider', 'views_input')
    )
    st.divider()

    # Temps écoulé depuis la publication
    st.subheader("Temps écoulé depuis la publication (heures)")
    st.slider(
        "Temps écoulé (heures)",
        min_value=1,
        max_value=72,
        value=st.session_state.hours_since_posted,
        key='hours_since_posted'
    )
    st.divider()

    # Nombre de likes
    st.subheader("Nombre de likes")
    st.number_input(
        "Entrez le nombre de likes",
        min_value=0,
        max_value=500,
        value=st.session_state.likes,
        step=1,
        key='likes_input',
        on_change=sync_input_with_slider,
        args=('likes_input', 'likes_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=500,
        value=st.session_state.likes,
        step=1,
        key='likes_slider',
        on_change=sync_slider_with_input,
        args=('likes_slider', 'likes_input')
    )
    st.divider()

    # Nombre de commentaires
    st.subheader("Nombre de commentaires")
    st.number_input(
        "Entrez le nombre de commentaires",
        min_value=0,
        max_value=200,
        value=st.session_state.comments,
        step=1,
        key='comments_input',
        on_change=sync_input_with_slider,
        args=('comments_input', 'comments_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=200,
        value=st.session_state.comments,
        step=1,
        key='comments_slider',
        on_change=sync_slider_with_input,
        args=('comments_slider', 'comments_input')
    )
    st.divider()

    # Nombre de partages
    st.subheader("Nombre de partages")
    st.number_input(
        "Entrez le nombre de partages",
        min_value=0,
        max_value=500,
        value=st.session_state.shares,
        step=1,
        key='shares_input',
        on_change=sync_input_with_slider,
        args=('shares_input', 'shares_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=500,
        value=st.session_state.shares,
        step=1,
        key='shares_slider',
        on_change=sync_slider_with_input,
        args=('shares_slider', 'shares_input')
    )
    st.divider()

# --- Récupération des valeurs synchronisées ---
followers = st.session_state.followers_input
likes = st.session_state.likes_input
comments = st.session_state.comments_input
shares = st.session_state.shares_input
views = st.session_state.views_input
hours_since_posted = st.session_state.hours_since_posted

# --- Calculs des indicateurs ---
reactions = likes + comments + shares

# --- Normalisation des métriques ---
# Définir des valeurs maximales hypothétiques pour la normalisation
max_views = 3000  # Réduit pour augmenter la contribution des vues
max_reactions = 1000  # Exemple

# Normaliser chaque métrique
normalized_views = min(views / max_views, 1)
normalized_reactions = min(reactions / max_reactions, 1)

# --- Attribution des poids ---
# Donner un poids important aux vues (85%) et réactions (15%)
weight_views = 0.85
weight_reactions = 0.15
# Assurez-vous que la somme des poids est égale à 1 (100%)

# --- Calcul du score global ---
global_score = (
    normalized_views * weight_views +
    normalized_reactions * weight_reactions
) * 100  # Pour obtenir un score sur 100

# --- Détermination de la performance globale (basée sur les vues) ---
def determine_performance_label(views, thresholds, labels):
    for i, threshold in enumerate(thresholds):
        if views < threshold:
            return labels[i]
    return labels[-1]

global_performance = determine_performance_label(views, global_performance_thresholds, global_performance_labels)

# --- Assignation de l'icône basée sur la performance ---
performance_icon = performance_icons_dict.get(global_performance, "😐")

# --- Détermination de la couleur basée sur la performance ---
performance_color = performance_colors.get(global_performance, "#000000")  # Défaut à noir

# --- Calcul des indicateurs de performance individuels ---
reactions_perf_index = determine_performance_index(reactions, reactions_thresholds)

# --- Projection pour une performance idéale ---
# Définir des projections basées sur les vues actuelles
ideal_likes = (0.03 * views) if views > 0 else 100
ideal_comments = (0.02 * views) if views > 0 else 50
ideal_shares = (0.01 * views) if views > 0 else 20

# --- Affichage des résultats dans la deuxième colonne ---
with col2:
    st.header("Résultats")

    # Vérifier si les paramètres sont à leurs valeurs par défaut
    if (followers == default_values['followers'] and
        likes == default_values['likes'] and
        comments == default_values['comments'] and
        shares == default_values['shares'] and
        views == default_values['views'] and
        hours_since_posted == default_values['hours_since_posted']):
        st.info("En attente de vos paramètres...")
    else:
        # Indicateurs de Performance
        st.subheader("Indicateurs de Performance")

        # Utilisation de st.columns pour les indicateurs
        col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
        with col_perf1:
            st.metric("Nombre de vues", f"{views}")
            performance_index = determine_performance_index(views, views_thresholds)
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{views_labels[performance_index]}</div>", unsafe_allow_html=True)
        with col_perf2:
            st.metric("Nombre total de réactions", f"{reactions}")
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{reactions_labels[reactions_perf_index]}</div>", unsafe_allow_html=True)
        with col_perf3:
            engagement_rate = (reactions / views * 100) if views > 0 else 0
            st.metric("Taux d'engagement", f"{engagement_rate:.2f}%")
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{''}</div>", unsafe_allow_html=True)  # Pas de label pour taux d'engagement
        with col_perf4:
            st.metric("Nombre d'abonnés", f"{followers}")
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{''}</div>", unsafe_allow_html=True)  # Pas de label pour abonnés

        st.markdown("<br>", unsafe_allow_html=True)  # Espace entre les métriques et la performance globale

        # Performance globale avec icône et couleur
        st.markdown(
            f"""
            <div style='display: flex; align-items: center; background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
                <span style='font-size: 2em;'>{performance_icon}</span>
                <span style='color:{performance_color}; font-weight:bold; font-size: 1.5em; margin-left: 10px;'>
                    Performance globale : {global_performance}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)  # Espace avant la bulle d'info

        # Bulle d'info pour expliquer le calcul de la performance globale
        st.markdown(
            """
            <details>
            <summary><strong>Comment est calculée la performance globale ?</strong></summary>
            <p>La performance globale est calculée en combinant deux métriques clés :</p>
            <ul>
                <li><strong>Nombre de vues</strong> : 85% de la performance globale.</li>
                <li><strong>Nombre total de réactions</strong> (likes, commentaires, partages) : 15% de la performance globale.</li>
            </ul>
            <p>Chaque métrique est normalisée et pondérée pour obtenir un score global sur 100.</p>
            <p><strong>Formule :</strong><br>
            Performance Globale = (Vues / Max Vues) * 85 + (Réactions / Max Réactions) * 15</p>
            <p><strong>Catégories :</strong></p>
            <ul>
                <li><strong>Médiocre</strong> : < 500 vues 😟</li>
                <li><strong>Correct</strong> : < 1000 vues 👍</li>
                <li><strong>Bon</strong> : < 3000 vues 😊</li>
                <li><strong>Excellent</strong> : ≥ 3000 vues 🔥</li>
            </ul>
            </details>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # Projection pour une Performance Idéale
        st.subheader("Projection pour une Performance Idéale")
        st.write("Pour améliorer votre performance, vous pourriez viser environ :")

        # Encadré Stylisé pour la Projection
        st.markdown(
            f"""
            <div style='background-color: var(--secondaryBackgroundColor); border-left: 5px solid var(--primaryColor); padding: 15px; border-radius: 5px;'>
                <div style='display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;'>
                    <div style='text-align: center; flex: 1 1 100px; margin: 10px;'>
                        <span style='font-size: 2em;'>👍</span><br>
                        <strong>{ideal_likes:.0f} Likes</strong>
                    </div>
                    <div style='text-align: center; flex: 1 1 100px; margin: 10px;'>
                        <span style='font-size: 2em;'>💬</span><br>
                        <strong>{ideal_comments:.0f} Commentaires</strong>
                    </div>
                    <div style='text-align: center; flex: 1 1 100px; margin: 10px;'>
                        <span style='font-size: 2em;'>🔗</span><br>
                        <strong>{ideal_shares:.0f} Partages</strong>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # Conseils pour améliorer la performance
        st.subheader("Conseils pour améliorer la performance")
        if global_performance == "Médiocre":
            st.markdown("""
            - **Augmentez vos vues** : Partagez vos publications à des heures de pointe et utilisez des hashtags populaires.
            - **Stimulez les réactions** : Encouragez vos abonnés à liker et commenter en posant des questions ouvertes.
            - **Optimisez le contenu** : Publiez du contenu plus interactif et visuellement attrayant.
            """)
        elif global_performance == "Correct":
            st.markdown("""
            - **Augmentez vos vues** : Collaborez avec d'autres utilisateurs pour élargir votre audience.
            - **Maintenez les réactions** : Continuez à interagir avec les commentaires et les partages.
            - **Variez le contenu** : Intégrez des vidéos et des infographies pour diversifier vos publications.
            """)
        elif global_performance == "Bon":
            st.markdown("""
            - **Maximisez vos vues** : Utilisez des contenus visuels attractifs comme des vidéos et des infographies.
            - **Optimisez les réactions** : Proposez des appels à l'action clairs pour inciter au partage.
            - **Engagez davantage** : Répondez rapidement aux interactions et participez activement aux discussions.
            """)
        else:
            st.markdown("""
            - **Continuez vos excellentes pratiques** : Maintenez un haut niveau d'engagement et explorez de nouvelles stratégies de contenu.
            - **Développez votre réseau** : Engagez-vous avec des leaders d'opinion et participez à des discussions pertinentes.
            - **Innover** : Explorez de nouveaux formats de contenu et technologies pour rester à la pointe.
            """)

# --- Footer ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center;'>
        Développé à l'aide d'une IA sur la base du <a href='https://www.elorezo.com/r%C3%A9ussir-son-buzz-sur-linkedin-combien-faut-il-de-likes-pour-combien-de-vues' target='_blank'>blog</a> d'<a href='https://antoinejambart.com' target='_blank'>Antoine Jambart</a>.
    </div>
    """,
    unsafe_allow_html=True
)
