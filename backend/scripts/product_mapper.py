import pandas as pd

def mapear_excel(df: pd.DataFrame) -> list[dict] :
    """
    Transforma el DataFrame del Excel en una lista de productos
    con el formato interno del sistema.
    
    Args:
        df(pd.DataFrame): DataFrame con columnas normalizados
    Returns:
        list[dict] : Lista de productos mapeados
    """

    productos: list[dict] = []

    for _, fila in df.iterrows():
        producto = {
            "id" : str(fila["ID"]).zfill(3),
            "nombre": fila["TIPO_PRENDA"],
            "descripcion": fila["DESCRIPCION"],
            "categoria": fila["CATEGORIA"],
            "color": fila["COLOR"],
            "talle": fila["TALLA"],
            "precio_unitario": float(fila["PRECIO_50_U"]),
            "stock": int(fila["CANTIDAD_DISPONIBLE"]),
            "disponible": str(fila["DISPONIBLE"]).strip().upper() == "SI"
        }

        productos.append(producto)

    return productos
    

    

    