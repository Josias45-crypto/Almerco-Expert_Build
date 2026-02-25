# fase1_compatibilidad/checker.py
# ============================================================
# ENTREGABLE FASE 1 - Motor de Compatibilidad
# Valida que un conjunto de piezas seleccionadas sean
# compatibles entre sí usando las matrices NumPy
# ============================================================

import sys
import os

ROOT_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE1_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(ROOT_DIR, 'database'))
sys.path.insert(0, FASE1_DIR)

from matrix_builder import MatrizCompatibilidad


# ------------------------------------------------------------
# RESULTADO DE VALIDACIÓN
# ------------------------------------------------------------

class ResultadoValidacion:
    """
    Contiene el resultado completo de validar un build de PC.
    """
    def __init__(self):
        self.es_valido   = True
        self.errores     = []
        self.advertencias = []
        self.resumen     = {}

    def agregar_error(self, mensaje: str):
        self.es_valido = False
        self.errores.append(f"❌ {mensaje}")

    def agregar_advertencia(self, mensaje: str):
        self.advertencias.append(f"⚠️  {mensaje}")

    def imprimir(self):
        print("\n" + "="*55)
        print("       RESULTADO DE COMPATIBILIDAD - ALMERCO")
        print("="*55)

        # Piezas del build
        print("\n📦 Build seleccionado:")
        for pieza, valor in self.resumen.items():
            print(f"   {pieza}: {valor}")

        # Errores
        if self.errores:
            print("\n🔴 Errores de incompatibilidad:")
            for e in self.errores:
                print(f"   {e}")

        # Advertencias
        if self.advertencias:
            print("\n🟡 Advertencias:")
            for a in self.advertencias:
                print(f"   {a}")

        # Veredicto final
        print("\n" + "-"*55)
        if self.es_valido:
            print("✅ BUILD COMPATIBLE — ¡Todas las piezas encajan!")
        else:
            print("❌ BUILD INCOMPATIBLE — Revisa los errores.")
        print("="*55 + "\n")


# ------------------------------------------------------------
# CHECKER PRINCIPAL
# ------------------------------------------------------------

class CompatibilityChecker:
    """
    Valida la compatibilidad de un build completo de PC.

    Uso:
        checker = CompatibilityChecker()
        resultado = checker.validar(
            cpu_id        = 1,
            motherboard_id= 7,
            gpu_id        = 13,
            gabinete_id   = 18,
        )
        resultado.imprimir()
    """

    def __init__(self):
        # Construir las matrices al iniciar (se cachean en memoria)
        self.matriz = MatrizCompatibilidad().construir()

    def _buscar_por_id(self, lista, producto_id):
        """Busca un producto en una lista por su ID."""
        for item in lista:
            if item.id == producto_id:
                return item
        return None

    def validar(
        self,
        cpu_id:         int,
        motherboard_id: int,
        gpu_id:         int,
        gabinete_id:    int,
    ) -> ResultadoValidacion:

        resultado = ResultadoValidacion()

        # --------------------------------------------------
        # Buscar las piezas seleccionadas
        # --------------------------------------------------
        cpu      = self._buscar_por_id(self.matriz.cpus,         cpu_id)
        mb       = self._buscar_por_id(self.matriz.motherboards,  motherboard_id)
        gpu      = self._buscar_por_id(self.matriz.gpus,          gpu_id)
        gabinete = self._buscar_por_id(self.matriz.gabinetes,     gabinete_id)

        # Verificar que todos existen
        if not cpu:
            resultado.agregar_error(f"CPU con id={cpu_id} no encontrada en el catálogo.")
        if not mb:
            resultado.agregar_error(f"Motherboard con id={motherboard_id} no encontrada.")
        if not gpu:
            resultado.agregar_error(f"GPU con id={gpu_id} no encontrada.")
        if not gabinete:
            resultado.agregar_error(f"Gabinete con id={gabinete_id} no encontrado.")

        if not resultado.es_valido:
            return resultado

        # --------------------------------------------------
        # Guardar resumen del build
        # --------------------------------------------------
        resultado.resumen = {
            "CPU"       : str(cpu),
            "Motherboard": str(mb),
            "GPU"       : str(gpu),
            "Gabinete"  : str(gabinete),
        }

        # --------------------------------------------------
        # VALIDACIÓN 1: CPU ↔ Motherboard (socket)
        # --------------------------------------------------
        if not self.matriz.es_compatible_cpu_mb(cpu_id, motherboard_id):
            resultado.agregar_error(
                f"Socket incompatible: {cpu.marca} {cpu.modelo} usa {cpu.socket} "
                f"pero {mb.marca} {mb.modelo} requiere {mb.socket}."
            )

        # --------------------------------------------------
        # VALIDACIÓN 2: GPU ↔ Gabinete (dimensiones físicas)
        # --------------------------------------------------
        if not self.matriz.es_compatible_gpu_gab(gpu_id, gabinete_id):
            resultado.agregar_error(
                f"GPU no entra en el gabinete: {gpu.marca} {gpu.modelo} mide "
                f"{gpu.largo_mm}mm pero {gabinete.marca} {gabinete.modelo} "
                f"soporta máximo {gabinete.max_gpu_largo_mm}mm."
            )
        else:
            espacio = gabinete.max_gpu_largo_mm - gpu.largo_mm
            if espacio < 20:
                resultado.agregar_advertencia(
                    f"Espacio muy justo: solo {espacio}mm libres entre GPU y gabinete."
                )

        return resultado


# ------------------------------------------------------------
# DEMO — Casos de prueba
# ------------------------------------------------------------

if __name__ == "__main__":

    checker = CompatibilityChecker()

    print("\n🧪 CASO 1: Build compatible (Intel i9 + Z790 + RTX 4090 + Lian Li)")
    resultado = checker.validar(
        cpu_id         = 1,   # Intel i9-14900K  (LGA1700)
        motherboard_id = 7,   # ASUS ROG Z790    (LGA1700)
        gpu_id         = 13,  # RTX 4090         (336mm)
        gabinete_id    = 18,  # Lian Li O11      (max 420mm)
    )
    resultado.imprimir()

    print("\n🧪 CASO 2: Build incompatible (AMD CPU + Intel Motherboard)")
    resultado = checker.validar(
        cpu_id         = 4,   # AMD Ryzen 9 7950X (AM5)
        motherboard_id = 7,   # ASUS ROG Z790     (LGA1700) ← incompatible
        gpu_id         = 13,  # RTX 4090
        gabinete_id    = 18,  # Lian Li O11
    )
    resultado.imprimir()

    print("\n🧪 CASO 3: GPU no entra en el gabinete")
    resultado = checker.validar(
        cpu_id         = 1,   # Intel i9-14900K
        motherboard_id = 7,   # ASUS ROG Z790
        gpu_id         = 13,  # RTX 4090 (336mm)
        gabinete_id    = 21,  # Cooler Master Q300L (max 360mm) ← justo
    )
    resultado.imprimir()