import streamlit as st

# Titre de l'application
st.title("Simulateur de Performance LinkedIn")

# Description de l'application
st.write("""
Bienvenue dans votre simulateur de performance LinkedIn. 
Ajustez les curseurs ci-dessous pour saisir vos données réelles ou estimées et obtenez des conseils 
pour améliorer la performance de votre post !
""")

# Saisie des paramètres via curseurs
followers = st.slider("Nombre d'abonnés", min_value=0, max_value=100000, value=5000, step=500)
likes = st.slider("Nombre de likes", min_value=0, max_value=1000, value=50, step=10)
comments = st.slider("Nombre de commentaires", min_value=0, max_value=500, value=10, step=5)
shares = st.slider("Nombre de partages", min_value=0, max_value=200, value=5, step=5)
views = st.slider("Nombre de vues générées", min_value=0, max_value=100000, value=5000, step=500)
hours_since_posted = st.slider("Temps écoulé depuis la publication (en heures)", min_value=1, max_value=48, value=10)

# Calcul de la portée actuelle et du taux d'engagement
engagements = likes + comments + shares
engagement_rate = (engagements / views) * 100 if views > 0 else 0

# Déterminer la performance actuelle du post
if views < 500:
    performance = "Médiocre"
elif 500 <= views < 1000:
    performance = "Correct"
elif 1000 <= views < 3000:
    performance = "Bonne"
else:
    performance = "Vrai buzz!"

# Projection pour une performance idéale (pour atteindre un buzz)
ideal_likes = (0.1 * views) if views > 0 else 100
ideal_comments = (0.05 * views) if views > 0 else 50
ideal_shares = (0.02 * views) if views > 0 else 20

# Affichage des résultats de performance actuelle
st.subheader("Performance Actuelle")
st.write(f"**Nombre total d'engagements** : {engagements}")
st.write(f"**Taux d'engagement** : {engagement_rate:.2f}%")
st.write(f"**Évaluation de la performance globale** : {performance}")

# Affichage de la projection idéale
st.subheader("Projection idéale pour un Buzz")
st.write(f"Pour atteindre une performance de buzz, il vous faudrait environ :")
st.write(f"- **{ideal_likes:.0f} likes**")
st.write(f"- **{ideal_comments:.0f} commentaires**")
st.write(f"- **{ideal_shares:.0f} partages**")

# Conseils personnalisés pour améliorer la performance
st.subheader("Conseils pour améliorer la performance")
if engagement_rate < 5:
    st.write("""
    - **Engagez davantage vos abonnés** : Posez des questions ou invitez-les à donner leur avis dans les commentaires.
    - **Répondez à tous les commentaires** : Encouragez la discussion pour maintenir l'engagement.
    - **Partagez le post à des moments stratégiques** : Essayez de publier quand vos abonnés sont les plus actifs.
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
