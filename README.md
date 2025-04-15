📌 Explorador de Usuarios con Favoritos

Objetivo del Proyecto

Este proyecto consiste en una aplicación web interactiva para visualizar y gestionar información de usuarios a partir de la API pública de JSONPlaceholder. Además, permite a los usuarios autenticados marcar otros usuarios como favoritos, simulando la persistencia en una base de datos DuckDB.

Uso de Python y Paradigma Funcional
El proyecto está desarrollado en Python, aprovechando el paradigma de programación funcional para lograr un código modular, reutilizable y fácil de escalar. 

Se priorizó:
- Funciones puras que reciben datos y retornan nuevos valores sin modificar estados globales.

- Uso de funciones para separar responsabilidades como la autenticación, el manejo de datos y la consulta de favoritos.

Uso de Streamlit
- Se eligió Streamlit como framework principal para la interfaz web debido a su simplicidad y facilidad de integración con Python. Streamlit permite:

- Renderización rápida de DataFrames para visualizar y editar información de usuarios.

- Componentes interactivos como botones, tablas y formularios sin necesidad de escribir HTML o JavaScript.

🚀 Contenido del Proyecto
Conexión a la API JSONPlaceholder para obtener la lista de usuarios.

Visualización dinámica de usuarios en una tabla interactiva con Streamlit.

Sistema de autenticación simulado basado en cookies para identificar el usuario activo.

Funcionalidad de "Marcar como Favorito" para registrar usuarios seleccionados en una base de datos.

Persistencia de datos utilizando DuckDB (Base de Datos en Memoria), simulando una estructura relacional como PostgreSQL o MySQL.

🏛️ Diseño de la Base de Datos Relacional (PostgreSQL / MySQL)

Para simular una estructura relacional, se usa DuckDB, una base de datos en memoria. 

Se diseñaron dos tablas con una relación uno-a-muchos:

1️⃣ Usuarios: Almacena la información básica de los usuarios del sistema. 
2️⃣ Favoritos: Relaciona el usuario autenticado con los usuarios que ha marcado como favoritos.

📂 Tabla de usuarios
Almacena información de todos los usuarios del sistema.

CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    clave VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL
);

⭐ Tabla de favoritos
Relaciona el usuario autenticado con los usuarios que ha marcado como favoritos.

CREATE TABLE favoritos (
    id_favorito INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,  -- Usuario autenticado que marca favoritos
    id_usuario_favorito INT NOT NULL,  -- Usuario marcado como favorito
    marcado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario_favorito) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

🔹 Explicación de la Estructura
✅ Cada usuario (id_usuario) puede marcar múltiples favoritos (id_usuario_favorito), asegurando una relación uno-a-muchos. 

🔥 ¿Cómo se integra en el proyecto?
✔️ En DuckDB, la estructura se simula sin AUTO_INCREMENT, pero con una secuencia. 
✔️ El usuario autenticado se extrae desde las cookies y se usa para registrar favoritos en la base de datos. 
✔️ La consulta de favoritos se hace filtrando por id_usuario, asegurando que cada usuario vea solo sus propios favoritos.
