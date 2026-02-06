import streamlit as st
import requests
from datetime import datetime, timedelta

# --- CREDENCIALES ---
TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
ID_CANAL = "-5298539210"
API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"

st.set_page_config(page_title="STOMS RESCATE", layout="wide")

# --- DISEÑO NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .neon-card { border: 2px solid #00ff41; padding: 15px; border-radius: 12px; margin-bottom: 10px; background: #050505; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ STOMS RECOVERY MODE")

# --- SIDEBAR ---
banca = st.sidebar.number_input("BANCA ($)", value=600)
meta = banca * 0.06
st.sidebar.markdown(f"### META HOY: ${meta:.2f}")

# --- FUNCIÓN DE ESCANEO ---
def buscar_partidos(fecha):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    try:
        res = requests.get(url, headers=headers, params={"date": fecha}, timeout=10)
        return res.json().get('response', [])
    except:
        return []

# --- BOTÓN DE ACCIÓN ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 ESCANEAR HOY"):
        hoy = datetime.now().strftime('%Y-%m-%d')
        partidos = buscar_partidos(hoy)
        st.session_state['lista'] = partidos
        if not partidos: st.error("No hay partidos hoy en la API.")

with col2:
    if st.button("📅 ESCANEAR MAÑANA"):
        manana = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        partidos = buscar_partidos(manana)
        st.session_state['lista'] = partidos
        if not partidos: st.error("No hay partidos mañana.")

# --- MOSTRAR RESULTADOS ---
if 'lista' in st.session_state and st.session_state['lista']:
    for p in st.session_state['lista'][:15]:
        h, a = p['teams']['home']['name'], p['teams']['away']['name']
        liga = p['league']['name']
        
        st.markdown(f"""
            <div class="neon-card">
                <small>{liga}</small>
                <h3>{h} vs {a}</h3>
                <p style="color:#00ff41;">MERCADO: OVER 1.5 | STAKE: ${(meta*0.4):.2f}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📲 NOTIFICAR {h}", key=f"btn_{h}"):
            msg = f"⚽ SEÑAL: {h} vs {away}\n💰 Stake: ${meta*0.4:.2f}\n🎯 Over 1.5"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": ID_CANAL, "text": msg})
            st.toast("Enviado")
