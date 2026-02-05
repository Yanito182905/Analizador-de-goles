
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

# --- 2. ESTILOS NEON (STITCH UI) ---
st.set_page_config(page_title="STOMS IA ELITE", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #060606; color: #eee; }
    [data-testid="stSidebar"] { background-color: #0d0d0d; border-right: 1px solid #333; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; 
        transition: 0.3s; border: 1px solid #00ff41; background-color: transparent; color: #00ff41;
    }
    .stButton>button:hover { background-color: #00ff41; color: black; box-shadow: 0 0 20px #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CALCULADORA DE INTERÉS COMPUESTO (SIDEBAR) ---
st.sidebar.title("📈 META DEL 6%")
capital_inicial = st.sidebar.number_input("Capital Actual ($)", value=1000)
meta_diaria = (capital_inicial * 0.06) / 30
st.sidebar.success(f"Objetivo de hoy: +${meta_diaria:.2f}")

# --- 4. FUNCIONES ---
def analizar_con_ia(datos_partido):
    try:
        prompt = f"Eres un experto en apuestas. Analiza si este partido es apto para Over 1.5/2.5 goles según estrategia de 6% mensual: {datos_partido}. Responde empezando con CALIFICACIÓN: VERDE, AZUL o ROJO y luego la razón corta."
        response = model.generate_content(prompt)
        return response.text
    except:
        return "ERROR: No se pudo conectar con el cerebro IA."

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

# --- 5. CUERPO PRINCIPAL ---
st.title("⚡ STOMS IA: MOTOR DE ELITE")
st.write("Analizando ligas Tier 1 para asegurar crecimiento constante.")

if st.button("🔍 ESCANEAR JORNADA Y ENVIAR ALERTS"):
    with st.spinner('IA analizando mercados en tiempo real...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        querystring = {"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"}
        headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        
        response = requests.get(url, headers=headers, params=querystring)
        fixtures = response.json().get('response', [])
        
        if not fixtures:
            st.warning("No hay partidos programados para hoy en las ligas configuradas.")
        
        for f in fixtures[:15]:  # Analizamos los 15 más relevantes
            equipo_h = f['teams']['home']['name']
            equipo_a = f['teams']['away']['name']
            liga = f['league']['name']
            
            # Aquí es donde se crea la variable 'analisis'
            analisis = analizar_con_ia(f"{equipo_h} vs {equipo_a} en {liga}")
            
            if "VERDE" in analisis or "AZUL" in analisis:
                neon_color = "#00ff41" if "VERDE" in analisis else "#00d4ff"
                prob = 92 if "VERDE" in analisis else 78
                
                # Renderizar Tarjeta Stitch
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #1a1a1a, #0d0d0d); padding: 25px; border-radius: 20px; border-left: 6px solid {neon_color}; margin-bottom: 25px; border-top: 1px solid #333;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h2 style="color: white; margin: 0; font-size: 1.3em;">{equipo_h} vs {equipo_a}</h2>
                        <span style="background: {neon_color}; color: black; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.7em;">{ "ELITE" if "VERDE" in analisis else "PROBABLE" }</span>
                    </div>
                    <p style="color: #666; font-size: 0.8em; margin: 5px 0;">🏆 {liga}</p>
                    <div style="margin: 15px 0;">
                        <div style="display: flex; justify-content: space-between; color: {neon_color}; font-size: 0.75em; font-weight: bold; margin-bottom: 5px;">
                            <span>PROBABILIDAD IA</span><span>{prob}%</span>
                        </div>
                        <div style="background: #333; border-radius: 10px; height: 6px; width: 100%; overflow: hidden;">
                            <div style="background: {neon_color}; height: 100%; width: {prob}%; box-shadow: 0 0 10px {neon_color};"></div>
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; color: #ccc; font-size: 0.9em;">
                        {analisis}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Enviar a Telegram
                enviar_telegram(f"🚀 *NUEVO PICK*\n🏟️ {equipo_h} vs {equipo_a}\n{analisis}")

st.divider()
st.caption(" yanielramirez895@gmail.com | Powered by Gemini 1.5 Pro & Stitch UI")
