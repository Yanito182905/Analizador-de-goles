
import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from datetime import datetime

# --- 1. CONFIGURACIÓN DE LAS LLAVES (SEGURIDAD) ---
GOOGLE_API_KEY = "AIzaSyAIDAx_6DD0nSY6hv4aZ4RKsvw-xjy0bYw"
FOOTBALL_API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
TELEGRAM_CHAT_ID = "5298539210"

# Configurar Cerebro Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Versión rápida y potente

# --- 2. ESTILO NEON PROFESIONAL (Basado en Stitch) ---
st.set_page_config(page_title="STOMS IA ELITE", layout="wide")

st.markdown(f"""
    <style>
    .main {{ background-color: #060606; color: #00ff41; }}
    .stButton>button {{ 
        width: 100%; border-radius: 12px; height: 4em; font-weight: bold; 
        transition: 0.3s; border: 2px solid #00ff41; background-color: transparent; color: #00ff41;
    }}
    .stButton>button:hover {{ background-color: #00ff41; color: black; box-shadow: 0 0 20px #00ff41; }}
    .card {{ 
        background-color: #111; padding: 20px; border-radius: 15px; 
        border: 1px solid #333; margin-bottom: 10px; 
    }}
    .neon-text-green {{ color: #00ff41; text-shadow: 0 0 5px #00ff41; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCIONES LÓGICAS ---
def analizar_con_ia(datos_partido):
    prompt_sistema = f"""
    Eres STOMS IA. Analiza este partido para mi estrategia del 6% de crecimiento.
    Reglas: Solo Over 1.5/2.5. Ligas Top. 
    Datos del partido: {datos_partido}
    Responde en este formato:
    CALIFICACIÓN: [VERDE/AZUL/ROJO]
    RAZÓN: [Breve explicación de xG y probabilidad]
    """
    response = model.generate_content(prompt_sistema)
    return response.text

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

# --- 4. INTERFAZ DE USUARIO ---
st.title("⚡ STOMS IA: MOTOR DE ELITE")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/5968/5968866.png", width=100)
st.sidebar.header("Control de Inversión")
st.sidebar.write("🎯 Objetivo: **6% Growth**")
st.sidebar.write("📧 yanielramirez895@gmail.com")

# Fila de Botones Neon (Diseño Stitch)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔍 ESCANEAR JORNADA"):
        with st.spinner('IA analizando mercados...'):
            # Simulación de llamada a API (Ligas Top)
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            querystring = {"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"}
            headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
            
            response = requests.get(url, headers=headers, params=querystring)
            fixtures = response.json().get('response', [])[:10] # Analizamos los primeros 10 para ahorrar tiempo

            for f in fixtures:
                equipo_h = f['teams']['home']['name']
                equipo_a = f['teams']['away']['name']
                liga = f['league']['name']
                
                # Llamada al cerebro de Google
                analisis = analizar_con_ia(f"{equipo_h} vs {equipo_a} en {liga}")
                
                if "VERDE" in analisis or "AZUL" in analisis:
                    st.markdown(f"""
                    <div class="card">
                        <span class="neon-text-green">{analisis.split('RAZÓN:')[0]}</span><br>
                        <b>Partido:</b> {equipo_h} vs {equipo_a}<br>
                        <b>Análisis IA:</b> {analisis.split('RAZÓN:')[1] if 'RAZÓN:' in analisis else analisis}
                    </div>
                    """, unsafe_allow_html=True)
                    enviar_telegram(f"🚀 *PICK DETECTADO*\n🏟️ {equipo_h} vs {equipo_a}\n{analisis}")

with col2:
    if st.button("📊 RENDIMIENTO 10 DÍAS"):
        st.write("Generando tabla de crecimiento...")
        df_stats = pd.DataFrame({"Día": ["1", "2", "3"], "Crecimiento": ["+1.2%", "+0.8%", "+1.5%"]})
        st.table(df_stats)

with col3:
    if st.button("🔔 TEST NOTIFICACIÓN"):
        enviar_telegram("✅ Sistema STOMS IA vinculado con Google Gemini correctamente.")
        st.toast("Mensaje enviado!")

# Footer
st.divider()
st.caption("Conectado a Google AI Studio | API-Football | 2026 Elite System")
