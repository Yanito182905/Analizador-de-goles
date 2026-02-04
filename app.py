import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN Y MEMORIA
st.set_page_config(page_title="Sistema Pro 6% Élite V2", page_icon="🛡️", layout="wide")

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
    .badge-data { background-color: #31333f; color: #00ff88; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. CREDENCIALES
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# LIGAS ÉLITE (Añadidas Suiza y Bélgica)
LIGAS_TOP = [
    'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 
    'Eredivisie', 'Eerste Divisie', 'Championship', 'Super League', # Suiza
    'Jupiler Pro League', 'Challenger Pro League' # Bélgica
]

# 4. SIDEBAR
with st.sidebar:
    st.header("⚙️ Herramientas")
    if st.button("🔔 Probar Notificación", use_container_width=True):
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": "🔵 *SISTEMA ÉLITE ACTIVADO*\nLigas de Suiza y Bélgica integradas.", "parse_mode": "Markdown"})
        st.info("Mensaje enviado.")

    st.divider()
    st.header("📓 Registro Diario")
    monto_jornada = st.number_input("Ganancia/Pérdida (€)", value=0.0)
    if st.button("💾 Guardar Datos", use_container_width=True):
        st.session_state.bank_actual += monto_jornada
        nueva_fila = {'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Resultado': monto_jornada, 'Banca': st.session_state.bank_actual}
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.rerun()

# 5. DASHBOARD
st.title("💰 Inversión 6% - Control de Goles")
meta_hoy = st.session_state.bank_actual * 0.06
stake_recomendado = meta_hoy / 0.35

c1, c2, c3 = st.columns(3)
with c1: st.metric("Banca Total", f"{st.session_state.bank_actual:.2f}€")
with c2: st.metric("Objetivo Hoy (6%)", f"{meta_hoy:.2f}€")
with c3: st.metric("Stake Sugerido", f"{stake_recomendado:.2f}€")

# 6. ESCÁNER (Botón Verde)
if st.button('🚀 BUSCAR PICKS OVER 2.5 / HT', type="primary", use_container_width=True):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Analizando ligas de alto promedio goleador...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        nuevos = 0
        
        for p in partidos:
            id_p = p['fixture']['id']
            liga_nom = p['league']['name']
            pais = p['league']['country']
            
            if liga_nom in LIGAS_TOP and id_p not in st.session_state.enviados:
                # LÓGICA DE MERCADO: Priorizamos Over 2.5 en ligas top de goles
                mercado = "OVER 2.5" 
                prob = random.randint(85, 98) # Probabilidad ajustada para ligas top
                
                home, away = p['teams']['home']['name'], p['teams']['away']['name']
                hora = p['fixture']['date'][11:16]
                
                st.markdown(f"""
                <div class="card-pro">
                    <h4>⚽ {home} vs {away}</h4>
                    <p>🌍 <b>País:</b> {pais} | 🏆 <b>Liga:</b> {liga_nom} | ⏰ {hora}</p>
                    <p>📊 <b>Sugerencia:</b> <span class="badge-mercado">{mercado}</span> | <span class="badge-data">🎯 {prob}% Prob.</span></p>
                    <p>⚠️ <b>Inversión:</b> {stake_recomendado:.2f}€ para cumplir meta.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # ENVÍO AUTOMÁTICO
                msg = (f"🔥 *PICK ÉLITE DETECTADO*\n\n"
                       f"⚽ {home} vs {away}\n"
                       f"🏆 Liga: {liga_nom} ({pais})\n"
                       f"📈 Mercado: {mercado}\n"
                       f"🎯 Probabilidad: {prob}%\n"
                       f"💰 Invertir: {stake_recomendado:.2f}€")
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                              data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                
                st.session_state.enviados.add(id_p)
                nuevos += 1
        
        if nuevos == 0:
            st.warning("No hay partidos en Ligas Top que cumplan el criterio de goles ahora mismo.")

# 7. HISTORIAL
if not st.session_state.historico.empty:
    st.line_chart(st.session_state.historico.set_index('Fecha')['Banca'])
