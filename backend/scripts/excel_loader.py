from pathlib import Path
import pandas as pd

def cargar_productos_desde_excel(nombre_archivo: str) -> pd.DataFrame:
    """
    Carga el Excel de productos usando una ruta absoluta
    basada en la carpeta donde está este script.
    """

    # La carpeta base es el padre de scripts, es decir: backend/
    ruta_base = Path(__file__).resolve().parents[2]  # backend/
    ruta_excel = ruta_base / nombre_archivo

    print(f"[EXCEL] Intentando cargar Excel en: {ruta_excel}")

    if not ruta_excel.exists():
        raise FileNotFoundError(f"Excel de productos no encontrado en: {ruta_excel}")

    df = pd.read_excel(ruta_excel, engine="openpyxl")

    print(f"[EXCEL] Excel cargado con éxito: filas={df.shape[0]}, columnas={df.shape[1]}")

    return df
