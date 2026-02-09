from fastapi import APIRouter, Query, HTTPException
from mcp.database import get_connection
from scripts.product_repository import buscar_productos, obtener_producto_por_id

router = APIRouter()


def _normalize_product(p: dict) -> dict:
    """Convierte campos para salida de API (ej: disponible 0/1 -> bool)."""
    if "disponible" in p:
        p["disponible"] = bool(p["disponible"])
    return p


@router.get("/search")
def search_products(
    nombre: str | None = Query(default=None),
    color: str | None = Query(default=None),
    talle: str | None = Query(default=None),
    categoria: str | None = Query(default=None),
    solo_disponibles: bool = Query(default=True),
):
    """
    Busca productos aplicando filtros dinámicos.
    Todos los parámetros son opcionales.
    """
    filtros = {
        "nombre": nombre,
        "color": color,
        "talle": talle,
        "categoria": categoria,
        "solo_disponibles": solo_disponibles,
    }

    conn = get_connection()
    productos = buscar_productos(conn, filtros)
    conn.close()

    productos = [_normalize_product(p) for p in productos]

    return {"count": len(productos), "results": productos}


@router.get("/{product_id}")
def get_product_detail(product_id: str):
    """
    Obtiene el detalle de un producto específico por ID.
    """
    conn = get_connection()
    producto = obtener_producto_por_id(conn, product_id)
    conn.close()

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return _normalize_product(producto)
