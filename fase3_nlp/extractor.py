# fase3_nlp/extractor.py
# ============================================================
# Extrae entidades técnicas de la consulta del usuario
# Traduce términos de búsqueda a prioridades de hardware
# ============================================================

import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "fase3_nlp"))

from preprocesador import Preprocesador


# ------------------------------------------------------------
# DICCIONARIO DE INTENCIONES
# Mapea stems/tokens → prioridades de hardware
# Escala: 0.0 (sin prioridad) a 1.0 (máxima prioridad)
# ------------------------------------------------------------

INTENCIONES = {
    # Renderizado / Video / 3D
    "renderiz": {"cpu": 1.0, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.7},
    "render":   {"cpu": 1.0, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.7},
    "vide":     {"cpu": 0.8, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.8},
    "4k":       {"cpu": 0.9, "ram": 0.8, "gpu": 0.9, "almacenamiento": 0.7},
    "8k":       {"cpu": 1.0, "ram": 1.0, "gpu": 1.0, "almacenamiento": 0.9},
    "3d":       {"cpu": 0.9, "ram": 0.9, "gpu": 0.9, "almacenamiento": 0.7},

    # Diseño / Fotografía
    "diseñ":    {"cpu": 0.8, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},
    "grafic":   {"cpu": 0.8, "ram": 0.8, "gpu": 0.9, "almacenamiento": 0.7},
    "fot":      {"cpu": 0.7, "ram": 0.8, "gpu": 0.6, "almacenamiento": 0.9},
    "edicion":  {"cpu": 0.9, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},
    "edic":     {"cpu": 0.9, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},

    # Gaming
    "gaming":    {"cpu": 0.8, "ram": 0.7, "gpu": 1.0, "almacenamiento": 0.6},
    "gamer":     {"cpu": 0.8, "ram": 0.7, "gpu": 1.0, "almacenamiento": 0.6},
    "jueg":      {"cpu": 0.7, "ram": 0.6, "gpu": 1.0, "almacenamiento": 0.5},
    "streaming": {"cpu": 0.8, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.6},

    # Oficina / Básico
    "oficin":    {"cpu": 0.4, "ram": 0.4, "gpu": 0.1, "almacenamiento": 0.5},
    "ofimati":   {"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.4},
    "barat":     {"cpu": 0.3, "ram": 0.3, "gpu": 0.2, "almacenamiento": 0.3},
    "economic":  {"cpu": 0.3, "ram": 0.3, "gpu": 0.2, "almacenamiento": 0.3},
    "basic":     {"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.4},

    # Programación
    "program":   {"cpu": 0.8, "ram": 0.8, "gpu": 0.3, "almacenamiento": 0.7},
    "codigo":    {"cpu": 0.7, "ram": 0.7, "gpu": 0.3, "almacenamiento": 0.6},
    "desarroll": {"cpu": 0.8, "ram": 0.8, "gpu": 0.3, "almacenamiento": 0.7},

    # Potencia general
    "potent":    {"cpu": 0.9, "ram": 0.8, "gpu": 0.8, "almacenamiento": 0.6},
    "rapid":     {"cpu": 0.8, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.8},
    "alta":      {"cpu": 0.7, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.5},
}

# Perfil por defecto si no se detecta ninguna intención
PRIORIDADES_DEFAULT = {
    "cpu": 0.5, "ram": 0.5, "gpu": 0.3, "almacenamiento": 0.5
}


# ------------------------------------------------------------
# CLASE EXTRACTOR
# ------------------------------------------------------------

class Extractor:
    """
    Extrae entidades técnicas y prioridades de hardware
    a partir de los tokens procesados por el Preprocesador.
    """

    def __init__(self):
        self.preprocesador = Preprocesador()

    def extraer(self, texto: str) -> dict:
        """
        Dado un texto de búsqueda, retorna las prioridades
        de hardware detectadas.

        Returns:
            dict con:
                consulta_original : texto del usuario
                intenciones_detectadas : lista de términos clave encontrados
                prioridades : {cpu, ram, gpu, almacenamiento} (0.0 - 1.0)
                perfil_sugerido : Gamer / Disenador / Oficina
        """
        resultado_nlp = self.preprocesador.procesar(texto)
        stems         = resultado_nlp["stems"]
        tokens        = resultado_nlp["tokens_filtrados"]

        # Buscar intenciones en stems Y tokens originales
        terminos_busqueda    = set(stems + tokens)
        intenciones_detectadas = []
        prioridades_acumuladas = {
            "cpu": [], "ram": [], "gpu": [], "almacenamiento": []
        }

        for termino in terminos_busqueda:
            if termino in INTENCIONES:
                intenciones_detectadas.append(termino)
                for componente, valor in INTENCIONES[termino].items():
                    prioridades_acumuladas[componente].append(valor)

        # Calcular promedio de prioridades detectadas
        if intenciones_detectadas:
            prioridades = {
                comp: round(sum(vals) / len(vals), 3)
                for comp, vals in prioridades_acumuladas.items()
                if vals
            }
            # Rellenar componentes sin datos con default
            for comp in PRIORIDADES_DEFAULT:
                if comp not in prioridades:
                    prioridades[comp] = PRIORIDADES_DEFAULT[comp]
        else:
            prioridades = PRIORIDADES_DEFAULT.copy()

        # Determinar perfil sugerido
        perfil = self._determinar_perfil(prioridades)

        return {
            "consulta_original"     : texto,
            "intenciones_detectadas": intenciones_detectadas,
            "prioridades"           : prioridades,
            "perfil_sugerido"       : perfil,
        }

    def _determinar_perfil(self, prioridades: dict) -> str:
        """
        Determina el perfil del cliente según las prioridades extraídas.
        """
        gpu = prioridades.get("gpu", 0)
        cpu = prioridades.get("cpu", 0)
        ram = prioridades.get("ram", 0)

        if gpu >= 0.8:
            return "Gamer"
        elif cpu >= 0.8 and ram >= 0.8:
            return "Disenador"
        else:
            return "Oficina"


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    extractor = Extractor()

    consultas = [
        "Busco una PC potente para renderizar video 4K",
        "Quiero una computadora barata para la oficina",
        "Necesito un equipo para gaming y streaming",
        "PC para diseño gráfico y edición de fotos profesional",
        "Computadora para programar y desarrollar aplicaciones",
    ]

    print("\n🧠 Extracción de entidades técnicas:\n")
    for consulta in consultas:
        resultado = extractor.extraer(consulta)
        print(f"  Consulta   : {resultado['consulta_original']}")
        print(f"  Intenciones: {resultado['intenciones_detectadas']}")
        print(f"  Prioridades: {resultado['prioridades']}")
        print(f"  Perfil     : {resultado['perfil_sugerido']}")
        print()