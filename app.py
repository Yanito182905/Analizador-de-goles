import streamlit as st
import requests
from datetime import datetime

# --- CREDENCIALES FIJAS ---
TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
ID_CANAL = "-5298539210"
API_FOOTBALL_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"

st.set_page_config(page_title="STOMS ULTRA ELITE", layout="wide")

# --- DISEÑO NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .neon-card { 
        border: 2px solid #00ff41; padding: 20px; border-radius: 15px; 
        margin-bottom: 15px; background: #050505;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 900; height: 3em; }
    .neon-title { color: #00ff41; text-shadow: 0 0 10px #00ff41; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GESTIÓN DE DINERO ---
st.sidebar.markdown("<h2 style='color:#00ff41;'>💰 BANCA STOMS</h2>", unsafe_allow_html=True)
banca = st.sidebar.number_input("Capital Actual ($)", value=600)
meta_6 = banca * 0.06
st.sidebar.markdown(f"<div style='border:1px solid #ffd700; padding:10px; text-align:center;'>META HOY: <br><b style='font-size:1.5em;'>${meta_6:.2f}</b></div>", unsafe_allow_html=True)

# --- CUERPO ---
st.markdown("<h1 class='neon-title'>⚡ TERMINAL DE SEÑALES ELITE</h1>", unsafe_allow_html=True)

# Botón principal de escaneo
if st.button("🔍 ESCANEAR PARTIDOS DE HOY"):
    with st.spinner('Conectando con el satélite...'):
        url_api = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": API_FOOTBALL_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        hoy = datetime.now().strftime('%Y-%m-%d')
        
        try:
            response = requests.get(url_api, headers=headers, params={"date": hoy}, timeout=15)
            data = response.json()
            partidos = data.get('response', [])
            
            if partidos:
                st.success(f"✅ Se han detectado {len(partidos)} partidos.")
                for p in partidos[:15]:
                    home = p['teams']['home']['name']
                    away = p['teams']['away']['name']
                    liga = p['league']['name']
                    hora = p['fixture']['date'][11:16]
                    
                    # Cálculo de Stake para tus 36€ de meta
                    stake_sug = (meta_6 * 0.40) / 0.5 # Basado en cuota 1.50

                    st.markdown(f"""
                    <div class="neon-card">
                        <div style="display: flex; justify-content: space-between; color: #888;">
                            <span>🏆 {liga}</span><span>⏰ {hora}</span>
                        </div>
                        <h2 style="margin:10px 0;">{home} vs {away}</h2>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color:#00ff41; font-weight:bold;">🎯 MERCADO: OVER 1.5</span>
                            <span style="color:#ffd700; font-weight:bold;">💰 STAKE: ${stake_sug:.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Botón de envío individual
                    if st.button(f"📲 NOTIFICAR A TELEGRAM: {home}", key=f"btn_{home}"):
                        msg = f"⚽ *SEÑAL STOMS*\n🏟️ {home} vs {away}\n🏆 {liga}\n💰 *STAKE: ${stake_sug:.2f}*\n🎯 Mercado: Over 1.5"
                        res_tel = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": ID_CANAL, "text": msg, "parse_mode": "Markdown"})
                        if res_tel.status_code == 200:
                            st.toast("¡Señal enviada con éxito! ✅")
                        else:
                            st.error("Error de envío: El bot no es Administrador del canal.")
            else:
                st.warning("No hay partidos programados para hoy según la API.")
        except Exception as e:
            st.error(f"Fallo crítico de conexión: {e}")

st.markdown("---")
st.caption("STOMS IA - Meta de crecimiento diario: 6%")
