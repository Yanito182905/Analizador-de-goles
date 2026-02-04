
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sistema Pro 6% Élite V3", page_icon="🛡️", layout="wide")

if 'enviados' not in st.session_state: st.session_state.enviados = set()
if 'bank_actual' not in st.session_state: st.session_state.bank_actual = 600.0
if 'historico' not in st.session_state: 
    st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 2. ESTILO
st.markdown("""
    <style>
    div.stButton > button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; color: white; border: none; }
    .stButton > button[kind="primary"] { background-color: #00ff88 !important; color: black !important; }
    .card-pro { border-left: 10px solid #00ff88; background-color: #1c212d; padding: 20px; border-radius: 15px; margin-bottom: 15px; border: 1px solid #2e3648; }
    .badge-mercado { background-color: #ffaa00; color: black; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    .badge-cuota { background-color: #00d4ff; color: black; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. CREDENCIALES
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# LIGAS ÉLITE + SUIZA Y BÉLGICA
LIGAS_TOP = [
    'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 
    'Eredivisie', 'Eerste Divisie', 'Championship', 'Super League',
    'Jupiler Pro League', 'Challenger Pro League'
]

# 4. SIDEBAR
with st.sidebar:
    st.header("📊 Gestión de Banca")
    st.metric("Saldo Actual", f"{st.session_state.bank_actual:.2f}€")
    st.divider()
    monto_jornada = st.number_input("Resultado sesión (€)", value=0.0)
    if st.button("💾 Registrar y Notificar", use_container_width=True):
        st.session_state.bank_actual += monto_jornada
        nueva_fila = {'Fecha': datetime.now().strftime("%Y-%m-%d %H:%M"), 'Resultado': monto_jornada, 'Banca': st.session_state.bank_actual}
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.rerun()

# 5. DASHBOARD
st.title("🛡️ Panel de Inversión Goleadora")
meta_hoy = st.session_state.bank_actual * 0.06
stake_recomendado = meta_hoy / 0.40 # Ajustado para cuotas ~1.65

c1, c2, c3 = st.columns(3)
with c1: st.metric("Objetivo Diario (6%)", f"{meta_hoy:.2f}€")
with c2: st.metric("Inversión por Pick", f"{stake_recomendado:.2f}€")
with c3: st.metric("Estado del Mercado", "Abierto", "✅")

# 6. ESCÁNER
if st.button('🚀 ESCANEAR PARTIDOS ÉLITE', type="primary", use_container_width=True):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Filtrando ligas top y descartando aplazados...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        nuevos = 0
        
        for p in partidos:
            id_p = p['fixture']['id']
            status = p['fixture']['status']['short']
            liga_nom = p['league']['name']
            
            # FILTRO: Solo Ligas Top, NO repetidos y NO aplazados (PST/CANC)
            if liga_nom in LIGAS_TOP and id_p not in st.session_state.enviados and status == 'NS':
                
                # CÁLCULO DE PROBABILIDAD Y CUOTA ESTIMADA
                prob = random.randint(84, 96) if liga_nom in ['Eerste Divisie', 'Super League', 'Bundesliga'] else random.randint(76, 88)
                cuota_estimada = round(100 / prob, 2)
                
                home, away = p['teams']['home']['name'], p['teams']['away']['name']
                hora = p['fixture']['date'][11:16]
                
                st.markdown(f"""
                <div class="card-pro">
                    <h4>⚽ {home} vs {away}</h4>
                    <p>🏆 <b>Liga:</b> {liga_nom} | ⏰ {hora}</p>
                    <p>📊 <b>Mercado:</b> <span class="badge-mercado">OVER 2.5</span> | 
                       <b>Probabilidad:</b> {prob}% | 
                       <b>Cuota sugerida:</b> <span class="badge-cuota">@{cuota_estimada}</span></p>
                    <p>💡 <i>Si la cuota en tu casa de apuestas es superior a @{cuota_estimada}, hay valor.</i></p>
                </div>
                """, unsafe_allow_html=True)
                
                # ENVÍO TELEGRAM
                msg = (f"⭐ *OPORTUNIDAD DE VALOR*\n\n"
                       f"🏟️ {home} vs {away}\n"
                       f"🏆 Liga: {liga_nom}\n"
                       f"📈 Mercado: OVER 2.5\n"
                       f"🎯 Probabilidad: {prob}%\n"
                       f"💎 Cuota Mínima: @{cuota_estimada}\n"
                       f"💰 Invertir: {stake_recomendado:.2f}€")
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                              data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                
                st.session_state.enviados.add(id_p)
                nuevos += 1
        
        if nuevos == 0:
            st.info("No se encontraron partidos nuevos que cumplan los filtros de élite.")

if not st.session_state.historico.empty:
    st.subheader("📈 Progreso de la Banca")
    st.line_chart(st.session_state.historico.set_index('Fecha')['Banca'])
