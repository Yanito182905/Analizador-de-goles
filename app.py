import streamlit as st
import requests

# --- TUS CREDENCIALES ---
TOKEN_BOT = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
ID_CANAL = "-5298539210"

st.set_page_config(page_title="STOMS OPERATOR PRO", layout="wide")

# Diseño Elite
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1a1a1a !important; color: #00ff41 !important; border: 1px solid #00ff41 !important;
    }
    .stButton>button {
        width: 100%; background: #00ff41 !important; color: #000 !important; font-weight: bold; border-radius: 10px; height: 3em;
    }
    .header-box { border: 2px solid #00ff41; padding: 20px; border-radius: 15px; text-align: center; background: #000; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- ESTRATEGIA 6% ---
st.sidebar.title("📊 GESTIÓN DE RIESGO")
banca = st.sidebar.number_input("BANCA TOTAL ($)", value=600)
meta_diaria = banca * 0.06

st.sidebar.markdown(f"""
    <div style='background:#1a1a1a; padding:15px; border-radius:10px; border: 1px solid #ffd700;'>
        <p style='margin:0; color:#888;'>OBJETIVO HOY</p>
        <h2 style='margin:0; color:#ffd700;'>${meta_diaria:.2f}</h2>
    </div>
""", unsafe_allow_html=True)

# --- CUERPO ---
st.markdown('<div class="header-box"><h1>⚡ PANEL DE SEÑALES STOMS</h1><p>Introduce el partido manualmente para calcular el Stake exacto</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    local = st.text_input("🏠 EQUIPO LOCAL", placeholder="Ej: Real Madrid")
    visita = st.text_input("🚀 EQUIPO VISITANTE", placeholder="Ej: Getafe")

with col2:
    liga = st.text_input("🏆 LIGA", placeholder="Ej: La Liga")
    cuota = st.number_input("📈 CUOTA OVER 1.5", value=1.40, step=0.01)

# LÓGICA DE STAKE INTELIGENTE
# Buscamos ganar el 33% de la meta diaria en esta entrada (necesitas 3 aciertos para el 6%)
ganancia_buscada = meta_diaria / 3
stake_necesario = ganancia_buscada / (cuota - 1)

st.markdown(f"""
    <div style="background:#111; padding:20px; border-radius:15px; border-left: 10px solid #00ff41; margin: 20px 0;">
        <p style="margin:0; color:#888;">ANÁLISIS DE ENTRADA</p>
        <h2 style="margin:0;">{local} vs {visita}</h2>
        <h1 style="color:#00ff41;">STAKE SUGERIDO: ${stake_necesario:.2f}</h1>
        <small style="color:#ffd700;">Con este stake buscas una ganancia de ${ganancia_buscada:.2f}</small>
    </div>
""", unsafe_allow_html=True)

if st.button("🚀 ENVIAR ALERTA A TELEGRAM"):
    if local and visita:
        msg = (
            f"⚽ *NUEVA SEÑAL STOMS*\n\n"
            f"🏟️ *Partido:* {local} vs {visita}\n"
            f"🏆 *Liga:* {liga}\n"
            f"🎯 *Mercado:* Over 1.5 Goles\n"
            f"💰 *Stake:* ${stake_necesario:.2f}\n"
            f"📉 *Cuota:* {cuota}\n\n"
            f"📈 *Estrategia:* Crecimiento 6% Diario"
        )
        
        try:
            url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
            r = requests.post(url, json={"chat_id": ID_CANAL, "text": msg, "parse_mode": "Markdown"})
            if r.status_code == 200:
                st.success("✅ ¡Señal enviada al canal!")
            else:
                st.error("Error al enviar. Revisa el Token del Bot.")
        except:
            st.error("Fallo de conexión con Telegram.")
    else:
        st.error("Por favor, rellena los equipos.")

st.markdown("---")
st.caption("Modo Manual Activo | Evitando bloqueos de API externa.")
