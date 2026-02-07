import streamlit as st
import requests

# --- TUS CREDENCIALES ACTUALIZADAS ---
API_TOKEN = "c5992c3e7e074dc5b8e9bea0f6abaf88"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
CHAT_ID = "-5298539210"

st.set_page_config(page_title="STOMS PRO SCANNER", layout="wide")

# --- ESTILO NEÓN ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    .card { 
        border: 2px solid #00ff41; padding: 25px; border-radius: 15px; 
        background: #161b22; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 900; background: transparent; border: 1px solid #00ff41; color: #00ff41; height: 3.5em; }
    .stButton>button:hover { background: #00ff41 !important; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GESTIÓN 6% ---
st.sidebar.title("💰 CONTROL DE BANCA")
banca = st.sidebar.number_input("BANCA ACTUAL ($)", value=600)
meta_6 = banca * 0.06
st.sidebar.markdown(f"""
    <div style='border:1px solid #ffd700; padding:15px; text-align:center; border-radius:10px;'>
        <span style='color:#ffd700;'>OBJETIVO DIARIO</span><br>
        <b style='font-size:1.8em; color:#ffd700;'>${meta_6:.2f}</b>
    </div>
""", unsafe_allow_html=True)

# --- PANEL PRINCIPAL ---
st.title("⚡ ESCÁNER REAL-TIME STOMS")
st.write("Conectado mediante Football-Data API (Direct)")

if st.button("🔍 ESCANEAR PARTIDOS DE HOY"):
    with st.spinner('Obteniendo partidos de las Ligas Top...'):
        # Endpoint para partidos programados (Scheduled)
        url = "https://api.football-data.org/v2/matches"
        headers = {"X-Auth-Token": API_TOKEN}
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                
                if not matches:
                    st.warning("No hay partidos de las ligas principales programados para las próximas horas.")
                else:
                    st.success(f"Se han encontrado {len(matches)} partidos disponibles.")
                    
                    for m in matches[:15]: # Mostramos los primeros 15
                        h = m['homeTeam']['name']
                        a = m['awayTeam']['name']
                        liga = m['competition']['name']
                        hora = m['utcDate'][11:16]
                        
                        # Cálculo de Stake para tu meta de $36 (6% de 600)
                        # Buscamos ganar aprox. $12 por partido (1/3 de la meta)
                        stake = (meta_6 * 0.35) / 0.5 

                        st.markdown(f"""
                        <div class="card">
                            <div style="display: flex; justify-content: space-between; color: #8b949e; font-size: 0.9em;">
                                <span>🏆 {liga}</span><span>⏰ {hora} UTC</span>
                            </div>
                            <h2 style="margin:15px 0; color:#fff;">{h} vs {a}</h2>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="color:#00ff41; font-weight:bold; font-size:1.1em;">🎯 OVER 1.5 GOLES</span>
                                <span style="color:#ffd700; font-weight:bold; font-size:1.2em;">STAKE: ${stake:.2f}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"📲 NOTIFICAR: {h}", key=f"btn_{h}"):
                            msg = f"⚽ *SEÑAL STOMS*\n🏟️ {h} vs {a}\n🏆 {liga}\n🎯 Mercado: Over 1.5\n💰 *Stake: ${stake:.2f}*"
                            r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                                             json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                            if r.status_code == 200:
                                st.toast(f"¡Señal de {h} enviada!")
                            else:
                                st.error("Error al enviar a Telegram.")
            else:
                st.error(f"Error de API: {response.status_code}. Revisa si la Token es correcta.")
                
        except Exception as e:
            st.error(f"Fallo de conexión: {e}")

st.markdown("---")
st.caption("STOMS IA v6.0 - Sistema de Crecimiento Acelerado (6%)")
