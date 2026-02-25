# database/connection.py
# ============================================================
# Manejador de conexión a la base de datos SQLite
# ============================================================

import sqlite3
import os

# Ruta de la base de datos (se crea en la carpeta database/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "almerco.db")


def get_connection():
    """
    Retorna una conexión activa a la base de datos.
    Activa las foreign keys (desactivadas por defecto en SQLite).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row  # permite acceder columnas por nombre
    return conn


def init_db():
    """
    Lee el schema.sql y crea todas las tablas si no existen.
    """
    schema_path = os.path.join(BASE_DIR, "schema.sql")

    with get_connection() as conn:
        with open(schema_path, "r", encoding="utf-8") as f:
            sql = f.read()
        conn.executescript(sql)
        print("✅ Base de datos inicializada correctamente.")


if __name__ == "__main__":
    init_db()