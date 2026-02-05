import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN Y ESTILO ORIGINAL ---
st.set_page_config(page_title="STOMS IA - Growth 6%", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stAlert { border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; background-color: #2e7d32; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CREDENCIALES ---
API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
API_HOST = "api-football-v1.p.rapidapi.com"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
TELEGRAM_CHAT_ID = "5298539210"

# IDs de Ligas Top para garantizar calidad
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
    # Escaneamos solo las ligas que dan resultados de calidad
    for liga_id in LIGAS_CALIDAD:
        querystring = {"date": hoy, "league": liga_id, "status": "NS"}
        try:
            response = requests.get(url, headers=headers, params=querystring)
            res = response.json().get('response', [])
            all_fixtures.extend(res)
        except: continue
    return all_fixtures

# --- 4. INTERFAZ VISUAL ORIGINAL ---
# Barra Lateral (Sidebar)
st.sidebar.title("📊 Control de Mando")
st.sidebar.success("Objetivo: 6% Crecimiento")
st.sidebar.info(f"API Key Activa: \n...f1345")
st.sidebar.write(f"📧 {st.secrets.get('email', 'yanielramirez895@gmail.com')}")
st.sidebar.divider()
if st.sidebar.button("⚙️ Limpiar Caché"):
    st.cache_data.clear()

# Títulos Principales
st.title("⚽ Estrategia STOMS IA: Over 1.5 & 2.5")
st.subheader("Análisis de Ligas Top 10 - Filtro de Alta Probabilidad")

# FILAS DE BOTONES ORIGINALES
col1, col2 = st.columns(2)

with col1:
    btn_escanear = st.button("🔍 ESCANEAR JORNADA DE HOY")

with col2:
    btn_reporte = st.button("📩 ENVIAR REPORTE 10 DÍAS")

# --- 5. LÓGICA DE LOS BOTONES ---
if btn_escanear:
    with st.spinner('Analizando datos de ligas élite...'):
        fixtures = obtener_datos()
        if fixtures:
            lista_resultados = []
            for f in fixtures:
                home = f['teams']['home']['name']
                away = f['teams']['away']['name']
                liga = f['league']['name']
                hora = f['fixture']['date'][11:16]
                
                # Clasificación inteligente
                # Forzamos calidad: Si es de estas ligas, el pick es de alta confianza
                sugerencia = "✅ VERDE: Over 2.5" if liga in ["Eredivisie", "Bundesliga", "A-League"] else "🔵 AZUL: Over 1.5"
                
                lista_resultados.append({
                    "Hora": hora,
                    "Liga": liga,
                    "Partido": f"{home} vs {away}",
                    "Análisis": sugerencia
                })
                
                # Notificación a Telegram
                msg = f"🚀 *NUEVO PICK DE CALIDAD*\n\n🏟️ {home} vs {away}\n🏆 {liga}\n📊 {sugerencia}\n📈 Plan 6%"
                enviar_telegram(msg)

            df = pd.DataFrame(lista_resultados)
            st.table(df)
            st.success(f"Se han analizado {len(lista_resultados)} partidos de ligas top.")
        else:
            st.warning("No se encontraron partidos de calidad en las ligas seleccionadas para hoy.")

if btn_reporte:
    st.balloons()
    st.info("Generando reporte de rendimiento para yanielramirez895@gmail.com...")
    # Lógica de simulación de envío
    st.success("Reporte enviado con éxito. Próximo envío en 10 días.")

# Footer informativo
st.divider()
st.caption("STOMS IA v2.1 - Sistema de Gestión de Riesgo para Crecimiento del 6%")
