import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="FUTUMED - Mapa de Zona", layout="centered")

st.title("📍 Delimitación Zona FUTUMED")
st.info("Visualización del Distrito de Innovación (Ruta N y alrededores)")

# 1. Definir puntos clave de la zona
data = {
    'name': [
        'Ruta N (Centro)', 'Límite Norte (Explora)', 
        'Límite Sur (SENA)', 'Límite Este (Hospital)', 
        'Límite Oeste (Río)'
    ],
    'lat': [6.2650, 6.2678, 6.2605, 6.2645, 6.2642],
    'lon': [-75.5663, -75.5651, -75.5675, -75.5620, -75.5695]
}

df = pd.DataFrame(data)

# 2. Renderizar el mapa (Este es el que no se queda cargando)
st.subheader("Mapa de Influencia")
st.map(df, latitude='lat', longitude='lon', zoom=14)

# 3. Mostrar las coordenadas exactas para el proyecto
st.subheader("Coordenadas del Perímetro")
st.dataframe(df, use_container_width=True)

# 4. Botón de descarga
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    "Descargar CSV para Ruta N",
    csv,
    "coordenadas_futumed.csv",
    "text/csv"
)
