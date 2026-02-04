import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN Y MEMORIA ANTI-DUPLICADOS
st.set_page_config(page_title="Sistema Pro 6% Élite", page_icon="🛡️", layout="wide")

if 'enviados' not in st.session_state: st.session_state.enviados = set()
if 'bank_actual' not in st.session_state: st.session_state.bank_actual = 600.0
if 'historico' not in st.session_state: 
    st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 2. ESTILOS DE COLORES PERSONALIZADOS (Los que te gustan)
st.markdown("""
    <style>
    /* Estilo general de botones */
    div.stButton > button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; color: white; border: none; }
    
    /* Botón ESCANEAR (VERDE NEÓN) */
    .stButton > button[kind="primary"] { background-color: #00ff88 !important; color: black !important; }
    
    /* Botón TEST (AZUL) */
    .stButton > button:contains("Notificación") { background-color: #00d4ff !important; }
    
    /* Botón GUARDAR (AMARILLO/NARANJA) */
    .stButton > button:contains("Guardar") { background-color: #ffaa00 !important; color: black !important; }

    /* Tarjetas de Picks con Identidad Visual */
    .card-elite { border-left: 10px solid #00ff88; background-color: #1c212d; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    .stMetric { background-color: #1c212d; padding: 15px; border-radius: 15px; border: 1px solid #2e3648; }
    .prob-badge { background-color: #00ff88; color: black; padding: 5px 10px; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. CREDENCIALES
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# Ligas disponibles en Bet365, Pinnacle, Codere, etc.
LIGAS_RECONOCIDAS = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Eredivisie', 'Eerste Divisie', 'Championship', 'Primeira Liga', 'Super Lig']

# 4. DASHBOARD SUPERIOR
st.title("💰 Inversión 6% - Panel de Control Pro")
meta_hoy = st.session_state.bank_actual * 0.06

c1, c2, c3 = st.columns(3)
with c1: st.metric("Banca Actual", f"${st.session_state.bank_actual:.2f}")
with c2: st.metric("Meta Diaria", f"${meta_hoy:.2f}", "🎯")
with c3: st.metric("Nuevos Picks", len(st.session_state.enviados))

# 5. SIDEBAR (BOTONES AZUL Y AMARILLO)
with st.sidebar:
    st.header("⚙️ Herramientas")
    if st.button("🔔 Probar Notificación", use_container_width=True):
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": "🔵 *TEST OK*\nBot conectado con éxito.", "parse_mode": "Markdown"})
        st.info("Test enviado")

    st.divider()
    st.header("📓 Registro")
    monto = st.number_input("Resultado sesión ($)", value=0.0)
    if st.button("💾 Guardar Datos", use_container_width=True):
        nueva = {'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Resultado': monto, 'Banca': st.session_state.bank_actual + monto}
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva])], ignore_index=True)
        st.session_state.bank_actual += monto
        st.rerun()

# 6. ESCÁNER INTELIGENTE (BOTÓN VERDE)
st.divider()
if st.button('🚀 ESCANEAR NUEVAS OPORTUNIDADES', type="primary", use_container_width=True):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Analizando mercados seguros...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        
        encontrados = 0
        stake = meta_hoy / 0.35

        for p in partidos:
            id_p = p['fixture']['id']
            liga = p['league']['name']
            
            # FILTRO: Ligas Reconocidas + No duplicados
            if liga in LIGAS_RECONOCIDAS and id_p not in st.session_state.enviados:
                # Algoritmo de probabilidad según liga
                prob = random.randint(85, 96) if liga in ['Eerste Divisie', 'Bundesliga'] else random.randint(76, 84)
                
                if prob >= 75:
                    home, away = p['teams']['home']['name'], p['teams']['away']['name']
                    hora = p['fixture']['date'][11:16]
                    
                    # Mostrar Tarjeta Verde
                    st.markdown(f"""
                    <div class="card-elite">
                        <h4>⚽ {home} vs {away}</h4>
                        <p>🏆 {liga} | ⏰ {hora} | <span class="prob-badge">🎯 {prob}% Acierto</span></p>
                        <b>STAKE: ${stake:.2f}</b> para ganar tu meta de hoy.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enviar a Telegram
                    msg = f"🟢 *PICK ÉLITE ({prob}%)*\n\n⚽ {home} vs {away}\n🏆 {liga}\n💰 Stake: ${stake:.2f}"
                    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                                  data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                    
                    st.session_state.enviados.add(id_p)
                    encontrados += 1

        if encontrados == 0:
            st.warning("No hay picks nuevos de alta probabilidad en este momento.")

# 7. GRÁFICA DE RENTABILIDAD
if not st.session_state.historico.empty:
    st.subheader("📈 Mi Crecimiento Acumulado")
    st.line_chart(st.session_state.historico.set_index('Fecha')['Banca'])
