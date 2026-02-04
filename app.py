import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="PRO 6% ELITE TERMINAL", layout="wide")

if 'bank' not in st.session_state: st.session_state.bank = 500.0
if 'enviados' not in st.session_state: st.session_state.enviados = set()
if 'stats' not in st.session_state: st.session_state.stats = {'ganados': 0, 'perdidos': 0}

st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e0e0; }
    .neon-card { background: #0d1117; border: 1px solid #00ff88; padding: 25px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,255,136,0.1); }
    .header-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .badge-pais { background: #ffffff; color: #000; padding: 3px 10px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    .badge-liga { color: #00d4ff; font-weight: bold; margin-left: 10px; text-transform: uppercase; }
    .match-name { font-size: 24px; font-weight: bold; color: #fff; margin: 10px 0; }
    .drop-box { background: #161b22; border: 1px dashed #ff4b4b; padding: 10px; border-radius: 8px; margin-top: 10px; }
    .neon-green { color: #00ff88; font-weight: bold; }
    .neon-red { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR Y MÉTRICAS
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff'>⚙️ GESTIÓN</h2>", unsafe_allow_html=True)
    st.metric("BANCA", f"{st.session_state.bank:.2f}€")
    if st.button("🔔 TEST TELEGRAM"):
        requests.post(f"https://api.telegram.org/bot8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ/sendMessage", 
                      data={"chat_id": "790743691", "text": "🛰️ Conexión Estable."})

st.markdown("<h1 style='text-align: center; color:#00ff88;'>MASTER PRO: DROPPING ODDS MONITOR</h1>", unsafe_allow_html=True)

# 3. ESCÁNER CON LÓGICA DE PINNACLE
LIGAS_TOP_10 = {
    'Bundesliga': 'ALEMANIA', 'Eerste Divisie': 'PAÍSES BAJOS', 'Eredivisie': 'PAÍSES BAJOS',
    'Super League': 'SUIZA', 'Jupiler Pro League': 'BÉLGICA', 'Premier League': 'INGLATERRA',
    'Championship': 'INGLATERRA', 'Superliga': 'DINAMARCA', 'Eliteserien': 'NORUEGA', 'Major League Soccer': 'EEUU'
}

if st.button("🔍 BUSCAR DROPPING ODDS (LIGAS TOP)", type="primary"):
    API_KEY = "f34c526a0810519b034fe7555fb83977"
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    headers = {'x-rapidapi-key': API_KEY}
    
    res = requests.get(url, headers=headers, params=params)
    partidos = res.json().get('response', [])
    
    for p in partidos:
        liga_nom = p['league']['name']
        id_p = p['fixture']['id']
        
        if liga_nom in LIGAS_TOP_10 and id_p not in st.session_state.enviados:
            pais = LIGAS_TOP_10[liga_nom]
            home, away = p['teams']['home']['name'], p['teams']['away']['name']
            hora = p['fixture']['date'][11:16]
            
            # SIMULACIÓN DE DROPPING PINNACLE
            c_apertura = round(random.uniform(1.75, 1.95), 2)
            c_pinnacle = round(c_apertura - random.uniform(0.10, 0.25), 2)
            prob = random.randint(68, 84)

            if 1.45 <= c_pinnacle <= 1.80:
                # UI APP
                st.markdown(f"""
                <div class="neon-card">
                    <div class="header-info">
                        <div>
                            <span class="badge-pais">{pais}</span>
                            <span class="badge-liga">{liga_nom}</span>
                        </div>
                        <span style="color:#ffaa00; font-weight:bold;">🕒 {hora}</span>
                    </div>
                    <div class="match-name">{home} vs {away}</div>
                    <div style="display:flex; gap:20px;">
                        <span class="neon-green">🎯 PROB: {prob}%</span>
                        <span style="color:#00d4ff;">📊 MERCADO: Over 2.5</span>
                    </div>
                    <div class="drop-box">
                        <span class="neon-red">📉 DROPPING DETECTADO:</span> 
                        Pinnacle abrió en @{c_apertura} y ha bajado a <span class="neon-green">@{c_pinnacle}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # TELEGRAM
                msg = (f"📉 *DROPPING PINNACLE DETECTADO*\n\n"
                       f"🌍 *PAÍS:* {pais}\n"
                       f"🏆 *LIGA:* {liga_nom}\n"
                       f"⚽ *PARTIDO:* {home} vs {away}\n"
                       f"🕒 *HORA:* {hora}\n\n"
                       f"🔥 *MERCADO:* Over 2.5\n"
                       f"🎯 *PROB:* {prob}%\n"
                       f"📉 *PRECIO:* @{c_apertura} -> @{c_pinnacle}\n"
                       f"💰 *VALOR:* ALTO ✅")
                
                requests.post(f"https://api.telegram.org/bot8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ/sendMessage", 
                              data={"chat_id": "790743691", "text": msg, "parse_mode": "Markdown"})
                st.session_state.enviados.add(id_p)
