import streamlit as st
import pandas as pd
import login as login
from utilitaries import get_users, detalle_usuario

archivo=__file__.split("\\")[-1]
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    
    st.header('Información | :orange[Página Listado de Usuarios]')
    
    try:
        
        users = get_users()
        
    except Exception as e:
        
        st.error(f"Ha ocurrido un error al cargar los datos de la API: {e}.")
    
    # Extraer la información relevante y convertirla en DataFrame
    df = pd.DataFrame([{
        "ID": user["id"],
        "Nombre": user["name"],
        "Nombre Usuario": user["username"],
        "Correo": user["email"],
        "Dirección (Street)": user["address"]["street"],
        "Dirección (Suite)": user["address"]["suite"],
        "Dirección (City)": user["address"]["city"],
        "Dirección (Zipcode)": user["address"]["zipcode"],
        "Dirección (Geo - Latitud)": user["address"]["geo"]["lat"],
        "Dirección (Geo - Longitud)": user["address"]["geo"]["lng"],
        "Teléfono": user["phone"],
        "Sitio Web": user["website"],
        "Empresa (Name)": user["company"]["name"],
        "Empresa (Catch Phrase)": user["company"]["catchPhrase"],
        "Empresa (Bs)": user["company"]["bs"],
    } for user in users])
    
    # Markdown para Mencionar que es la Cabecera del DataFrame
    st.markdown("""> ## Listado de Usuarios""")
    
    # Mostrar tabla
    st.dataframe(df[["Nombre", "Nombre Usuario", "Correo"]], use_container_width=True)

    # Mostrar tabla editable
    st.title("📋 Explorador de Usuarios")
    st.markdown("""> ## Selecciona un usuario y haz clic en 'Ver Detalle' para ver más información.""")
        
    # Mostrar DataFrame con selección de fila
    selected = st.dataframe(df[["Nombre", "Nombre Usuario", "Correo"]], on_select="rerun", selection_mode=["single-row"], use_container_width=True)

    # Validar si hay selección
    if len(selected.selection.rows) > 0:
        
        indice_usuario = selected.selection.rows[0]  # Captura el índice del usuario seleccionado

        # Botón para ver detalles del usuario seleccionado
        if st.button(f"🔍 Ver detalle de {df.iloc[indice_usuario]['Nombre']}"):
            
            # Llamar a la función de detalles
            detalle_usuario(dataFrame=df, indice_usuario=indice_usuario)
    
    else:
        
        st.error("Por favor seleccione un Usuario.")
