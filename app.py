
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

# --- 2. DISEÑO NEON EXTREMO (CSS PERSONALIZADO) ---
st.set_page_config(page_title="STOMS IA ELITE", layout="wide")

st.markdown("""
    <style>
    /* Forzar fondo negro total */
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #1a1a1a; }
    
    /* Títulos Neon */
    .neon-title { color: #00ff41; text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41; font-weight: 900; font-size: 2.5em; }

    /* Botón Neon Gigante */
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 4.5em; font-weight: 900; 
        border: 2px solid #00ff41; background-color: #000000; color: #00ff41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); transition: 0.3s;
        text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { 
        background-color: #00ff41; color: #000; box-shadow: 0 0 40px #00ff41; transform: scale(1.01);
    }

    /* Tarjetas Dinámicas de Colores */
    .card {
        background: #0a0a0a; padding: 25px; border-radius: 15px; margin-bottom: 25px;
        border: 1px solid #1a1a1a; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .verde { border-left: 10px solid #00ff41; box-shadow: inset 0 0 15px rgba(0, 255, 65, 0.1); }
    .azul { border-left: 10px solid #00d4ff; box-shadow: inset 0 0 15px rgba(0, 212, 255, 0.1); }
    .amarillo { border-left: 10px solid #ffd700; }
    .rojo { border-left: 10px solid #ff4b4b; }

    /* Barras de Probabilidad */
    .bar-bg { background: #1a1a1a; border-radius: 10px; height: 12px; width: 100%; margin-top: 10px; overflow: hidden; }
    .bar-fill { height: 100%; transition: width 0.8s ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRA LATERAL (CONTROL DE BANCA) ---
st.sidebar.markdown("<h2 style='color:#00ff41;'>STOMS IA</h2>", unsafe_allow_html=True)
capital = st.sidebar.number_input("💵 BANCA ACTUAL ($)", value=1000)
objetivo = (capital * 0.06) / 30
st.sidebar.markdown(f"""
    <div style='border: 1px solid #00ff41; padding: 15px; border-radius: 10px; background: rgba(0,255,65,0.05);'>
        <p style='color:#888; margin:0;'>OBJETIVO 6% HOY</p>
        <h3 style='color:#00ff41; margin:0;'>+ ${objetivo:.2f}</h3>
    </div>
    """, unsafe_allow_html=True)

# --- 4. CUERPO DE LA APP ---
st.markdown("<h1 class='neon-title'>⚡ PANEL DE CONTROL ELITE</h1>", unsafe_allow_html=True)
st.write("Bienvenido. El motor Gemini 1.5 Pro está listo para el análisis del 6%.")

if st.button("🔍 ESCANEAR JORNADA (MODO IA ACTIVADO)"):
    with st.spinner('Analizando partidos con el cerebro de Google...'):
        # Simulación de llamada a API para asegurar que veas el diseño
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        res = requests.get(url, headers=headers, params={"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"})
        fixtures = res.json().get('response', [])

        if fixtures:
            for f in fixtures[:10]:
                h, a = f['teams']['home']['name'], f['teams']['away']['name']
                liga = f['league']['name']
                
                # Llamada a la IA
                prompt = f"Analiza {h} vs {a}. Solo responde CALIFICACIÓN: [VERDE/AZUL/AMARILLO/ROJO] y una razón corta."
                analisis = model.generate_content(prompt).text
                
                # Determinar Color y Probabilidad
                color_class = "rojo"
                color_hex = "#ff4b4b"
                prob = 30
                
                if "VERDE" in analisis: 
                    color_class, color_hex, prob = "verde", "#00ff41", 95
                elif "AZUL" in analisis: 
                    color_class, color_hex, prob = "azul", "#00d4ff", 80
                elif "AMARILLO" in analisis: 
                    color_class, color_hex, prob = "amarillo", "#ffd700", 60

                # MOSTRAR TARJETA NEON
                st.markdown(f"""
                <div class="card {color_class}">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #666; font-size: 0.8em; font-weight: bold;">{liga.upper()}</span>
                        <span style="color: {color_hex}; font-weight: 900;">{color_class.upper()} PICK</span>
                    </div>
                    <h2 style="margin: 10px 0; color: #fff;">{h} vs {a}</h2>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8em; color: {color_hex};">
                        <span>CONFIANZA IA</span><span>{prob}%</span>
                    </div>
                    <div class="bar-bg">
                        <div class="bar-fill" style="width: {prob}%; background: {color_hex}; box-shadow: 0 0 10px {color_hex};"></div>
                    </div>
                    <p style="margin-top: 15px; color: #ccc; font-size: 0.9em; background: rgba(255,255,255,0.03); padding: 10px; border-radius: 8px;">
                        {analisis}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("No se detectaron partidos.")

st.sidebar.markdown("---")
st.sidebar.caption("yanielramirez895@gmail.com")
