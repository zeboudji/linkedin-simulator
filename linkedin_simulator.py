import streamlit as st

# Titre de l'application
st.title("Simulation de Performance LinkedIn")

# Saisie des paramètres
followers = st.number_input("Nombre d'abonnés", min_value=0, value=5000)
likes = st.number_input("Nombre de likes", min_value=0, value=50)
comments = st.number_input("Nombre de commentaires", min_value=0, value=10)
shares = st.number_input("Nombre de partages", min_value=0, value=5)
hours_since_posted = st.number_input("Durée depuis la publication (heures)", min_value=0, value=10)

# Calcul de la portée estimée et du taux d'engagement
views = (likes * 50 + comments * 100 + shares * 150) * (48 / (hours_since_posted + 1))
engagement_rate = (likes + comments + shares) / views * 100

# Performance globale
if views > 3000:
    performance = "Vrai buzz"
elif views > 1000:
    performance = "Très bonne performance"
elif views > 400:
    performance = "Correct"
else:
    performance = "Médiocre"

# Affichage des résultats
st.subheader("Résultats")
st.write(f"Nombre de vues estimé : {views:.2f}")
st.write(f"Taux d'engagement : {engagement_rate:.2f}%")
st.write(f"Performance globale : {performance}")

