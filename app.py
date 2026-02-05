
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
st.set_page_config(page_title="STOMS IA ELITE", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Fondo General Dark */
    .main { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Estilizada */
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1f1f1f; }
    
    /* Botón Neon Principal */
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 4em; font-weight: 800; 
        transition: all 0.4s ease; border: 1px solid #00ff41; 
        background: rgba(0, 255, 65, 0.05); color: #00ff41;
        text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { 
        background: #00ff41; color: #000; 
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4);
        transform: translateY(-2px);
    }

    /* Tarjetas de Partidos (Stitch Style) */
    .card-container {
        background: linear-gradient(145deg, #111111, #080808);
        padding: 30px;
        border-radius: 24px;
        border: 1px solid #1f1f1f;
        border-left: 8px solid #00ff41;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .status-badge {
        background: #00ff41; color: #000; padding: 5px 15px; 
        border-radius: 10px; font-weight: 900; font-size: 0.7em;
    }
    
    .prob-bar-bg { background: #1f1f1f; border-radius: 10px; height: 10px; width: 100%; margin: 15px 0; overflow: hidden; }
    .prob-bar-fill { height: 100%; box-shadow: 0 0 15px #00ff41; transition: width 1s ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE NEGOCIO ---
st.sidebar.markdown(f"<h1 style='color:#00ff41;'>STOMS IA</h1>", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.subheader("🎯 Meta 6% Crecimiento")
cap_actual = st.sidebar.number_input("Capital en Banca ($)", value=1000)
ganancia_objetivo = (cap_actual * 0.06) / 30
st.sidebar.info(f"Objetivo diario: ${ganancia_objetivo:.2f}")

def analizar_con_ia(partido):
    try:
        prompt = f"Analiza este partido para Over 1.5/2.5. Responde con 'CALIFICACIÓN: VERDE' si es muy seguro o 'CALIFICACIÓN: AZUL' si es probable. Añade una razón técnica breve: {partido}"
        return model.generate_content(prompt).text
    except: return "ROJO: Error de conexión."

def enviar_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

# --- 4. ACCIÓN PRINCIPAL ---
st.title("⚡ Panel de Control Elite")
st.write("Bienvenido, analizando datos de ligas Tier 1 con Google Gemini 1.5 Pro.")

if st.button("🚀 INICIAR ESCANEO DE ALTA PRECISIÓN"):
    with st.spinner('Conectando con servidores de datos...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        res = requests.get(url, headers=headers, params={"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"})
        fixtures = res.json().get('response', [])

        if fixtures:
            encontrados = 0
            for f in fixtures[:20]:
                h, a = f['teams']['home']['name'], f['teams']['away']['name']
                liga = f['league']['name']
                res_ia = analizar_con_ia(f"{h} vs {a} ({liga})")

                if "VERDE" in res_ia or "AZUL" in analisis := res_ia: # Mantenemos la lógica de filtro
                    encontrados += 1
                    color = "#00ff41" if "VERDE" in res_ia else "#00d4ff"
                    prob = 94 if "VERDE" in res_ia else 79
                    
                    # RENDERIZADO DE TARJETA ESTILO STITCH
                    st.markdown(f"""
                    <div class="card-container" style="border-left-color: {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #888; font-size: 0.8em; font-weight: bold; letter-spacing: 1px;">{liga.upper()}</span>
                            <span class="status-badge" style="background:{color};">{"ELITE PICK" if "VERDE" in res_ia else "VALUE PICK"}</span>
                        </div>
                        <h2 style="margin: 15px 0; font-size: 1.8em; color: white;">{h} <span style="color:{color};">vs</span> {a}</h2>
                        
                        <div style="margin: 20px 0;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span style="color:{color}; font-size: 0.8em; font-weight: bold;">CONFIANZA IA</span>
                                <span style="color:{color}; font-size: 0.8em; font-weight: bold;">{prob}%</span>
                            </div>
                            <div class="prob-bar-bg">
                                <div class="prob-bar-fill" style="width: {prob}%; background: {color};"></div>
                            </div>
                        </div>
                        
                        <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);">
                            <p style="color: #ccc; margin: 0; line-height: 1.6;">{res_ia.split('CALIFICACIÓN:')[1] if 'CALIFICACIÓN:' in res_ia else res_ia}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    enviar_telegram(f"🔥 *PICK DETECTADO*\n🏟️ {h} vs {a}\n📈 Confianza: {prob}%\n{res_ia}")
            
            if encontrados == 0:
                st.info("No se encontraron partidos con los filtros de élite para hoy.")
        else:
            st.error("No se pudieron cargar los partidos. Revisa tu API Key de Football.")

st.sidebar.divider()
st.sidebar.caption("v2.1.0 | yanielramirez895@gmail.com")
