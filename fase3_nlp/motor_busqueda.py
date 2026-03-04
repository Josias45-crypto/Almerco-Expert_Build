# fase3_nlp/motor_busqueda.py
# ============================================================
# ENTREGABLE FASE 3 — Motor de Búsqueda Semántica
# Une preprocesador + extractor + buscador en un solo módulo
# ============================================================

import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "fase3_nlp"))

from buscador import Buscador
from extractor import Extractor


# ------------------------------------------------------------
# CLASE PRINCIPAL
# ------------------------------------------------------------

class MotorBusqueda:
    """
    Entregable Fase 3 — Motor de Búsqueda Semántica Almerco.

    Uso:
        motor = MotorBusqueda()
        resultado = motor.buscar("Busco una PC para renderizar 4K")
        motor.imprimir(resultado)
    """

    def __init__(self):
        print("🚀 Iniciando Motor de Búsqueda Semántica Almerco...\n")
        self.buscador  = Buscador()
        self.historial = []   # Guarda las últimas búsquedas de la sesión

    def buscar(self, consulta: str) -> dict:
        """
        Procesa una consulta en lenguaje natural y retorna
        productos recomendados del catálogo.
        """
        if not consulta or not consulta.strip():
            return {"error": "La consulta no puede estar vacía."}

        resultado = self.buscador.buscar(consulta)
        self.historial.append(consulta)
        return resultado

    def imprimir(self, resultado: dict):
        """Muestra el resultado de búsqueda formateado."""
        if "error" in resultado:
            print(f"❌ Error: {resultado['error']}")
            return
        self.buscador.imprimir_resultados(resultado)

    def buscar_e_imprimir(self, consulta: str):
        """Atajo: busca e imprime en una sola llamada."""
        resultado = self.buscar(consulta)
        self.imprimir(resultado)

    def mostrar_historial(self):
        """Muestra las búsquedas realizadas en la sesión."""
        if not self.historial:
            print("📭 No hay búsquedas en el historial.")
            return
        print("\n📋 Historial de búsquedas:")
        for i, consulta in enumerate(self.historial, 1):
            print(f"   {i}. {consulta}")
        print()


# ------------------------------------------------------------
# MODO INTERACTIVO
# ------------------------------------------------------------

def modo_interactivo():
    """
    Permite al usuario escribir consultas en tiempo real
    como si fuera el buscador del e-commerce de Almerco.
    """
    motor = MotorBusqueda()

    print("="*60)
    print("   ALMERCO EXPERT-BUILD — Buscador Inteligente")
    print("   Escribe 'salir' para terminar")
    print("   Escribe 'historial' para ver búsquedas anteriores")
    print("="*60 + "\n")

    while True:
        try:
            consulta = input("🔍 ¿Qué PC estás buscando? → ").strip()

            if not consulta:
                continue
            elif consulta.lower() == "salir":
                print("\n👋 ¡Hasta luego!")
                break
            elif consulta.lower() == "historial":
                motor.mostrar_historial()
            else:
                motor.buscar_e_imprimir(consulta)

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    import sys

    # Si se pasa argumento --interactivo, modo interactivo
    if "--interactivo" in sys.argv:
        modo_interactivo()
    else:
        # Demo automático
        motor = MotorBusqueda()

        casos = [
            "Busco una PC potente para renderizar video 4K",
            "Quiero una computadora barata para la oficina",
            "Necesito un equipo para gaming y streaming",
            "PC para diseño gráfico y edición de fotos profesional",
            "Computadora para programar y desarrollar aplicaciones",
        ]

        for caso in casos:
            motor.buscar_e_imprimir(caso)

        motor.mostrar_historial()