
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Estrategia 6% - Bank $300", page_icon="💰", layout="wide")

# --- CREDENCIALES ---
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# --- LÓGICA FINANCIERA ---
# He configurado tu bank inicial en 300 como pediste
if 'banca' not in st.session_state:
    st.session_state.banca = 300.0

meta_diaria_valor = st.session_state.banca * 0.06 # Esto es $18.00 para empezar

# --- INTERFAZ ---
st.title("📈 Sistema de Interés Compuesto (Meta 6%)")

st.sidebar.header("💰 Gestión de Capital")
st.session_state.banca = st.sidebar.number_input("Banca Actual ($)", value=st.session_state.banca)
st.sidebar.metric("Meta de Hoy", f"${meta_diaria_valor:.2f}", "6%")

# Proyección
with st.expander("📅 Proyección de tus $300 a 30 días"):
    proyeccion = [round(st.session_state.banca * (1.06**i), 2) for i in range(31)]
    st.line_chart(proyeccion)
    st.write(f"Si cumples tu meta diaria, en 30 días tendrás: **${proyeccion[-1]:,.2f}**")

def enviar_alerta_con_stake(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

# --- BUSCADOR ---
st.header("🔍 Buscador de Picks con Stake")

if st.button('🚀 Buscar Oportunidades y Calcular Apuesta'):
    url = "https://v3.football.api-sports.io/fixtures"
    hoy = datetime.now().strftime('%Y-%m-%d')
    params = {'date': hoy, 'status': 'NS'}
    
    with st.spinner('Analizando partidos y calculando gestión de riesgo...'):
        response = requests.get(url, headers=HEADERS, params=params)
        partidos = response.json().get('response', [])
        
        # Ligas con alta tendencia de goles
        ligas_goleadoras = ['Eerste Divisie', 'Eredivisie', 'Bundesliga', 'S-League', 'J-League', 'Super League', 'Premier League', 'Regionalliga']
        
        encontrados = []
        # Calculamos el stake necesario para ganar la meta diaria con una cuota promedio de 1.35
        # Fórmula: Stake = Beneficio deseado / (Cuota - 1)
        stake_recomendado = meta_diaria_valor / (1.35 - 1)
        
        for p in partidos:
            liga = p['league']['name']
            if liga in ligas_goleadoras:
                home = p['teams']['home']['name']
                away = p['teams']['away']['name']
                hora = p['fixture']['date'][11:16]
                
                # Mensaje detallado para Telegram
                msg = (f"🎯 *PICK RECOMENDADO 6%*\n\n"
                       f"⚽ {home} vs {away}\n"
                       f"🏆 Liga: {liga}\n"
                       f"⏰ Hora: {hora}\n"
                       f"📊 Mercado: Over 1.5\n\n"
                       f"💰 *GESTIÓN DE BANCA:*\n"
                       f"💵 Invertir: **${stake_recomendado:.2f}**\n"
                       f"📈 Cuota sugerida: 1.35 o superior\n"
                       f"🏁 Objetivo: Ganar **${meta_diaria_valor:.2f}**")
                
                enviar_alerta_con_stake(msg)
                encontrados.append({"Hora": hora, "Partido": f"{home} vs {away}", "Inversión": f"${stake_recomendado:.2f}"})
        
        if encontrados:
            st.success(f"Se han enviado {len(encontrados)} alertas con el Stake calculado.")
            st.table(pd.DataFrame(encontrados))
        else:
            st.warning("No hay partidos en ligas TOP ahora mismo. Inténtalo más tarde.")

# Botón de prueba por si acaso
if st.button('🔔 Probar Telegram'):
    enviar_alerta_con_stake("✅ Conexión lista. Tu bank de $300 está configurado.")
    st.info("Revisa tu Telegram.")


