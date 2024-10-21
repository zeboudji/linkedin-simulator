from PIL import Image
import streamlit as st

# Ajout du logo
logo = Image.open('logo.png')  # Remplace par 'images/logo.png' si tu as mis le logo dans un sous-dossier
st.image(logo, width=150)

# Titre de l'application
st.title("Simulateur de Performance LinkedIn")

# Description de l'application
st.write("""
Bienvenue dans votre simulateur de performance LinkedIn. 
Vous pouvez ajuster les valeurs avec les curseurs ou entrer manuellement les données pour obtenir des résultats précis et des conseils.
""")

# Mise en page en colonnes : gauche pour les curseurs, droite pour les résultats
col1, col2 = st.columns(2)

# Saisie des paramètres dans la première colonne (gauche)
with col1:
    st.write("### Ajustez les paramètres ci-dessous")
    
    followers = st.slider("Nombre d'abonnés", min_value=0, max_value=100000, value=5000, step=500)
    followers_manual = st.number_input("Saisie manuelle - Nombre d'abonnés", min_value=0, max_value=100000, value=followers, step=500)
    
    likes = st.slider("Nombre de likes", min_value=0, max_value=1000, value=50, step=10)
    likes_manual = st.number_input("Saisie manuelle - Nombre de likes", min_value=0, max_value=1000, value=likes, step=10)
    
    comments = st.slider("Nombre de commentaires", min_value=0, max_value=500, value=10, step=5)
    comments_manual = st.number_input("Saisie manuelle - Nombre de commentaires", min_value=0, max_value=500, value=comments, step=5)
    
    shares = st.slider("Nombre de partages", min_value=0, max_value=200, value=5, step=5)
    shares_manual = st.number_input("Saisie manuelle - Nombre de partages", min_value=0, max_value=200, value=shares, step=5)
    
    views = st.slider("Nombre de vues générées", min_value=0, max_value=100000, value=5000, step=500)
    views_manual = st.number_input("Saisie manuelle - Nombre de vues générées", min_value=0, max_value=100000, value=views, step=500)
    
    hours_since_posted = st.slider("Temps écoulé depuis la publication (en heures)", min_value=1, max_value=48, value=10)

# Calcul des engagements et du taux d'engagement
engagements = likes_manual + comments_manual + shares_manual
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
