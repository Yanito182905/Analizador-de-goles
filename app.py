
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN Y ESTILO PRO
st.set_page_config(page_title="Sistema Triple 6% Pro", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
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

# 3. SESIÓN Y DATOS
if 'bank_actual' not in st.session_state: st.session_state.bank_actual = 300.0
if 'historico' not in st.session_state: 
    st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 4. FUNCIONES DE TELEGRAM
def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    return requests.post(url, data=payload)

# 5. SIDEBAR: CONTROL DE BANCA Y NOTIFICACIONES
with st.sidebar:
    st.header("⚙️ Configuración")
    if st.button("🔔 Probar Notificación"):
        enviar_telegram("✅ ¡Sistema 6% Conectado! Las notificaciones están activas.")
        st.success("Test enviado a Telegram")
    
    st.divider()
    st.header("📓 Registro Diario")
    monto = st.number_input("Resultado neto ($)", value=0.0, help="Positivo para ganancia, Negativo para pérdida")
    if st.button("💾 Guardar Jornada"):
        nueva = {'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Resultado': monto, 'Banca': st.session_state.bank_actual + monto}
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva])], ignore_index=True)
        st.session_state.bank_actual += monto
        st.rerun()

# 6. DASHBOARD PRINCIPAL
st.title("💰 Mi Panel de Inversión 6%")
meta_hoy = st.session_state.bank_actual * 0.06

col1, col2, col3 = st.columns(3)
with col1: st.metric("Banca Actual", f"${st.session_state.bank_actual:.2f}")
with col2: st.metric("Meta de Hoy", f"${meta_hoy:.2f}", "🎯")
with col3:
    ganancia_neta = st.session_state.bank_actual - 300.0
    st.metric("Balance Total", f"${ganancia_neta:.2f}", f"{((ganancia_neta/300)*100):.1f}%")

# 7. GRÁFICA DE RENTABILIDAD
if not st.session_state.historico.empty:
    st.subheader("📈 Evolución de mi Capital")
    st.line_chart(st.session_state.historico.set_index('Fecha')['Banca'])
else:
    st.info("La gráfica aparecerá cuando registres tu primer resultado en el panel lateral.")

# 8. ESCÁNER DE TRIPLE ESTRATEGIA
st.divider()
if st.button('🚀 ESCANEAR PARTIDOS DE HOY'):
    url_fixtures = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Analizando oportunidades de inversión...'):
        res = requests.get(url_fixtures, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        
        # Filtros de ligas por estrategia
        ligas_25 = ['Bundesliga', 'Super League', 'Allsvenskan', 'Norwegian Premier League']
        ligas_ht = ['Eerste Divisie', 'Eredivisie']
        
        stake = meta_hoy / 0.35 # Cálculo basado en cuota 1.35
        
        for p in partidos:
            liga = p['league']['name']
            home, away = p['teams']['home']['name'], p['teams']['away']['name']
            hora = p['fixture']['date'][11:16]
            
            # Clasificación inteligente
            if liga in ligas_25:
                est, css, emoj = "OVER 2.5", "card-25", "🔥"
            elif liga in ligas_ht:
                est, css, emoj = "OVER 0.5 HT", "card-ht", "⚡"
            else:
                est, css, emoj = "OVER 1.5", "card-15", "🛡️"

            # Mostrar en pantalla
            st.markdown(f"""<div class="{css}">
                <h4>{emoj} {home} vs {away}</h4>
                <b>ESTRATEGIA:</b> {est} | 🏆 {liga} | ⏰ {hora}<br>
                <b>INVERTIR:</b> ${stake:.2f} para ganar ${meta_hoy:.2f}
            </div>""", unsafe_allow_html=True)

            # Enviar a Telegram
            enviar_telegram(f"{emoj} *PICK {est}*\n⚽ {home} vs {away}\n💰 Stake: ${stake:.2f}\n📈 Meta: +${meta_hoy:.2f}")
