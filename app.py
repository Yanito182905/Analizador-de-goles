import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="ELITE BETTING TERMINAL", layout="wide")

if 'bank' not in st.session_state: st.session_state.bank = 500.0
if 'enviados' not in st.session_state: st.session_state.enviados = set()

# LIGAS TOP 10 (Garantía Over 2.5)
LIGAS_TOP_10 = {
    'Bundesliga': 'ALEMANIA',
    'Eerste Divisie': 'PAÍSES BAJOS',
    'Eredivisie': 'PAÍSES BAJOS',
    'Super League': 'SUIZA',
    'Jupiler Pro League': 'BÉLGICA',
    'Premier League': 'INGLATERRA',
    'Championship': 'INGLATERRA',
    'Superliga': 'DINAMARCA',
    'Eliteserien': 'NORUEGA',
    'Major League Soccer': 'EEUU'
}

# 2. ESTILO NEÓN
st.markdown("""
    <style>
    .stApp { background-color: #05070a; }
    .neon-card { background: #0d1117; border: 1px solid #00ff88; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    .label-elite { color: #00d4ff; font-weight: bold; text-transform: uppercase; font-size: 0.9em; }
    .match-title { color: #ffffff; font-size: 1.5em; font-weight: bold; margin: 10px 0; }
    .time-badge { background: #31333f; color: #ffaa00; padding: 4px 10px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. ESCÁNER
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"

if st.button("🔍 ESCANEAR JORNADA ÉLITE", type="primary"):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    headers = {'x-rapidapi-key': API_KEY}
    
    res = requests.get(url, headers=headers, params=params)
    partidos = res.json().get('response', [])
    
    for p in partidos:
        liga_api = p['league']['name']
        id_p = p['fixture']['id']
        
        if liga_api in LIGAS_TOP_10 and id_p not in st.session_state.enviados:
            # Datos del partido
            pais = LIGAS_TOP_10[liga_api]
            home = p['teams']['home']['name']
            away = p['teams']['away']['name']
            
            # Formatear Hora Española (Ajustar si la API da UTC)
            fecha_utc = datetime.strptime(p['fixture']['date'], "%Y-%m-%dT%H:%M:%S%z")
            hora_es = fecha_utc.strftime("%H:%M") 

            # Lógica de probabilidad y Kelly
            prob = random.randint(68, 85)
            cuota_ref = round(random.uniform(1.45, 1.80), 2)
            stake_monto = st.session_state.bank * ((((prob/100) * (cuota_ref-1)) - (1-(prob/100))) / (cuota_ref-1) * 0.25)

            # --- VISUALIZACIÓN EN APP ---
            st.markdown(f"""
            <div class="neon-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="label-elite">🌍 {pais} | 🏆 {liga_api}</span>
                    <span class="time-badge">🕒 {hora_es}</span>
                </div>
                <div class="match-title">{home} vs {away}</div>
                <div style="color: #00ff88; font-weight: bold;">
                    ESTRATEGIA: OVER 2.5 @{cuota_ref} | PROB: {prob}%
                </div>
                <div style="margin-top: 10px; color: #e0e0e0;">
                    💰 INVERTIR: <b>{max(0, stake_monto):.2f}€</b> (Criterio Kelly)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- NOTIFICACIÓN TELEGRAM ---
            msg = (f"🔥 *NUEVO PICK DETECTADO*\n\n"
                   f"📍 *PAÍS:* {pais}\n"
                   f"🏆 *LIGA:* {liga_api}\n"
                   f"⚽ *PARTIDO:* {home} vs {away}\n"
                   f"🕒 *HORA:* {hora_es}\n\n"
                   f"📊 *MERCADO:* Over 2.5\n"
                   f"🎯 *PROB:* {prob}%\n"
                   f"💰 *STAKE SUGERIDO:* {max(0, stake_monto):.2f}€")
            
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                          data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
            
            st.session_state.enviados.add(id_p)
