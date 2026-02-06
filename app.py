import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from datetime import datetime

# --- 1. CONFIGURACIÓN (REVISADA) ---
GOOGLE_API_KEY = "AIzaSyAIDAx_6DD0nSY6hv4aZ4RKsvw-xjy0bYw"
FOOTBALL_API_KEY = "646398b767msh76718816c52a095p16a309jsn7810459f1345"
TELEGRAM_TOKEN = "7663240865:AAG7V_6v8XN9Y_fBv-G-4Fq_9t1-G_9F4"
TELEGRAM_CHAT_ID = "5298539210"

# Inicializar IA
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error configurando la IA")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=data, timeout=10)
        return r.json() # Retornamos el JSON completo para ver el error
    except Exception as e:
        return {"ok": False, "description": str(e)}

# --- 2. ESTILO ---
st.set_page_config(page_title="STOMS ULTRA ELITE", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .neon-card { border: 1px solid #00ff41; padding: 20px; border-radius: 15px; margin-bottom: 10px; background: #050505; }
    .btn-notif button { border: 2px solid #00d4ff !important; color: #00d4ff !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
st.sidebar.title("🚀 SISTEMA ELITE")
if st.sidebar.button("🔔 TEST TELEGRAM"):
    res = enviar_telegram("📡 Test de conexión desde STOMS IA")
    if res.get("ok"):
        st.sidebar.success("¡Conexión Exitosa!")
    else:
        st.sidebar.error(f"Error {res.get('error_code')}: {res.get('description')}")
        st.sidebar.warning("Revisa si tu Bot está activo y si el ID es correcto.")

banca = st.sidebar.number_input("Banca ($)", value=600)
meta_hoy = banca * 0.06
st.sidebar.info(f"Objetivo: +${meta_hoy:.2f}")

# --- 4. PANEL DE CONTROL ---
st.markdown("<h1 style='color:#00ff41; text-align:center;'>⚡ TERMINAL ULTRA ELITE</h1>", unsafe_allow_html=True)

if st.button("🔍 ESCANEAR JORNADA COMPLETA"):
    with st.spinner('Accediendo a servidores de fútbol...'):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
        
        # Obtenemos TODOS los partidos de hoy sin filtros de estado
        hoy = datetime.now().strftime('%Y-%m-%d')
        res_api = requests.get(url, headers=headers, params={"date": hoy})
        
        if res_api.status_code != 200:
            st.error(f"Error de API Fútbol: {res_api.status_code}")
        else:
            fixtures = res_api.json().get('response', [])
            st.write(f"📊 Partidos detectados hoy: **{len(fixtures)}**")
            
            if fixtures:
                for f in fixtures[:15]:
                    h = f['teams']['home']['name']
                    a = f['teams']['away']['name']
                    liga = f['league']['name']
                    hora = f['fixture']['date'][11:16]
                    
                    # Cálculo de Stake
                    stake = (meta_hoy * 0.35) / 0.5 
                    
                    st.markdown(f"""
                    <div class="neon-card">
                        <div style="display: flex; justify-content: space-between; color: #888;">
                            <span>{liga}</span><span>{hora}</span>
                        </div>
                        <h2 style="margin:10px 0;">{h} vs {a}</h2>
                        <p style="color:#00ff41; font-weight:bold;">Mercado: Over 1.5 | Stake: ${stake:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"ENVIAR SEÑAL: {h}", key=f"btn_{h}"):
                        txt = f"⚽ *NUEVA SEÑAL*\n🏟️ {h} vs {a}\n🏆 {liga}\n💰 Stake: ${stake:.2f}\n🎯 Over 1.5"
                        res_tel = enviar_telegram(txt)
                        if res_tel.get("ok"): st.toast("¡Enviado!")
                        else: st.error("Error al enviar")
            else:
                st.warning("La API no devolvió partidos. Intenta cambiar la fecha.")
