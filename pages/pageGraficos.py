import streamlit as st
import pandas as pd
import login as login
import plotly.express as px
from utilitaries import get_users

archivo=__file__.split("\\")[-1]
login.generarLogin(archivo)
if 'usuario' in st.session_state:
    
    st.header('Información | :orange[Página Visualización de Datos]')
    
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
    
    # Contar ocurrencias de cada valor en las columnas relevantes
    city_counts = df["Dirección (City)"].value_counts().reset_index()
    city_counts.columns = ["Dirección (City)", "Cantidad"]

    website_counts = df["Sitio Web"].value_counts().reset_index()
    website_counts.columns = ["Sitio Web", "Cantidad"]

    company_counts = df["Empresa (Name)"].value_counts().reset_index()
    company_counts.columns = ["Empresa (Name)", "Cantidad"]

    # Crear gráficos de barras con Plotly
    fig_city = px.bar(city_counts, x="Dirección (City)", y="Cantidad", color="Dirección (City)", title="Conteo de Usuarios por Ciudad", text_auto=True)
    fig_website = px.bar(website_counts, x="Sitio Web", y="Cantidad", color="Sitio Web", title="Conteo de Usuarios por Sitio Web", text_auto=True)
    fig_company = px.bar(company_counts, x="Empresa (Name)", y="Cantidad", color="Empresa (Name)", title="Conteo de Usuarios por Empresa", text_auto=True)

    # Mostrar gráficos en Streamlit
    st.title("📊 Análisis de Usuarios")
    st.subheader("Distribución de usuarios según diferentes atributos")

    st.plotly_chart(fig_city, use_container_width=True)
    st.plotly_chart(fig_website, use_container_width=True)
    st.plotly_chart(fig_company, use_container_width=True)
