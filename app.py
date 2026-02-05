if "VERDE" in analisis or "AZUL" in analisis:
                    # 1. Extraer una probabilidad estimada del texto de la IA (o asignar una por defecto)
                    # Esto crea una barra de progreso visual dentro de la tarjeta
                    prob = 90 if "VERDE" in analisis else 75
                    neon_color = "#00ff41" if "VERDE" in analisis else "#00d4ff"
                    
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
                        padding: 25px;
                        border-radius: 20px;
                        border: 1px solid {neon_color}33;
                        border-left: 6px solid {neon_color};
                        margin-bottom: 25px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h2 style="color: white; margin: 0; font-size: 1.4em; letter-spacing: 1px;">
                                {equipo_h} <span style="color:{neon_color}; opacity: 0.8;">vs</span> {equipo_a}
                            </h2>
                            <span style="background: {neon_color}; color: black; padding: 4px 12px; border-radius: 8px; font-weight: 900; font-size: 0.75em; text-transform: uppercase;">
                                { "Confianza Elite" if "VERDE" in analisis else "Confianza Media" }
                            </span>
                        </div>
                        
                        <p style="color: #666; font-size: 0.9em; margin-bottom: 20px;">🏆 {liga}</p>
                        
                        <div style="margin-bottom: 20px;">
                            <div style="display: flex; justify-content: space-between; color: {neon_color}; font-size: 0.8em; font-weight: bold; margin-bottom: 5px;">
                                <span>PROBABILIDAD DE ÉXITO</span>
                                <span>{prob}%</span>
                            </div>
                            <div style="background: #333; border-radius: 10px; height: 8px; width: 100%; overflow: hidden;">
                                <div style="background: {neon_color}; height: 100%; width: {prob}%; box-shadow: 0 0 10px {neon_color};"></div>
                            </div>
                        </div>

                        <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 12px; color: #ccc; line-height: 1.5; font-size: 0.95em;">
                            <strong style="color: {neon_color};">STOMS IA Insights:</strong><br>
                            {analisis.replace('CALIFICACIÓN:', '').replace('RAZÓN:', '').strip()}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
