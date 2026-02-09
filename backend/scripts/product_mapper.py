import pandas as pd

def normalizar_columna_nombre(col: str) -> str:
    """
    Normaliza el nombre de la columna:
    - Pasa a mayúsculas
    - Quita acentos
    - Reemplaza espacios por guion bajo
    """
    import unicodedata
    col = col.strip()
    col = unicodedata.normalize("NFKD", col).encode("ASCII", "ignore").decode("ASCII")
    col = col.replace(" ", "_").upper()
    return col

def mapear_excel(df: pd.DataFrame) -> list[dict]:
    """
    Transforma el DataFrame del Excel al formato interno del sistema,
    normalizando las columnas.
    """

    # Normalizar columnas
    df = df.rename(columns={col: normalizar_columna_nombre(col) for col in df.columns})

    productos = []

    for _, fila in df.iterrows():
        producto = {
            "id": str(fila["ID"]),
            "nombre": fila.get("TIPO_PRENDA", ""),
            "descripcion": fila.get("DESCRIPCION", ""),
            "categoria": fila.get("CATEGORIA", ""),
            "color": fila.get("COLOR", ""),
            "talle": fila.get("TALLA", ""),
            "precio": float(fila.get("PRECIO_50_U", 0)),
            "stock": int(fila.get("CANTIDAD_DISPONIBLE", 0)),
            "disponible": str(fila.get("DISPONIBLE", "")).lower() in ["si", "yes", "true", "1"]
        }
        productos.append(producto)

    return productos
