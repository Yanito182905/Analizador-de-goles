import streamlit as st  # Corregido: "import" siempre en minúscula
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sistema 6% - Yaniel", page_icon="📈", layout="wide")

# 2. CREDENCIALES CONFIGURADAS
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
EMAIL_RESUMEN = "yanielramirez895@gmail.com"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# 3. ESTADO DE LA BANCA (Persistencia en sesión)
if 'bank_actual' not in st.session_state:
    st.session_state.bank_actual = 300.0
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 4. SIDEBAR: CONTROL FINANCIERO
st.sidebar.header("💰 Gestión de Capital")
# Actualizamos el valor de la banca basándonos en el estado de la sesión
st.session_state.bank_actual = st.sidebar.number_input("Banca Actual ($)", value=float(st.session_state.bank_actual))
meta_hoy = st.session_state.bank_actual * 0.06

st.sidebar.metric("Meta de Hoy (6%)", f"${meta_hoy:.2f}")

# Registro de resultados
with st.sidebar.form("registro_p"):
    st.write("📓 Registrar Resultado del Día")
    resultado_dia = st.number_input("Ganancia/Pérdida Neta ($)", value=0.0)
    
    # CORRECCIÓN LÍNEA 34: El método correcto es form_submit_button
    submit_button = st.form_submit_button("Guardar Jornada")
    
    if submit_button:
        nueva_banca = st.session_state.bank_actual + resultado_dia
        nueva_fila = {
            'Fecha': datetime.now().strftime("%Y-%m-%d"), 
            'Resultado': resultado_dia, 
            'Banca': nueva_banca
        }
        
        # Actualización de datos
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.session_state.bank_actual = nueva_banca
        st.success(f"¡Registrado! Nueva banca: ${nueva_banca:.2f}")
        # Recargamos para que los gráficos se actualicen inmediatamente
        st.rerun()

# 5. PANEL PRINCIPAL
st.title("⚽ Panel de Inversión 6% Diario")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Rendimiento Real")
    if not st.session_state.historico.empty:
        # Mostramos el gráfico de línea basado en el historial
        st.line_chart(st.session_state.historico.set_index('Fecha')['Banca'])
    else:
        st.info("Aquí aparecerá tu gráfica cuando registres tu primera apuesta.")

with col2:
    st.subheader("📅 Ciclo de Resumen")
    dias_transcurridos = len(st.session_state.historico)
    # Evitamos división por cero y limitamos el progreso a 100%
    progreso = min((dias_transcurridos / 10), 1.0) 
    st.write(f"Días registrados: **{dias_transcurridos}/10**")
    st.progress(progreso)
    st.caption(f"Resumen cada 10 días a: {EMAIL_RESUMEN}")

# 6. BUSCADOR DE PICKS Y TELEGRAM
st.divider()
st.header("🔍 Escáner de Oportunidades")

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, data=payload)
    except Exception as e:
        st.error(f"Error al enviar Telegram: {e}")

if st.button('🚀 Buscar Partidos y Enviar al Móvil'):
    url_fixtures = "https://v3.football.api-sports.io/fixtures"
    hoy = datetime.now().strftime('%Y-%m-%d')
    params = {'date': hoy, 'status': 'NS'}
    
    with st.spinner('Filtrando ligas de alta probabilidad...'):
        try:
            res = requests.get(url_fixtures, headers=HEADERS, params=params)
            partidos = res.json().get('response', [])
            
            ligas_top = ['Eerste Divisie', 'Eredivisie', 'Bundesliga', 'Premier League', 'J-League', 'Super League']
            # Calculamos Stake para ganar el 6% con cuota promedio 1.35
            stake = meta_hoy / (1.35 - 1)
            
            encontrados = []
            for p in partidos:
                if p['league']['name'] in ligas_top:
                    home = p['teams']['home']['name']
                    away = p['teams']['away']['name']
                    hora = p['fixture']['date'][11:16]
                    
                    msg = (f"🎯 *ALERTA 6%*\n\n⚽ {home} vs {away}\n🏆 {p['league']['name']}\n⏰ {hora}\n\n"
                           f"💰 *APUESTA:* **${stake:.2f}**\n📈 *MERCADO:* Over 1.5\n🏁 *OBJETIVO:* +${meta_hoy:.2f}")
                    
                    enviar_telegram(msg)
                    encontrados.append({"Hora": hora, "Partido": f"{home} vs {away}", "Inversión": f"${stake:.2f}"})

            if encontrados:
                st.success(f"Se enviaron {len(encontrados)} picks a Telegram.")
                st.table(pd.DataFrame(encontrados))
            else:
                st.warning("No hay partidos de ligas TOP disponibles por ahora.")
        except Exception as e:
            st.error(f"Error en la conexión con la API: {e}")

# 7. BOTÓN DE PRUEBA
if st.sidebar.button("🔔 Test de Notificación"):
    enviar_telegram("✅ Sistema conectado. ¡Tu meta del 6% empieza hoy!")

