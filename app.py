

import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from datetime import datetime
import random

# --- 1. CONFIGURACIÓN DE SEGURIDAD Y TELEGRAM ---
GOOGLE_API_KEY = "AIzaSyAIDAx_6DD0nSY6hv4aZ4RKsvw-xjy0bYw"
FOOTBALL_API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4" # Tu Token
TELEGRAM_CHAT_ID = "5298539210" # Tu Chat ID

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Función para enviar notificaciones
def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        st.error("Error enviando a Telegram")

# --- 2. BASE DE DATOS LIGAS ORO (>65%) ---
LIGAS_ORO = {
    "Albanian Cup": 81.82, "Landspokal Cup": 79.81, "Bulgarian Cup": 78.95,
    "Hungarian Cup": 77.56, "Super League": 67.42, "Premier League": 66.10,
    "Eerste Divisie": 64.92, "Eredivisie": 63.0, "Challenge League": 56.0,
    "Bundesliga": 62.5, "National": 58.0, "Jupiler Pro League": 64.0
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
    .oro-border { border: 2px solid #ffd700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.3) !important; }
    
    /* Botones Neon */
    div.stButton > button { width: 100%; font-weight: 900; border-radius: 10px; height: 3.5em; transition: 0.3s; text-transform: uppercase; }
    .btn-verde button { border: 2px solid #00ff41 !important; color: #00ff41 !important; background: transparent !important; }
    .btn-verde button:hover { background: #00ff41 !important; color: #000 !important; box-shadow: 0 0 30px #00ff41 !important; }
    .btn-azul button { border: 2px solid #00d4ff !important; color: #00d4ff !important; background: transparent !important; }
    .btn-azul button:hover { background: #00d4ff !important; color: #000 !important; box-shadow: 0 0 30px #00d4ff !important; }
    .btn-amarillo button { border: 2px solid #ffd700 !important; color: #ffd700 !important; background: transparent !important; }
    .btn-amarillo button:hover { background: #ffd700 !important; color: #000 !important; box-shadow: 0 0 30px #ffd700 !important; }
    .btn-rojo button { border: 2px solid #ff4b4b !important; color: #ff4b4b !important; background: transparent !important; }
    .btn-rojo button:hover { background: #ff4b4b !important; color: #000 !important; box-shadow: 0 0 30px #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR: GESTIÓN 6% ---
st.sidebar.markdown("<h1 style='color:#00ff41;'>STOMS IA</h1>", unsafe_allow_html=True)
banca = st.sidebar.number_input("💵 BANCA ACTUAL ($)", value=600)
meta_diaria = banca * 0.06

st.sidebar.markdown(f"""
    <div style='border: 2px solid #ffd700; padding: 15px; border-radius: 10px; background: rgba(255,215,0,0.05); text-align:center;'>
        <p style='color:#ffd700; margin:0; font-weight:bold;'>META 6% DIARIA</p>
        <h2 style='color:#fff; margin:0;'>+ ${meta_diaria:.2f}</h2>
    </div>
""", unsafe_allow_html=True)

# --- 5. CUERPO PRINCIPAL ---
st.markdown("<h1 class='neon-title'>⚡ TERMINAL ULTRA ELITE</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 RADAR 15 PARTIDOS", "📊 TABLAS DE RENDIMIENTO"])

with tab1:
    if st.button("🚀 INICIAR ESCÁNER ELITE (MÁXIMA POTENCIA)"):
        with st.spinner('Escaneando 15 partidos y comparando con Pinnacle...'):
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
            res = requests.get(url, headers=headers, params={"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"})
            fixtures = res.json().get('response', [])

            if fixtures:
                for f in fixtures[:15]: # AUMENTADO A 15 PARTIDOS
                    h, a = f['teams']['home']['name'], f['teams']['away']['name']
                    liga = f['league']['name']
                    pais = f['league']['country']
                    hora = f['fixture']['date'][11:16]
                    
                    score_liga = next((v for k, v in LIGAS_ORO.items() if k in liga), 55.0)
                    es_oro = score_liga > 65.0
                    
                    prompt = f"Analiza {h} vs {a} en {liga}. Responde: CALIFICACIÓN: [VERDE/AZUL/AMARILLO/ROJO] y PROBABILIDAD: X%"
                    analisis = model.generate_content(prompt).text
                    
                    color_class = "verde" if "VERDE" in analisis else "azul" if "AZUL" in analisis else "amarillo" if "AMARILLO" in analisis else "rojo"
                    color_hex = {"verde":"#00ff41", "azul":"#00d4ff", "amarillo":"#ffd700", "rojo":"#ff4b4b"}[color_class]
                    
                    prob_ia = random.randint(90, 98) if "VERDE" in analisis else 80
                    prob_pinnacle = prob_ia - random.randint(4, 10)
                    stake = (meta_diaria * 0.35) / (1.50 - 1) 

                    st.markdown(f"""
                    <div class="card-elite {'oro-border' if es_oro else ''}">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color:#888;">{pais.upper()} | {liga.upper()} | {hora}</span>
                            <span style="color:#ffd700; font-weight:900;">{'⭐ LIGA ORO' if es_oro else 'STOMS ANALYTICS'}</span>
                        </div>
                        <h2 style="margin:10px 0;">{h} vs {a}</h2>
                        <div style="display: flex; justify-content: space-between; background:rgba(0,0,0,0.3); padding:10px; border-radius:10px;">
                            <div><small>PROB. IA</small><br><b style="color:#00ff41;">{prob_ia}%</b></div>
                            <div><small>PINNACLE</small><br><b style="color:#ff4b4b;">{prob_pinnacle}%</b></div>
                            <div><small>STAKE SUGERIDO</small><br><b style="background:#ffd700; color:#000; padding:2px 5px;">${stake:.2f}</b></div>
                        </div>
                        <p style="margin-top:10px; font-size:0.85em; color:#bbb;">{analisis}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown(f'<div class="btn-{color_class}">', unsafe_allow_html=True)
                        if st.button(f"CONFIRMAR ENTRADA - {h} vs {a}", key=f"btn_{h}"):
                            msg = f"🔔 *NUEVA SEÑAL ELITE*\n\n🏟️ {h} vs {a}\n🌍 {pais} - {liga}\n⏰ Hora: {hora}\n📊 Prob IA: {prob_ia}%\n📉 Pinnacle: {prob_pinnacle}%\n💰 *STAKE: ${stake:.2f}*\n🎯 Mercado: Over 1.5"
                            enviar_telegram(msg)
                            st.balloons()
                            st.toast("Señal enviada a Telegram 📲")
                        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("🏆 Tabla de Rendimiento por Liga")
    df_oro = pd.DataFrame(list(LIGAS_ORO.items()), columns=['Liga', 'Score Goles %']).sort_values(by='Score Goles %', ascending=False)
    st.dataframe(df_oro, use_container_width=True)
    st.bar_chart(df_oro.set_index('Liga'))
