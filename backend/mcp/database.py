import sqlite3

DATABASE_PATH = "database/database.sqlite"

def get_connection() -> sqlite3.Connection:
    """
    Devuelve una conexion a la base de datos SQLITE.
    """

    return sqlite3.connect(DATABASE_PATH)