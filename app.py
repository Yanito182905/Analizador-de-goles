import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. ESTILO Y CONFIGURACIÓN
st.set_page_config(page_title="Sistema Triple 6%", page_icon="📈", layout="wide")

# CSS para diferenciar las 3 estrategias por colores
st.markdown("""
    <style>
    .stMetric { background-color: #1c212d; padding: 15px; border-radius: 15px; border: 1px solid #2e3648; }
    .card-15 { border-left: 5px solid #00ff88; background-color: #1c212d; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .card-25 { border-left: 5px solid #ffaa00; background-color: #1c212d; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .card-ht { border-left: 5px solid #00d4ff; background-color: #1c212d; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CREDENCIALES
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

if 'bank_actual' not in st.session_state: st.session_state.bank_actual = 300.0
if 'historico' not in st.session_state: st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 3. PANEL DE CONTROL
st.title("📊 Sistema de Inversión Triple")
meta_hoy = st.session_state.bank_actual * 0.06

col1, col2, col3 = st.columns(3)
with col1: st.metric("Banca", f"${st.session_state.bank_actual:.2f}")
with col2: st.metric("Meta 6%", f"${meta_hoy:.2f}")
with col3: 
    ganado = len(st.session_state.historico[st.session_state.historico['Resultado'] > 0])
    perdido = len(st.session_state.historico[st.session_state.historico['Resultado'] < 0])
    st.write(f"✅ {ganado} | ❌ {perdido}")

# Registro de pérdidas/ganancias en el sidebar
with st.sidebar:
    st.header("📓 Registro")
    monto = st.number_input("Resultado ($)", value=0.0)
    if st.button("Guardar"):
        nueva = {'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Resultado': monto, 'Banca': st.session_state.bank_actual + monto}
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva])], ignore_index=True)
        st.session_state.bank_actual += monto
        st.rerun()

# 4. ESCÁNER PRO
if st.button('🚀 BUSCAR OPORTUNIDADES'):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Analizando estadísticas de goles...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        
        # Ligas TOP para cada estrategia
        ligas_15 = ['Premier League', 'Serie A', 'La Liga']
        ligas_25 = ['Bundesliga', 'Super League (Suiza)', 'Allsvenskan']
        ligas_ht = ['Eerste Divisie (Holanda)', 'Eredivisie']

        for p in partidos:
            liga = p['league']['name']
            home = p['teams']['home']['name']
            away = p['teams']['away']['name']
            hora = p['fixture']['date'][11:16]
            
            # Clasificar según liga y tendencia
            if liga in ligas_25:
                est, css, emoji = "OVER 2.5 GOLES", "card-25", "🔥"
            elif liga in ligas_ht:
                est, css, emoji = "OVER 0.5 HT (Gol 1T)", "card-ht", "⚡"
            else:
                est, css, emoji = "OVER 1.5 GOLES", "card-15", "🛡️"

            # Mostrar en App
            st.markdown(f"""<div class="{css}">
                <h4>{emoji} {home} vs {away}</h4>
                <b>ESTRATEGIA:</b> {est} | 🏆 {liga} | ⏰ {hora}<br>
                <b>STAKE:</b> ${(meta_hoy/0.35):.2f} (para ganar ${meta_hoy:.2f})
            </div>""", unsafe_allow_html=True)

            # Enviar a Telegram
            msg = f"{emoji} *PICK {est}*\n⚽ {home} vs {away}\n💰 Invertir: ${(meta_hoy/0.35):.2f}"
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                          data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

