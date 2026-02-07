import streamlit as st
import requests

# --- TUS DATOS ---
API_TOKEN = "c5992c3e7e074dc5b8e9bea0f6abaf88"
TOKEN_BOT = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
ID_CANAL = "-5298539210"

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="STOMS ALPHA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .neon-card { border: 1px solid #00ff41; padding: 20px; border-radius: 15px; background: #0a0a0a; margin-bottom: 15px; box-shadow: 0 0 10px #00ff41; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 900; background: transparent; border: 1px solid #00ff41; color: #00ff41; }
    .stButton>button:hover { background: #00ff41; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR 6% ---
st.sidebar.title("📈 ESTRATEGIA STOMS")
banca = st.sidebar.number_input("BANCA ($)", value=600)
meta_6 = banca * 0.06
st.sidebar.success(f"OBJETIVO HOY: ${meta_6:.2f}")

st.title("⚡ ESCÁNER DE FÚTBOL REAL")

# --- FUNCIÓN TELEGRAM ---
def enviar_alerta(txt):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    requests.post(url, json={"chat_id": ID_CANAL, "text": txt, "parse_mode": "Markdown"})

# --- LÓGICA DE DATOS ---
if st.button("🔍 CARGAR PARTIDOS DE HOY"):
    # Usamos el endpoint de partidos del día (Today)
    url = "https://api.football-data.org/v2/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            if not matches:
                st.info("No hay partidos en curso o programados ahora mismo en las ligas soportadas.")
            else:
                st.success(f"✅ Conectado. Mostrando {len(matches)} partidos.")
                
                for m in matches:
                    home = m['homeTeam']['name']
                    away = m['awayTeam']['name']
                    liga = m['competition']['name']
                    status = m['status']
                    
                    # Stake calculado para tu meta de 6%
                    stake = (meta_6 * 0.35) / 0.5 
                    
                    st.markdown(f"""
                    <div class="neon-card">
                        <small style="color:#888;">{liga} | Status: {status}</small>
                        <h2>{home} vs {away}</h2>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color:#00ff41; font-weight:bold;">MERCADO: OVER 1.5</span>
                            <span style="color:#ffd700; font-weight:bold;">STAKE: ${stake:.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"📲 NOTIFICAR: {home}", key=f"{home}_{m['id']}"):
                        mensaje = f"⚽ *SEÑAL STOMS*\n🏟️ {home} vs {away}\n🏆 {liga}\n🎯 Mercado: Over 1.5\n💰 *Stake: ${stake:.2f}*"
                        enviar_alerta(mensaje)
                        st.toast("Enviado al canal")
                        
        elif response.status_code == 403:
            st.error("🚫 Error 403 persistente.")
            st.info("Tu Token es correcto, pero es posible que el plan gratuito necesite unas horas para activarse tras confirmar el email. Intentemos de nuevo en un momento.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        st.error(f"Error de conexión: {e}")

st.markdown("---")
st.caption("STOMS Terminal - Trabajando con tu meta de crecimiento del 6%.")
