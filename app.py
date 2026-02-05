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

# --- 2. INTERFAZ MAESTRA (ESTILO STITCH NEON) ---
st.set_page_config(page_title="STOMS IA ELITE", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1f1f1f; }
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 4em; font-weight: 800; 
        transition: all 0.4s ease; border: 1px solid #00ff41; 
        background: rgba(0, 255, 65, 0.05); color: #00ff41;
        text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { 
        background: #00ff41; color: #000; box-shadow: 0 0 30px rgba(0, 255, 65, 0.4);
    }
    .card-container {
        background: linear-gradient(145deg, #111111, #080808);
        padding: 30px; border-radius: 24px; border: 1px solid #1f1f1f;
        margin-bottom: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    .prob-bar-bg { background: #1f1f1f; border-radius: 10px; height: 10px; width: 100%; margin: 15px 0; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
st.sidebar.title("🎯 META 6%")
cap_actual = st.sidebar.number_input("Capital Actual ($)", value=1000)
st.sidebar.info(f"Objetivo diario: ${(cap_actual * 0.06 / 30):.2f}")

# --- 4. FUNCIONES ---
def analizar_con_ia(partido):
    try:
        prompt = f"Analiza para Over 1.5/2.5. Responde: CALIFICACIÓN: [VERDE/AZUL] y razón breve: {partido}"
        return model.generate_content(prompt).text
    except: return "ROJO: Error"

def enviar_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

# --- 5. LÓGICA PRINCIPAL ---
st.title("⚡ STOMS IA: PANEL ELITE")

if st.button("🚀 INICIAR ESCANEO DE ALTA PRECISIÓN"):
    with st.spinner('Escaneando mercados...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        res = requests.get(url, headers=headers, params={"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"})
        fixtures = res.json().get('response', [])

        if fixtures:
            for f in fixtures[:15]:
                h, a = f['teams']['home']['name'], f['teams']['away']['name']
                liga = f['league']['name']
                
                # CORRECCIÓN AQUÍ: Separamos la asignación de la comparación
                res_ia = analizar_con_ia(f"{h} vs {a} ({liga})")
                
                if "VERDE" in res_ia or "AZUL" in res_ia:
                    color = "#00ff41" if "VERDE" in res_ia else "#00d4ff"
                    prob = 94 if "VERDE" in res_ia else 79
                    
                    st.markdown(f"""
                    <div class="card-container" style="border-left: 8px solid {color};">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #888; font-size: 0.8em;">{liga}</span>
                            <span style="background:{color}; color:black; padding:2px 10px; border-radius:5px; font-weight:bold; font-size:0.7em;">IA PICK</span>
                        </div>
                        <h2 style="color: white; margin: 10px 0;">{h} vs {a}</h2>
                        <div class="prob-bar-bg"><div style="width:{prob}%; background:{color}; height:100%;"></div></div>
                        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:10px; color:#ccc;">
                            {res_ia}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    enviar_telegram(f"✅ PICK: {h} vs {a}\n{res_ia}")
        else:
            st.error("No se encontraron partidos.")
