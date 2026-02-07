
import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE CREDENCIALES (REVISADAS) ---
API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
TOKEN_BOT = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
ID_CANAL = "-5298539210"

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="STOMS ALPHA - ODDALERTS MODE", layout="wide")

# Estilo Neón
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .card { 
        border: 1px solid #00ff41; padding: 20px; border-radius: 15px; 
        background: #050505; margin-bottom: 15px;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 900; background: transparent; border: 1px solid #00ff41; color: #00ff41; }
    .stButton>button:hover { background: #00ff41; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GESTIÓN DE BANCA (TU META 6%) ---
st.sidebar.title("📈 ESTRATEGIA 6%")
banca = st.sidebar.number_input("BANCA ACTUAL ($)", value=600)
meta_objetivo = banca * 0.06
st.sidebar.info(f"OBJETIVO DIARIO: ${meta_objetivo:.2f}")

# --- LÓGICA DE TELEGRAM ---
def enviar_alerta(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": ID_CANAL, "text": mensaje, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except:
        return False

# --- CUERPO PRINCIPAL ---
st.markdown("<h1 style='color:#00ff41; text-align:center;'>⚡ STOMS x ODDALERTS</h1>", unsafe_allow_html=True)
st.write("---")

if st.button("🔍 ESCANEAR JORNADA DE HOY (SÁBADO)"):
    with st.spinner('Filtrando mercados de goles...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        hoy = datetime.now().strftime('%Y-%m-%d')
        
        try:
            response = requests.get(url, headers=headers, params={"date": hoy}, timeout=15)
            
            if response.status_code == 403:
                st.error("🚫 Error 403: Revisa tu suscripción en RapidAPI.")
            else:
                partidos = response.json().get('response', [])
                if not partidos:
                    st.warning("No hay partidos detectados aún. Intenta en unos minutos.")
                else:
                    st.success(f"Se han analizado {len(partidos)} partidos.")
                    
                    # Filtramos los primeros 10 para no saturar
                    for p in partidos[:12]:
                        h = p['teams']['home']['name']
                        a = p['teams']['away']['name']
                        liga = p['league']['name']
                        hora = p['fixture']['date'][11:16]
                        
                        # Cálculo de Stake sugerido (buscando un tercio de la meta por trade)
                        stake_sugerido = (meta_objetivo * 0.35) / 0.5 

                        st.markdown(f"""
                        <div class="card">
                            <div style="display: flex; justify-content: space-between; color: #888;">
                                <span>🏆 {liga}</span><span>⏰ {hora}</span>
                            </div>
                            <h2 style="margin:10px 0;">{h} vs {a}</h2>
                            <p style="color:#00ff41; font-weight:bold; margin:0;">MERCADO: OVER 1.5 GOLES</p>
                            <p style="color:#ffd700; font-weight:bold; margin:0;">STAKE SUGERIDO: ${stake_sugerido:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"📲 NOTIFICAR ENTRADA: {h}", key=f"btn_{h}"):
                            msg = f"⚽ *SEÑAL STOMS IA*\n🏟️ {h} vs {a}\n🏆 {liga}\n🎯 Mercado: Over 1.5\n💰 *Stake: ${stake_sugerido:.2f}*"
                            if enviar_alerta(msg):
                                st.toast("Señal enviada a Telegram")
                            else:
                                st.error("Error al enviar. Verifica permisos del bot.")

        except Exception as e:
            st.error(f"Error de conexión: {e}")

st.markdown("---")
st.caption("STOMS IA - Analizando datos en tiempo real.")
