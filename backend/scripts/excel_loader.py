from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/

def cargar_productos_desde_excel(nombre_archivo: str) -> pd.DataFrame:
    """
    Carga el Excel de productos usando una ruta absoluta
    en producción (Render, Docker, etc).
    """

    ruta = BASE_DIR / nombre_archivo

    print(f"[EXCEL] Intentando cargar Excel en: {ruta}")

    # Verifico que exista
    if not ruta.exists():
        raise FileNotFoundError(f"Excel de productos no encontrado en: {ruta}")

    df = pd.read_excel(ruta, engine="openpyxl")

    print(f"[EXCEL] Excel cargado con éxito: filas={df.shape[0]} columnas={df.shape[1]}")

    return df
