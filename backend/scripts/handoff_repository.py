import sqlite3
import uuid
from datetime import datetime

def crear_tabla_handoffs(conn: sqlite3.Connection) -> None:
    """
    Crea la tabla handoffs si no existe.
    Esta tabla registra derivacion solicitadas por el agente hacia un humano,
    guardando contexto de la conversacion para auditoria o integracion posterior
    con un CRM 

    Args:
        conn(sqlite3.Connection): Conexion activa a la base de datos
    """

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS handoffs (
            id TEXT PRIMARY KEY,
            cart_id TEXT NOT NULL,
            motivo TEXT NOT NULL,
            contexto TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (cart_id) REFERENCES carts(id)
        )
    """)

    conn.commit()


def registrar_handoff(conn: sqlite3.Connection, cart_id: str, motivo: str, contexto: str | None) -> str:
    """
    Registra una derivacion (handoff) en la base de datos.
    Args:
        conn (sqlite3.Connection): Conexion activa a la base de datos.
        cart_id(str): ID del carrito / conversacion.
        motivo(str): Motivo de la derivacion
        contexto(str | None): Contexto adicional (resumen de intencion del usuario).
    
    Returns:
        str: ID unico del handoff (UUID).
    """

    handoff_id = str(uuid.uuid4())
    ahora = datetime.utcnow().isoformat()

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO handoffs (id, cart_id, motivo, contexto, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (handoff_id, cart_id, motivo, contexto, ahora))

    conn.commit()
    return handoff_id

