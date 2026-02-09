from fastapi import FastAPI
from mcp.products_api import router as products_router
from mcp.cart_api import router as cart_router
from mcp.database import get_connection

from scripts.product_repository import crear_tabla_productos
from scripts.cart_repository import crear_tablas_carrito
from scripts.handoff_repository import crear_tabla_handoffs
from mcp.handoff_api import router as handoff_router


app = FastAPI(
    title="MCP - Agente de Compras",
    description="API HTTP consumida por un agente de IA",
    version="1.0.0"
)

@app.on_event("startup")
def inicializar_base_de_datos() -> None:
    """
    Inicializa (si no existen) las tablas necesarias del sistema.

    Se ejecuta automáticamente al levantar la aplicación y garantiza que:
    - products exista
    - carts exista
    - cart_items exista

    Esto evita errores en runtime cuando el agente consume endpoints.
    """
    conn = get_connection()
    crear_tabla_productos(conn)
    crear_tablas_carrito(conn)
    crear_tabla_handoffs(conn)
    conn.close()

app.include_router(products_router)
app.include_router(cart_router)
app.include_router(handoff_router)
