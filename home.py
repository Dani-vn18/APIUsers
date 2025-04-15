import streamlit as st
import login as login

archivo=__file__.split("\\")[-1]
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    st.header('Información | :orange[Página Principal]')
    
    st.markdown("""
    # 👥 **:blue[Explorador de Usuarios]**
    Bienvenid@ a **Explorador de Usuarios** 🚀

    ### 🔍 **Características principales**
    - **📋 Listado de usuarios:** Obtén y muestra información de cada usuario, incluyendo su nombre, correo electrónico y sus detalles ampliados.
    - **⭐ Gestión de favoritos:** Marca usuarios como favoritos usando DuckDB y una Base de Datos en Memoria.
    - **📊 Visualización de gráficos:** Experiencia intuitiva para el usuario que permite visualizar diferentes gráficos dinámicos sobre las columnas de los Usuarios.

    ### 🌍 **Objetivo**
    La aplicación permite explorar datos de usuarios de la API pública **JSONPlaceholder**, facilitando la comprensión del consumo de APIs y la manipulación de datos en el aplicativo.

    """)