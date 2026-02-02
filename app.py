import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Analizador de Goles 6%", page_icon="⚽")

# TU API KEY (Ya integrada)
API_KEY = "f34c526a0810519b034fe7555fb83977"

st.title("⚽ Estrategia de Goles - Meta 6%")
st.sidebar.header("💰 Gestión de Banca")
banca_actual = st.sidebar.number_input("Tu banca actual ($)", value=1000.0)
meta_diaria = banca_actual * 0.06

st.sidebar.success(f"Objetivo de hoy: ${meta_diaria:.2f}")

def obtener_datos():
    url = "https://v3.football.api-sports.io/fixtures"
    hoy = datetime.now().strftime('%Y-%m-%d')
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': API_KEY
    }
    params = {'date': hoy}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return data.get('response', [])
    except:
        return []

st.write(f"### Partidos de hoy: {datetime.now().strftime('%d/%m/%Y')}")

with st.spinner('Analizando mercados de goles...'):
    partidos = obtener_datos()
    
    if partidos:
        lista_analisis = []
        for p in partidos:
            liga = p['league']['name']
            home = p['teams']['home']['name']
            away = p['teams']['away']['name']
            hora = p['fixture']['date'][11:16]
            
            # Filtro inteligente de ligas "Over" (Países Bajos, Alemania, Islandia, etc.)
            ligas_top_goles = ['Eerste Divisie', 'Eredivisie', 'Bundesliga', 'S-League', 'J-League', 'Super League']
            
            confianza = "ALTA 🔥" if liga in ligas_top_goles else "MEDIA 📊"
            
            lista_analisis.append({
                "Hora": hora,
                "Partido": f"{home} vs {away}",
                "Liga": liga,
                "Confianza": confianza,
                "Mercado Sugerido": "Over 1.5" if confianza == "ALTA 🔥" else "Over 2.5 (Riesgo)"
            })
        
        df = pd.DataFrame(lista_analisis)
        
        # Mostrar tabla estilizada
        st.table(df)
        
        st.info("💡 Consejo: Para tu meta del 6%, busca cuotas entre 1.50 y 1.70 con los partidos marcados como 'ALTA'.")
    else:
        st.error("No se pudieron cargar datos. Revisa tu límite de API o conexión.")

st.caption("App conectada a API-Football en tiempo real.")