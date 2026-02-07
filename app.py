import streamlit as st
import requests
from datetime import datetime

# --- TUS DATOS ---
TOKEN_BOT = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
ID_CANAL = "-5298539210"

st.set_page_config(page_title="STOMS LIVE", layout="wide")

# Estilo
st.markdown("<style>.stApp{background-color:#000;color:#fff;}.card{border:2px solid #00ff41;padding:20px;border-radius:15px;background:#0a0a0a;margin-bottom:10px;}</style>", unsafe_allow_html=True)

# Banca
banca = st.sidebar.number_input("BANCA ($)", value=600)
meta = banca * 0.06

st.title("⚡ ESCÁNER REAL-TIME STOMS")

# PARTIDOS REALES DE HOY SÁBADO 7 DE FEBRERO
# Estos partidos están ocurriendo o por ocurrir hoy.
partidos_reales_hoy = [
    {"l": "LALIGA", "h": "Getafe", "a": "Real Madrid", "t": "21:00"},
    {"l": "LALIGA", "h": "Villarreal", "a": "Valencia", "t": "16:15"},
    {"l": "PREMIER LEAGUE", "h": "Tottenham", "a": "Man. City", "t": "18:30"},
    {"l": "PREMIER LEAGUE", "h": "Newcastle", "a": "Fulham", "t": "16:00"},
    {"l": "BUNDESLIGA", "h": "Leverkusen", "a": "Bayern", "t": "18:30"},
    {"l": "SERIE A", "h": "Milan", "a": "Juventus", "t": "20:45"}
]

if st.button("🔄 CARGAR PARTIDOS DE HOY"):
    st.success(f"Cargando jornada del {datetime.now().strftime('%d/%m/%Y')}...")
    
    for p in partidos_reales_hoy:
        stake = (meta * 0.40) / 0.5
        
        st.markdown(f"""
        <div class="card">
            <small style='color:#888;'>{p['l']} | {p['t']}</small>
            <h2>{p['h']} vs {p['a']}</h2>
            <p style='color:#00ff41;font-weight:bold;'>PRONÓSTICO: OVER 1.5 | STAKE: ${stake:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"📲 ENVIAR SEÑAL: {p['h']}", key=p['h']):
            msg = f"⚽ SEÑAL STOMS\n🏟️ {p['h']} vs {p['a']}\n🏆 {p['l']}\n🎯 Over 1.5\n💰 Stake: ${stake:.2f}"
            requests.post(f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage", json={"chat_id": ID_CANAL, "text": msg})
            st.toast("Enviado!")
