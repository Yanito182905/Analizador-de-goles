import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
GOOGLE_API_KEY = "AIzaSyAIDAx_6DD0nSY6hv4aZ4RKsvw-xjy0bYw"
FOOTBALL_API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
TELEGRAM_CHAT_ID = "5298539210"

# Inicializar Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. INTERFAZ MAESTRA (DISEÑO STITCH NEON COMPLETO) ---
st.set_page_config(page_title="STOMS IA ELITE", layout="wide")

st.markdown("""
    <style>
    /* Fondo y Base */
    .main { background-color: #060606; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1f1f1f; }
    
    /* Títulos y Texto */
    h1 { color: #00ff41; text-shadow: 0 0 15px rgba(0,255,65,0.3); font-weight: 800; }
    
    /* Botón Neon Gigante */
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 5em; font-weight: 900; 
        transition: all 0.4s ease; border: 2px solid #00ff41; 
        background: rgba(0, 255, 65, 0.05); color: #00ff41;
        text-transform: uppercase; letter-spacing: 2px;
        margin-top: 20px;
    }
    .stButton>button:hover { 
        background: #00ff41; color: #000; 
        box-shadow: 0 0 40px rgba(0, 255, 65, 0.6);
        transform: scale(1.01);
    }

    /* Tarjetas de Partidos Estilo Stitch */
    .card-container {
        background: linear-gradient(145deg, #111111, #080808);
        padding: 30px; border-radius: 25px; border: 1px solid #222;
        margin-bottom: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    
    .prob-bar-bg { background: #222; border-radius: 20px; height: 12px; width: 100%; margin: 15px 0; overflow: hidden; }
    .prob-bar-fill { height: 100%; box-shadow: 0 0 15px #00ff41; border-radius: 20px; }
    
    .badge {
        padding: 5px 15px; border-radius: 8px; font-weight: 800; font-size: 0.7em; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRA LATERAL (CONTROL DE BANCA 6%) ---
st.sidebar.markdown("# 🚀 STOMS IA")
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Plan de Crecimiento")
banca = st.sidebar.number_input("Capital en Banca ($)", value=1000)
objetivo_diario = (banca * 0.06) / 30
st.sidebar.markdown(f"""
    <div style="background: rgba(0,255,65,0.1); padding: 15px; border-radius: 10px; border: 1px solid #00ff41;">
        <p style="color: #00ff41; margin: 0; font-size: 0.8em;">OBJETIVO DIARIO</p>
        <h2 style="color: #00ff41; margin: 0;">${objetivo_diario:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.caption("Usuario: yanielramirez895@gmail.com")

# --- 4. FUNCIONES ---
def analizar_con_ia(partido):
    try:
        prompt = f"Analiza para Over 1.5/2.5 goles: {partido}. Responde 'CALIFICACIÓN: VERDE' o 'CALIFICACIÓN: AZUL' seguido de una breve razón técnica."
        return model.generate_content(prompt).text
    except: return "ERROR: Sin conexión"

def enviar_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

# --- 5. CUERPO DE LA APP ---
st.title("⚡ PANEL DE CONTROL ELITE")
st.markdown("Analizando mercados internacionales bajo estrategia de interés compuesto.")

# Botón principal con estilo
if st.button("🔥 ESCANEAR MERCADOS Y ACTIVAR ALERTA"):
    with st.spinner('IA procesando datos de API-Football...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        res = requests.get(url, headers=headers, params={"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"})
        fixtures = res.json().get('response', [])

        if fixtures:
            for f in fixtures[:15]:
                h, a = f['teams']['home']['name'], f['teams']['away']['name']
                liga = f['league']['name']
                
                res_ia = analizar_con_ia(f"{h} vs {a} ({liga})")
                
                # Filtro de Calidad
                if "VERDE" in res_ia or "AZUL" in res_ia:
                    color = "#00ff41" if "VERDE" in res_ia else "#00d4ff"
                    label = "ELITE PICK" if "VERDE" in res_ia else "VALUE PICK"
                    prob = 94 if "VERDE" in res_ia else 78
                    
                    # TARJETA MODERNIZADA
                    st.markdown(f"""
                    <div class="card-container" style="border-left: 10px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #666; font-weight: bold; font-size: 0.8em;">🏆 {liga.upper()}</span>
                            <span class="badge" style="background: {color}; color: black;">{label}</span>
                        </div>
                        <h2 style="margin: 15px 0; color: white;">{h} <span style="color: {color};">vs</span> {a}</h2>
                        
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="color: {color}; font-size: 0.8em; font-weight: bold;">CONFIANZA DEL SISTEMA</span>
                            <span style="color: {color}; font-size: 0.8em; font-weight: bold;">{prob}%</span>
                        </div>
                        <div class="prob-bar-bg">
                            <div class="prob-bar-fill" style="width: {prob}%; background: {color};"></div>
                        </div>
                        
                        <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px; border: 1px solid #222;">
                            <p style="color: #ddd; margin: 0; line-height: 1.6;">{res_ia}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    enviar_telegram(f"🚀 *PICK DETECTADO*\n🏟️ {h} vs {a}\n📈 Confianza: {prob}%\n{res_ia}")
        else:
            st.error("No se detectaron partidos para procesar.")
