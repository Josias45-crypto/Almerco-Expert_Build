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
    # --------------------------------------------------------
    # RENDERIZADO / VIDEO / 3D
    # --------------------------------------------------------
    "renderiz": {"cpu": 1.0, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.7},
    "render":   {"cpu": 1.0, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.7},
    "vide":     {"cpu": 0.8, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.8},
    "4k":       {"cpu": 0.9, "ram": 0.8, "gpu": 0.9, "almacenamiento": 0.7},
    "8k":       {"cpu": 1.0, "ram": 1.0, "gpu": 1.0, "almacenamiento": 0.9},
    "3d":       {"cpu": 0.9, "ram": 0.9, "gpu": 0.9, "almacenamiento": 0.7},
    "animacion":{"cpu": 0.9, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.8},
    "animac":   {"cpu": 0.9, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.8},
    "blender":  {"cpu": 1.0, "ram": 0.9, "gpu": 0.9, "almacenamiento": 0.7},
    "after":    {"cpu": 0.9, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.8},
    "premier":  {"cpu": 0.9, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.9},
    "davinci":  {"cpu": 0.9, "ram": 0.9, "gpu": 0.9, "almacenamiento": 0.9},

    # --------------------------------------------------------
    # DISEÑO / FOTOGRAFÍA / CREATIVIDAD
    # --------------------------------------------------------
    "diseñ":    {"cpu": 0.8, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},
    "grafic":   {"cpu": 0.8, "ram": 0.8, "gpu": 0.9, "almacenamiento": 0.7},
    "fot":      {"cpu": 0.7, "ram": 0.8, "gpu": 0.6, "almacenamiento": 0.9},
    "edicion":  {"cpu": 0.9, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},
    "edic":     {"cpu": 0.9, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},
    "edit":     {"cpu": 0.9, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},
    "photoshop":{"cpu": 0.8, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},
    "illustrat":{"cpu": 0.7, "ram": 0.8, "gpu": 0.6, "almacenamiento": 0.7},
    "creativ":  {"cpu": 0.8, "ram": 0.8, "gpu": 0.7, "almacenamiento": 0.7},
    "ilustrac": {"cpu": 0.7, "ram": 0.8, "gpu": 0.7, "almacenamiento": 0.7},
    "arqu":     {"cpu": 0.9, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.8},
    "autocad":  {"cpu": 0.9, "ram": 0.8, "gpu": 0.8, "almacenamiento": 0.7},

    # --------------------------------------------------------
    # GAMING / JUEGOS
    # --------------------------------------------------------
    "gaming":   {"cpu": 0.8, "ram": 0.7, "gpu": 1.0, "almacenamiento": 0.6},
    "gamer":    {"cpu": 0.8, "ram": 0.7, "gpu": 1.0, "almacenamiento": 0.6},
    "jueg":     {"cpu": 0.7, "ram": 0.6, "gpu": 1.0, "almacenamiento": 0.5},
    "jugar":    {"cpu": 0.7, "ram": 0.6, "gpu": 1.0, "almacenamiento": 0.5},
    "jug":      {"cpu": 0.7, "ram": 0.6, "gpu": 1.0, "almacenamiento": 0.5},
    "videojueg":{"cpu": 0.7, "ram": 0.6, "gpu": 1.0, "almacenamiento": 0.6},
    "fps":      {"cpu": 0.8, "ram": 0.7, "gpu": 1.0, "almacenamiento": 0.5},
    "esport":   {"cpu": 0.8, "ram": 0.7, "gpu": 1.0, "almacenamiento": 0.5},
    "fortnit":  {"cpu": 0.7, "ram": 0.6, "gpu": 0.9, "almacenamiento": 0.5},
    "minecraft":{"cpu": 0.6, "ram": 0.6, "gpu": 0.7, "almacenamiento": 0.5},
    "roblox":   {"cpu": 0.5, "ram": 0.5, "gpu": 0.6, "almacenamiento": 0.4},
    "roblo":    {"cpu": 0.5, "ram": 0.5, "gpu": 0.6, "almacenamiento": 0.4},
    "warzon":   {"cpu": 0.8, "ram": 0.7, "gpu": 1.0, "almacenamiento": 0.6},
    "valorant": {"cpu": 0.7, "ram": 0.6, "gpu": 0.8, "almacenamiento": 0.5},
    "valoran":  {"cpu": 0.7, "ram": 0.6, "gpu": 0.8, "almacenamiento": 0.5},
    "steam":    {"cpu": 0.7, "ram": 0.6, "gpu": 0.9, "almacenamiento": 0.7},
    "streaming":{"cpu": 0.8, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.6},

    # --------------------------------------------------------
    # PROGRAMACIÓN / DESARROLLO
    # --------------------------------------------------------
    "program":  {"cpu": 0.8, "ram": 0.8, "gpu": 0.3, "almacenamiento": 0.7},
    "programar":{"cpu": 0.8, "ram": 0.8, "gpu": 0.3, "almacenamiento": 0.7},
    "codigo":   {"cpu": 0.7, "ram": 0.7, "gpu": 0.3, "almacenamiento": 0.6},
    "cod":      {"cpu": 0.7, "ram": 0.7, "gpu": 0.3, "almacenamiento": 0.6},
    "desarroll":{"cpu": 0.8, "ram": 0.8, "gpu": 0.3, "almacenamiento": 0.7},
    "develop":  {"cpu": 0.8, "ram": 0.8, "gpu": 0.3, "almacenamiento": 0.7},
    "softwar":  {"cpu": 0.8, "ram": 0.8, "gpu": 0.3, "almacenamiento": 0.7},
    "web":      {"cpu": 0.6, "ram": 0.7, "gpu": 0.2, "almacenamiento": 0.6},
    "python":   {"cpu": 0.7, "ram": 0.7, "gpu": 0.4, "almacenamiento": 0.6},
    "java":     {"cpu": 0.7, "ram": 0.8, "gpu": 0.2, "almacenamiento": 0.6},
    "backend":  {"cpu": 0.8, "ram": 0.8, "gpu": 0.2, "almacenamiento": 0.7},
    "frontend": {"cpu": 0.6, "ram": 0.7, "gpu": 0.3, "almacenamiento": 0.6},
    "docker":   {"cpu": 0.8, "ram": 0.9, "gpu": 0.2, "almacenamiento": 0.8},
    "maquina":  {"cpu": 0.8, "ram": 0.9, "gpu": 0.3, "almacenamiento": 0.8},
    "virtual":  {"cpu": 0.8, "ram": 0.9, "gpu": 0.3, "almacenamiento": 0.8},

    # --------------------------------------------------------
    # INTELIGENCIA ARTIFICIAL / DATA SCIENCE
    # --------------------------------------------------------
    "inteligencia": {"cpu": 0.9, "ram": 1.0, "gpu": 1.0, "almacenamiento": 0.8},
    "intelig":  {"cpu": 0.9, "ram": 1.0, "gpu": 1.0, "almacenamiento": 0.8},
    "machine":  {"cpu": 0.9, "ram": 1.0, "gpu": 1.0, "almacenamiento": 0.8},
    "deep":     {"cpu": 0.9, "ram": 1.0, "gpu": 1.0, "almacenamiento": 0.8},
    "data":     {"cpu": 0.8, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.9},
    "ciencia":  {"cpu": 0.8, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.8},
    "modelo":   {"cpu": 0.9, "ram": 1.0, "gpu": 1.0, "almacenamiento": 0.8},
    "entrena":  {"cpu": 0.9, "ram": 1.0, "gpu": 1.0, "almacenamiento": 0.8},

    # --------------------------------------------------------
    # ESTUDIO / UNIVERSIDAD / COLEGIO
    # --------------------------------------------------------
    "estudi":   {"cpu": 0.5, "ram": 0.5, "gpu": 0.3, "almacenamiento": 0.5},
    "univers":  {"cpu": 0.6, "ram": 0.6, "gpu": 0.4, "almacenamiento": 0.6},
    "universid":{"cpu": 0.6, "ram": 0.6, "gpu": 0.4, "almacenamiento": 0.6},
    "colegio":  {"cpu": 0.4, "ram": 0.4, "gpu": 0.2, "almacenamiento": 0.4},
    "coleg":    {"cpu": 0.4, "ram": 0.4, "gpu": 0.2, "almacenamiento": 0.4},
    "clase":    {"cpu": 0.4, "ram": 0.4, "gpu": 0.2, "almacenamiento": 0.4},
    "clas":     {"cpu": 0.4, "ram": 0.4, "gpu": 0.2, "almacenamiento": 0.4},
    "tarea":    {"cpu": 0.4, "ram": 0.4, "gpu": 0.2, "almacenamiento": 0.4},
    "tar":      {"cpu": 0.4, "ram": 0.4, "gpu": 0.2, "almacenamiento": 0.4},
    "trabaj":   {"cpu": 0.5, "ram": 0.5, "gpu": 0.3, "almacenamiento": 0.5},
    "ingenier": {"cpu": 0.7, "ram": 0.7, "gpu": 0.5, "almacenamiento": 0.6},
    "ingenieri":{"cpu": 0.7, "ram": 0.7, "gpu": 0.5, "almacenamiento": 0.6},
    "simulac":  {"cpu": 0.9, "ram": 0.9, "gpu": 0.7, "almacenamiento": 0.6},
    "calculo":  {"cpu": 0.6, "ram": 0.6, "gpu": 0.3, "almacenamiento": 0.5},
    "calcul":   {"cpu": 0.6, "ram": 0.6, "gpu": 0.3, "almacenamiento": 0.5},
    "zoom":     {"cpu": 0.4, "ram": 0.4, "gpu": 0.2, "almacenamiento": 0.3},
    "meet":     {"cpu": 0.4, "ram": 0.4, "gpu": 0.2, "almacenamiento": 0.3},

    # --------------------------------------------------------
    # OFICINA / USO BÁSICO
    # --------------------------------------------------------
    "oficin":   {"cpu": 0.4, "ram": 0.4, "gpu": 0.1, "almacenamiento": 0.5},
    "ofimati":  {"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.4},
    "word":     {"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.4},
    "excel":    {"cpu": 0.4, "ram": 0.4, "gpu": 0.1, "almacenamiento": 0.4},
    "powerpoint":{"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.4},
    "naveg":    {"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.3},
    "correo":   {"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.3},
    "document": {"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.4},

    # --------------------------------------------------------
    # PRESUPUESTO
    # --------------------------------------------------------
    "barat":    {"cpu": 0.3, "ram": 0.3, "gpu": 0.2, "almacenamiento": 0.3},
    "economic": {"cpu": 0.3, "ram": 0.3, "gpu": 0.2, "almacenamiento": 0.3},
    "baj":      {"cpu": 0.3, "ram": 0.3, "gpu": 0.2, "almacenamiento": 0.3},
    "bajo":     {"cpu": 0.3, "ram": 0.3, "gpu": 0.2, "almacenamiento": 0.3},
    "basic":    {"cpu": 0.3, "ram": 0.3, "gpu": 0.1, "almacenamiento": 0.4},
    "potent":   {"cpu": 0.9, "ram": 0.8, "gpu": 0.8, "almacenamiento": 0.6},
    "rapid":    {"cpu": 0.8, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.8},
    "alta":     {"cpu": 0.7, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.5},
    "mejor":    {"cpu": 0.9, "ram": 0.8, "gpu": 0.9, "almacenamiento": 0.7},
    "top":      {"cpu": 0.9, "ram": 0.8, "gpu": 0.9, "almacenamiento": 0.7},
    "profes":   {"cpu": 0.9, "ram": 0.9, "gpu": 0.8, "almacenamiento": 0.8},

    # --------------------------------------------------------
    # MARCAS
    # --------------------------------------------------------
    "asus":     {"cpu": 0.6, "ram": 0.6, "gpu": 0.6, "almacenamiento": 0.5},
    "intel":    {"cpu": 0.7, "ram": 0.5, "gpu": 0.4, "almacenamiento": 0.5},
    "amd":      {"cpu": 0.7, "ram": 0.5, "gpu": 0.6, "almacenamiento": 0.5},
    "nvidia":   {"cpu": 0.6, "ram": 0.5, "gpu": 0.9, "almacenamiento": 0.5},
    "ryzen":    {"cpu": 0.8, "ram": 0.6, "gpu": 0.5, "almacenamiento": 0.5},
    "core":     {"cpu": 0.8, "ram": 0.6, "gpu": 0.5, "almacenamiento": 0.5},
    "samsung":  {"cpu": 0.5, "ram": 0.5, "gpu": 0.5, "almacenamiento": 0.8},
    "corsair":  {"cpu": 0.5, "ram": 0.8, "gpu": 0.5, "almacenamiento": 0.5},
    "msi":      {"cpu": 0.6, "ram": 0.6, "gpu": 0.7, "almacenamiento": 0.5},
    
     # --------------------------------------------------------
    # LENGUAJE CASUAL / CONSULTAS CORTAS
    # --------------------------------------------------------
    "buena":    {"cpu": 0.7, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.6},
    "buen":     {"cpu": 0.7, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.6},
    "bueno":    {"cpu": 0.7, "ram": 0.7, "gpu": 0.7, "almacenamiento": 0.6},
    "hij":      {"cpu": 0.5, "ram": 0.5, "gpu": 0.6, "almacenamiento": 0.5},
    "hijo":     {"cpu": 0.5, "ram": 0.5, "gpu": 0.6, "almacenamiento": 0.5},
    "hija":     {"cpu": 0.5, "ram": 0.5, "gpu": 0.6, "almacenamiento": 0.5},
    "niño":     {"cpu": 0.4, "ram": 0.4, "gpu": 0.5, "almacenamiento": 0.4},
    "niñ":      {"cpu": 0.4, "ram": 0.4, "gpu": 0.5, "almacenamiento": 0.4},
    "regalo":   {"cpu": 0.6, "ram": 0.6, "gpu": 0.6, "almacenamiento": 0.5},
    "regal":    {"cpu": 0.6, "ram": 0.6, "gpu": 0.6, "almacenamiento": 0.5},
    "trabaj":   {"cpu": 0.6, "ram": 0.6, "gpu": 0.4, "almacenamiento": 0.6},
    "cas":      {"cpu": 0.5, "ram": 0.5, "gpu": 0.4, "almacenamiento": 0.5},
    "casa":     {"cpu": 0.5, "ram": 0.5, "gpu": 0.4, "almacenamiento": 0.5},
    "todo":     {"cpu": 0.7, "ram": 0.7, "gpu": 0.6, "almacenamiento": 0.6},
    "tod":      {"cpu": 0.7, "ram": 0.7, "gpu": 0.6, "almacenamiento": 0.6},
    "multitare":{"cpu": 0.8, "ram": 0.8, "gpu": 0.5, "almacenamiento": 0.6},
    "complet":  {"cpu": 0.7, "ram": 0.7, "gpu": 0.6, "almacenamiento": 0.6},
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
        Determina el perfil usando el componente dominante,
        no el promedio. Si alguien menciona gaming aunque sea
        junto a estudio, la GPU alta manda.
        """
        gpu = prioridades.get("gpu", 0)
        cpu = prioridades.get("cpu", 0)
        ram = prioridades.get("ram", 0)

        # Si GPU es alta → Gamer (aunque haya otras intenciones)
        if gpu >= 0.75:
            return "Gamer"
        # Si CPU y RAM son altas → Diseñador / Programador
        elif cpu >= 0.75 and ram >= 0.75:
            return "Disenador"
        # Si CPU es alta pero RAM no tanto → también Diseñador
        elif cpu >= 0.8:
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