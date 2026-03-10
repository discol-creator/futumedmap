import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuración de página
st.set_page_config(page_title="FUTUMED - Delimitación de Zonas", layout="wide")

st.title("🚀 FUTUMED: Mapa de Influencia y Talento")
st.write("Visualización del Distrito de Innovación y zonas estratégicas de Medellín.")

# 1. Datos de puntos clave
puntos_clave = [
    {"name": "Ruta N (Core)", "lat": 6.2650, "lon": -75.5663, "info": "Centro de Innovación"},
    {"name": "U. de Antioquia", "lat": 6.2637, "lon": -75.5675, "info": "Talento Humano"},
    {"name": "SENA (Chagualo)", "lat": 6.2605, "lon": -75.5675, "info": "Formación Técnica"}
]

# 2. Crear el mapa base centrado en Medellín (Ruta N)
m = folium.Map(location=[6.2650, -75.5663], zoom_start=15, control_scale=True)

# 3. DELIMITAR LA ZONA (Polígono de influencia FUTUMED)
# Definimos los vértices que encierran el área de interés
zona_futumed = [
    [6.2685, -75.5645], # Norte (Cerca a Explora)
    [6.2650, -75.5615], # Oriente (Cerca a San Vicente)
    [6.2595, -75.5665], # Sur (Cerca a SENA/Pascual Bravo)
    [6.2635, -75.5700]  # Occidente (Cerca al Río)
]

folium.Polygon(
    locations=zona_futumed,
    color="orange",
    fill=True,
    fill_color="orange",
    fill_opacity=0.3,
    popup="Zona de Influencia FUTUMED"
).add_to(m)

# 4. Agregar marcadores individuales
for punto in puntos_clave:
    folium.Marker(
        location=[punto["lat"], punto["lon"]],
        popup=f"{punto['name']}: {punto['info']}",
        tooltip=punto["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 5. Mostrar el mapa en Streamlit
st_folium(m, width=1200, height=500)

# 6. Sección de datos
st.subheader("📍 Coordenadas de la Delimitación")
df_coords = pd.DataFrame(zona_futumed, columns=["Latitud", "Longitud"])
st.table(df_coords)