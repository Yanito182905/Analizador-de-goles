


import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Sistema 6% Goles Pro", page_icon="⚽", layout="wide")

# --- CREDENCIALES YA INGRESADAS ---
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# --- ESTILO ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GESTIÓN DE CAPITAL ---
st.sidebar.header("💰 Gestión de Banca")
banca_inicial = st.sidebar.number_input("Banca Actual ($)", value=1000.0)
meta_diaria = banca_inicial * 0.06

st.sidebar.metric("Objetivo Hoy (6%)", f"${meta_diaria:.2f}")

st.sidebar.markdown("---")
st.sidebar.subheader("📓 Diario de Hoy")
ganancia_real = st.sidebar.number_input("Ganancia Real hoy ($)", value=0.0)
if st.sidebar.checkbox("✅ Meta Alcanzada"):
    st.sidebar.success("¡Disciplina de hierro! Deja de operar.")
    st.balloons()

# --- CUERPO PRINCIPAL ---
st.title("📈 Panel de Control 6% Diario")

# Proyección de Interés Compuesto
with st.expander("📅 Ver Proyección a 30 días"):
    proyeccion = [round(banca_inicial * (1.06**i), 2) for i in range(31)]
    st.line_chart(proyeccion)
    st.write(f"Si mantienes la disciplina, en 30 días tendrás: **${proyeccion[-1]:,.2f}**")

def enviar_alerta(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except:
        st.error("Error enviando alerta a Telegram")

# --- BUSCADOR DE PICKS ---
st.header("🔍 Buscador de Oportunidades")

if st.button('🚀 Escanear Ligas TOP y Enviar a Telegram'):
    url = "https://v3.football.api-sports.io/fixtures"
    hoy = datetime.now().strftime('%Y-%m-%d')
    params = {'date': hoy, 'status': 'NS'}
    
    with st.spinner('Analizando partidos en tiempo real...'):
        response = requests.get(url, headers=HEADERS, params=params)
        partidos = response.json().get('response', [])
        
        # Ligas con alta tendencia de goles
        ligas_goleadoras = ['Eerste Divisie', 'Eredivisie', 'Bundesliga', 'S-League', 'J-League', 'Super League', 'Premier League']
        
        encontrados = []
        for p in partidos:
            liga = p['league']['name']
            if liga in ligas_goleadoras:
                home = p['teams']['home']['name']
                away = p['teams']['away']['name']
                hora = p['fixture']['date'][11:16]
                
                # Crear mensaje para Telegram
                msg = f"⚽ *AVISO DE VALOR 6%*\n\n🔥 {home} vs {away}\n🏆 Liga: {liga}\n⏰ Hora: {hora}\n🎯 Mercado: Over 1.5\n\n_Busca cuota min: 1.35_"
                enviar_alerta(msg)
                
                encontrados.append({
                    "Hora": hora,
                    "Partido": f"{home} vs {away}",
                    "Liga": liga,
                    "Confianza": "ALTA 🔥"
                })
        
        if encontrados:
            st.write("### ✅ Picks enviados a tu móvil")
            st.table(pd.DataFrame(encontrados))
            st.info("Revisa tu Telegram. Los partidos ya están en tu chat.")
        else:
            st.warning("No hay partidos de ligas TOP ahora mismo. ¡Paciencia!")

st.markdown("---")
st.caption("Estrategia 6% - Generada para uso personal. No compartas tu Token.")

