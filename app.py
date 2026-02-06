import streamlit as st
import requests
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
ID_CANAL = "-5298539210"
API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"

st.set_page_config(page_title="STOMS ELITE V3", layout="wide")

# --- ESTILO NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .neon-card { border: 2px solid #00ff41; padding: 20px; border-radius: 15px; margin-bottom: 15px; background: #0a0a0a; box-shadow: 0 0 10px #00ff41; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 900; background: transparent; border: 1px solid #00ff41; color: #00ff41; }
    .stButton>button:hover { background: #00ff41; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("📊 CONTROL DE BANCA")
banca = st.sidebar.number_input("BANCA ($)", value=600)
meta_6 = banca * 0.06
st.sidebar.markdown(f"### OBJETIVO: ${meta_6:.2f}")

# --- FILTRO DE FECHA ---
st.markdown("<h1 style='color:#00ff41; text-align:center;'>⚡ ESCÁNER PROFESIONAL STOMS</h1>", unsafe_allow_html=True)
fecha_busqueda = st.date_input("Selecciona el día para analizar", datetime.now())

# --- LÓGICA DE API ---
if st.button("🔍 BUSCAR PARTIDOS REALES"):
    with st.spinner('Conectando con la API central...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        querystring = {"date": fecha_busqueda.strftime('%Y-%m-%d')}
        
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            data = response.json()
            
            # Verificación de errores de la API
            if response.status_code != 200:
                st.error(f"Error de Servidor: {response.status_code}")
            elif 'errors' in data and data['errors']:
                st.error(f"Error de API: {data['errors']}")
            else:
                partidos = data.get('response', [])
                
                if not partidos:
                    st.warning(f"No se encontraron partidos para la fecha {fecha_busqueda}. Intenta con el día de mañana.")
                else:
                    st.success(f"✅ ¡Éxito! {len(partidos)} partidos encontrados.")
                    
                    for f in partidos[:15]:
                        h = f['teams']['home']['name']
                        a = f['teams']['away']['name']
                        liga = f['league']['name']
                        hora = f['fixture']['date'][11:16]
                        
                        stake = (meta_6 * 0.40) / 0.5

                        st.markdown(f"""
                        <div class="neon-card">
                            <div style="display: flex; justify-content: space-between; color: #888;">
                                <span>{liga}</span><span>{hora}</span>
                            </div>
                            <h2 style="margin:10px 0;">{h} vs {a}</h2>
                            <p style="color:#00ff41; font-weight:bold;">MERCADO: OVER 1.5 | STAKE: ${stake:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"ENVIAR SEÑAL: {h}", key=f"btn_{h}"):
                            msg = f"⚽ SEÑAL: {h} vs {a}\n🏆 {liga}\n💰 Stake: ${stake:.2f}\n🎯 Over 1.5"
                            r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": ID_CANAL, "text": msg})
                            if r.status_code == 200:
                                st.toast("Señal enviada!")
                            else:
                                st.error("Fallo Telegram. ¿Hiciste al bot ADMIN?")
                                
        except Exception as e:
            st.error(f"Error de conexión: {e}")
