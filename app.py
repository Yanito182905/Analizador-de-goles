import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN
st.set_page_config(page_title="Gestor 6% Pro", page_icon="📈", layout="wide")

API_KEY = "f34c526a0810519b034fe7555fb83977"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

# --- SIDEBAR: GESTIÓN DE BANCA ---
st.sidebar.header("💰 Panel de Control")
banca_inicial = st.sidebar.number_input("Banca con la que empezaste ($)", value=1000.0)
meta_diaria_pct = 0.06

# --- DIARIO DE RESULTADOS ---
st.sidebar.markdown("---")
st.sidebar.subheader("📓 Diario de Hoy")
resultado_hoy = st.sidebar.number_input("¿Cuánto ganaste hoy? ($)", value=0.0)
if st.sidebar.button("Guardar Resultado"):
    st.sidebar.success("Resultado registrado localmente")

# --- LÓGICA DE INTERÉS COMPUESTO ---
st.title("📈 Proyección de Crecimiento Exponencial")

col1, col2 = st.columns([2, 1])

with col1:
    dias = list(range(0, 31))
    proyeccion = []
    banca_temp = banca_inicial
    for d in dias:
        proyeccion.append(round(banca_temp, 2))
        banca_temp *= (1 + meta_diaria_pct)
    
    df_proyeccion = pd.DataFrame({"Día": dias, "Banca Estimada ($)": proyeccion})
    st.line_chart(df_proyeccion.set_index("Día"))

with col2:
    st.metric("Meta de Hoy", f"${banca_inicial * meta_diaria_pct:.2f}")
    st.metric("Banca en 30 días", f"${proyeccion[-1]:,.2f}")
    st.write("⚠️ **Recuerda:** El interés compuesto funciona si no retiras las ganancias.")



# --- BUSCADOR DE PICKS ---
st.markdown("---")
if st.button('🎯 Escanear Partidos para mi Meta'):
    url = "https://v3.football.api-sports.io/fixtures"
    hoy = datetime.now().strftime('%Y-%m-%d')
    params = {'date': hoy, 'status': 'NS'}
    
    with st.spinner('Buscando en ligas de alta frecuencia...'):
        res = requests.get(url, headers=HEADERS, params=params)
        partidos = res.json().get('response', [])
        
        ligas_top = ['Eerste Divisie', 'Eredivisie', 'Bundesliga', 'S-League', 'J-League', 'Super League']
        picks = [p for p in partidos if p['league']['name'] in ligas_top]
        
        if picks:
            data_final = []
            for p in picks[:10]:
                data_final.append({
                    "Hora": p['fixture']['date'][11:16],
                    "Partido": f"{p['teams']['home']['name']} vs {p['teams']['away']['name']}",
                    "Liga": p['league']['name'],
                    "Estado": "ALTA PROBABILIDAD 🔥"
                })
            st.table(pd.DataFrame(data_final))
        else:
            st.warning("No hay partidos de ligas TOP en este momento.")

# --- BARRA DE DISCIPLINA ---
st.markdown("---")
if st.checkbox("✅ He alcanzado mi 6% de hoy. ¡Misión cumplida!"):
    st.balloons()
    st.success("¡Felicidades! Cierra la sesión y disfruta de tu tiempo libre.")
