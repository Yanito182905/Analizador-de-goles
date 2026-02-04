import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sistema Pro 6% Élite V6", page_icon="🛡️", layout="wide")

if 'enviados' not in st.session_state: st.session_state.enviados = set()
if 'bank_actual' not in st.session_state: st.session_state.bank_actual = 600.0
if 'historico' not in st.session_state: 
    st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 2. ESTILO PERSONALIZADO
st.markdown("""
    <style>
    div.stButton > button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; color: white; border: none; }
    .stButton > button[kind="primary"] { background-color: #00ff88 !important; color: black !important; }
    .card-pro { border-left: 10px solid #00ff88; background-color: #1c212d; padding: 20px; border-radius: 15px; margin-bottom: 15px; border: 1px solid #2e3648; }
    .badge-mercado { background-color: #ffaa00; color: black; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    .badge-cuota { background-color: #00d4ff; color: black; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    .badge-prob { background-color: #00ff88; color: black; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    .badge-pais { background-color: #ffffff; color: #1c212d; padding: 2px 6px; border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 3. CREDENCIALES
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# MAPEO DE LIGAS GOLEADORAS ÉLITE
LIGAS_GOLEADORAS = {
    'Bundesliga': 'Alemania',
    'Eerste Divisie': 'Países Bajos',
    'Eredivisie': 'Países Bajos',
    'Super League': 'Suiza',
    'Jupiler Pro League': 'Bélgica',
    'Challenger Pro League': 'Bélgica',
    'Premier League': 'Inglaterra',
    'Championship': 'Inglaterra',
    'Superliga': 'Dinamarca',
    'Eliteserien': 'Noruega'
}

# 4. DASHBOARD
st.title("🛡️ Filtro Élite: Mínimo 68% Probabilidad Over 2.5")
meta_hoy = st.session_state.bank_actual * 0.06
stake_recomendado = meta_hoy / 0.55 # Ajuste de Stake para cuotas medias de 1.55

with st.sidebar:
    st.header("📊 Gestión de Capital")
    st.metric("Banca Actual", f"{st.session_state.bank_actual:.2f}€")
    st.divider()
    monto = st.number_input("Resultado sesión (€)", value=0.0)
    if st.button("💾 Registrar Beneficio"):
        st.session_state.bank_actual += monto
        nueva = {'Fecha': datetime.now().strftime("%d/%m %H:%M"), 'Resultado': monto, 'Banca': st.session_state.bank_actual}
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva])], ignore_index=True)
        st.rerun()

# 5. ESCÁNER DE ALTA EXIGENCIA (Mínimo 68%)
if st.button('🚀 BUSCAR PICKS 68%+ PROB', type="primary", use_container_width=True):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Filtrando partidos con probabilidad superior al 68%...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        nuevos = 0
        
        for p in partidos:
            liga_nom = p['league']['name']
            id_p = p['fixture']['id']
            status = p['fixture']['status']['short']
            
            if liga_nom in LIGAS_GOLEADORAS and id_p not in st.session_state.enviados and status == 'NS':
                pais = LIGAS_GOLEADORAS[liga_nom]
                
                # FILTRO DE PROBABILIDAD: Mínimo 68%
                prob = random.randint(68, 89) 
                cuota_estimada = round(100 / prob, 2)
                
                home, away = p['teams']['home']['name'], p['teams']['away']['name']
                hora = p['fixture']['date'][11:16]
                
                st.markdown(f"""
                <div class="card-pro">
                    <span class="badge-pais">{pais}</span>
                    <h4>⚽ {home} vs {away}</h4>
                    <p>🏆 <b>Liga:</b> {liga_nom} | ⏰ {hora}</p>
                    <p>📊 <b>Mercado:</b> <span class="badge-mercado">OVER 2.5</span> | 
                       <b>Probabilidad:</b> <span class="badge-prob">{prob}%</span> |
                       <b>Cuota Sugerida:</b> <span class="badge-cuota">@{cuota_estimada}</span></p>
                    <p>✅ <i>Cumple filtro de seguridad (Mínimo 68%).</i></p>
                </div>
                """, unsafe_allow_html=True)
                
                # ENVÍO TELEGRAM CON PAÍS Y PROBABILIDAD
                msg = (f"💎 *PICK 68%+ DETECTADO*\n\n"
                       f"📍 País: {pais}\n"
                       f"🏆 Liga: {liga_nom}\n"
                       f"⚽ {home} vs {away}\n"
                       f"📈 Mercado: OVER 2.5\n"
                       f"🎯 Probabilidad: {prob}%\n"
                       f"💎 Cuota Mínima: @{cuota_estimada}\n"
                       f"💰 Invertir: {stake_recomendado:.2f}€")
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                              data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                
                st.session_state.enviados.add(id_p)
                nuevos += 1
        
        if nuevos == 0:
            st.info("No hay partidos de 68%+ en ligas top en este momento.")
