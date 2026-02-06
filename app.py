import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD (ID ACTUALIZADO) ---
GOOGLE_API_KEY = "AIzaSyAIDAx_6DD0nSY6hv4aZ4RKsvw-xjy0bYw"
FOOTBALL_API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
# Revisa que este Token sea el correcto en tu BotFather
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
TELEGRAM_CHAT_ID = "-5298539210" 

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

# --- 2. DISEÑO NEON EXTREMO ---
st.set_page_config(page_title="STOMS ULTRA ELITE", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .neon-card { border: 1px solid #00ff41; padding: 20px; border-radius: 15px; margin-bottom: 10px; background: #050505; }
    .neon-title { color: #00ff41; text-shadow: 0 0 15px #00ff41; text-align: center; font-weight: 900; }
    div.stButton > button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
st.sidebar.markdown("<h1 style='color:#00ff41;'>STOMS IA</h1>", unsafe_allow_html=True)
banca = st.sidebar.number_input("💵 BANCA ACTUAL ($)", value=600)
meta_6 = banca * 0.06

if st.sidebar.button("🔔 PROBAR CONEXIÓN TELEGRAM"):
    res = enviar_telegram("✅ Test de Conexión STOMS - Canal Detectado")
    if res.get("ok"):
        st.sidebar.success("¡Conexión Exitosa!")
    else:
        st.sidebar.error(f"Error {res.get('error_code')}: {res.get('description')}")
        st.sidebar.warning("RECUERDA: Debes añadir al bot al grupo/canal y hacerlo ADMIN.")

# --- 4. CUERPO PRINCIPAL ---
st.markdown("<h1 class='neon-title'>⚡ TERMINAL ULTRA ELITE</h1>", unsafe_allow_html=True)

if st.button("🚀 ESCANEAR PARTIDOS DE HOY"):
    with st.spinner('Accediendo a la API de Fútbol...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        hoy = datetime.now().strftime('%Y-%m-%d')
        
        try:
            res_api = requests.get(url, headers=headers, params={"date": hoy}, timeout=15)
            data = res_api.json()
            fixtures = data.get('response', [])
        except:
            fixtures = []
            st.error("Error de conexión con el servidor de deportes.")

        if fixtures:
            st.success(f"Se detectaron {len(fixtures)} partidos hoy.")
            for f in fixtures[:15]:
                h, a = f['teams']['home']['name'], f['teams']['away']['name']
                liga = f['league']['name']
                hora = f['fixture']['date'][11:16]
                stake = (meta_6 * 0.35) / 0.5

                st.markdown(f"""
                <div class="neon-card">
                    <small style="color:#888;">{liga} | {hora}</small>
                    <h3>{h} vs {a}</h3>
                    <p style="color:#00ff41;">Mercado: Over 1.5 | <b>Stake Sugerido: ${stake:.2f}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"ENVIAR SEÑAL: {h}", key=f"btn_{h}"):
                    txt = f"⚽ *SEÑAL STOMS*\n🏟️ {h} vs {a}\n🏆 {liga}\n💰 *STAKE: ${stake:.2f}*\n🎯 Mercado: Over 1.5"
                    res_tel = enviar_telegram(txt)
                    if res_tel.get("ok"): st.toast("¡Señal en Telegram!")
                    else: st.error(f"Error: {res_tel.get('description')}")
        else:
            st.warning("No se recibieron partidos. Verifica si tu API Key de RapidAPI sigue activa.")
