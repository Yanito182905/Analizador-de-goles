import streamlit as st
import requests

# Tu nueva llave
token = "c5992c3e7e074dc5b8e9bea0f6abaf88"

st.title("🧪 Test de Conexión STOMS")

if st.button("Verificar Token"):
    url = "https://api.football-data.org/v2/competitions/PL/matches?status=SCHEDULED"
    headers = {"X-Auth-Token": token}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        st.success("✅ ¡CONEXIÓN EXITOSA! La llave ya funciona.")
        st.json(response.json()) # Esto mostrará los partidos reales
    elif response.status_code == 403:
        st.error("🚫 ERROR 403: Acceso Denegado.")
        st.info("Casi siempre es porque no has confirmado el email que te enviaron. Revisa tu correo (y la carpeta de Spam).")
    else:
        st.warning(f"Error {response.status_code}: {response.text}")
