from PIL import Image
import streamlit as st

# Ajout du logo
logo = Image.open('linkedin_logo.png')  # Remplace par 'images/logo.png' si tu as mis le logo dans un sous-dossier
st.image(logo, width=150)

# Titre de l'application
st.title("Simulateur de Performance LinkedIn")

# Description de l'application
st.write("""
Bienvenue dans votre simulateur de performance LinkedIn. 
Vous pouvez ajuster les valeurs avec les curseurs ou entrer manuellement les données pour obtenir des résultats précis et des conseils.
""")

# Initialisation des valeurs dans st.session_state si elles n'existent pas
if 'followers' not in st.session_state:
    st.session_state.followers = 5000
if 'likes' not in st.session_state:
    st.session_state.likes = 0
if 'comments' not in st.session_state:
    st.session_state.comments = 0
if 'shares' not in st.session_state:
    st.session_state.shares = 0
if 'views' not in st.session_state:
    st.session_state.views = 0

# Fonction pour synchroniser les widgets
def sync_followers():
    st.session_state.followers_slider = st.session_state.followers_input

def sync_followers_slider():
    st.session_state.followers_input = st.session_state.followers_slider

def sync_likes():
    st.session_state.likes_slider = st.session_state.likes_input

def sync_likes_slider():
    st.session_state.likes_input = st.session_state.likes_slider

def sync_comments():
    st.session_state.comments_slider = st.session_state.comments_input

def sync_comments_slider():
    st.session_state.comments_input = st.session_state.comments_slider

def sync_shares():
    st.session_state.shares_slider = st.session_state.shares_input

def sync_shares_slider():
    st.session_state.shares_input = st.session_state.shares_slider

def sync_views():
    st.session_state.views_slider = st.session_state.views_input

def sync_views_slider():
    st.session_state.views_input = st.session_state.views_slider

# Mise en page en colonnes : gauche pour les curseurs, droite pour les résultats
col1, col2 = st.columns(2)

# Saisie des paramètres dans la première colonne (gauche)
with col1:
    st.write("### Ajustez les paramètres ci-dessous")
    
    st.number_input("Nombre d'abonnés", min_value=0, max_value=100000, value=st.session_state.followers, step=500, key='followers_input', on_change=sync_followers)
    st.slider("Nombre d'abonnés (Curseur)", min_value=0, max_value=100000, value=st.session_state.followers, step=500, key='followers_slider', on_change=sync_followers_slider)
    
    st.number_input("Nombre de likes", min_value=0, max_value=1000, value=st.session_state.likes, step=10, key='likes_input', on_change=sync_likes)
    st.slider("Nombre de likes (Curseur)", min_value=0, max_value=1000, value=st.session_state.likes, step=10, key='likes_slider', on_change=sync_likes_slider)
    
    st.number_input("Nombre de commentaires", min_value=0, max_value=500, value=st.session_state.comments, step=5, key='comments_input', on_change=sync_comments)
    st.slider("Nombre de commentaires (Curseur)", min_value=0, max_value=500, value=st.session_state.comments, step=5, key='comments_slider', on_change=sync_comments_slider)
    
    st.number_input("Nombre de partages", min_value=0, max_value=200, value=st.session_state.shares, step=5, key='shares_input', on_change=sync_shares)
    st.slider("Nombre de partages (Curseur)", min_value=0, max_value=200, value=st.session_state.shares, step=5, key='shares_slider', on_change=sync_shares_slider)
    
    st.number_input("Nombre de vues générées", min_value=0, max_value=100000, value=st.session_state.views, step=500, key='views_input', on_change=sync_views)
    st.slider("Nombre de vues générées (Curseur)", min_value=0, max_value=100000, value=st.session_state.views, step=500, key='views_slider', on_change=sync_views_slider)
    
    hours_since_posted = st.slider("Temps écoulé depuis la publication (en heures)", min_value=1, max_value=48, value=10)

# Récupération des valeurs synchronisées
followers = st.session_state.followers_input
likes = st.session_state.likes_input
comments = st.session_state.comments_input
shares = st.session_state.shares_input
views_manual = st.session_state.views_input

# Calcul des engagements et du taux d'engagement
engagements = likes + comments + shares
engagement_rate = (engagements / views_manual) * 100 if views_manual > 0 else 0

# Déterminer la performance actuelle du post
if views_manual < 500:
    performance = "Médiocre"
    performance_color = "red"
elif 500 <= views_manual < 1000:
    performance = "Correct"
    performance_color = "orange"
elif 1000 <= views_manual < 3000:
    performance = "Bonne"
    performance_color = "yellow"
else:
    performance = "Vrai buzz!"
    performance_color = "green"

# Projection pour une performance idéale
ideal_likes = (0.1 * views_manual) if views_manual > 0 else 100
ideal_comments = (0.05 * views_manual) if views_manual > 0 else 50
ideal_shares = (0.02 * views_manual) if views_manual > 0 else 20

# Affichage des résultats dans la deuxième colonne (droite)
with col2:
    st.subheader("Indicateurs de Performance")
    
    st.markdown(f"**Nombre total d'engagements** : {engagements}")
    st.markdown(f"**Taux d'engagement** : {engagement_rate:.2f}%")

    # Utilisation de la couleur pour la performance globale
    st.markdown(f"<span style='color:{performance_color}; font-weight:bold;'>Performance globale : {performance}</span>", unsafe_allow_html=True)

    st.subheader("Projection pour un Buzz")
    st.write(f"Pour atteindre un buzz, il vous faudrait environ :")
    st.write(f"- **{ideal_likes:.0f} likes**")
    st.write(f"- **{ideal_comments:.0f} commentaires**")
    st.write(f"- **{ideal_shares:.0f} partages**")

# Conseils personnalisés en bas
st.subheader("Conseils pour améliorer la performance")
if engagement_rate < 5:
    st.write("""
    - Engagez davantage vos abonnés : Posez des questions ou invitez-les à donner leur avis dans les commentaires.
    - Répondez à tous les commentaires : Encouragez la discussion pour maintenir l'engagement.
    - Partagez le post à des moments stratégiques : Essayez de publier quand vos abonnés sont les plus actifs.
    """)
elif engagement_rate < 10:
    st.write("""
    - Vous êtes sur la bonne voie ! Pour améliorer encore, essayez d'augmenter les interactions en ajoutant des questions ouvertes.
    - Faites des mentions ou tags pour encourager les réponses de certains abonnés.
    """)
else:
    st.write("""
    - Excellent travail ! Continuez à répondre aux commentaires pour maintenir ce niveau d'engagement.
    - Encouragez le partage du post pour atteindre encore plus d'abonnés.
    """)

# Footer
st.write("---")
st.write("Développé avec ❤️ par votre IA. Améliorez vos performances LinkedIn grâce à des projections intelligentes !")


