import sqlite3

def crear_tabla_productos(conn: sqlite3.Connection) -> None:
    """
    Crea la tabla products si no existe.

    Args:
        conn (sqlite3.Connection): Conexion activa a la base de datos.
        
    """

    cursor = conn.cursor()
    cursor.execute( """
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            categoria TEXT,
            color TEXT,
            talle TEXT,
            precio REAL,
            stock INTEGER,
            disponible BOOLEAN
        )
    """)
    conn.commit()


def insertar_productos(conn: sqlite3.Connection, productos: list[dict]) -> None:
    """
    Inserta o actualiza productos a la base de datos.

    Args:
        conn (sqlite3.Connection): Conexion activa a la base de datos.
        productos(list[dict]): Lista de productos mapeados
        
    """

    cursor = conn.cursor()

    for producto in productos:
        cursor.execute("""
            INSERT OR REPLACE INTO products
                (id,
                nombre,
                descripcion,
                categoria,
                color,
                talle,
                precio,
                stock,
                disponible
            ) VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            producto["id"],
            producto["nombre"],
            producto["descripcion"],
            producto["categoria"],
            producto["color"],
            producto["talle"],
            producto["precio_unitario"],
            producto["stock"],
            producto["disponible"]
        ))

    conn.commit()

def buscar_productos(conn: sqlite3.Connection, filtros: dict) -> list [dict]:
    """
    Busca productos aplicando filtros dinamicos.
    Args:
        conn(sqlite3.Connection): Conexion activa a la base de datos.
        filtros(dict): Diccionario con filtros posibles.
        Claves soportadas:
        - nombre
        - color
        - talle
        - categoria
        - solo_disponible(bool)
    Returns:
        list[dict]: Lista de productos que coinciden con los filtros
  
    """
    query = """
        SELECT
            id,
            nombre,
            descripcion,
            categoria,
            color,
            talle,
            precio,
            stock,
            disponible
        FROM products
        WHERE 1=1
    """

    parametros: list = []

    if "nombre" in filtros :
        query += "AND nombre LIKE ?"
        parametros.append(f"%{filtros["nombre"]}%")

    if "color" in filtros:
        query += "AND color = ?"
        parametros.append(filtros["color"])

    if "talle" in filtros:
        query += "AND talle = ?"
        parametros.append(filtros["talle"])
    
    if "categoria" in filtros:
        query += "AND categoria = ?"
        parametros.append(filtros["categoria"])
    
    if filtros.get("solo_disponibles"):
        query += "AND disponible = 1"
    
    cursor = conn.cursor()
    cursor.execute(query, parametros)

    columnas = [col[0] for col in cursor.description]
    
    return [dict(zip(columnas, fila ))
            for fila in cursor.fetchall()]


def obtener_producto_por_id(conn: sqlite3.Connection, product_id: str) -> dict | None:
    """
    Obtiene el detalle de un producto por su ID.
    Args:
        conn(sqlite3.Connection): Conexion activa a la base de datos.
        product_id(str): ID del producto.
    Returns:
        dict | None: Un diccionario con el producto si existe, None si no existe.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            id,
            nombre,
            descripcion,
            categoria,
            color,
            talle,
            precio,
            stock,
            disponible
        FROM products
        WHERE id = ?
    """, (product_id,))

    fila = cursor.fetchone()

    if fila is None:
        return None
    
    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas,fila))

