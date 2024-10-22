from PIL import Image
import streamlit as st
import base64
from io import BytesIO
import pandas as pd  # Si vous utilisez des graphiques

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

# --- Chargement et encodage du logo ---
logo_base64 = get_image_base64('linkedin_logo.png')  # Assurez-vous que le chemin vers votre logo est correct

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

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Fonctions de synchronisation des widgets ---
def sync_input_with_slider(input_key, slider_key):
    st.session_state[slider_key] = st.session_state[input_key]

def sync_slider_with_input(slider_key, input_key):
    st.session_state[input_key] = st.session_state[slider_key]

# --- Fonction pour déterminer la performance ---
def determine_performance(value, thresholds, labels):
    for threshold, label in zip(thresholds, labels):
        if value < threshold:
            return label
    return labels[-1]

# --- Définition des seuils et labels pour chaque métrique avec émoticônes ---
engagements_thresholds = [5, 10, 40, 50]  # Ajusté pour plus de granularité
engagements_labels = ["😟", "😐", "🙂", "🚀"]  # Faible, Moyen, Bon, Excellent

engagement_rate_thresholds = [1, 2, 4, 10]
engagement_rate_labels = ["😕", "👍", "😊", "🚀"]  # À améliorer, Correct, Bon, Excellent

views_thresholds = [500, 1000, 3000]
views_labels = ["😟", "👍", "😊", "🔥"]  # Médiocre, Correct, Bon, Vrai buzz!

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
        max_value=100_000,
        value=st.session_state.followers,
        step=200,
        key='followers_input',
        on_change=sync_input_with_slider,
        args=('followers_input', 'followers_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=100_000,
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
        max_value=10_000,
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
        max_value=2000,
        value=st.session_state.likes,
        step=1,
        key='likes_input',
        on_change=sync_input_with_slider,
        args=('likes_input', 'likes_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=2000,
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
        max_value=1000,
        value=st.session_state.comments,
        step=1,
        key='comments_input',
        on_change=sync_input_with_slider,
        args=('comments_input', 'comments_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=1000,
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
engagements = likes + comments + shares
engagement_rate = (engagements / views) * 100 if views > 0 else 0

# --- Normalisation des métriques ---
# Définir des valeurs maximales hypothétiques pour la normalisation
max_views = 5_000  # Ajusté pour que 1 500 vues pour 5 000 abonnés tombe dans "Bon"
max_engagements = 1_000  # Exemple
max_engagement_rate = 20  # 20%
max_followers = 100_000  # Exemple
max_hours = 72  # Maximum du slider

# Normaliser chaque métrique
normalized_views = min(views / max_views, 1)
normalized_engagements = min(engagements / max_engagements, 1)
normalized_engagement_rate = min(engagement_rate / max_engagement_rate, 1)
normalized_followers = min(followers / max_followers, 1)
normalized_time = min((max_hours - hours_since_posted) / max_hours, 1)  # Plus le temps est court, plus le score est élevé

# --- Attribution des poids ---
# Donner un poids important aux vues
weight_views = 0.40
weight_engagements = 0.25
weight_engagement_rate = 0.20
weight_followers = 0.10
weight_time = 0.05
# Assurez-vous que la somme des poids est égale à 1 (100%)

# --- Calcul du score global ---
global_score = (
    normalized_views * weight_views +
    normalized_engagements * weight_engagements +
    normalized_engagement_rate * weight_engagement_rate +
    normalized_followers * weight_followers +
    normalized_time * weight_time
) * 100  # Pour obtenir un score sur 100

# --- Définition des seuils pour la performance globale ---
global_performance_thresholds = [35, 60, 80]
global_performance_labels = ["😟", "😐", "🙂", "🔥"]  # Médiocre, Correct, Bon, Excellent

# --- Détermination de la performance globale ---
global_performance = determine_performance(global_score, global_performance_thresholds, global_performance_labels)

# --- Couleurs associées à chaque catégorie de performance ---
performance_colors = {
    "😟": "#FF4B4B",  # Rouge vif
    "😐": "#FFA500",  # Orange
    "🙂": "#32CD32",  # Vert lime
    "🔥": "#1E90FF"   # Bleu dodger
}

# --- Détermination de la couleur basée sur la performance ---
performance_color = performance_colors.get(global_performance, "#FFFFFF")

# --- Détermination de l'icône basée sur la performance ---
performance_icon = global_performance

# --- Calcul des indicateurs de performance individuels ---
engagements_perf = determine_performance(engagements, engagements_thresholds, engagements_labels)
engagement_rate_perf = determine_performance(engagement_rate, engagement_rate_thresholds, engagement_rate_labels)
views_perf = determine_performance(views, views_thresholds, views_labels)

# --- Projection pour une performance idéale ---
# Définir des projections basées sur les vues actuelles
ideal_likes = (0.1 * views) if views > 0 else 100
ideal_comments = (0.05 * views) if views > 0 else 50
ideal_shares = (0.02 * views) if views > 0 else 20

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
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{views_perf}</div>", unsafe_allow_html=True)
        with col_perf2:
            st.metric("Nombre total d'engagements", f"{engagements}")
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{engagements_perf}</div>", unsafe_allow_html=True)
        with col_perf3:
            st.metric("Taux d'engagement", f"{engagement_rate:.2f}%")
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{engagement_rate_perf}</div>", unsafe_allow_html=True)
        with col_perf4:
            st.metric("Nombre d'abonnés", f"{followers}")

        st.markdown("<br>", unsafe_allow_html=True)  # Espace entre les métriques et la performance globale

        # Performance globale avec icône et couleur
        st.markdown(
            f"""
            <div style='display: flex; align-items: center;'>
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
            <p>La performance globale est calculée en combinant plusieurs métriques clés :</p>
            <ul>
                <li><strong>Nombre de vues</strong> : Nombre total de vues de la publication.</li>
                <li><strong>Nombre total d'engagements</strong> : Somme des likes, commentaires et partages.</li>
                <li><strong>Taux d'engagement</strong> : (Engagements / Vues) * 100.</li>
                <li><strong>Nombre d'abonnés</strong> : Nombre total d'abonnés de votre profil.</li>
                <li><strong>Temps écoulé depuis la publication</strong> : Nombre d'heures écoulées depuis la publication.</li>
            </ul>
            <p>Chaque métrique est normalisée et pondérée pour obtenir un score global sur 100.</p>
            <p><strong>Formule :</strong><br>
            Performance Globale = (Vues / Max Vues) * 40 + (Engagements / Max Engagements) * 25 + (Taux d'engagement / Max Taux d'engagement) * 20 + (Abonnés / Max Abonnés) * 10 + ((Max heures - Heures écoulées) / Max heures) * 5</p>
            </details>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # Projection pour une performance idéale
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
        if global_score < 50:
            st.markdown("""
            - **Augmentez vos vues et engagements** : Encouragez vos abonnés à liker, commenter et partager vos publications.
            - **Optimisez vos horaires de publication** : Publiez lorsque vos abonnés sont les plus actifs.
            - **Améliorez le contenu** : Publiez du contenu plus interactif et visuellement attrayant.
            - **Utilisez des hashtags pertinents** pour augmenter la visibilité.
            - **Engagez-vous avec votre communauté** : Répondez aux commentaires et participez aux discussions.
            """)
        elif global_score < 70:
            st.markdown("""
            - **Continuez à augmenter vos vues et engagements** : Posez des questions ouvertes pour stimuler les discussions.
            - **Variez le type de contenu** : Intégrez des vidéos, infographies et autres formats interactifs.
            - **Analysez les performances passées** : Identifiez ce qui fonctionne et ajustez votre stratégie en conséquence.
            - **Utilisez des hashtags de niche** pour toucher une audience plus ciblée.
            """)
        elif global_score < 85:
            st.markdown("""
            - **Maintenez vos bonnes pratiques** : Continuez à publier du contenu engageant et pertinent.
            - **Encouragez le partage** : Incitez vos abonnés à partager vos publications pour augmenter votre portée.
            - **Collaborez avec d'autres utilisateurs** : Participez à des collaborations pour élargir votre audience.
            - **Utilisez des appels à l'action** pour inciter à l'engagement.
            """)
        else:
            st.markdown("""
            - **Excellent travail !** Continuez à maintenir votre haut niveau d'engagement.
            - **Maximisez l'impact de vos publications** en publiant du contenu exclusif ou en avant-première.
            - **Développez votre marque personnelle** en créant un hashtag unique et en le promouvant.
            - **Interagissez régulièrement** avec votre communauté pour renforcer les relations.
            - **Analysez et ajustez continuellement** votre stratégie pour rester performant.
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
