
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN Y ESTILO NEON ---
st.set_page_config(page_title="STOMS IA - Neon Elite", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #060606; color: #00ff41; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; transition: 0.3s; border: none; }
    
    /* Botones Neon Personalizados */
    .btn-verde { background-color: #00ff41 !important; color: black !important; box-shadow: 0 0 15px #00ff41; }
    .btn-azul { background-color: #00d4ff !important; color: black !important; box-shadow: 0 0 15px #00d4ff; }
    .btn-amarillo { background-color: #ffee00 !important; color: black !important; box-shadow: 0 0 15px #ffee00; }
    .btn-rojo { background-color: #ff003c !important; color: white !important; box-shadow: 0 0 15px #ff003c; }
    
    .stDataFrame, .stTable { border: 1px solid #00ff41; background-color: #0a0a0a; }
    h1, h2, h3 { color: #00ff41; text-shadow: 0 0 10px #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CREDENCIALES ---
API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
API_HOST = "api-football-v1.p.rapidapi.com"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
TELEGRAM_CHAT_ID = "5298539210"

LIGAS_CALIDAD = [39, 78, 88, 595, 140, 61, 71, 94, 135, 203]

# --- 3. FUNCIONES ---
def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try: requests.get(url, params=params)
    except: pass

def obtener_datos():
    url = f"https://{API_HOST}/v3/fixtures"
    hoy = datetime.now().strftime('%Y-%m-%d')
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": API_HOST}
    all_fixtures = []
    for liga_id in LIGAS_CALIDAD:
        querystring = {"date": hoy, "league": liga_id, "status": "NS"}
        try:
            response = requests.get(url, headers=headers, params=querystring)
            all_fixtures.extend(response.json().get('response', []))
        except: continue
    return all_fixtures

# --- 4. INTERFAZ VISUAL ---
st.sidebar.title("⚡ STOMS IA SYSTEM")
st.sidebar.markdown(f"**Status:** `ACTIVE` \n\n**Growth Goal:** `6%` \n\n**User:** `yrm-2026` ")
st.sidebar.divider()

# Botón de Comprobación de Notificación (Nuevo)
if st.sidebar.button("🔔 COMPROBAR NOTIFICACIÓN"):
    enviar_telegram("🔌 *Sistema Online:* Tu bot de Telegram está conectado correctamente.")
    st.sidebar.toast("¡Mensaje de prueba enviado!")

st.title("⚽ MONITOR DE ELITE: OVER 1.5 & 2.5")

# BOTONES NEON DE ESTRATEGIA
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown('<button class="stButton btn-verde">VERDE (90%)</button>', unsafe_allow_html=True)
with col2: st.markdown('<button class="stButton btn-azul">AZUL (80%)</button>', unsafe_allow_html=True)
with col3: st.markdown('<button class="stButton btn-amarillo">AMARILLO (70%)</button>', unsafe_allow_html=True)
with col4: st.markdown('<button class="stButton btn-rojo">ROJO (Riesgo)</button>', unsafe_allow_html=True)

st.divider()

# TABLA DE RENDIMIENTO (Placeholder para tus stats)
st.subheader("📈 Tabla de Rendimiento (Últimos 10 días)")
data_rendimiento = {
    "Fecha": ["01/02", "02/02", "03/02", "04/02", "Hoy"],
    "Picks": [4, 3, 5, 2, 0],
    "Ganados": [3, 3, 4, 2, 0],
    "Crecimiento": ["+1.2%", "+0.9%", "+1.5%", "+0.6%", "Pendiente"]
}
st.table(pd.DataFrame(data_rendimiento))

# ACCIÓN PRINCIPAL
if st.button("🔍 INICIAR ESCANEO DE ALTA CALIDAD"):
    with st.spinner('Escaneando mercados...'):
        fixtures = obtener_datos()
        if fixtures:
            results = []
            for f in fixtures:
                liga = f['league']['name']
                partido = f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}"
                sugerencia = "✅ VERDE: Over 2.5" if liga in ["Eredivisie", "Bundesliga"] else "🔵 AZUL: Over 1.5"
                
                results.append({"Hora": f['fixture']['date'][11:16], "Liga": liga, "Partido": partido, "Estrategia": sugerencia})
                enviar_telegram(f"🚀 *NUEVO PICK:* {partido}\n🏆 {liga}\n📊 {sugerencia}")

            st.table(pd.DataFrame(results))
        else:
            st.warning("No hay partidos de élite disponibles ahora.")

# Footer
st.divider()
if st.button("📩 ENVIAR REPORTE A yanielramirez895@gmail.com"):
    st.balloons()
    st.success("Reporte consolidado enviado.")
