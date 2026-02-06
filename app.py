
import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from datetime import datetime
import random

# --- 1. CONFIGURACIÓN DE SEGURIDAD Y TELEGRAM ---
GOOGLE_API_KEY = "AIzaSyAIDAx_6DD0nSY6hv4aZ4RKsvw-xjy0bYw"
FOOTBALL_API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
TELEGRAM_CHAT_ID = "5298539210"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload)
        return r.status_code == 200
    except:
        return False

# --- 2. LIGAS AMPLIADAS (MÁS FLEXIBILIDAD) ---
LIGAS_ORO = {
    "Albanian Cup": 81.82, "Landspokal Cup": 79.81, "Bulgarian Cup": 78.95,
    "Hungarian Cup": 77.56, "Super League": 67.42, "Premier League": 66.10,
    "Eerste Divisie": 64.92, "Eredivisie": 63.0, "Challenge League": 56.0,
    "Bundesliga": 62.5, "La Liga": 55.0, "Serie A": 54.0, "Ligue 1": 53.0,
    "Primeira Liga": 58.0, "Jupiler Pro League": 64.0
}

# --- 3. DISEÑO NEON EXTREMO ---
st.set_page_config(page_title="STOMS ULTRA ELITE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .neon-title { color: #00ff41; text-shadow: 0 0 15px #00ff41; font-weight: 900; text-align: center; font-size: 3em; }
    .card-elite {
        background: #050505; border-radius: 15px; padding: 20px;
        margin-bottom: 15px; border: 1px solid #1a1a1a;
    }
    .oro-border { border: 2px solid #ffd700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.4) !important; }
    
    /* Botones Neon Personalizados */
    div.stButton > button { width: 100%; font-weight: 900; border-radius: 10px; height: 3.5em; transition: 0.3s; text-transform: uppercase; }
    .btn-telegram button { border: 2px solid #00d4ff !important; color: #00d4ff !important; background: rgba(0,212,255,0.1) !important; margin-bottom: 20px; }
    .btn-verde button { border: 2px solid #00ff41 !important; color: #00ff41 !important; }
    .btn-verde button:hover { background: #00ff41 !important; color: #000 !important; box-shadow: 0 0 30px #00ff41 !important; }
    .btn-azul button { border: 2px solid #00d4ff !important; color: #00d4ff !important; }
    .btn-amarillo button { border: 2px solid #ffd700 !important; color: #ffd700 !important; }
    .btn-rojo button { border: 2px solid #ff4b4b !important; color: #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
st.sidebar.markdown("<h1 style='color:#00ff41;'>STOMS IA</h1>", unsafe_allow_html=True)
banca = st.sidebar.number_input("💵 BANCA ACTUAL ($)", value=600)
meta_diaria = banca * 0.06

st.sidebar.markdown(f"<div style='border: 2px solid #ffd700; padding: 10px; border-radius: 10px; text-align:center;'>META: <b>${meta_diaria:.2f}</b></div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write("📲 **ESTADO NOTIFICACIONES**")
with st.sidebar.container():
    st.markdown('<div class="btn-telegram">', unsafe_allow_html=True)
    if st.button("🔔 TEST TELEGRAM"):
        exito = enviar_telegram("✅ ¡Sistema STOMS IA Conectado! Listo para el 6%.")
        if exito: st.success("¡Mensaje enviado!")
        else: st.error("Error de conexión.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. CUERPO PRINCIPAL ---
st.markdown("<h1 class='neon-title'>⚡ TERMINAL ULTRA ELITE</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 RADAR 15 PARTIDOS", "📊 RENDIMIENTO"])

with tab1:
    if st.button("🚀 INICIAR ESCÁNER (FLEXIBLE)"):
        with st.spinner('Escaneando mercados...'):
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
            # Quitamos el estatus 'NS' para que traiga cualquier partido de hoy y sea más fácil encontrar datos
            res = requests.get(url, headers=headers, params={"date": datetime.now().strftime('%Y-%m-%d')})
            fixtures = res.json().get('response', [])

            st.write(f"🔎 Partidos encontrados hoy: **{len(fixtures)}**")

            if fixtures:
                for f in fixtures[:15]:
                    h, a = f['teams']['home']['name'], f['teams']['away']['name']
                    liga = f['league']['name']
                    pais = f['league']['country']
                    hora = f['fixture']['date'][11:16]
                    
                    # Score de liga (si no está, ponemos 50% por defecto)
                    score_liga = next((v for k, v in LIGAS_ORO.items() if k in liga), 50.0)
                    es_oro = score_liga > 60.0 # Bajamos el filtro a 60% para que salten más
                    
                    # IA ANALISIS
                    prompt = f"Analiza {h} vs {a} (+1.5 goles). Responde: CALIFICACIÓN: [VERDE/AZUL/AMARILLO] y % Probabilidad."
                    try:
                        analisis = model.generate_content(prompt).text
                    except:
                        analisis = "CALIFICACIÓN: AZUL. Análisis estándar activo."
                    
                    color_class = "verde" if "VERDE" in analisis else "azul" if "AZUL" in analisis else "amarillo"
                    color_hex = {"verde":"#00ff41", "azul":"#00d4ff", "amarillo":"#ffd700"}[color_class]
                    
                    stake = (meta_diaria * 0.35) / 0.5 # Stake para buscar un tercio de la meta

                    st.markdown(f"""
                    <div class="card-elite {'oro-border' if es_oro else ''}">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color:#888;">{pais.upper()} | {liga.upper()}</span>
                            <span style="color:#ffd700;">{'⭐ LIGA ORO' if es_oro else ''}</span>
                        </div>
                        <h2 style="margin:5px 0;">{h} vs {a} <small style="color:#666;">{hora}</small></h2>
                        <div style="display: flex; justify-content: space-between; font-weight:bold;">
                            <span style="color:{color_hex};">IA: {color_class.upper()}</span>
                            <span style="color:#ffd700;">STAKE: ${stake:.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown(f'<div class="btn-{color_class}">', unsafe_allow_html=True)
                        if st.button(f"ENVIAR SEÑAL: {h}", key=f"btn_{h}"):
                            msg = f"⚽ *SEÑAL STOMS*\n🏟️ {h} vs {a}\n🏆 {liga}\n💰 Stake: ${stake:.2f}\n🎯 Mercado: Over 1.5"
                            enviar_telegram(msg)
                            st.toast("¡Enviado!")
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No se encontraron partidos. Intenta de nuevo en unos minutos.")

with tab2:
    st.subheader("🏆 Ligas en el Radar")
    st.write(pd.DataFrame(list(LIGAS_ORO.items()), columns=['Liga', 'Score %']))
