# fase2_segmentacion/data_builder.py
# ============================================================
# Genera datos simulados de comportamiento de clientes
# Simula navegación y búsquedas en el e-commerce de Almerco
# ============================================================

import sys
import os
import numpy as np
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, 'database'))

from connection import get_connection

# ------------------------------------------------------------
# CONFIGURACIÓN DE PERFILES
# Cada perfil tiene un patrón de comportamiento distinto
# Esto simula cómo navega cada tipo de cliente en la tienda
# ------------------------------------------------------------

PERFILES_CONFIG = {
    "Gamer": {
        "peso_gpu":           (0.85, 0.10),   # (media, desviación estándar)
        "peso_cpu":           (0.70, 0.10),
        "peso_ram":           (0.60, 0.10),
        "peso_refrigeracion": (0.65, 0.10),
        "peso_fuente":        (0.70, 0.10),
        "rango_precio":       (800,  400),     # (media precio total, desviación)
        "n_clientes":         120,
    },
    "Disenador": {
        "peso_gpu":           (0.75, 0.10),
        "peso_cpu":           (0.85, 0.10),   # priorizan CPU para renderizado
        "peso_ram":           (0.90, 0.08),   # mucha RAM para edición
        "peso_refrigeracion": (0.70, 0.10),
        "peso_fuente":        (0.65, 0.10),
        "rango_precio":       (1200, 500),
        "n_clientes":         80,
    },
    "Oficina": {
        "peso_gpu":           (0.20, 0.10),   # poca GPU, usan integrada
        "peso_cpu":           (0.45, 0.10),
        "peso_ram":           (0.40, 0.10),
        "peso_refrigeracion": (0.25, 0.10),
        "peso_fuente":        (0.35, 0.10),
        "rango_precio":       (350,  150),
        "n_clientes":         150,
    },
}

# ------------------------------------------------------------
# CATEGORÍAS QUE USAMOS COMO FEATURES
# ------------------------------------------------------------
FEATURES = ["peso_gpu", "peso_cpu", "peso_ram", "peso_refrigeracion", "peso_fuente"]
FEATURE_NOMBRES = ["interes_gpu", "interes_cpu", "interes_ram", "interes_refrig", "interes_fuente"]


def generar_datos_clientes() -> pd.DataFrame:
    """
    Genera un DataFrame con datos simulados de comportamiento
    de clientes navegando el catálogo de Almerco.

    Columnas:
        cliente_id      : ID único del cliente
        interes_gpu     : Nivel de interés en GPUs (0.0 - 1.0)
        interes_cpu     : Nivel de interés en CPUs (0.0 - 1.0)
        interes_ram     : Nivel de interés en RAM (0.0 - 1.0)
        interes_refrig  : Nivel de interés en refrigeración (0.0 - 1.0)
        interes_fuente  : Nivel de interés en fuentes de poder (0.0 - 1.0)
        presupuesto     : Presupuesto estimado en USD
        perfil_real     : Perfil real (solo para validación, no se usa en K-Means)
    """
    np.random.seed(42)  # Reproducibilidad
    filas = []
    cliente_id = 1

    for perfil, config in PERFILES_CONFIG.items():
        n = config["n_clientes"]

        for _ in range(n):
            fila = {"cliente_id": cliente_id, "perfil_real": perfil}

            # Generar interés por categoría con distribución normal
            for feature, nombre in zip(FEATURES, FEATURE_NOMBRES):
                media, std = config[feature]
                valor = np.random.normal(media, std)
                # Clampear entre 0 y 1
                fila[nombre] = float(np.clip(valor, 0.0, 1.0))

            # Generar presupuesto
            media_precio, std_precio = config["rango_precio"]
            presupuesto = np.random.normal(media_precio, std_precio)
            fila["presupuesto"] = float(np.clip(presupuesto, 100, 5000))

            filas.append(fila)
            cliente_id += 1

    df = pd.DataFrame(filas)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Mezclar filas

    return df


def guardar_datos_mock(df: pd.DataFrame, ruta: str = None):
    """Guarda el DataFrame como CSV en data/mock/."""
    if ruta is None:
        ruta = os.path.join(ROOT_DIR, "data", "mock", "clientes_navegacion.csv")

    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df.to_csv(ruta, index=False)
    print(f"  ✅ Datos guardados en: {ruta}")
    return ruta


def cargar_datos_mock(ruta: str = None) -> pd.DataFrame:
    """Carga el CSV de datos de clientes."""
    if ruta is None:
        ruta = os.path.join(ROOT_DIR, "data", "mock", "clientes_navegacion.csv")

    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}\nEjecuta primero: python data_builder.py")

    return pd.read_csv(ruta)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    print("\n🚀 Generando datos de comportamiento de clientes...\n")

    df = generar_datos_clientes()

    print(f"  ✅ Total clientes generados: {len(df)}")
    print(f"  ✅ Distribución de perfiles:")
    print(df["perfil_real"].value_counts().to_string())
    print(f"\n  ✅ Muestra de datos:")
    print(df.head(5).to_string())

    guardar_datos_mock(df)

    print("\n✅ data_builder completado.\n")