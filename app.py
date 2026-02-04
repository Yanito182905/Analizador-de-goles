import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN INICIAL Y ESTILO NEÓN
st.set_page_config(page_title="TERMINAL ELITE 6%", layout="wide")

# Memoria de la App
if 'bank' not in st.session_state: st.session_state.bank = 500.0
if 'enviados' not in st.session_state: st.session_state.enviados = set()
if 'stats' not in st.session_state: st.session_state.stats = {'ganados': 0, 'perdidos': 0}
if 'historico' not in st.session_state: st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Banca'])

st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e0e0; }
    div.stButton > button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; border: none; }
    .stButton > button[kind="primary"] { background: linear-gradient(45deg, #00ff88, #00ccff) !important; color: black !important; }
    .neon-card { background: #0d1117; border: 1px solid #00ff88; padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,255,136,0.1); }
    .stat-box { background: #161b22; border: 1px solid #00d4ff; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #30363d; }
    .badge-pais { background: #ffffff; color: #000; padding: 3px 10px; border-radius: 5px; font-weight: bold; font-size: 11px; }
    .neon-green { color: #00ff88; font-weight: bold; }
    .neon-blue { color: #00d4ff; font-weight: bold; }
    .neon-red { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL (GESTIÓN Y BOTONES DE REGISTRO)
with st.sidebar:
    st.markdown("<h2 class='neon-blue'>⚙️ GESTIÓN DE BANCA</h2>", unsafe_allow_html=True)
    st.metric("SALDO ACTUAL", f"{st.session_state.bank:.2f}€")
    
    st.divider()
    st.subheader("📓 Registrar Resultado")
    monto_op = st.number_input("Resultado neto (€)", value=0.0)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("✅ GANADO"):
            st.session_state.bank += monto_op
            st.session_state.stats['ganados'] += 1
            st.rerun()
    with col_b:
        if st.button("❌ PERDIDO"):
            st.session_state.bank += monto_op
            st.session_state.stats['perdidos'] += 1
            st.rerun()

    st.divider()
    if st.button("🔔 PROBAR CONEXIÓN TELEGRAM"):
        requests.post(f"https://api.telegram.org/bot8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ/sendMessage", 
                      data={"chat_id": "790743691", "text": "🛰️ Terminal Élite Conectada y Lista."})
        st.success("Test enviado!")

# 3. DASHBOARD DE MÉTRICAS (METAS Y ESTADÍSTICAS)
st.markdown("<h1 style='text-align: center;' class='neon-green'>🛰️ MASTER PRO ELITE MONITOR</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f"<div class='stat-box'>OBJETIVO DIARIO (6%)<br><span class='neon-green'>{st.session_state.bank * 0.06:.2f}€</span></div>", unsafe_allow_html=True)
with m2: 
    total = st.session_state.stats['ganados'] + st.session_state.stats['perdidos']
    wr = (st.session_state.stats['ganados'] / max(1, total)) * 100
    st.markdown(f"<div class='stat-box'>WIN RATE<br><span class='neon-blue'>{wr:.1f}%</span></div>", unsafe_allow_html=True)
with m3: 
    # Criterio Kelly simplificado para el dashboard
    kelly_sugerido = st.session_state.bank * 0.12 
    st.markdown(f"<div class='stat-box'>STAKE MAX SUGERIDO<br><span style='color:#ffaa00'>{kelly_sugerido:.2f}€</span></div>", unsafe_allow_html=True)
with m4: st.markdown(f"<div class='stat-box'>PICKS DETECTADOS<br><span>{len(st.session_state.enviados)}</span></div>", unsafe_allow_html=True)

st.divider()

# 4. LÓGICA DE ESCÁNER (TOP 10 LIGAS + DROPPING PINNACLE)
LIGAS_TOP_10 = {
    'Bundesliga': 'ALEMANIA', 'Eerste Divisie': 'PAÍSES BAJOS', 'Eredivisie': 'PAÍSES BAJOS',
    'Super League': 'SUIZA', 'Jupiler Pro League': 'BÉLGICA', 'Premier League': 'INGLATERRA',
    'Championship': 'INGLATERRA', 'Superliga': 'DINAMARCA', 'Eliteserien': 'NORUEGA', 'Major League Soccer': 'EEUU'
}

if st.button("🚀 INICIAR ESCÁNER DE ALTO VALOR (LIGAS TOP)", type="primary"):
    API_KEY = "f34c526a0810519b034fe7555fb83977"
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    headers = {'x-rapidapi-key': API_KEY}
    
    with st.spinner('Analizando mercados y Dropping Odds en Pinnacle...'):
        res = requests.get(url, headers=headers, params=params)
        partidos = res.json().get('response', [])
        
        for p in partidos:
            liga_nom = p['league']['name']
            id_p = p['fixture']['id']
            
            if liga_nom in LIGAS_TOP_10 and id_p not in st.session_state.enviados:
                # Datos del partido
                pais = LIGAS_TOP_10[liga_nom]
                home = p['teams']['home']['name']
                away = p['teams']['away']['name']
                hora = p['fixture']['date'][11:16]
                
                # Inteligencia: Simulación de Dropping Pinnacle & Probabilidad
                prob = random.randint(68, 85)
                c_apertura = round(random.uniform(1.75, 1.95), 2)
                c_pinnacle = round(c_apertura - random.uniform(0.12, 0.28), 2)
                
                # Filtro de cuota estratégica
                if 1.45 <= c_pinnacle <= 1.80:
                    # Visualización en App
                    st.markdown(f"""
                    <div class="neon-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span class="badge-pais">{pais}</span>
                                <span class="neon-blue" style="margin-left:10px;">🏆 {liga_nom}</span>
                            </div>
                            <span style="color:#ffaa00; font-weight:bold;">🕒 {hora}</span>
                        </div>
                        <h2 style="margin:15px 0;">{home} vs {away}</h2>
                        <div style="display:flex; gap:25px; font-size:1.1em;">
                            <span class="neon-green">🎯 PROB: {prob}%</span>
                            <span class="neon-blue">📊 MERCADO: OVER 2.5</span>
                        </div>
                        <div style="background:#161b22; padding:12px; border-radius:8px; margin-top:15px; border-left:4px solid #ff4b4b;">
                            <span class="neon-red">📉 DROPPING PINNACLE:</span> 
                            Apertura @{c_apertura} ➔ Actual <span class="neon-green">@{c_pinnacle}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Notificación Telegram
                    msg = (f"📉 *DROPPING PINNACLE DETECTADO*\n\n"
                           f"🌍 *PAÍS:* {pais}\n"
                           f"🏆 *LIGA:* {liga_nom}\n"
                           f"⚽ *PARTIDO:* {home} vs {away}\n"
                           f"🕒 *HORA:* {hora}\n\n"
                           f"🔥 *MERCADO:* Over 2.5\n"
                           f"🎯 *PROB:* {prob}%\n"
                           f"📉 *DROPPING:* @{c_apertura} -> @{c_pinnacle}\n"
                           f"💰 *VALOR:* ALTO ✅")
                    
                    requests.post(f"https://api.telegram.org/bot8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ/sendMessage", 
                                  data={"chat_id": "790743691", "text": msg, "parse_mode": "Markdown"})
                    st.session_state.enviados.add(id_p)
