import sqlite3
from .excel_loader import cargar_productos_desde_excel
from product_mapper import mapear_excel
from product_repository import crear_tabla_productos, insertar_productos



def main() -> None:
    """
    Punto de entrada del proceso de importacion de productos.

    """
    df = cargar_productos_desde_excel("products.xlsx")
    productos = mapear_excel(df)

    conn = sqlite3.connect("database/database.sqlite")

    crear_tabla_productos(conn)
    insertar_productos(conn, productos)

    conn.close()
    print(f" {len(productos)} Productos importados correctamente")



if __name__ =="__main__":
    main()

