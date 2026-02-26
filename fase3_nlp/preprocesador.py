# fase3_nlp/preprocesador.py
# ============================================================
# Limpia y tokeniza el texto de búsqueda del usuario
# Herramientas: NLTK
# ============================================================

import sys
import os
import re
import nltk

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Descargar recursos NLTK necesarios (solo la primera vez)
def descargar_recursos():
    recursos = ["punkt", "stopwords", "punkt_tab"]
    for recurso in recursos:
        try:
            nltk.data.find(f"tokenizers/{recurso}")
        except LookupError:
            nltk.download(recurso, quiet=True)

descargar_recursos()

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------

IDIOMA         = "spanish"
STEMMER        = SnowballStemmer(IDIOMA)
STOPWORDS_ES   = set(stopwords.words(IDIOMA))

# Palabras técnicas que NUNCA deben eliminarse aunque sean stopwords
PALABRAS_CLAVE_TECNICAS = {
    "4k", "8k", "hd", "ram", "cpu", "gpu", "ssd", "hdd",
    "nvme", "rgb", "wifi", "bluetooth", "usb", "pcie",
    "gaming", "gamer", "streaming", "renderizar", "renderizado",
    "edicion", "editar", "diseño", "disenar", "oficina",
    "potente", "rapido", "economico", "barato", "caro",
    "video", "foto", "musica", "programar", "codigo",
}


# ------------------------------------------------------------
# CLASE PREPROCESADOR
# ------------------------------------------------------------

class Preprocesador:
    """
    Limpia y normaliza el texto de búsqueda del usuario.

    Pipeline:
        1. Convertir a minúsculas
        2. Eliminar caracteres especiales
        3. Tokenizar
        4. Eliminar stopwords (excepto palabras técnicas)
        5. Aplicar stemming
    """

    def __init__(self):
        self.stopwords = STOPWORDS_ES - PALABRAS_CLAVE_TECNICAS

    def limpiar(self, texto: str) -> str:
        """
        Paso 1 y 2: minúsculas + eliminar caracteres especiales.
        """
        texto = texto.lower().strip()
        # Eliminar caracteres especiales pero conservar letras con tilde
        texto = re.sub(r"[^\w\sáéíóúüñ]", " ", texto)
        # Eliminar espacios múltiples
        texto = re.sub(r"\s+", " ", texto)
        return texto

    def tokenizar(self, texto: str) -> list:
        """
        Paso 3: divide el texto en tokens (palabras).
        """
        return word_tokenize(texto, language=IDIOMA)

    def eliminar_stopwords(self, tokens: list) -> list:
        """
        Paso 4: elimina palabras vacías conservando términos técnicos.
        """
        return [t for t in tokens if t not in self.stopwords or t in PALABRAS_CLAVE_TECNICAS]

    def aplicar_stemming(self, tokens: list) -> list:
        """
        Paso 5: reduce cada palabra a su raíz.
        Ej: 'renderizando' → 'render', 'potente' → 'potent'
        """
        return [STEMMER.stem(t) for t in tokens]

    def procesar(self, texto: str) -> dict:
        """
        Ejecuta el pipeline completo sobre el texto de entrada.

        Returns:
            dict con:
                texto_original  : texto tal como lo escribió el usuario
                texto_limpio    : texto normalizado
                tokens          : lista de tokens
                tokens_filtrados: tokens sin stopwords
                stems           : tokens con stemming aplicado
        """
        texto_limpio        = self.limpiar(texto)
        tokens              = self.tokenizar(texto_limpio)
        tokens_filtrados    = self.eliminar_stopwords(tokens)
        stems               = self.aplicar_stemming(tokens_filtrados)

        return {
            "texto_original"  : texto,
            "texto_limpio"    : texto_limpio,
            "tokens"          : tokens,
            "tokens_filtrados": tokens_filtrados,
            "stems"           : stems,
        }


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    preprocesador = Preprocesador()

    consultas = [
        "Busco una PC potente para renderizar video 4K",
        "Quiero una computadora barata para la oficina",
        "Necesito un equipo para gaming y streaming en alta calidad",
        "PC para diseño gráfico y edición de fotos profesional",
    ]

    print("\n🔍 Pruebas de preprocesamiento:\n")
    for consulta in consultas:
        resultado = preprocesador.procesar(consulta)
        print(f"  Original : {resultado['texto_original']}")
        print(f"  Limpio   : {resultado['texto_limpio']}")
        print(f"  Tokens   : {resultado['tokens_filtrados']}")
        print(f"  Stems    : {resultado['stems']}")
        print()