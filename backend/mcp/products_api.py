from fastapi import APIRouter, Query
from mcp.database import get_connection
from scripts.product_repository import buscar_productos, obtener_producto_por_id
from fastapi import HTTPException

router = APIRouter()

@router.get("/search")
def search_products(nombre: str | None = Query(default=None),
                    color: str | None = Query(default=None),
                    talle: str | None = Query(default=None),
                    categoria: str | None = Query(default=None),
                    solo_disponibles: bool = True):
    
    """
    Busca productos aplicando filtros dinamicos.
    Todos los parametros son opcionales.

    Returns:
        dict: cantidad de resultados y lista de productos.

    """

    filtros = {
        "nombre": nombre,
        "color": color,
        "talle": talle,
        "categoria": categoria,
        "solo_disponibles": solo_disponibles
    }
    
    conn = get_connection()
    productos = buscar_productos(conn, filtros)
    conn.close()

    return {
        "count": len(productos),
        "results": productos
    }

@router.get("/{product_id}")
def get_product_detail(product_id: str):
    """
    Obtiene el detalle de un productos especifico por ID.
    Args:
        product_id(str): Identificador del producto.
    Raises:
        HTTPException: 404 si el producto no existe.
    Returns:
        dict: Detalle completo del producto
    """

    conn = get_connection()
    producto = obtener_producto_por_id(conn, product_id)
    conn.close()

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto