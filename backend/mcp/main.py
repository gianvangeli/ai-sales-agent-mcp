from fastapi import FastAPI
from mcp.products_api import router as products_router
from mcp.cart_api import router as cart_router
from mcp.database import get_connection
from scripts.product_repository import crear_tabla_productos
from scripts.import_products import main as import_products



app = FastAPI(title="MCP - AI Sales Agent")

app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])

@app.on_event("startup")
def inicializar_base_de_datos():
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM products")
    cantidad = cursor.fetchone()[0]

    print(f"[STARTUP] Productos en DB: {cantidad}")

    if cantidad == 0:
        print("[STARTUP] Importando productos...")
        try:
            import_products()
            print("[STARTUP] Importación ok")
        except Exception as e:
            print(f"[STARTUP] ERROR importando products: {e}")

    conn.close()

    
    

@app.get("/health")
def health() -> dict:
    """Endpoint simple para verificar que el servicio está vivo."""
    return {"status": "ok"}
