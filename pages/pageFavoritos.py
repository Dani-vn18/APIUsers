import streamlit as st
import pandas as pd
import login as login
import duckdb
from utilitaries import get_users, detalle_usuario, crear_base_datos, insertar_favorito

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    
    st.header('Información | :orange[Página Agregar a Favoritos]')
    
    st.markdown("> ## Se crea una Base de Datos en Memoria usando DuckDB con Tablas como: Usuarios y Favoritos.")
    
    conn = crear_base_datos()

    if conn:
        
        # Obtener el username del usuario actual desde la sesión
        cookie_Usuario = st.session_state['usuario']
        
        usuario_actual = conn.execute("SELECT * FROM usuarios WHERE usuario = ?", (cookie_Usuario,)).fetchdf()

        if not usuario_actual.empty:
            id_usuario = usuario_actual.iloc[0]["id_usuario"]
            nombre_usuario = usuario_actual.iloc[0]["nombre"]
            st.success(f"Bienvenid@ {nombre_usuario} - #ID{id_usuario}")
            
            df_Listado_Usuarios = conn.execute("SELECT * FROM usuarios").fetchdf()
            
            # Mostrar DataFrame con selección de fila (Usuarios)
            selected = st.dataframe(df_Listado_Usuarios[["usuario", "nombre"]], on_select="rerun", selection_mode=["single-row"], use_container_width=True)

            # Validar si hay selección
            if len(selected.selection.rows) > 0:
                
                usuario_favorito = selected.selection.rows[0]  # Captura el índice del usuario seleccionado

                # Botón para ver detalles del usuario seleccionado
                if st.button(f"⭐ Agregar como Favorito a: {df_Listado_Usuarios.iloc[usuario_favorito]['nombre']}"):
                    
                    # Llamar a la función de detalles
                    insertar_favorito(conn, int(id_usuario), int(usuario_favorito))
            
            else:
                
                st.error("Por favor seleccione un Usuario.")
                
                
            st.markdown("> ## Al momento de añadir a favoritos se hace la consulta a la tabla y se visualiza que se guarde correctamente la información.")
            
            df_Listado_Favoritos = conn.execute("SELECT * FROM favoritos WHERE id_usuario = ?", (int(id_usuario),)).fetchdf()
            
            st.dataframe(df_Listado_Favoritos)
