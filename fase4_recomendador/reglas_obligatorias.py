# fase4_recomendador/reglas_obligatorias.py
# ============================================================
# Reglas fijas de recomendación obligatoria
# Ej: i9-14900K → refrigeración 360mm + fuente 850W+
# ============================================================

import sys
import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "database"))

from connection import get_connection


# ------------------------------------------------------------
# REGLAS OBLIGATORIAS
# formato: condición → lista de recomendaciones obligatorias
# ------------------------------------------------------------

REGLAS = [
    {
        "nombre"    : "CPU de alto TDP requiere refrigeración líquida 360mm",
        "condicion" : lambda producto, specs: (
            producto["categoria"] == "CPU" and
            specs.get("tdp_w", 0) >= 125
        ),
        "recomendar": {
            "categoria" : "Refrigeracion",
            "filtro"    : lambda specs: specs.get("tipo") == "liquida" and
                                        specs.get("radiador_mm", 0) >= 360,
            "mensaje"   : "⚠️  CPU de alto rendimiento: se recomienda refrigeración líquida 360mm obligatoriamente.",
        }
    },
    {
        "nombre"    : "CPU + GPU de alto TDP requiere fuente 850W+",
        "condicion" : lambda producto, specs: (
            producto["categoria"] == "CPU" and
            specs.get("tdp_w", 0) >= 125
        ),
        "recomendar": {
            "categoria" : "Fuente",
            "filtro"    : lambda specs: specs.get("watts", 0) >= 850,
            "mensaje"   : "⚠️  CPU de alto rendimiento: se requiere fuente de poder de 850W o más.",
        }
    },
    {
        "nombre"    : "GPU de alto consumo requiere fuente 850W+",
        "condicion" : lambda producto, specs: (
            producto["categoria"] == "GPU" and
            specs.get("tdp_w", 0) >= 300
        ),
        "recomendar": {
            "categoria" : "Fuente",
            "filtro"    : lambda specs: specs.get("watts", 0) >= 850,
            "mensaje"   : "⚠️  GPU de alto consumo: se requiere fuente de poder de 850W o más.",
        }
    },
    {
        "nombre"    : "GPU grande requiere gabinete compatible",
        "condicion" : lambda producto, specs: (
            producto["categoria"] == "GPU" and
            specs.get("largo_mm", 0) >= 300
        ),
        "recomendar": {
            "categoria" : "Gabinete",
            "filtro"    : lambda specs: specs.get("max_gpu_largo_mm", 0) >= 380,
            "mensaje"   : "⚠️  GPU de gran tamaño: verifica que el gabinete soporte más de 380mm.",
        }
    },
]


# ------------------------------------------------------------
# MOTOR DE REGLAS
# ------------------------------------------------------------

class MotorReglas:
    """
    Aplica reglas obligatorias sobre el producto seleccionado
    y retorna los productos que DEBEN acompañarlo.
    """

    def __init__(self):
        self.productos = self._cargar_productos()

    def _cargar_productos(self) -> list:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.marca, p.modelo, p.precio, p.specs,
                       c.nombre as categoria
                FROM productos p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.activo = 1
            """)
            filas = cursor.fetchall()

        resultado = []
        for fila in filas:
            resultado.append({
                "id"       : fila["id"],
                "marca"    : fila["marca"],
                "modelo"   : fila["modelo"],
                "precio"   : fila["precio"],
                "categoria": fila["categoria"],
                "specs"    : json.loads(fila["specs"]),
            })
        return resultado

    def aplicar(self, producto_id: int) -> dict:
        """
        Dado el ID de un producto seleccionado,
        aplica todas las reglas y retorna recomendaciones obligatorias.
        """
        # Buscar el producto seleccionado
        producto = next((p for p in self.productos if p["id"] == producto_id), None)
        if not producto:
            return {"error": f"Producto id={producto_id} no encontrado."}

        specs = producto["specs"]
        recomendaciones = []
        mensajes        = []

        for regla in REGLAS:
            if regla["condicion"](producto, specs):
                filtro    = regla["recomendar"]["filtro"]
                categoria = regla["recomendar"]["categoria"]
                mensaje   = regla["recomendar"]["mensaje"]

                # Buscar productos que cumplan el filtro
                candidatos = [
                    p for p in self.productos
                    if p["categoria"] == categoria and filtro(p["specs"])
                ]

                if candidatos:
                    # Ordenar por precio descendente (más potente primero)
                    candidatos.sort(key=lambda x: x["precio"], reverse=True)
                    recomendaciones.append({
                        "categoria"  : categoria,
                        "productos"  : candidatos[:3],
                        "obligatorio": True,
                    })
                    mensajes.append(mensaje)

        return {
            "producto_seleccionado": producto,
            "recomendaciones"      : recomendaciones,
            "mensajes"             : mensajes,
            "tiene_obligatorios"   : len(recomendaciones) > 0,
        }

    def imprimir(self, resultado: dict):
        if "error" in resultado:
            print(f"❌ {resultado['error']}")
            return

        prod = resultado["producto_seleccionado"]
        print(f"\n{'='*60}")
        print(f"  🖥️  Producto: {prod['marca']} {prod['modelo']}")
        print(f"  💰 Precio: ${prod['precio']:.2f}")
        print(f"{'='*60}")

        if not resultado["tiene_obligatorios"]:
            print("  ✅ No hay recomendaciones obligatorias para este producto.")
            return

        for msg in resultado["mensajes"]:
            print(f"\n  {msg}")

        for rec in resultado["recomendaciones"]:
            print(f"\n  📦 {rec['categoria']} — OBLIGATORIO:")
            for p in rec["productos"]:
                print(f"     → {p['marca']} {p['modelo']} — ${p['precio']:.2f}")

        print(f"{'='*60}\n")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    motor = MotorReglas()

    print("\n🧪 Probando reglas obligatorias...\n")

    # i9-14900K
    print("CASO 1: Intel Core i9-14900K")
    motor.imprimir(motor.aplicar(1))

    # RTX 4090
    print("CASO 2: NVIDIA RTX 4090")
    motor.imprimir(motor.aplicar(13))

    # Ryzen 5 (bajo TDP - no debe tener obligatorios)
    print("CASO 3: AMD Ryzen 5 7600X (bajo TDP)")
    motor.imprimir(motor.aplicar(6))