
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN
st.set_page_config(page_title="App 6% - Alertas Pro", page_icon="📲", layout="wide")

# CREDENCIALES
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN =8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ "PEGA_AQUI_TU_TOKEN_DE_BOTFATHER"
TELEGRAM_CHAT_ID =790743691 "PEGA_AQUI_TU_CHAT_ID"

HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

st.title("📲 Alertas Inteligentes - Meta 6%")

# --- BUSCADOR ---
if st.button('🔍 Escanear y Enviar Alertas al Móvil'):
    url_fixtures = "https://v3.football.api-sports.io/fixtures"
    hoy = datetime.now().strftime('%Y-%m-%d')
    params = {'date': hoy, 'status': 'NS'}
    
    with st.spinner('Escaneando mercado de goles...'):
        res = requests.get(url_fixtures, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        
        ligas_goleadoras = ['Eerste Divisie', 'Eredivisie', 'Bundesliga', 'S-League', 'J-League', 'Super League']
        picks_encontrados = []

        for p in partidos:
            liga_nombre = p['league']['name']
            if liga_nombre in ligas_goleadoras:
                home = p['teams']['home']['name']
                away = p['teams']['away']['name']
                hora = p['fixture']['date'][11:16]
                
                msg = f"⚽ *NUEVA OPORTUNIDAD 6%*\n\n🔥 {home} vs {away}\n🏆 Liga: {liga_nombre}\n⏰ Hora: {hora}\n📈 Mercado: Over 1.5"
                enviar_telegram(msg)
                picks_encontrados.append({"Partido": f"{home} vs {away}", "Liga": liga_nombre})

        if picks_encontrados:
            st.success(f"¡Se han enviado {len(picks_encontrados)} alertas a tu Telegram!")
            st.table(pd.DataFrame(picks_encontrados))
        else:
            st.warning("No se encontraron partidos 'TOP' en este momento.")

# --- TU CALCULADORA DE INTERÉS COMPUESTO (Mantener debajo) ---
st.markdown("---")
st.subheader("📊 Tu proyección de crecimiento")
banca = st.sidebar.number_input("Banca Actual ($)", value=1000.0)
st.write(f"Tu meta de hoy es ganar: **${banca * 0.06:.2f}**")

