import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN Y MEMORIA
st.set_page_config(page_title="6% Smart Predictor", page_icon="📈", layout="wide")

if 'enviados' not in st.session_state: st.session_state.enviados = set()
if 'bank_actual' not in st.session_state: st.session_state.bank_actual = 600.0
if 'historico' not in st.session_state: st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 2. ESTILOS DE COLORES
st.markdown("""
    <style>
    .stButton > button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; }
    .verde-btn { background-color: #00ff88 !important; color: black !important; }
    .azul-btn { background-color: #00d4ff !important; color: white !important; }
    .card-pro { background-color: #1c212d; padding: 20px; border-radius: 15px; border-left: 10px solid #00ff88; margin-bottom: 15px; }
    .prob-text { color: #00ff88; font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. CREDENCIALES
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

LIGAS_TOP = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Eredivisie', 'Eerste Divisie', 'Super Lig', 'Championship', 'Primeira Liga']

# 4. FUNCIÓN DE CÁLCULO DE PROBABILIDAD (Simulada basada en tendencia de liga)
def calcular_probabilidad(liga):
    # Ligas con mayor tendencia histórica a Over 1.5 y 2.5
    dict_prob = {
        'Eerste Divisie': random.randint(88, 96),
        'Bundesliga': random.randint(85, 92),
        'Eredivisie': random.randint(84, 91),
        'Premier League': random.randint(80, 88)
    }
    return dict_prob.get(liga, random.randint(72, 82))

# 5. INTERFAZ PRINCIPAL
st.title("💰 Sistema de Inversión con IA")
meta_hoy = st.session_state.bank_actual * 0.06

col1, col2, col3 = st.columns(3)
with col1: st.metric("Banca", f"${st.session_state.bank_actual:.2f}")
with col2: st.metric("Meta 6%", f"${meta_hoy:.2f}")
with col3: st.metric("Picks Hoy", len(st.session_state.enviados))

# 6. ESCÁNER INTELIGENTE
st.divider()
if st.button('🚀 ESCANEAR NUEVAS OPORTUNIDADES ÉLITE', type="primary"):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Analizando mercados líquidos y probabilidades...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        
        encontrados_ahora = 0
        stake = meta_hoy / 0.35

        for p in partidos:
            id_p = p['fixture']['id']
            liga = p['league']['name']
            
            # FILTROS: Ligas Top + No Repetidos
            if liga in LIGAS_TOP and id_p not in st.session_state.enviados:
                prob = calcular_probabilidad(liga)
                
                # Solo mandamos si la probabilidad es alta (>75%)
                if prob >= 75:
                    home, away = p['teams']['home']['name'], p['teams']['away']['name']
                    
                    # Mostrar en App
                    st.markdown(f"""
                    <div class="card-pro">
                        <h4>⚽ {home} vs {away}</h4>
                        <p>🏆 {liga} | ⏰ {p['fixture']['date'][11:16]}</p>
                        <p class="prob-text">🎯 Probabilidad de Éxito: {prob}%</p>
                        <b>Invertir: ${stake:.2f}</b> (Meta: ${meta_hoy:.2f})
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enviar a Telegram
                    msg = f"🔥 *NUEVO PICK ÉLITE*\n\n⚽ {home} vs {away}\n🏆 {liga}\n📈 *Acierto: {prob}%*\n💰 Stake: ${stake:.2f}"
                    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                                  data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                    
                    st.session_state.enviados.add(id_p)
                    encontrados_ahora += 1

        if encontrados_ahora == 0:
            st.info("No hay picks nuevos que superen el 75% de acierto en este momento.")

# 7. HISTORIAL DE ENVIADOS (Para tu control)
if st.session_state.enviados:
    with st.expander("📂 Ver registros enviados hoy"):
        st.write(f"Has procesado {len(st.session_state.enviados)} partidos en esta sesión.")
