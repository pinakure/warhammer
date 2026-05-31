import sqlite3
import psycopg2
import os
from psycopg2 import extras

SQLITE_DB = 'db.sqlite3'
POSTGRES_CONFIG = {
    'dbname': 'postgres',
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': '5432'
}
TARGET_CONFIG = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': '5432'
}

def migrar_datos():
    try:
        conn_sqlite = sqlite3.connect(SQLITE_DB)
        cursor_sqlite = conn_sqlite.cursor()
        conn_pg = psycopg2.connect(**POSTGRES_CONFIG)
        conn_pg.autocommit = True
        cursor_pg = conn_pg.cursor()
        # 1. Crear base de datos (eliminarla si existe primero para resetear los autoincrementales)
        cursor_pg.execute(f"DROP DATABASE { os.environ.get('DB_NAME') };")
        cursor_pg.execute(f"CREATE DATABASE { os.environ.get('DB_NAME') };")
        cursor_pg.execute(f"USE { os.environ.get('DB_NAME') };")
        cursor_pg.close()
        conn_pg.close()

        conn_pg = psycopg2.connect(**TARGET_CONFIG)
        conn_pg.autocommit = False
        cursor_pg = conn_pg.cursor()
        # 2. Obtener el nombre de todas las tablas de SQLite (excluyendo las del sistema)
        cursor_sqlite.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tablas = [fila[0] for fila in cursor_sqlite.fetchall()]
        
        print(f"Se encontraron {len(tablas)} tablas para migrar.")
        
        # 3. Iterar sobre cada tabla para extraer e insertar
        for tabla in tablas:
            if not tabla.startswith('dmscreen_'): continue
            print(f"Migrando tabla: {tabla}...", end="", flush=True)
            
            # Extraer registros de SQLite
            cursor_sqlite.execute(f'SELECT * FROM "{tabla}"')
            filas = cursor_sqlite.fetchall()
            
            if not filas:
                print(" (Vacía, saltando)")
                continue
            
            # Obtener nombres y tipos de las columnas usando el PRAGMA de SQLite
            cursor_sqlite.execute(f'PRAGMA table_info("{tabla}")')
            info_columnas = cursor_sqlite.fetchall()
            
            # Identificamos los índices de las columnas que son de tipo booleano
            # En SQLite suelen declararse como 'bool', 'boolean' o 'bool_int'
            indices_booleanos = [
                i for i, col in enumerate(info_columnas) 
                if 'bool' in col[2].lower()
            ]
            
            # Corregimos los datos al vuelo si la tabla tiene campos booleanos
            if indices_booleanos:
                filas_corregidas = []
                for fila in filas:
                    lista_fila = list(fila)
                    for idx in indices_booleanos:
                        if lista_fila[idx] is not None:
                            lista_fila[idx] = bool(lista_fila[idx])
                    filas_corregidas.append(tuple(lista_fila))
                filas = filas_corregidas
            
            # Obtener los nombres de las columnas para la Query
            columnas = [col[1] for col in info_columnas]
            columnas_str = ", ".join([f'"{col}"' for col in columnas])
            
            # Preparar la consulta de inserción para PostgreSQL
            query_insert = f'INSERT INTO "{tabla}" ({columnas_str}) VALUES %s'
            
            # Insertar los datos de forma masiva (ahora con booleanos reales)
            extras.execute_values(cursor_pg, query_insert, filas)
            
            print(f" OK ({len(filas)} filas copiadas)")
        
        # Guardar cambios permanentemente en PostgreSQL
        conn_pg.commit()
        print("\n¡Migración completada con éxito!")
        
    except Exception as e:
        print(f"\nError durante la migración: {e}")
        if 'conn_pg' in locals():
            conn_pg.rollback()
            print("Se ha realizado un rollback de los cambios en PostgreSQL.")
        
    finally:
        # 4. Cerrar conexiones de forma segura
        if 'cursor_sqlite' in locals(): cursor_sqlite.close()
        if 'conn_sqlite' in locals(): conn_sqlite.close()
        if 'cursor_pg' in locals(): cursor_pg.close()
        if 'conn_pg' in locals(): conn_pg.close()

if __name__ == "__main__":
    migrar_datos()
