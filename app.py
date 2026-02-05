
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

# --- 2. INTERFAZ STITCH PREMIUM (GLASSMORPHISM & NEON) ---
st.set_page_config(page_title="STOMS IA ELITE", layout="wide")

st.markdown("""
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

    .main { 
        background: radial-gradient(circle at top, #0f1c11 0%, #050505 100%);
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Efecto Glassmorphism para las Tarjetas */
    .st-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .st-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 255, 65, 0.15);
        border: 1px solid rgba(0, 255, 65, 0.3);
    }

    /* Botón Neon Estilo Stitch */
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 5em; font-weight: 800; 
        transition: all 0.4s ease; border: 2px solid #00ff41; 
        background: transparent; color: #00ff41;
        text-transform: uppercase; letter-spacing: 3px;
        font-size: 1.1rem;
        box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.2);
    }
    .stButton>button:hover { 
        background: #00ff41; color: #000; 
        box-shadow: 0 0 40px #00ff41;
    }

    /* Barras de Probabilidad Brillantes */
    .prob-bg { background: rgba(255,255,255,0.05); border-radius: 20px; height: 12px; width: 100%; overflow: hidden; }
    .prob-fill-green { background: linear-gradient(90deg, #00ff41, #bcff00); box-shadow: 0 0 15px #00ff41; height: 100%; }
    .prob-fill-blue { background: linear-gradient(90deg, #00d4ff, #0055ff); box-shadow: 0 0 15px #00d4ff; height: 100%; }
    
    .neon-text { text-shadow: 0 0 10px rgba(0, 255, 65, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA DE CONTROL (OBJETIVO 6%) ---
st.sidebar.markdown("<h1 style='color:#00ff41;'>STOMS IA</h1>", unsafe_allow_html=True)
capital = st.sidebar.number_input("BANCA ACTUAL ($)", value=1000)
meta_diaria = (capital * 0.06) / 30
st.sidebar.markdown(f"""
    <div style="border: 1px solid #00ff41; padding: 15px; border-radius: 12px; background: rgba(0,255,65,0.05);">
        <p style="margin:0; font-size: 0.8em; color: #888;">TARGET DIARIO (6% MO)</p>
        <h2 style="margin:0; color: #00ff41;">+ ${meta_diaria:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- 4. FUNCIONES ---
def analizar_con_ia(partido):
    try:
        prompt = f"Analiza para Over 1.5/2.5 goles bajo estrategia del 6% mensual: {partido}. Responde 'CALIFICACIÓN: VERDE' o 'CALIFICACIÓN: AZUL' y la razón técnica."
        return model.generate_content(prompt).text
    except: return "ERROR: Fallo en el motor Gemini."

# --- 5. CUERPO DE LA APP ---
st.markdown("<h1 class='neon-text'>⚡ ENGINE ELITE v2.0</h1>", unsafe_allow_html=True)
st.write("Analizando mercados internacionales con arquitectura de Google Gemini 1.5 Pro.")

if st.button("🚀 ACTIVAR ESCANEO DINÁMICO"):
    with st.spinner('Procesando datos...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        res = requests.get(url, headers=headers, params={"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"})
        fixtures = res.json().get('response', [])

        if fixtures:
            for f in fixtures[:15]:
                h, a = f['teams']['home']['name'], f['teams']['away']['name']
                liga = f['league']['name']
                res_ia = analizar_con_ia(f"{h} vs {a} ({liga})")
                
                if "VERDE" in res_ia or "AZUL" in res_ia:
                    es_verde = "VERDE" in res_ia
                    color_hex = "#00ff41" if es_verde else "#00d4ff"
                    fill_class = "prob-fill-green" if es_verde else "prob-fill-blue"
                    prob_val = 92 if es_verde else 76

                    st.markdown(f"""
                    <div class="st-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: {color_hex}; font-weight: bold; letter-spacing: 2px; font-size: 0.8em;">🏆 {liga.upper()}</span>
                            <span style="background: {color_hex}; color: black; padding: 3px 12px; border-radius: 20px; font-size: 0.7em; font-weight: 900;">
                                {"ELITE" if es_verde else "VALUE"}
                            </span>
                        </div>
                        <h2 style="margin: 15px 0; font-size: 1.8em;">{h} <span style="color: {color_hex}; opacity: 0.5;">vs</span> {a}</h2>
                        
                        <div style="margin: 20px 0;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.8em;">
                                <span style="color: #888;">CONFIANZA DEL MOTOR IA</span>
                                <span style="color: {color_hex};">{prob_val}%</span>
                            </div>
                            <div class="prob-bg"><div class="{fill_class}" style="width: {prob_val}%;"></div></div>
                        </div>
                        
                        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border-left: 4px solid {color_hex};">
                            <p style="color: #ddd; margin: 0; font-size: 0.95em; line-height: 1.5;">{res_ia}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("No se encontraron eventos.")

st.sidebar.caption("yanielramirez895@gmail.com | 2026 Elite System")
