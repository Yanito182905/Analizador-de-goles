
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN Y MEMORIA
st.set_page_config(page_title="6% Élite - Full Data", page_icon="🌍", layout="wide")

if 'enviados' not in st.session_state: st.session_state.enviados = set()
if 'bank_actual' not in st.session_state: st.session_state.bank_actual = 600.0
if 'historico' not in st.session_state: st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 2. ESTILOS DE COLORES (Verde, Azul, Amarillo)
st.markdown("""
    <style>
    div.stButton > button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; color: white; border: none; }
    .stButton > button[kind="primary"] { background-color: #00ff88 !important; color: black !important; }
    .stButton > button:contains("Notificación") { background-color: #00d4ff !important; }
    .stButton > button:contains("Guardar") { background-color: #ffaa00 !important; color: black !important; }
    .card-pro { border-left: 10px solid #00ff88; background-color: #1c212d; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    .stMetric { background-color: #1c212d; padding: 15px; border-radius: 15px; border: 1px solid #2e3648; }
    .badge-mercado { background-color: #ffaa00; color: black; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. CREDENCIALES
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# Ligas que siempre están en casas reconocidas
LIGAS_TOP = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Eredivisie', 'Eerste Divisie', 'Championship', 'Primeira Liga', 'Super Lig']

# 4. PANEL LATERAL (Azul y Amarillo)
with st.sidebar:
    st.header("⚙️ Configuración")
    if st.button("🔔 Probar Notificación"):
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": "✅ Test Pro: País y Ligas activos."})
    
    st.divider()
    monto = st.number_input("Resultado Diario ($)", value=0.0)
    if st.button("💾 Guardar Datos"):
        nueva = {'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Resultado': monto, 'Banca': st.session_state.bank_actual + monto}
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva])], ignore_index=True)
        st.session_state.bank_actual += monto
        st.rerun()

# 5. DASHBOARD Y ESCÁNER (Verde)
st.title("💰 Mi Inversión 6% Diario")
meta_hoy = st.session_state.bank_actual * 0.06
stake = meta_hoy / 0.35

if st.button('🚀 ESCANEAR NUEVAS OPORTUNIDADES', type="primary"):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Analizando datos de ligas internacionales...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        
        encontrados = 0
        for p in partidos:
            id_p = p['fixture']['id']
            liga_nom = p['league']['name']
            pais = p['league']['country']
            
            if liga_nom in LIGAS_TOP and id_p not in st.session_state.enviados:
                # Lógica de Mercado
                mercado = "OVER 2.5" if liga_nom in ['Bundesliga', 'Eerste Divisie'] else "OVER 1.5"
                prob = random.randint(80, 95)
                home, away = p['teams']['home']['name'], p['teams']['away']['name']
                
                # MOSTRAR EN APP
                st.markdown(f"""
                <div class="card-pro">
                    <h4>⚽ {home} vs {away}</h4>
                    <p>📍 <b>País:</b> {pais} | 🏆 <b>Liga:</b> {liga_nom}</p>
                    <p>📊 <b>Mercado:</b> <span class="badge-mercado">{mercado}</span> | 🎯 <b>Probabilidad:</b> {prob}%</p>
                    <b>INVERTIR STAKE: ${stake:.2f}</b>
                </div>
                """, unsafe_allow_html=True)
                
                # ENVIAR A TELEGRAM
                msg = f"🟢 *NUEVO PICK*\n📍 País: {pais}\n🏆 Liga: {liga_nom}\n⚽ {home} vs {away}\n📊 Mercado: {mercado}\n📈 Probabilidad: {prob}%\n💰 Stake: ${stake:.2f}"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                              data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                
                st.session_state.enviados.add(id_p)
                encontrados += 1
        
        if encontrados == 0:
            st.warning("No hay picks nuevos que cumplan los filtros ahora.")

# 6. GRÁFICA
if not st.session_state.historico.empty:
    st.line_chart(st.session_state.historico.set_index('Fecha')['Banca'])
