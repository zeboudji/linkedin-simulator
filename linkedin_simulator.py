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
engagements_thresholds = [5,10,40,50]
engagements_labels = ["😟", "😐", "🙂", "🚀"]  # Faible, Moyen, Élevé

engagement_rate_thresholds = [2, 5, 10]
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
        max_value=10_000,
        value=st.session_state.followers,
        step=200,
        key='followers_input',
        on_change=sync_input_with_slider,
        args=('followers_input', 'followers_slider')
    )
    st.slider(
        "",
        min_value=0,
        max_value=10_000,
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
        max_value=10_000,  # Ajusté pour une plus grande flexibilité
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
        max_value=2000,  # Ajusté pour une plus grande flexibilité
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

# --- Calcul du seuil de buzz dynamique ---
# Facteur de proportionnalité (par exemple, 0.6 pour obtenir 3000 vues pour 5000 abonnés)
proportion_factor = 0.6
ideal_views = int(followers * proportion_factor)

# Assurer un seuil minimum de 3000 vues
if ideal_views < 3000:
    ideal_views = 3000

# --- Calcul des indicateurs de performance ---
engagements_perf = determine_performance(engagements, engagements_thresholds, engagements_labels)
engagement_rate_perf = determine_performance(engagement_rate, engagement_rate_thresholds, engagement_rate_labels)
views_perf = determine_performance(views, views_thresholds, views_labels)

# --- Projection pour une performance idéale ---
ideal_likes = (0.1 * ideal_views) if ideal_views > 0 else 100
ideal_comments = (0.05 * ideal_views) if ideal_views > 0 else 50
ideal_shares = (0.02 * ideal_views) if ideal_views > 0 else 20

# --- Détermination de la performance actuelle du post ---
if views < 500:
    performance = "Médiocre 😟"
    performance_color = "#FF4B4B"  # Rouge vif
    performance_icon = "😟"
elif 500 <= views < 1000:
    performance = "Correct 👍"
    performance_color = "#FFA500"  # Orange
    performance_icon = "👍"
elif 1000 <= views < 3000:
    performance = "Bon 😊"
    performance_color = "#32CD32"  # Vert lime
    performance_icon = "😊"
else:
    performance = "Vrai buzz! 🔥"
    performance_color = "#1E90FF"  # Bleu dodger
    performance_icon = "🔥"

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
            st.metric("Nombre total d'engagements", f"{engagements}")
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{engagements_perf}</div>", unsafe_allow_html=True)
        with col_perf2:
            st.metric("Taux d'engagement", f"{engagement_rate:.2f}%")
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{engagement_rate_perf}</div>", unsafe_allow_html=True)
        with col_perf3:
            st.metric("Nombre de vues", f"{views}")
            st.markdown(f"<div style='text-align: center; font-size: 1em;'>{views_perf}</div>", unsafe_allow_html=True)
        with col_perf4:
            st.metric("Seuil de buzz", f"{ideal_views}")

        st.markdown("<br>", unsafe_allow_html=True)  # Espace entre les métriques et la performance globale

        # Performance globale avec icône et couleur
        st.markdown(
            f"""
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 2em;'>{performance_icon}</span>
                <span style='color:{performance_color}; font-weight:bold; font-size: 1.5em; margin-left: 10px;'>
                    Performance globale : {performance}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)  # Espace avant la bulle d'info

        # Bulle d'info pour expliquer le calcul du taux d'engagement
        st.markdown(
            """
            <details>
            <summary><strong>Comment est calculé le taux d'engagement ?</strong></summary>
            <p>Le taux d'engagement est calculé en divisant le nombre total d'engagements (likes, commentaires, partages) par le nombre total de vues, puis en multipliant par 100 pour obtenir un pourcentage.</p>
            <p><strong>Formule :</strong><br>
            Taux d'engagement (%) = (Engagements / Vues) * 100</p>
            </details>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # Projection pour un Buzz
        st.subheader("Projection pour un Buzz")
        st.write("Pour atteindre un buzz, il vous faudrait environ :")

        # Encadré Stylisé pour la Projection
        st.markdown(
            f"""
            <div style='background-color: var(--secondaryBackgroundColor); border-left: 5px solid var(--primaryColor); padding: 15px; border-radius: 5px;'>
                <div style='display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;'>
                    <div style='text-align: center; flex: 1 1 100px; margin: 10px;'>
                        <span style='font-size: 2em;'>👀</span><br>
                        <strong>{ideal_views} Vues</strong>
                    </div>
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
        if engagement_rate < 5:
            st.markdown("""
            - **Engagez davantage vos abonnés** : Posez des questions ou invitez-les à donner leur avis dans les commentaires.
            - **Répondez à tous les commentaires** : Encouragez la discussion pour maintenir l'engagement.
            - **Partagez le post à des moments stratégiques** : Publiez lorsque vos abonnés sont les plus actifs.
            - **Meilleurs moments pour publier** :
                - **Jours** : Mardi et jeudi.
                - **Heures** : Entre 10h et 11h.
            - **Stratégies supplémentaires** :
                - **Type de Contenu** : Publiez plus de contenus visuels ou interactifs.
                - **Utilisation des Hashtags** : Utilisez des hashtags pertinents et populaires.
            """)
        elif engagement_rate < 10:
            st.markdown("""
            - **Vous êtes sur la bonne voie !** Pour améliorer encore, augmentez les interactions en posant des questions ouvertes.
            - **Mentionnez ou taguez** des personnes pour encourager leur participation.
            - **Optimisez vos horaires de publication** :
                - **Jours** : Mardi, mercredi et jeudi.
                - **Heures** : Entre 9h et 12h.
            - **Stratégies supplémentaires** :
                - **Type de Contenu** : Variez les formats (vidéos, infographies).
                - **Utilisation des Hashtags** : Intégrez des hashtags de niche pour toucher une audience spécifique.
            """)
        else:
            st.markdown("""
            - **Excellent travail !** Continuez à répondre aux commentaires pour maintenir ce niveau d'engagement.
            - **Encouragez le partage du post** pour atteindre encore plus d'abonnés.
            - **Maximisez l'impact de vos publications** :
                - **Jours** : Mardi et jeudi.
                - **Heures** : Entre 8h et 10h ou entre 12h et 14h.
            - **Stratégies supplémentaires** :
                - **Type de Contenu** : Publiez des contenus exclusifs ou en avant-première.
                - **Utilisation des Hashtags** : Créez et promouvez un hashtag de marque unique.
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
