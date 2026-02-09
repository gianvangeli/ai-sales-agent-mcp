from mcp.database import get_connection
from .excel_loader import cargar_productos_desde_excel
from .product_mapper import mapear_excel
from .product_repository import crear_tabla_productos, insertar_productos

def import_products(conn:None) -> None:
    """
    Punto de entrada del proceso de importacion de productos.
    """
    df = cargar_productos_desde_excel("products.xlsx")
    productos = mapear_excel(df)

    # Si no se pasa conexión, crear una nueva
    if conn is None:
        conn = get_connection()
        debe_cerrar = True
    else:
        debe_cerrar = False

    crear_tabla_productos(conn)
    insertar_productos(conn, productos)

    if debe_cerrar:
        conn.close()
    
    print(f" {len(productos)} Productos importados correctamente")


def main() -> None:
    """Wrapper para ejecutar desde línea de comandos"""
    import_products()
   



if __name__ =="__main__":
    main()

