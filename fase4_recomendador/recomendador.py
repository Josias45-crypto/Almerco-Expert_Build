# fase4_recomendador/recomendador.py
# ============================================================
# ENTREGABLE FASE 4 — Recomendador "Next Best Offer"
# Une reglas obligatorias + modelo Deep Learning
# ============================================================

import sys
import os

ROOT_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE4_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, FASE4_DIR)

from reglas_obligatorias import MotorReglas
from modelo import EntrenadorModelo


class RecomendadorNBO:
    """
    Entregable Fase 4 — Next Best Offer Almerco.
    Combina reglas obligatorias + modelo Deep Learning.
    """

    def __init__(self):
        print("🚀 Iniciando Recomendador NBO Almerco...\n")

        self.motor_reglas = MotorReglas()
        self.entrenador   = EntrenadorModelo(n_epochs=50)
        ruta_modelo       = os.path.join(FASE4_DIR, "modelo_entrenado.pt")

        if os.path.exists(ruta_modelo):
            self.entrenador.cargar(ruta_modelo)
        else:
            self.entrenador.entrenar()
            self.entrenador.guardar(ruta_modelo)

        print("\n✅ Recomendador listo.\n")

    def recomendar(self, producto_id: int) -> dict:
        resultado_reglas = self.motor_reglas.aplicar(producto_id)

        if "error" in resultado_reglas:
            return resultado_reglas

        try:
            sugeridos = self.entrenador.predecir(producto_id, top_n=5)
        except Exception:
            sugeridos = []

        categorias_obligatorias = {
            rec["categoria"]
            for rec in resultado_reglas["recomendaciones"]
        }

        sugeridos_filtrados = [
            s for s in sugeridos
            if s["categoria"] not in categorias_obligatorias
        ]

        return {
            "producto_seleccionado": resultado_reglas["producto_seleccionado"],
            "obligatorios"         : resultado_reglas["recomendaciones"],
            "mensajes"             : resultado_reglas["mensajes"],
            "sugeridos"            : sugeridos_filtrados,
        }

    def imprimir(self, resultado: dict):
        if "error" in resultado:
            print(f"❌ {resultado['error']}")
            return

        prod = resultado["producto_seleccionado"]
        print(f"\n{'='*60}")
        print(f"  🖥️  Seleccionaste: {prod['marca']} {prod['modelo']}")
        print(f"  💰 Precio: ${prod['precio']:.2f}")
        print(f"{'='*60}")

        if resultado["obligatorios"]:
            print("\n  🔴 RECOMENDACIONES OBLIGATORIAS:")
            for msg in resultado["mensajes"]:
                print(f"  {msg}")
            for rec in resultado["obligatorios"]:
                print(f"\n  📦 {rec['categoria']}:")
                for p in rec["productos"]:
                    print(f"     → {p['marca']} {p['modelo']} — ${p['precio']:.2f}")

        if resultado["sugeridos"]:
            print("\n  🟡 TAMBIÉN TE PODRÍA INTERESAR:")
            for s in resultado["sugeridos"]:
                print(f"     → [{s['categoria']}] {s['marca']} {s['modelo']} — ${s['precio']:.2f}")

        print(f"\n{'='*60}\n")

    def recomendar_e_imprimir(self, producto_id: int):
        self.imprimir(self.recomendar(producto_id))


if __name__ == "__main__":
    recomendador = RecomendadorNBO()

    print("🧪 CASO 1: Intel Core i9-14900K")
    recomendador.recomendar_e_imprimir(1)

    print("🧪 CASO 2: NVIDIA RTX 4090")
    recomendador.recomendar_e_imprimir(13)

    print("🧪 CASO 3: AMD Ryzen 5 7600X (gama baja)")
    recomendador.recomendar_e_imprimir(6)