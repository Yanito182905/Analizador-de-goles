
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN Y ESTILO VISUAL (Colores y Botones)
st.set_page_config(page_title="Sistema Pro 6%", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Estilo General */
    .main { background-color: #0e1117; }
    
    /* Botones con Colores Específicos */
    div.stButton > button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; color: white; border: none; transition: 0.3s; }
    
    /* Botón Escanear (VERDE) */
    .stButton > button[kind="primary"] { background-color: #00ff88 !important; color: black !important; }
    
    /* Botón Test (AZUL) */
    .stButton > button:contains("Notificación") { background-color: #00d4ff !important; }
    
    /* Botón Guardar (AMARILLO/NARANJA) */
    .stButton > button:contains("Guardar") { background-color: #ffaa00 !important; color: black !important; }

    /* Tarjetas de Picks con Colores */
    .card-15 { border-left: 8px solid #00ff88; background-color: #1c212d; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    .card-25 { border-left: 8px solid #ffaa00; background-color: #1c212d; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    .card-ht { border-left: 8px solid #00d4ff; background-color: #1c212d; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
    
    .stMetric { background-color: #1c212d; padding: 15px; border-radius: 15px; border: 1px solid #2e3648; }
    </style>
    """, unsafe_allow_html=True)

# 2. CREDENCIALES Y VARIABLES DE SESIÓN
API_KEY = "f34c526a0810519b034fe7555fb83977"
TELEGRAM_TOKEN = "8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ"
TELEGRAM_CHAT_ID = "790743691"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

if 'bank_actual' not in st.session_state: st.session_state.bank_actual = 600.0
if 'historico' not in st.session_state: 
    st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Resultado', 'Banca'])

# 3. FUNCIONES AUXILIARES
def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    return requests.post(url, data=payload)

# 4. SIDEBAR: HERRAMIENTAS Y REGISTRO
with st.sidebar:
    st.header("🛠️ Panel Técnico")
    
    # Botón de Notificación (AZUL)
    if st.button("🔔 Probar Notificación", use_container_width=True):
        enviar_telegram("🔵 *SISTEMA CONECTADO*\nEl bot está listo para enviar picks.")
        st.success("Test enviado")

    st.divider()
    st.header("📓 Libro de Registro")
    monto = st.number_input("Resultado de la sesión ($)", value=0.0, help="Usa '-' para pérdidas")
    
    # Botón de Guardar (AMARILLO)
    if st.button("💾 Guardar Datos", use_container_width=True):
        nueva = {'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Resultado': monto, 'Banca': st.session_state.bank_actual + monto}
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva])], ignore_index=True)
        st.session_state.bank_actual += monto
        st.rerun()

# 5. DASHBOARD PRINCIPAL (Métricas y Gráfica)
st.title("💰 Inversión Estratégica 6%")
meta_hoy = st.session_state.bank_actual * 0.06

c1, c2, c3 = st.columns(3)
with c1: st.metric("Capital Actual", f"${st.session_state.bank_actual:.2f}")
with c2: st.metric("Meta del Día (6%)", f"${meta_hoy:.2f}", "🎯")
with c3:
    balance_total = st.session_state.bank_actual - 600.0
    color_delta = "normal" if balance_total >= 0 else "inverse"
    st.metric("Balance Total", f"${balance_total:.2f}", f"{((balance_total/600)*100):.1f}%", delta_color=color_delta)

# Gráfica de Rentabilidad
if not st.session_state.historico.empty:
    st.subheader("📈 Curva de Crecimiento")
    st.line_chart(st.session_state.historico.set_index('Fecha')['Banca'])
else:
    st.info("💡 Aquí aparecerá tu gráfica cuando registres tu primer resultado diario.")

# 6. ESCÁNER ÉLITE (Botón VERDE)
st.divider()
if st.button('🚀 ESCANEAR MERCADO (FILTRO ÉLITE)', type="primary", use_container_width=True):
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    with st.spinner('Filtrando mejores oportunidades...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        
        # Filtros de Ligas Élite
        ligas_25 = ['Bundesliga', 'Swiss Super League', 'Allsvenskan', 'Norway Eliteserien']
        ligas_ht = ['Eerste Divisie', 'Eredivisie']
        
        encontrados = 0
        stake_rec = meta_hoy / 0.35

        for p in partidos:
            liga = p['league']['name']
            home, away = p['teams']['home']['name'], p['teams']['away']['name']
            hora = p['fixture']['date'][11:16]
            
            # Clasificación y Visualización
            if liga in ligas_25:
                est, css, emoj, dot = "OVER 2.5", "card-25", "🔥", "🟠"
            elif liga in ligas_ht:
                est, css, emoj, dot = "OVER 0.5 HT", "card-ht", "⚡", "🔵"
            else:
                est, css, emoj, dot = "OVER 1.5", "card-15", "🛡️", "🟢"

            # Solo mostrar ligas que conocemos como rentables
            ligas_todas = ligas_25 + ligas_ht + ['Premier League', 'Serie A', 'J1 League', 'Super Lig']
            
            if liga in ligas_todas:
                encontrados += 1
                st.markdown(f"""<div class="{css}">
                    <h4>{emoj} {home} vs {away}</h4>
                    <b>ESTRATEGIA:</b> {est} | 🏆 {liga} | ⏰ {hora}<br>
                    <b>INVERTIR:</b> ${stake_rec:.2f} (Para meta de ${meta_hoy:.2f})
                </div>""", unsafe_allow_html=True)

                # Enviar a Telegram con círculo de color
                msg = f"{dot} *PICK ÉLITE*\n⚽ {home} vs {away}\n📊 Mercado: {est}\n💰 Stake: ${stake_rec:.2f}"
                enviar_telegram(msg)
        
        if encontrados == 0:
            st.warning("Mercado cerrado o sin picks de alta probabilidad ahora mismo.")
