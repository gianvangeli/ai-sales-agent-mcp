from fastapi import FastAPI
from mcp.products_api import router as products_router
from mcp.cart_api import router as cart_router
from mcp.database import get_connection
from scripts.import_products import main as import_products

app = FastAPI(title="MCP - AI Sales Agent")

app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])

@app.on_event("startup")
def inicializar_base_de_datos():
    conn = get_connection()
    cursor = conn.cursor()

    # 1) Crear tablas si no existen
    from scripts.product_repository import crear_tabla_productos
    from scripts.cart_repository import crear_tablas_carrito
    from scripts.import_products  import import_products 

    crear_tabla_productos(conn)
    crear_tablas_carrito(conn)
    conn.commit()

    # 2) Comprobar si hay productos
    try:
        cursor.execute("SELECT count(*) FROM products")
        cantidad = cursor.fetchone()[0]
    except Exception as e:
        cantidad = 0

    print(f"[STARTUP] Productos en DB: {cantidad}")

    # 3) Si está vacío, importar desde Excel
    if cantidad == 0:
        try:
            print("[STARTUP] Importando productos...")
            import_products()
            print("[STARTUP] Importación completada correctamente.")
        except Exception as e:
            print(f"[STARTUP] ERROR importando products: {e}")

    conn.close()

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
