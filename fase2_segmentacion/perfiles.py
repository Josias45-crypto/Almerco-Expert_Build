# fase2_segmentacion/perfiles.py
# ============================================================
# Define las reglas de interpretación de cada perfil
# Traduce un cluster de K-Means a un perfil de cliente
# ============================================================

from dataclasses import dataclass, field
from typing import List


# ------------------------------------------------------------
# DEFINICIÓN DE PERFILES
# ------------------------------------------------------------

@dataclass
class PerfilCliente:
    """
    Representa un perfil de cliente con sus características
    y recomendaciones de hardware asociadas.
    """
    nombre:           str
    descripcion:      str
    categorias_clave: List[str]        # Categorías que más le interesan
    presupuesto_min:  float
    presupuesto_max:  float
    color:            str              # Para visualización en gráficos

    def __str__(self):
        return f"[{self.nombre}] {self.descripcion}"


# ------------------------------------------------------------
# CATÁLOGO DE PERFILES
# ------------------------------------------------------------

PERFILES = {
    "Gamer": PerfilCliente(
        nombre           = "Gamer",
        descripcion      = "Busca alto rendimiento en videojuegos. Prioriza GPU y alta frecuencia de RAM.",
        categorias_clave = ["GPU", "RAM", "Refrigeracion", "Fuente"],
        presupuesto_min  = 600,
        presupuesto_max  = 2000,
        color            = "#e74c3c",   # Rojo
    ),
    "Disenador": PerfilCliente(
        nombre           = "Disenador",
        descripcion      = "Trabaja en diseño gráfico, edición de video o renderizado 3D. Prioriza CPU y RAM.",
        categorias_clave = ["CPU", "RAM", "GPU", "Refrigeracion"],
        presupuesto_min  = 900,
        presupuesto_max  = 3000,
        color            = "#9b59b6",   # Morado
    ),
    "Oficina": PerfilCliente(
        nombre           = "Oficina",
        descripcion      = "Uso cotidiano: ofimática, navegación web, videollamadas. Prioriza precio y eficiencia.",
        categorias_clave = ["CPU", "RAM"],
        presupuesto_min  = 200,
        presupuesto_max  = 700,
        color            = "#3498db",   # Azul
    ),
}


# ------------------------------------------------------------
# MOTOR DE CLASIFICACIÓN
# Dado el centroide de un cluster, determina a qué perfil
# corresponde comparando sus características dominantes
# ------------------------------------------------------------

# Features en el mismo orden que el DataFrame
FEATURE_NOMBRES = ["interes_gpu", "interes_cpu", "interes_ram", "interes_refrig", "interes_fuente"]

# Pesos esperados por perfil (misma escala que data_builder)
PESOS_ESPERADOS = {
    "Gamer":     {"interes_gpu": 0.85, "interes_cpu": 0.70, "interes_ram": 0.60,
                  "interes_refrig": 0.65, "interes_fuente": 0.70},
    "Disenador": {"interes_gpu": 0.75, "interes_cpu": 0.85, "interes_ram": 0.90,
                  "interes_refrig": 0.70, "interes_fuente": 0.65},
    "Oficina":   {"interes_gpu": 0.20, "interes_cpu": 0.45, "interes_ram": 0.40,
                  "interes_refrig": 0.25, "interes_fuente": 0.35},
}


def clasificar_cluster(centroide: dict) -> str:
    """
    Dado el centroide de un cluster (dict feature→valor),
    retorna el nombre del perfil más cercano usando
    distancia euclidiana contra los pesos esperados.

    Args:
        centroide: dict con keys = FEATURE_NOMBRES

    Returns:
        Nombre del perfil: 'Gamer', 'Disenador' o 'Oficina'
    """
    import numpy as np

    mejor_perfil   = None
    menor_distancia = float("inf")

    for perfil, pesos in PESOS_ESPERADOS.items():
        # Vector del centroide
        v_centroide = np.array([centroide[f] for f in FEATURE_NOMBRES])
        # Vector del perfil esperado
        v_esperado  = np.array([pesos[f] for f in FEATURE_NOMBRES])
        # Distancia euclidiana
        distancia = np.linalg.norm(v_centroide - v_esperado)

        if distancia < menor_distancia:
            menor_distancia = distancia
            mejor_perfil    = perfil

    return mejor_perfil


def obtener_perfil(nombre: str) -> PerfilCliente:
    """Retorna el objeto PerfilCliente dado su nombre."""
    if nombre not in PERFILES:
        raise ValueError(f"Perfil '{nombre}' no existe. Opciones: {list(PERFILES.keys())}")
    return PERFILES[nombre]


# ------------------------------------------------------------
# MAIN — mostrar los perfiles disponibles
# ------------------------------------------------------------

if __name__ == "__main__":
    print("\n📋 Perfiles de cliente definidos:\n")
    for nombre, perfil in PERFILES.items():
        print(f"  {perfil}")
        print(f"     Categorías clave : {', '.join(perfil.categorias_clave)}")
        print(f"     Presupuesto      : ${perfil.presupuesto_min} - ${perfil.presupuesto_max}")
        print()