import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

# Configuración de página
st.set_page_config(page_title="FUTUMED - Creador de Zonas Profesional", layout="wide")

st.title("🗺️ Delimitador de Zonas con Contexto Urbano")
st.write("Traza tu zona de influencia de FUTUMED en Medellín, visualiza barrios y exporta los resultados.")

# --- BARRA LATERAL: CONFIGURACIÓN ---
st.sidebar.header("1. Configura tu Zona")

# Elegir color de la zona
color_zona = st.sidebar.color_picker("Elige el color para la zona", "#FF4B4B")

# Ingreso manual de coordenadas (Límites)
st.sidebar.subheader("2. Ingresa los Vértices")
st.sidebar.info("Copia y pega desde Google Maps con el formato: `Latitud, Longitud` (uno por línea).")

coord_input = st.sidebar.text_area(
    "Coordenadas del perímetro",
    "6.2685, -75.5645\n6.2650, -75.5615\n6.2595, -75.5665\n6.2635, -75.5700",
    help="Se necesitan al menos 3 puntos para cerrar un área.",
    height=150
)

# --- PROCESAMIENTO DE DATOS ---
def procesar_coords(texto):
    puntos = []
    try:
        for linea in texto.split('\n'):
            linea = linea.strip()
            if ',' in linea:
                # Limpiar espacios extra y convertir a float
                partes = linea.split(',')
                if len(partes) == 2:
                    lat = float(partes[0].strip())
                    lon = float(partes[1].strip())
                    puntos.append([lat, lon])
        return puntos
    except ValueError:
        st.error("Error en el formato de números. Asegúrate de usar punto (.) para decimales y coma (,) para separar latitud de longitud.")
        return []
    except Exception as e:
        st.error(f"Error inesperado procesando coordenadas: {e}")
        return []

lista_puntos = procesar_coords(coord_input)

# --- MAPA INTERACTIVO CON CONTEXTO URBANO ---
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Mapa de Influencia (con nombres de barrios)")
    
    # Crear mapa base centrado en el primer punto o en Ruta N
    centro = lista_puntos[0] if lista_puntos else [6.2650, -75.5663]
    
    # Usamos tiles="openstreetmap" para asegurar que los nombres de los barrios se vean
    m = folium.Map(location=centro, zoom_start=15, tiles="openstreetmap")
    
    # --- FUNCIONALIDAD DE IMAGEN (BOTÓN DE IMPRESIÓN) ---
    # Añadimos un plugin de Folium para permitir guardar como imagen
    from folium.plugins import PrintMap
    PrintMap().add_to(m)
    # Explicación para el usuario
    st.caption("ℹ️ Para descargar la imagen, haz clic en el icono de impresora 🖨️ arriba a la izquierda del mapa.")

    if len(lista_puntos) > 2:
        # Dibujar el Polígono personalizado
        folium.Polygon(
            locations=lista_puntos,
            color=color_zona,
            fill=True,
            fill_color=color_zona,
            fill_opacity=0.4,
            popup="Zona Delimitada FUTUMED",
            tooltip="Área de Influencia"
        ).add_to(m)
        
        # Agregar marcadores pequeños en los vértices para precisión
        for i, p in enumerate(lista_puntos):
            folium.CircleMarker(p, radius=2, color="#333333", fill=True, fill_color="#FFFFFF").add_to(m)

    # Renderizar mapa con streamlit-folium
    # Se especifica height para controlar el tamaño del componente
    st_folium(m, width="100%", height=550)

with col2:
    st.subheader("Exportar Datos")
    if lista_puntos:
        df_export = pd.DataFrame(lista_puntos, columns=["Latitud", "Longitud"])
        st.dataframe(df_export, use_container_width=True, height=200)
        
        st.write("---")
        st.subheader("Formatos Digitales")
        
        # --- FUNCIONALIDAD DE DESCARGA DE DATOS ---
        # 1. Descargar como CSV
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Coordenadas (CSV)",
            data=csv,
            file_name='coordenadas_zona_futumed.csv',
            mime='text/csv',
            use_container_width=True
        )
        
        # 2. Descargar como GeoJSON (Estándar profesional GIS)
        geojson_data = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {
                    "proyecto": "FUTUMED",
                    "color_hex": color_zona,
                    "origen": "Generado en App Streamlit"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[ [p[1], p[0]] for p in lista_puntos ] + [[lista_puntos[0][1], lista_puntos[0][0]]]]
                }
            }]
        }
        
        st.download_button(
            label="🌍 Descargar Mapa Digital (GeoJSON)",
            data=json.dumps(geojson_data, indent=2),
            file_name='mapa_zona_futumed.geojson',
            mime='application/json',
            use_container_width=True
        )
        st.info("El formato GeoJSON es el ideal para entregar a Ruta N o Planeación Municipal.")

if len(lista_puntos) < 3:
    st.warning("⚠️ Ingresa al menos 3 coordenadas en la barra lateral para delimitar un área.")
