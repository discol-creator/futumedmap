import streamlit as st
import pandas as pd
import folium
from folium.plugins import PrintMap # Movido aquí para evitar el ImportError
from streamlit_folium import st_folium
import json

# Configuración de página
st.set_page_config(page_title="FUTUMED - Mapa Profesional", layout="wide")

st.title("🗺️ Delimitador de Zonas FUTUMED")
st.write("Configura el perímetro de impacto y descarga los datos para Ruta N.")

# --- BARRA LATERAL ---
st.sidebar.header("Configuración")
color_zona = st.sidebar.color_picker("Color de la zona", "#FF4B4B")

st.sidebar.subheader("Vértices (Lat, Lon)")
coord_input = st.sidebar.text_area(
    "Ingresa coordenadas:",
    "6.2685, -75.5645\n6.2650, -75.5615\n6.2595, -75.5665\n6.2635, -75.5700",
    height=150
)

# Procesar coordenadas de forma segura
def limpiar_coords(texto):
    puntos = []
    for linea in texto.split('\n'):
        if ',' in linea:
            try:
                lat, lon = map(float, linea.split(','))
                puntos.append([lat, lon])
            except: continue
    return puntos

lista_puntos = limpiar_coords(coord_input)

# --- MAPA ---
col1, col2 = st.columns([3, 1])

with col1:
    centro = lista_puntos[0] if lista_puntos else [6.2650, -75.5663]
    # Usamos el mapa base con etiquetas claras de barrios
    m = folium.Map(location=centro, zoom_start=15, tiles="OpenStreetMap")
    
    # AGREGAR BOTÓN DE IMPRESIÓN (Para descargar imagen)
    try:
        PrintMap(pos="topleft").add_to(m)
    except Exception as e:
        st.error("No se pudo cargar el botón de impresión, pero el mapa seguirá funcionando.")

    if len(lista_puntos) > 2:
        folium.Polygon(
            locations=lista_puntos,
            color=color_zona,
            fill=True,
            fill_color=color_zona,
            fill_opacity=0.4
        ).add_to(m)
        
    # Renderizado
    st_folium(m, width="100%", height=550)
    st.info("💡 Haz clic en el icono de la impresora (arriba a la izq) para guardar el mapa como PDF o Imagen.")

with col2:
    st.subheader("Exportar")
    if lista_puntos:
        df = pd.DataFrame(lista_puntos, columns=["Latitud", "Longitud"])
        
        # Descarga CSV
        st.download_button("📥 Descargar CSV", df.to_csv(index=False), "zona_futumed.csv", "text/csv", use_container_width=True)
        
        # Descarga GeoJSON
        geojson = {
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [[ [p[1], p[0]] for p in lista_puntos ] + [[lista_puntos[0][1], lista_puntos[0][0]]]]}
        }
        st.download_button("🌍 Descargar GeoJSON", json.dumps(geojson), "zona_futumed.geojson", "application/json", use_container_width=True)

st.success("App lista para el proyecto de innovación.")
