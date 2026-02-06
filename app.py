
import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
GOOGLE_API_KEY = "AIzaSyAIDAx_6DD0nSY6hv4aZ4RKsvw-xjy0bYw"
FOOTBALL_API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
TELEGRAM_CHAT_ID = "5298539210"

# Inicializar IA
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200, r.text
    except Exception as e:
        return False, str(e)

# --- 2. LIGAS AMPLIADAS (MÁS FLEXIBILIDAD) ---
LIGAS_ORO = {
    "Albanian Cup": 81.82, "Landspokal Cup": 79.81, "Bulgarian Cup": 78.95,
    "Hungarian Cup": 77.56, "Super League": 67.42, "Premier League": 66.10,
    "Eerste Divisie": 64.92, "Eredivisie": 63.0, "Challenge League": 56.0,
    "Bundesliga": 62.5, "La Liga": 55.0, "Serie A": 54.0, "Ligue 1": 53.0
}

# --- 3. DISEÑO NEON EXTREMO ---
st.set_page_config(page_title="STOMS ULTRA ELITE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .neon-title { color: #00ff41; text-shadow: 0 0 15px #00ff41; font-weight: 900; text-align: center; font-size: 3em; }
    .card-elite {
        background: #0a0a0a; border-radius: 15px; padding: 20px;
        margin-bottom: 15px; border: 1px solid #1a1a1a;
    }
    .oro-border { border: 2px solid #ffd700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.4) !important; }
    div.stButton > button { width: 100%; font-weight: 900; border-radius: 10px; height: 3.5em; text-transform: uppercase; }
    .btn-telegram button { border: 2px solid #00d4ff !important; color: #00d4ff !important; background: rgba(0,212,255,0.1) !important; }
    .btn-verde button { border: 2px solid #00ff41 !important; color: #00ff41 !important; }
    .btn-verde button:hover { background: #00ff41 !important; color: #000 !important; box-shadow: 0 0 30px #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
st.sidebar.markdown("<h1 style='color:#00ff41;'>STOMS IA</h1>", unsafe_allow_html=True)
banca = st.sidebar.number_input("💵 BANCA ACTUAL ($)", value=600)
meta_diaria = banca * 0.06

st.sidebar.markdown(f"<div style='border: 2px solid #ffd700; padding: 10px; border-radius: 10px; text-align:center;'>META: <b>${meta_diaria:.2f}</b></div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write("📲 **BOTÓN DE NOTIFICACIÓN**")
with st.sidebar.container():
    st.markdown('<div class="btn-telegram">', unsafe_allow_html=True)
    if st.button("🔔 PROBAR CONEXIÓN TELEGRAM"):
        exito, r_text = enviar_telegram("✅ ¡Conexión establecida! Sistema listo para el 6%.")
        if exito: st.sidebar.success("¡Mensaje enviado!")
        else: st.sidebar.error(f"Error: {r_text}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. CUERPO PRINCIPAL ---
st.markdown("<h1 class='neon-title'>⚡ TERMINAL ULTRA ELITE</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 RADAR 15 PARTIDOS", "📊 RENDIMIENTO"])

with tab1:
    col_f1, col_f2 = st.columns([2, 1])
    fecha_consulta = col_f1.date_input("Selecciona fecha de análisis", datetime.now())
    
    if st.button("🚀 INICIAR ESCÁNER"):
        with st.spinner('Conectando con la base de datos mundial...'):
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
            
            # Buscamos partidos para la fecha seleccionada
            res = requests.get(url, headers=headers, params={"date": fecha_consulta.strftime('%Y-%m-%d')})
            data = res.json()
            fixtures = data.get('response', [])

            if fixtures:
                st.write(f"🔎 Partidos analizados: **{len(fixtures)}**")
                # Mostramos hasta 15 partidos
                for f in fixtures[:15]:
                    h, a = f['teams']['home']['name'], f['teams']['away']['name']
                    liga = f['league']['name']
                    pais = f['league']['country']
                    hora = f['fixture']['date'][11:16]
                    
                    score_liga = next((v for k, v in LIGAS_ORO.items() if k in liga), 50.0)
                    es_oro = score_liga > 60.0
                    
                    # Llamada IA simplificada para evitar bloqueos
                    try:
                        prompt = f"Analiza {h} vs {a}. Mercado Over 1.5. Responde solo CALIFICACIÓN: VERDE y %."
                        analisis = model.generate_content(prompt).text
                    except:
                        analisis = "CALIFICACIÓN: AZUL (Análisis técnico offline)"
                    
                    color_class = "verde" if "VERDE" in analisis else "azul"
                    color_hex = "#00ff41" if color_class == "verde" else "#00d4ff"
                    stake = (meta_diaria * 0.35) / 0.5 

                    st.markdown(f"""
                    <div class="card-elite {'oro-border' if es_oro else ''}">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color:#888;">{pais.upper()} | {liga.upper()}</span>
                            <span style="color:#ffd700; font-weight:bold;">{'⭐ LIGA ORO' if es_oro else ''}</span>
                        </div>
                        <h2 style="margin:5px 0;">{h} vs {a} <small style="color:#666;">{hora}</small></h2>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color:{color_hex}; font-weight:bold;">IA: {color_class.upper()}</span>
                            <span style="color:#ffd700; font-weight:bold;">STAKE: ${stake:.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown(f'<div class="btn-verde">', unsafe_allow_html=True)
                        if st.button(f"CONFIRMAR Y ENVIAR: {h}", key=f"btn_{h}"):
                            msg = f"⚽ *SEÑAL STOMS*\n🏟️ {h} vs {a}\n🏆 {liga}\n💰 Stake: ${stake:.2f}\n🎯 Mercado: Over 1.5"
                            ok, _ = enviar_telegram(msg)
                            if ok: st.toast("Señal enviada!")
                            else: st.error("Error al enviar")
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No hay partidos en esta fecha. Prueba a seleccionar el día de mañana.")

with tab2:
    st.subheader("📊 Tabla de Rendimiento")
    st.write(pd.DataFrame(list(LIGAS_ORO.items()), columns=['Liga', 'Score %']))
