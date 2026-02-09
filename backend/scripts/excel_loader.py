import pandas as pd
import unicodedata
from pathlib import Path

def normalizar_nombre_columna(nombre:str) -> str:
    """
    Normaliza un nombre de columna:
    -Elimina tildes
    -Convierte a mayusculas
    -Remplaza espacios por guiones
    Args:
        nombre(str)
    Returns:
        str
    """

    nombre = nombre.strip().upper().replace(" ", "_")
    nombre = unicodedata.normalize("NFKD", nombre)
    nombre = nombre.encode("ascii", "ignore").decode("ascii")

    return nombre

def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza todas las comunas del DataFrame.

    Args:
        df(pd.DataFrame): Datos crudos del Excel
    Returns:
        DataFrame con columnas normalizadas.
    """

    df = df.copy()
    df.columns = [normalizar_nombre_columna(col) for col in df.columns]
    return df

def cargar_productos_desde_excel(ruta_archivo: str | Path) -> pd.DataFrame:
    """
    Carga el archivo Excel y devuelve un DataFrame con columnas normalizadas .

    Args:
        ruta_archivo (str): Ruta del archivo Excel
    
    Returns:
        pd.DataFrama: DataFrame con columnas normalizadas
    """
    ruta = Path(ruta_archivo)
    
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontro el archivo: {ruta}")
    
    df = pd.read_excel(ruta)
    df = normalizar_columnas(df)

    return df