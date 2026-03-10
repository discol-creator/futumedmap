import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

# Configuración de página para FUTUMED
st.set_page_config(page_title="FUTUMED - Mapa de Innovación", layout="wide")

st.title("🗺️ Delimitador de Zonas FUTUMED")
st.write("Define el área de impacto en Medellín y exporta los datos para tu proyecto.")

# --- BARRA LATERAL ---
st.sidebar.header("Configuración de Zona")
color_zona = st.sidebar.color_picker("Color del Polígono", "#FF4B4B")

st.sidebar.subheader("Coordenadas (Lat, Lon)")
st.sidebar.caption("Ejemplo: 6.2650, -75.5663")
coord_input = st.sidebar.text_area(
    "Ingresa los vértices:",
    "6.2685, -75.5645\n6.2650, -75.5615\n6.2595, -75.5665\n6.2635, -75.5700",
    height=200
)

# Procesamiento de coordenadas
def obtener_puntos(texto):
    puntos = []
    for linea in texto.split('\n'):
        if ',' in linea:
            try:
                lat, lon = map(float, linea.split(','))
                puntos.append([lat, lon])
            except: continue
    return puntos

lista_puntos = obtener_puntos(coord_input)

# --- MAPA ---
col1, col2 = st.columns([3, 1])

with col1:
    # Centro en Medellín (Ruta N)
    centro_mapa = lista_puntos[0] if lista_puntos else [6.2650, -75.5663]
    
    # Creamos el mapa con fondo claro para que resalten los barrios
    m = folium.Map(location=centro_mapa, zoom_start=15, tiles="CartoDB positron")

    if len(lista_puntos) > 2:
        # Dibujamos el área delimitada
        folium.Polygon(
            locations=lista_puntos,
            color=color_zona,
            fill=True,
            fill_color=color_zona,
            fill_opacity=0.4,
            popup="Zona FUTUMED"
        ).add_to(m)
        
        # Marcadores discretos en las esquinas
        for p in lista_puntos:
            folium.CircleMarker(p, radius=2, color="black").add_to(m)

    # Renderizado estable
    st_folium(m, width="100%", height=550)
    st.info("📸 **Tip para tu informe:** Ajusta el zoom y toma una captura de pantalla (Win+Shift+S o Cmd+Shift+4) para insertar la zona en tu documento de FUTUMED.")

with col2:
    st.subheader("📦 Exportar")
    if lista_puntos:
        df = pd.DataFrame(lista_puntos, columns=["Latitud", "Longitud"])
        
        # Botones de descarga
        st.download_button(
            "📥 CSV (Excel)", 
            df.to_csv(index=False), 
            "puntos_futumed.csv", 
            use_container_width=True
        )
        
        # Generar GeoJSON manual para evitar dependencias
        geojson_str = json.dumps({
            "type": "Feature",
            "geometry": {
                "type": "Polygon", 
                "coordinates": [[ [p[1], p[0]] for p in lista_puntos ] + [[lista_puntos[0][1], lista_puntos[0][0]]]]
            },
            "properties": {"proyecto": "FUTUMED", "color": color_zona}
        })
        
        st.download_button(
            "🌍 GeoJSON (GIS)", 
            geojson_str, 
            "mapa_futumed.geojson", 
            use_container_width=True
        )

st.success("Mapa cargado con éxito. ¡Listo para Ruta N!")
