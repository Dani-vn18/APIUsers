# Importamos las librerías necesarias
import streamlit as st  # Librería para crear aplicaciones web interactivas. Instalación: pip install streamlit
import pandas as pd  # Librería para manipulación y análisis de datos. Instalación: pip install pandas
import os
from streamlit_cookies_controller import CookieController # Librería para manejar cookies en Streamlit. Instalación: pip install streamlit-cookies-controller

# Creamos una instancia de CookieController
controller = CookieController()

# Validación simple de usuario y clave con un archivo csv

def validarUsuario(usuario,clave):    
    """Permite la validación de usuario y clave

    Args:
        usuario (str): usuario a validar
        clave (str): clave del usuario

    Returns:
        bool: True usuario valido, False usuario invalido
    """
    
    # Obtiene la ruta del script actual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta relativa a el archivo CSV
    file_path = os.path.join(script_dir, 'usuarios.csv')
    
    # Leemos el archivo csv con los usuarios y claves
    dfusuarios = pd.read_csv(file_path)
    
    # Filtramos el dataframe para buscar el usuario y la clave
    if len(dfusuarios[(dfusuarios['usuario']==usuario) & (dfusuarios['clave']==clave)])>0:
        
        # Si el usuario y la clave existen, retornamos True
        return True
    else:
        
        # Si el usuario o la clave no existen, retornamos False
        return False

# Generación de menú según el usuario y el rol se maneja desde el código
def generarMenu(usuario):
    """Genera el menú dependiendo del usuario y el rol

    Args:
        usuario (str): usuario utilizado para generar el menú
    """
    
    with st.sidebar: # Creamos una barra lateral para el menú
        
        # Obtiene la ruta del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
        # Construye la ruta relativa a el archivo CSV
        file_path = os.path.join(script_dir, 'usuarios.csv')
    
        # Cargamos el CSV de usuarios
        dfusuarios = pd.read_csv(file_path)
        
        # Filtramos la tabla de usuarios por el usuario actual
        dfUsuario = dfusuarios[(dfusuarios['usuario']==usuario)]
        
        # Cargamos el nombre del usuario
        nombre = dfUsuario['nombre'].values[0]
        
        # Cargamos el rol
        rol = dfUsuario['rol'].values[0]
        
        #Mostramos el nombre del usuario
        st.write(f"Bienvenid@ **:blue-background[{nombre}]** ") # Mostramos el nombre del usuario con formato
        st.caption(f"Rol: **:red-background[{rol}]**") # Mostramos el rol del usuario
        
        # Mostramos los enlaces de páginas
        st.page_link("home.py", label="Inicio", icon=":material/home:") # Enlace a la página de inicio
        st.subheader("Menú de Navegación | **:blue-background[Prueba ConceptBPO]**") # Subtítulo para los menús
        
        # Mostramos los enlaces a las páginas según el rol del usuario
        if rol in ['admin','evaluador']:
            st.page_link("pages/pageListado.py", label="Información | Listado - Datos API", icon=":material/file_json:") # Enlace a la página de listado y detalles
        if rol in ['admin','evaluador']:
            st.page_link("pages/pageFavoritos.py", label="Información | Listado - Favoritos", icon=":material/stars:") # Enlace a la página de favoritos      
        if rol in ['admin','evaluador']:
            st.page_link("pages/pageGraficos.py", label="Información | Listado - Gráficos", icon=":material/monitoring:") # Enlace a la página de gráficos  
        
        # Botón para cerrar la sesión
        btnSalir=st.button("Salir") # Creamos un botón para salir
        
        if btnSalir: # Si se presiona el botón
            
            controller.remove('usuario') # Removemos de la cookie el usuario
            
            st.session_state.clear() # Limpiamos las variables de sesión
            
            # Luego de borrar el Session State reiniciamos la app para mostrar el formulario de usuario y clave
            
            st.rerun() # Reiniciamos la aplicación


# Validación de acceso a la página según los roles del usuario
def validarPagina(pagina,usuario):
    """Valida si el usuario tiene permiso para acceder a la página

    Args:
        pagina (str): página a validar
        usuario (str): usuario a validar

    Returns:
        bool: True si tiene permiso, False si no tiene permiso
    """
    # Obtiene la ruta del script actual
    script_dir_usr = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta relativa a el archivo CSV
    file_path_usr = os.path.join(script_dir_usr, 'usuarios.csv')

    # Obtiene la ruta del script actual
    script_dir_pages = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta relativa a el archivo CSV
    file_path_pages = os.path.join(script_dir_pages, 'rol_paginas.csv')

    # Cargamos la información de usuarios y roles
    dfusuarios = pd.read_csv(file_path_usr)
    dfPaginas = pd.read_csv(file_path_pages)
    
    dfUsuario = dfusuarios[(dfusuarios['usuario']==usuario)]
    
    rol = dfUsuario['rol'].values[0]
    
    dfPagina = dfPaginas[(dfPaginas['pagina'].str.contains(pagina))]
    
    # Validamos si el rol del usuario tiene acceso a la página
    if len(dfPagina)>0:
        if rol in dfPagina['roles'].values[0] or rol == "admin" or st.secrets["tipoPermiso"]=="rol":
            return True # El usuario tiene permiso
        else:
            return False # El usuario no tiene permiso
    else:
        return False # La página no existe en el archivo de permisos

# Generación de menú según el usuario y el rol se maneja desde un archivo csv
def generarMenuRoles(usuario):
    """Genera el menú dependiendo del usuario y el rol asociado a la página

    Args:
        usuario (str): usuario utilizado para generar el menú
    """        
    with st.sidebar: # Menú lateral
        
        # Obtiene la ruta del script actual
        script_dir_usr = os.path.dirname(os.path.abspath(__file__))
    
        # Construye la ruta relativa a el archivo CSV
        file_path_usr = os.path.join(script_dir_usr, 'usuarios.csv')
    
        # Obtiene la ruta del script actual
        script_dir_pages = os.path.dirname(os.path.abspath(__file__))
        
        # Construye la ruta relativa a el archivo CSV
        file_path_pages = os.path.join(script_dir_pages, 'rol_paginas.csv')
    
        # Cargamos la tabla de usuarios y páginas
        dfusuarios = pd.read_csv(file_path_usr)
        dfPaginas = pd.read_csv(file_path_pages)
        
        # Filtramos la tabla de usuarios por el usuario actual
        dfUsuario = dfusuarios[(dfusuarios['usuario']==usuario)]
        
        # Obtenemos el nombre y rol del usuario
        nombre= dfUsuario['nombre'].values[0]
        rol= dfUsuario['rol'].values[0]

        #Mostramos el nombre y el rol del usuario
        st.write(f"Bienvenid@ **:blue-background[{nombre}]** ")
        st.caption(f"Rol: {rol}")
        
        # Mostramos los enlaces de páginas        
        st.subheader("Opciones")
        
        # Verificamos si se deben ocultar o deshabilitar las opciones del menú
        if st.secrets["ocultarOpciones"]=="True": # Verificamos el valor del secreto "ocultarOpciones"
            
            if rol!='admin': # Si el rol no es admin
                
                # Filtramos la tabla de páginas por el rol actual
                dfPaginas = dfPaginas[dfPaginas['roles'].str.contains(rol)]

            # Ocultamos las páginas que no tiene permiso
            for index, row in dfPaginas.iterrows():
                
                icono=row['icono']            
                st.page_link(row['pagina'], label=row['nombre'], icon=f":material/{icono}:")  # Mostramos la página 
                
        else: # Si no se ocultan las opciones
            
            # Deshabilitamos las páginas que no tienen permiso
            for index, row in dfPaginas.iterrows():
                
                deshabilitarOpcion = True  # Valor por defecto para deshabilitar las opciones
                
                if rol in row["roles"] or rol == "admin": # Verificamos el rol
                    deshabilitarOpcion = False # Habilitamos la página si el usuario tiene permiso
                
                icono=row['icono']
                        
                # Mostramos el enlace de la página, deshabilitado o no según el permiso.
                st.page_link(row['pagina'], label=row['nombre'], icon=f":material/{icono}:",disabled=deshabilitarOpcion)         
        
        # Botón para cerrar la sesión
        btnSalir=st.button("Salir")
        
        if btnSalir:
            
            st.session_state.clear()
            
            controller.remove('usuario')
            
            st.rerun()

# Generación de la ventana de login y carga de menú
def generarLogin(archivo):
    """Genera la ventana de login o muestra el menú si el login es valido
    """    
    
    # Obtenemos el usuario de la cookie
    usuario = controller.get('usuario')
    
    # Validamos si el usuario ya fue ingresado
    if usuario:
        
        # Si ya hay usuario en el cookie, lo asignamos al session state
        st.session_state['usuario'] = usuario
        
    # Validamos si el usuario ya fue ingresado
    if 'usuario' in st.session_state: # Verificamos si la variable usuario esta en el session state
        
        # Si ya hay usuario cargamos el menu
        if st.secrets["tipoPermiso"]=="rolpagina":
            generarMenuRoles(st.session_state['usuario']) # Generamos el menú para la página
            
        else:
            generarMenu(st.session_state['usuario']) # Generamos el menú del usuario

        if validarPagina(archivo,st.session_state['usuario'])==False: # Si el usuario existe, verificamos la página
                    
            st.error(f"No tiene permisos para acceder a esta página {archivo}",icon=":material/gpp_maybe:")
            st.stop() # Detenemos la ejecución de la página
            
    else: # Si no hay usuario
        
        # Cargamos el formulario de login       
        with st.form('frmLogin'): # Creamos un formulario de login
            
            parUsuario = st.text_input('Usuario') # Creamos un campo de texto para usuario
            parPassword = st.text_input('Password',type='password') # Creamos un campo para la clave de tipo password
            btnLogin = st.form_submit_button('Ingresar',type='primary') # Botón Ingresar
            
            if btnLogin: # Verificamos si se presiono el boton ingresar
                
                if validarUsuario(parUsuario,parPassword): # Verificamos si el usuario y la clave existen
                    
                    st.session_state['usuario'] = parUsuario # Asignamos la variable de usuario
                    
                    # Set a cookie
                    controller.set('usuario', parUsuario)
                    
                    # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                    st.rerun() # Reiniciamos la aplicación
                    
                else:
                    
                    # Si el usuario es invalido, mostramos el mensaje de error
                    st.error("Usuario o clave inválidos",icon=":material/gpp_maybe:") # Mostramos un mensaje de error