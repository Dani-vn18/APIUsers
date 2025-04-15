import requests
import pandas as pd
import duckdb
import streamlit as st

@st.cache_data
def get_users():
    """Función para hacer una petición GET al endpoint para obtener los datos de los usuarios.

    Returns:
        response (JSON): Retorna el JSON con los resultados de la petición a la API.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    if response.status_code == 200:
        st.success("Datos cargados exitosamente.")
        return response.json()
    else:
        st.error("Datos no recibidos, por favor verifique su código.")
        return []
    

# Definición del diálogo usando el decorador @st.dialog
@st.dialog("Detalle del Usuario", width="large")
def detalle_usuario(dataFrame: pd.DataFrame, indice_usuario: int):
    """Función que recibe como parámetros el DataFrame y el Índice del Usuario para luego mostrarlos en un modal.

    Args:
        dataFrame (pd.DataFrame): Parámetro con el DataFrame que contiene el listado de Usuarios.
        indice_usuario (int): Parámetro con el índice del dato seleccionado en específico.
    """
    usuario_detalle = dataFrame.iloc[indice_usuario]
    st.write(f"**:blue[Nombre]:** {usuario_detalle['Nombre']}")
    st.write(f"**:blue[Username]:** {usuario_detalle['Nombre Usuario']}")
    st.write(f"**:blue[Correo]:** {usuario_detalle['Correo']}")
    st.write(f"**:blue[Dirección (Street)]:** {usuario_detalle['Dirección (Street)']}")
    st.write(f"**:blue[Dirección (Suite)]:** {usuario_detalle['Dirección (Suite)']}")
    st.write(f"**:blue[Dirección (City)]:** {usuario_detalle['Dirección (City)']}")
    st.write(f"**:blue[Dirección (Zipcode)]:** {usuario_detalle['Dirección (Zipcode)']}")
    st.write(f"**:blue[Dirección (Geo - Latitud)]:** {usuario_detalle['Dirección (Geo - Latitud)']}")
    st.write(f"**:blue[Dirección (Geo - Longitud)]:** {usuario_detalle['Dirección (Geo - Longitud)']}")
    st.write(f"**:blue[Teléfono]:** {usuario_detalle['Teléfono']}")
    st.write(f"**:blue[Sitio Web]:** {usuario_detalle['Sitio Web']}")
    st.write(f"**:blue[Empresa (Name)]:** {usuario_detalle['Empresa (Name)']}")
    st.write(f"**:blue[Empresa (Catch Phrase)]:** {usuario_detalle['Empresa (Catch Phrase)']}")
    st.write(f"**:blue[Empresa (Bs)]:** {usuario_detalle['Empresa (Bs)']}")
    

# Función para crear la base de datos y poblar las tablas
def crear_base_datos():
    try:
        conn = duckdb.connect(database=":memory:")

        # Crear tabla de usuarios
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT PRIMARY KEY,
                usuario TEXT UNIQUE,
                nombre TEXT,
                clave TEXT,
                rol TEXT
            )
        """)
        
        # Crear secuencia de id_favorito
        conn.execute("""
            CREATE SEQUENCE seq_favoriteid START 1;
        """)
        

        # Crear tabla de favoritos
        conn.execute("""
            CREATE TABLE IF NOT EXISTS favoritos (
                id_favorito INT PRIMARY KEY,
                id_usuario INT,  -- Usuario autenticado
                id_usuario_favorito INT,  -- Usuario marcado como favorito
                marcado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
                FOREIGN KEY (id_usuario_favorito) REFERENCES usuarios(id_usuario)
            )
        """)

        # Insertar valores iniciales
        usuarios_data = [
            (1, "admin", "admin", "admin", "admin"),
            (2, "usrEvaluador", "Evaluador", "evaluador123", "evaluador"),
            (3, "Bret", "Leanne Graham", "12345", "usuario"),
            (4, "Antonette", "Ervin Howell", "12345", "usuario"),
            (5, "Samantha", "Clementine Bauch", "12345", "usuario"),
            (6, "Karianne", "Patricia Lebsack", "12345", "usuario"),
            (7, "Kamren", "Chelsey Dietrich", "12345", "usuario"),
            (8, "Leopoldo_Corkery", "Mrs. Dennis Schulist", "12345", "usuario"),
            (9, "Elwyn.Skiles", "Kurtis Weissnat", "12345", "usuario"),
            (10, "Maxime_Nienow", "Nicholas Runolfsdottir V", "12345", "usuario"),
            (11, "Delphine", "Glenna Reichert", "12345", "usuario"),
            (12, "Moriah.Stanton", "Clementina DuBuque", "12345", "usuario")
        ]

        conn.executemany("INSERT OR IGNORE INTO usuarios VALUES (?, ?, ?, ?, ?)", usuarios_data)
        st.success("Base de datos creada y poblada correctamente.")
        
        return conn

    except Exception as e:
        st.error(f"Error creando la Base de Datos: {e}")
        return None


# Función para insertar un favorito en la tabla
def insertar_favorito(conn, id_usuario, id_usuario_favorito):
    try:
        conn.execute("""
            INSERT OR IGNORE INTO favoritos (id_favorito, id_usuario, id_usuario_favorito)
            VALUES (nextval('seq_favoriteid'), ?, ?)
        """, (id_usuario, id_usuario_favorito))
        st.success(f"Usuario {id_usuario_favorito} añadido a favoritos.")
    
    except Exception as e:
        st.error(f"Error al marcar favorito: {e}")