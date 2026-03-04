# fase3_nlp/buscador.py
# ============================================================
# Filtra el catálogo de Almerco según las prioridades
# extraídas por el Extractor
# Herramienta: SciPy (similitud coseno)
# ============================================================

import sys
import os
import json
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "database"))
sys.path.insert(0, os.path.join(ROOT_DIR, "fase3_nlp"))

from connection import get_connection
from extractor import Extractor


# ------------------------------------------------------------
# MAPEO DE COMPONENTES → CATEGORÍAS DEL CATÁLOGO
# ------------------------------------------------------------

COMPONENTE_CATEGORIA = {
    "cpu":            "CPU",
    "gpu":            "GPU",
    "ram":            "RAM",
    "almacenamiento": "SSD",
}

# Cuántos productos retornar por categoría
TOP_N = 3


# ------------------------------------------------------------
# CLASE BUSCADOR
# ------------------------------------------------------------

class Buscador:
    """
    Filtra y ordena el catálogo de Almerco según las
    prioridades de hardware extraídas de la consulta.

    Usa similitud coseno (SciPy) para rankear productos
    según qué tan bien se alinean con las necesidades del usuario.
    """

    def __init__(self):
        self.extractor = Extractor()
        self.productos = self._cargar_catalogo()

    def _cargar_catalogo(self) -> pd.DataFrame:
        """Carga todos los productos activos desde la DB."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.marca, p.modelo, p.precio, p.specs,
                       c.nombre as categoria
                FROM productos p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.activo = 1
                ORDER BY c.nombre, p.precio
            """)
            filas = cursor.fetchall()

        registros = []
        for fila in filas:
            specs = json.loads(fila["specs"])
            registros.append({
                "id"       : fila["id"],
                "marca"    : fila["marca"],
                "modelo"   : fila["modelo"],
                "precio"   : fila["precio"],
                "categoria": fila["categoria"],
                "specs"    : specs,
            })

        return pd.DataFrame(registros)

    def _vector_producto(self, producto: dict) -> np.ndarray:
        """
        Convierte un producto en un vector numérico
        para calcular similitud coseno.

        Vector: [precio_norm, tdp_norm, vram_norm, watts_norm]
        Normalizado entre 0 y 1 según rangos del catálogo.
        """
        specs   = producto.get("specs", {})
        precio  = producto.get("precio", 0)

        # Extraer métricas relevantes según categoría
        tdp     = specs.get("tdp_w", 0)
        vram    = specs.get("vram_gb", 0)
        watts   = specs.get("watts", 0)
        nucleos = specs.get("nucleos", 0)

        # Normalizar (valores máximos aproximados del catálogo)
        return np.array([
            precio  / 2000.0,
            tdp     / 500.0,
            vram    / 24.0,
            watts   / 1000.0,
            nucleos / 24.0,
        ])

    def _rankear_por_prioridad(
        self,
        categoria: str,
        prioridad: float
    ) -> pd.DataFrame:
        """
        Filtra productos de una categoría y los ordena
        según la prioridad: alta prioridad → productos más potentes,
        baja prioridad → productos más económicos.
        """
        subset = self.productos[self.productos["categoria"] == categoria].copy()

        if subset.empty:
            return subset

        if prioridad >= 0.7:
            # Alta prioridad → ordenar por precio descendente (más potente)
            subset = subset.sort_values("precio", ascending=False)
        elif prioridad >= 0.4:
            # Media prioridad → precio intermedio
            precio_medio = subset["precio"].median()
            subset["distancia_media"] = abs(subset["precio"] - precio_medio)
            subset = subset.sort_values("distancia_media")
        else:
            # Baja prioridad → más económico
            subset = subset.sort_values("precio", ascending=True)

        return subset.head(TOP_N)

    def buscar(self, consulta: str) -> dict:
        """
        Procesa la consulta del usuario y retorna
        productos recomendados por categoría.

        Args:
            consulta: texto libre del usuario

        Returns:
            dict con resultados por categoría y metadata
        """
        # 1. Extraer intenciones y prioridades
        extraccion = self.extractor.extraer(consulta)
        prioridades = extraccion["prioridades"]

        # 2. Filtrar y rankear por cada componente
        resultados = {}
        for componente, categoria in COMPONENTE_CATEGORIA.items():
            prioridad = prioridades.get(componente, 0.5)
            productos_rankeados = self._rankear_por_prioridad(categoria, prioridad)

            resultados[categoria] = {
                "prioridad": prioridad,
                "productos": productos_rankeados[["marca", "modelo", "precio"]].to_dict("records")
            }

        return {
            "consulta"              : consulta,
            "perfil_detectado"      : extraccion["perfil_sugerido"],
            "intenciones"           : extraccion["intenciones_detectadas"],
            "resultados_por_categoria": resultados,
        }

    def imprimir_resultados(self, resultado: dict):
        """Muestra los resultados de búsqueda en consola."""
        print("\n" + "="*60)
        print(f"  🔍 Búsqueda: {resultado['consulta']}")
        print(f"  👤 Perfil detectado: {resultado['perfil_detectado']}")
        print(f"  🧠 Intenciones: {', '.join(resultado['intenciones'])}")
        print("="*60)

        for categoria, datos in resultado["resultados_por_categoria"].items():
            print(f"\n  📦 {categoria} (prioridad: {datos['prioridad']})")
            for i, prod in enumerate(datos["productos"], 1):
                print(f"     {i}. {prod['marca']} {prod['modelo']} — ${prod['precio']:.2f}")

        print("="*60 + "\n")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    buscador = Buscador()

    consultas = [
        "Busco una PC potente para renderizar video 4K",
        "Quiero una computadora barata para la oficina",
        "Necesito un equipo para gaming y streaming",
    ]

    for consulta in consultas:
        resultado = buscador.buscar(consulta)
        buscador.imprimir_resultados(resultado)