# fase4_recomendador/dataset.py
# ============================================================
# Prepara datos de entrenamiento para el modelo PyTorch
# Simula historial de compras: qué productos se compran juntos
# ============================================================

import sys
import os
import json
import numpy as np
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "database"))

from connection import get_connection


PATRONES = {
    "Gamer": {
        "CPU":           [2, 3],
        "Motherboard":   [7, 8],
        "GPU":           [13, 14, 16],
        "RAM":           [29, 30],
        "Gabinete":      [18, 19, 20],
        "Fuente":        [22, 23],
        "Refrigeracion": [27, 28],
    },
    "Disenador": {
        "CPU":           [1, 4],
        "Motherboard":   [7, 10],
        "GPU":           [13, 16],
        "RAM":           [29, 30],
        "Gabinete":      [18, 20],
        "Fuente":        [22, 23],
        "Refrigeracion": [27, 28],
    },
    "Oficina": {
        "CPU":           [5, 6],
        "Motherboard":   [9, 12],
        "GPU":           [15, 17],
        "RAM":           [30, 31],
        "Gabinete":      [21],
        "Fuente":        [24, 25],
        "Refrigeracion": [28],
    },
}

CATEGORIAS_ORDER = [
    "CPU", "Motherboard", "GPU", "RAM",
    "Gabinete", "Fuente", "Refrigeracion"
]


class DatasetRecomendador:
    """
    Genera pares de entrenamiento (producto_entrada, producto_recomendado)
    basados en patrones de compra simulados.
    """

    def __init__(self):
        self.productos   = self._cargar_productos()
        self.n_productos = len(self.productos)
        self.id_a_idx    = {p["id"]: i for i, p in enumerate(self.productos)}
        self.idx_a_id    = {i: p["id"] for i, p in enumerate(self.productos)}

    def _cargar_productos(self) -> list:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.marca, p.modelo, p.precio, p.specs,
                       c.nombre as categoria
                FROM productos p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.activo = 1
                ORDER BY p.id
            """)
            filas = cursor.fetchall()

        return [{
            "id"       : f["id"],
            "marca"    : f["marca"],
            "modelo"   : f["modelo"],
            "precio"   : f["precio"],
            "categoria": f["categoria"],
            "specs"    : json.loads(f["specs"]),
        } for f in filas]

    def generar_pares(self, n_muestras: int = 1000) -> pd.DataFrame:
        """Genera pares (producto_entrada, producto_recomendado)."""
        np.random.seed(42)
        pares = []
        perfiles = list(PATRONES.keys())

        for _ in range(n_muestras):
            perfil      = np.random.choice(perfiles)
            patron      = PATRONES[perfil]
            cat_entrada = np.random.choice(CATEGORIAS_ORDER[:-2])
            ids_entrada = patron.get(cat_entrada, [])

            if not ids_entrada:
                continue

            prod_entrada_id = int(np.random.choice(ids_entrada))

            for cat_rec in CATEGORIAS_ORDER:
                if cat_rec == cat_entrada:
                    continue
                ids_rec = patron.get(cat_rec, [])
                if not ids_rec:
                    continue
                prod_rec_id = int(np.random.choice(ids_rec))
                pares.append({
                    "perfil"           : perfil,
                    "producto_entrada" : prod_entrada_id,
                    "categoria_entrada": cat_entrada,
                    "producto_rec"     : prod_rec_id,
                    "categoria_rec"    : cat_rec,
                })

        return pd.DataFrame(pares).drop_duplicates()

    def preparar_tensores(self, df: pd.DataFrame):
        """Convierte pares en tensores PyTorch one-hot."""
        import torch

        X_list, y_list = [], []

        for _, fila in df.iterrows():
            idx_entrada = self.id_a_idx.get(fila["producto_entrada"])
            idx_rec     = self.id_a_idx.get(fila["producto_rec"])

            if idx_entrada is None or idx_rec is None:
                continue

            x = np.zeros(self.n_productos)
            y = np.zeros(self.n_productos)
            x[idx_entrada] = 1.0
            y[idx_rec]     = 1.0

            X_list.append(x)
            y_list.append(y)

        X = torch.FloatTensor(np.array(X_list))
        y = torch.FloatTensor(np.array(y_list))
        return X, y


if __name__ == "__main__":
    print("\n🚀 Generando dataset de entrenamiento...\n")

    dataset = DatasetRecomendador()
    print(f"  ✅ Productos en catálogo: {dataset.n_productos}")

    df = dataset.generar_pares(n_muestras=500)
    print(f"  ✅ Pares generados: {len(df)}")
    print(f"  ✅ Distribución por perfil:")
    print(df["perfil"].value_counts().to_string())

    X, y = dataset.preparar_tensores(df)
    print(f"\n  ✅ Tensor X: {X.shape}")
    print(f"  ✅ Tensor y: {y.shape}")
    print("\n✅ Dataset listo.\n")