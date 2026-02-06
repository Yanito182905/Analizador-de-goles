import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURACIÓN ---
TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
ID_CANAL = "-5298539210"

st.set_page_config(page_title="STOMS ULTRA ELITE", layout="wide")

# --- DISEÑO NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .neon-card { 
        border: 2px solid #00ff41; padding: 20px; border-radius: 15px; 
        margin-bottom: 15px; background: #050505;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("💰 GESTIÓN 6%")
banca = st.sidebar.number_input("BANCA ($)", value=600)
meta_diaria = banca * 0.06
st.sidebar.success(f"OBJETIVO HOY: ${meta_diaria:.2f}")

st.sidebar.markdown("---")
st.sidebar.write("⚙️ **ESTADO TELEGRAM**")
if st.sidebar.button("🔔 PROBAR ENVÍO"):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, json={"chat_id": ID_CANAL, "text": "🚀 Test STOMS IA"})
    if res.status_code == 200:
        st.sidebar.success("¡CONECTADO!")
    else:
        st.sidebar.error("Desconectado (Haz al bot ADMIN)")

# --- PANEL PRINCIPAL ---
st.markdown("<h1 style='color:#00ff41; text-align:center;'>⚡ TERMINAL ULTRA ELITE</h1>", unsafe_allow_html=True)

if st.button("🚀 BUSCAR PARTIDOS DE HOY"):
    with st.spinner('Escaneando jornada...'):
        # API DE FUTBOL
        headers = {
            "X-RapidAPI-Key": "646398b767msh76718816c52a095p16a309jsn7810459f1345",
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        hoy = datetime.now().strftime('%Y-%m-%d')
        # Buscamos partidos de hoy
        res = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures", headers=headers, params={"date": hoy})
        
        data = res.json()
        partidos = data.get('response', [])

        if partidos:
            st.write(f"✅ Se han encontrado **{len(partidos)}** partidos.")
            for p in partidos[:15]: # Mostramos los primeros 15
                h = p['teams']['home']['name']
                a = p['teams']['away']['name']
                liga = p['league']['name']
                pais = p['league']['country']
                hora = p['fixture']['date'][11:16]
                
                # Cálculo de Stake
                stake = (meta_diaria * 0.40) / 0.5

                # TARJETA VISUAL
                st.markdown(f"""
                <div class="neon-card">
                    <div style="display: flex; justify-content: space-between; color: #888;">
                        <span>{pais} | {liga}</span><span>{hora}</span>
                    </div>
                    <h2 style="margin:10px 0; color: #fff;">{h} vs {a}</h2>
                    <p style="color:#ffd700; font-weight:bold; margin:0;">MERCADO: OVER 1.5</p>
                    <p style="color:#00ff41; font-weight:bold; margin:0;">STAKE RECOMENDADO: ${stake:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botón de envío (aunque Telegram falle, esto no romperá la app)
                if st.button(f"ENVIAR SEÑAL: {h}", key=f"btn_{h}"):
                    msg = f"⚽ SEÑAL: {h} vs {a}\n🏆 {liga}\n💰 Stake: ${stake:.2f}\n🎯 Over 1.5"
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": ID_CANAL, "text": msg})
                    st.toast(f"Intento de envío para {h} realizado")
        else:
            st.warning("No se encontraron partidos. Revisa tu conexión o intenta más tarde.")
