import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path #Para manejar rutas

#obtener la ruta de este archivo
current_path = Path(__file__).resolve()

#buscamos el archivo .env en la carpeta
env_path = current_path.parent.parent / '.env'

#Cargar las variables del archivo .env
load_dotenv(dotenv_path=env_path)

# --- DEBUGGING (Imprimir para ver si carga) ---
print("--- VERIFICACIÓN DE VARIABLES ---")
print(f"Buscando .env en: {env_path}")
print(f"Usuario: {os.getenv('DB_USER')}") # Debería imprimir 'postgres'
print(f"Base de Datos: {os.getenv('DB_NAME')}") # Debería imprimir 'ebay_monitor'
print("-------------------------------")

#Obtener credenciales
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

#Crear la cadena de conexión (connection String)
#formato: postgresql://usuario:password@host:puerto/nombre_bd

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def probar_conexion():
    print(f"Intento conectar a: {DB_NAME} en localhost...")

    try:
        #Crear el motor de conexión
        engine = create_engine(DATABASE_URL)

        #Conectar realmente para verificar
        with engine.connect() as connection:
            print("¡Conexión Exitosa a PostgreSQL!")

            #Crear un dato de prueba (Mock Data)
            datos_prueba = {
                "item_id": ["TEST-001"],
                "titulo": ["Producto de Prueba - Conexión Python"],
                "precio": [100.50],
                "moneda": ["EUR"],
                "vendedor": ["test_user"],
                "fecha_extraccion": [pd.Timestamp.now()]
            }

            df = pd.DataFrame(datos_prueba)

            #Insertar en la tabla 'precios_competencia'
            #if_exists='append' significa: agrega al final, no borres lo anterior

            df.to_sql('precios_competencia', engine, if_exists='append', index=False)

            print("Dato de prueba insertado correctamente en la tabla.")

    except Exception as e:
        print(f"Error Crítico: {e}")
        print("Sugerencia: Revisa tu contraseña en el archivo .env o si PostgreSQL está abierto.")

if __name__ == "__main__":
    probar_conexion()