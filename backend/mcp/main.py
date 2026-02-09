from fastapi import FastAPI
from mcp.products_api import router as products_router
from mcp.cart_api import router as cart_router
from mcp.database import get_connection
from scripts.import_products import main as import_products

import sqlite3
import os

app = FastAPI(title="MCP - AI Sales Agent")

app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])

@app.on_event("startup")
def inicializar_base_de_datos():
    conn = get_connection()
    # Si la tabla está vacía, importamos
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM products")
    cantidad = cursor.fetchone()[0]
    if cantidad == 0:
        print("Importando productos desde Excel...")
        import_products()
        print("Importación completada correctamente.")
    conn.close()

@app.get("/health")
def health() -> dict:
    """Endpoint simple para verificar que el servicio está vivo."""
    return {"status": "ok"}
