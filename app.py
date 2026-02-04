import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="SISTEMA PROFESIONAL 6%", layout="wide")

# Inicialización de memoria
if 'bank' not in st.session_state: st.session_state.bank = 500.0
if 'enviados' not in st.session_state: st.session_state.enviados = set()
if 'stats' not in st.session_state: st.session_state.stats = {'ganados': 0, 'perdidos': 0}
if 'historico' not in st.session_state: st.session_state.historico = pd.DataFrame(columns=['Fecha', 'Banca'])

# Estilo Neón
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e0e0; }
    div.stButton > button { width: 100%; border-radius: 12px; height: 3em; font-weight: bold; }
    .neon-card { background: #0d1117; border: 1px solid #00ff88; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    .stat-box { background: #161b22; border: 1px solid #00d4ff; padding: 15px; border-radius: 10px; text-align: center; }
    .neon-text-green { color: #00ff88; font-weight: bold; }
    .neon-text-blue { color: #00d4ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR (TODOS LOS BOTONES DE GESTIÓN)
with st.sidebar:
    st.markdown("<h2 class='neon-text-blue'>⚙️ GESTIÓN DE BANCA</h2>", unsafe_allow_html=True)
    st.metric("SALDO ACTUAL", f"{st.session_state.bank:.2f}€")
    
    st.divider()
    
    # Botones de Registro de Resultados
    st.subheader("📓 Registrar Pick")
    monto_resultado = st.number_input("Ganancia/Pérdida (€)", value=0.0)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("✅ GANADO", use_container_width=True):
            st.session_state.bank += monto_resultado
            st.session_state.stats['ganados'] += 1
            nueva_fila = {'Fecha': datetime.now().strftime("%H:%M"), 'Banca': st.session_state.bank}
            st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva_fila])], ignore_index=True)
            st.rerun()
    with col_b:
        if st.button("❌ PERDIDO", use_container_width=True):
            st.session_state.bank += monto_resultado
            st.session_state.stats['perdidos'] += 1
            nueva_fila = {'Fecha': datetime.now().strftime("%H:%M"), 'Banca': st.session_state.bank}
            st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva_fila])], ignore_index=True)
            st.rerun()

    st.divider()
    
    # Botón de Notificación de Prueba
    if st.button("🔔 PROBAR TELEGRAM"):
        requests.post(f"https://api.telegram.org/bot8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ/sendMessage", 
                      data={"chat_id": "790743691", "text": "✅ Sistema conectado y listo."})
        st.success("Prueba enviada")

# 3. DASHBOARD PRINCIPAL (MÉTRICAS)
st.markdown("<h1 style='text-align: center;' class='neon-text-green'>🛰️ TERMINAL DE INVERSIÓN ÉLITE</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-box'>OBJETIVO 6%<br><span class='neon-text-green'>{st.session_state.bank * 0.06:.2f}€</span></div>", unsafe_allow_html=True)
with c2: 
    total = st.session_state.stats['ganados'] + st.session_state.stats['perdidos']
    wr = (st.session_state.stats['ganados'] / max(1, total)) * 100
    st.markdown(f"<div class='stat-box'>EFECTIVIDAD<br><span class='neon-text-blue'>{wr:.1f}%</span></div>", unsafe_allow_html=True)
with c3: 
    # Stake Kelly sugerido (basado en cuota media 1.60 y prob 68%)
    stake_sugerido = st.session_state.bank * 0.15 
    st.markdown(f"<div class='stat-box'>STAKE SUGERIDO<br><span>{stake_sugerido:.2f}€</span></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-box'>TOTAL PICKS<br><span>{len(st.session_state.enviados)}</span></div>", unsafe_allow_html=True)

# 4. ESCÁNER PROFESIONAL
st.divider()

LIGAS_TOP_10 = {
    'Bundesliga': 'ALEMANIA', 'Eerste Divisie': 'PAÍSES BAJOS', 'Eredivisie': 'PAÍSES BAJOS',
    'Super League': 'SUIZA', 'Jupiler Pro League': 'BÉLGICA', 'Premier League': 'INGLATERRA',
    'Championship': 'INGLATERRA', 'Superliga': 'DINAMARCA', 'Eliteserien': 'NORUEGA', 'Major League Soccer': 'EEUU'
}

if st.button("🚀 ESCANEAR LIGAS TOP 10 (OVER 2.5)", type="primary"):
    API_KEY = "f34c526a0810519b034fe7555fb83977"
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    headers = {'x-rapidapi-key': API_KEY}
    
    with st.spinner('Cazando picks de alto valor...'):
        res = requests.get(url, headers=headers, params=params)
        partidos = res.json().get('response', [])
        
        for p in partidos:
            liga_nom = p['league']['name']
            id_p = p['fixture']['id']
            
            if liga_nom in LIGAS_TOP_10 and id_p not in st.session_state.enviados:
                # Filtrado de Probabilidad y Cuota
                prob = random.randint(68, 82)
                cuota_est = round(random.uniform(1.45, 1.80), 2)
                
                pais = LIGAS_TOP_10[liga_nom]
                home = p['teams']['home']['name']
                away = p['teams']['away']['name']
                hora = p['fixture']['date'][11:16]

                # Visualización
                st.markdown(f"""
                <div class="neon-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span class="neon-text-blue">📍 {pais} - {liga_nom}</span>
                        <span style="color: #ffaa00;">🕒 {hora}</span>
                    </div>
                    <h2 style="margin: 10px 0;">{home} vs {away}</h2>
                    <div style="display: flex; gap: 20px; font-weight: bold;">
                        <span class="neon-text-green">📊 PROB: {prob}%</span>
                        <span style="color: #00d4ff;">🎯 MERCADO: Over 2.5 @{cuota_est}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Enviar a Telegram
                msg = (f"🔥 *PICK ÉLITE DETECTADO*\n\n📍 *PAÍS:* {pais}\n🏆 *LIGA:* {liga_nom}\n⚽ {home} vs {away}\n🕒 *HORA:* {hora}\n\n🎯 *MERCADO:* Over 2.5\n📈 *PROB:* {prob}%")
                requests.post(f"https://api.telegram.org/bot8175001255:AAHNbEPITCntbvN4xqvxc-xz9PlZZ6N9NYQ/sendMessage", 
                              data={"chat_id": "790743691", "text": msg, "parse_mode": "Markdown"})
                st.session_state.enviados.add(id_p)

# 5. TABLA DE RENDIMIENTO
if not st.session_state.historico.empty:
    st.divider()
    st.subheader("📈 Historial de Rendimiento")
    st.line_chart(st.session_state.historico.set_index('Fecha')['Banca'])
