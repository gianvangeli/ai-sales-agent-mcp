from __future__ import annotations
import sqlite3
from pathlib import Path

# Base: carpeta "backend/" (root directory en Render)
BASE_DIR = Path(__file__).resolve().parents[1]  # .../backend
DB_DIR = BASE_DIR / "database"
DATABASE_PATH = DB_DIR / "database.sqlite"


def get_connection() -> sqlite3.Connection:
    """
    Devuelve una conexión SQLite.

    - Asegura que exista el directorio 'backend/database' antes de conectar.
    - Usa una ruta absoluta para evitar errores de working directory en Render.

    Returns:
        sqlite3.Connection: Conexión activa a SQLite.
    """
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn
