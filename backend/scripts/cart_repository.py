import sqlite3
from datetime import datetime

def crear_tablas_carrito(conn: sqlite3.Connection) -> None:
    """
    Crea las tablas necesarias para manejar carritos de compra.
    Tablas:
        - carts: Representa un carrito asociado a una conversacion.
        - cart_items: Producto agregados al carrito.
    Args:
        conn(sqlite3.Connection): Conexion activa a la base de datos.
    """

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carts (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            qty INTEGER NOT NULL,
            FOREIGN KEY (cart_id) REFERENCES carts(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()

def crear_carrito(conn: sqlite3.Connection, cart_id: str) -> None:
    """
    Crea un carrito nuevo si no existe.
    El cart_id normalmente representa el id de conversacion o usuario.

    Args:
        conn(sqlite3.Connection) : Conexion activa a la base de datos
        cart_id(str): Identificador unico del carrito
    """

    ahora = datetime.utcnow().isoformat()

    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO carts (id, created_at, updated_at)
        VALUES (?, ?, ?)
    """, (cart_id, ahora, ahora))

    conn.commit()

def agregar_item_al_carrito(conn: sqlite3.Connection, cart_id: str,
        product_id: str,
        cantidad: int) -> None:
    """
    Agrega un producto al carrito.
    Si el producto ya existe, se incrementa la cantidad.
    Si no existe, crea el item.

    Args:
        conn(slite3.Connection): Conexion activa a la base de datos.
        cart_id(str): ID del carrito
        product_id(str): ID del producto
        cantidad(int): Cantidad a agregar
    """

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, qty
        FROM cart_items
        WHERE cart_id = ? AND product_id = ?
    """, (cart_id, product_id))

    fila = cursor.fetchone()

    if fila is not None:
        qty_actual = fila [0]
        nueva_qty = qty_actual + cantidad

        cursor.execute("""
            UPDATE cart_items
            SET qty = ?
            WHERE cart_id = ? AND product_id = ?
        """, (nueva_qty, cart_id, product_id))
    else:
        cursor.execute("""
            INSERT INTO cart_items (cart_id, product_id, qty)
            VALUES (?, ?, ?) 
            
        """, (cart_id, product_id, cantidad))
    
    cursor.execute("""
        UPDATE carts
        SET updated_at = ?
        WHERE id = ?
    """, (datetime.utcnow().isoformat(), cart_id))

    conn.commit()

def obtener_carrito(conn: sqlite3.Connection, cart_id: str) -> dict:
    """
    Obtiene el estado actual del carrito con sus productos.
    Devuelve una estructura lista para ser consumida por
    - API, MCP, IA

    Args:
        conn(sqlite3.Connection) : Conexion activa a la base de datos.
        cart_id(str): ID del carrito.
    Returns:
        dict: Informacion del carrito y sus items.
  
    """

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, created_at, updated_at
        FROM carts
        WHERE id = ?
    """, (cart_id,))

    carrito = cursor.fetchone()

    if not carrito:
        return {
            "id": cart_id,
            "items": [],
            "total": 0
        }
    
    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.descripcion,
            p.color,
            p.talle,
            p.precio,
            ci.qty
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.cart_id = ?
    """, (cart_id,))

    items = []

    for fila in cursor.fetchall():
        subtotal = fila[5] * fila[6]
        items.append({
            "id": fila[0],
            "nombre": fila[1],
            "descripcion":fila[2],
            "color": fila[3],
            "talle": fila[4],
            "precio_unitario": fila[5],
            "cantidad": fila[6],
            "subtotal": subtotal
        })
    
    total = sum(item["subtotal"] for item in items)

    return {
        "id": carrito[0],
        "created_at": carrito[1],
        "updated_at": carrito[2],
        "items": items,
        "total": total
    }

def actualizar_cantidad_item(conn: sqlite3.Connection, cart_id: str, product_id:str, nueva_cantidad: int) -> None:
    """
    Actualiza la canitad de un producto en el carrito.
    Reglas:
        -Si nueva_canitad <=0, se elimina el item 
        -Si el item no existe, no hace cambios.
    Args:
        conn(sqlite3.Connection): Conexion activa a la base de datos.
        cart_id(str): ID del carrito.
        product_id(str): ID del producto a actualizas.
        nueva_cantidad(int): Nueva cantidad deseada
    """
    cursor = conn.cursor()

    if nueva_cantidad <=0:
        cursor.execute("""
            DELETE FROM cart_items
            WHERE cart_id = ? AND product_id = ?
        """, (cart_id, product_id))
    else:
        cursor.execute("""
            UPDATE cart_items
            SET qty = ?
            WHERE cart_id = ? AND product_id = ?
        """,(nueva_cantidad, cart_id, product_id))

    cursor.execute("""
        UPDATE carts
        SET updated_at = ?
        WHERE id = ?
    """, (datetime.utcnow().isoformat(), cart_id))

    conn.commit()

def eliminar_item_del_carrito(conn: sqlite3.Connection, cart_id: str, product_id:str) -> None:
    """
    Elimina un producto del carrito.
    Args:
        conn(sqlite3.Connection): Conexion activa a la base de datos
        cart_id(str): ID del carrito
        product_id(str): ID del producto a eliminar
    """
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cart_items
        WHERE cart_id = ? AND product_id = ?
    """, (cart_id, product_id))

    cursor.execute("""
        UPDATE carts
        SET updated_at = ?
        WHERE id = ?
    """, (datetime.utcnow().isoformat(), cart_id))

    conn.commit()