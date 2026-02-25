# fase1_compatibilidad/matrix_builder.py
# ============================================================
# Construye matrices binarias de compatibilidad usando NumPy
# Fuente de datos: almerco.db
# ============================================================

import sys
import os
import numpy as np

# Rutas para importar módulos del proyecto
ROOT_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE1_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(ROOT_DIR, 'database'))
sys.path.insert(0, FASE1_DIR)

from connection import get_connection
from models.hardware import CPU, Motherboard, GPU, Gabinete


class MatrizCompatibilidad:
    """
    Construye y gestiona las matrices binarias de compatibilidad.

    Matrices disponibles:
      - matriz_cpu_mb   : shape (n_cpus, n_motherboards) → 1 si compatible, 0 si no
      - matriz_gpu_gab  : shape (n_gpus, n_gabinetes)    → 1 si entra físicamente, 0 si no

    Los índices de las matrices se mapean a IDs reales de productos
    mediante los diccionarios cpu_index, mb_index, gpu_index, gab_index.
    """

    def __init__(self):
        self.cpus         = []
        self.motherboards = []
        self.gpus         = []
        self.gabinetes    = []

        # Mapas: producto.id → índice en la matriz
        self.cpu_index = {}
        self.mb_index  = {}
        self.gpu_index = {}
        self.gab_index = {}

        # Las matrices en sí
        self.matriz_cpu_mb  = None
        self.matriz_gpu_gab = None

    # ----------------------------------------------------------
    # CARGA DE DATOS DESDE LA DB
    # ----------------------------------------------------------

    def _cargar_productos(self, conn):
        """Carga todos los productos relevantes desde la DB."""
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.id, p.marca, p.modelo, p.precio, p.specs
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE c.nombre = 'CPU' AND p.activo = 1
        """)
        self.cpus = [CPU.from_db_row(r) for r in cursor.fetchall()]

        cursor.execute("""
            SELECT p.id, p.marca, p.modelo, p.precio, p.specs
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE c.nombre = 'Motherboard' AND p.activo = 1
        """)
        self.motherboards = [Motherboard.from_db_row(r) for r in cursor.fetchall()]

        cursor.execute("""
            SELECT p.id, p.marca, p.modelo, p.precio, p.specs
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE c.nombre = 'GPU' AND p.activo = 1
        """)
        self.gpus = [GPU.from_db_row(r) for r in cursor.fetchall()]

        cursor.execute("""
            SELECT p.id, p.marca, p.modelo, p.precio, p.specs
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE c.nombre = 'Gabinete' AND p.activo = 1
        """)
        self.gabinetes = [Gabinete.from_db_row(r) for r in cursor.fetchall()]

    # ----------------------------------------------------------
    # CONSTRUCCIÓN DE ÍNDICES
    # ----------------------------------------------------------

    def _construir_indices(self):
        """Mapea cada producto.id a su posición en la matriz."""
        self.cpu_index = {cpu.id: i for i, cpu in enumerate(self.cpus)}
        self.mb_index  = {mb.id:  i for i, mb  in enumerate(self.motherboards)}
        self.gpu_index = {gpu.id: i for i, gpu in enumerate(self.gpus)}
        self.gab_index = {gab.id: i for i, gab in enumerate(self.gabinetes)}

    # ----------------------------------------------------------
    # CONSTRUCCIÓN DE MATRICES NUMPY
    # ----------------------------------------------------------

    def _construir_matriz_cpu_mb(self, conn):
        """
        Matriz binaria (n_cpus x n_motherboards).
        Lee la tabla compatibilidad_cpu_motherboard y vuelca los valores.
        """
        n_cpus = len(self.cpus)
        n_mbs  = len(self.motherboards)

        # Inicializar en ceros
        self.matriz_cpu_mb = np.zeros((n_cpus, n_mbs), dtype=np.int8)

        cursor = conn.cursor()
        cursor.execute("""
            SELECT cpu_id, motherboard_id, compatible
            FROM compatibilidad_cpu_motherboard
        """)

        for row in cursor.fetchall():
            cpu_idx = self.cpu_index.get(row["cpu_id"])
            mb_idx  = self.mb_index.get(row["motherboard_id"])

            if cpu_idx is not None and mb_idx is not None:
                self.matriz_cpu_mb[cpu_idx][mb_idx] = row["compatible"]

    def _construir_matriz_gpu_gab(self, conn):
        """
        Matriz binaria (n_gpus x n_gabinetes).
        Usa operaciones vectoriales NumPy sobre dimensiones físicas.
        """
        n_gpus = len(self.gpus)
        n_gabs = len(self.gabinetes)

        # Vectores de dimensiones
        gpu_largos = np.array([gpu.largo_mm for gpu in self.gpus], dtype=np.float32)
        gab_maximos = np.array([gab.max_gpu_largo_mm for gab in self.gabinetes], dtype=np.float32)

        # Operación matricial: broadcasting NumPy
        # Compara cada GPU contra cada gabinete en una sola operación
        # gpu_largos[:, None] → columna (n_gpus, 1)
        # gab_maximos[None, :] → fila (1, n_gabinetes)
        # Resultado: matriz (n_gpus, n_gabinetes) con True/False
        self.matriz_gpu_gab = (gpu_largos[:, None] <= gab_maximos[None, :]).astype(np.int8)

    # ----------------------------------------------------------
    # MÉTODO PRINCIPAL
    # ----------------------------------------------------------

    def construir(self):
        """Ejecuta todo el pipeline de construcción de matrices."""
        print("🔧 Construyendo matrices de compatibilidad...")

        with get_connection() as conn:
            self._cargar_productos(conn)
            self._construir_indices()
            self._construir_matriz_cpu_mb(conn)
            self._construir_matriz_gpu_gab(conn)

        print(f"  ✅ CPUs cargadas:        {len(self.cpus)}")
        print(f"  ✅ Motherboards cargadas: {len(self.motherboards)}")
        print(f"  ✅ GPUs cargadas:         {len(self.gpus)}")
        print(f"  ✅ Gabinetes cargados:    {len(self.gabinetes)}")
        print(f"  ✅ Matriz CPU-MB:         {self.matriz_cpu_mb.shape}")
        print(f"  ✅ Matriz GPU-Gabinete:   {self.matriz_gpu_gab.shape}")
        print("✅ Matrices listas.\n")

        return self

    # ----------------------------------------------------------
    # CONSULTAS RÁPIDAS
    # ----------------------------------------------------------

    def es_compatible_cpu_mb(self, cpu_id: int, mb_id: int) -> bool:
        """Consulta O(1) usando índices de la matriz."""
        cpu_idx = self.cpu_index.get(cpu_id)
        mb_idx  = self.mb_index.get(mb_id)

        if cpu_idx is None or mb_idx is None:
            raise ValueError(f"ID no encontrado → cpu_id={cpu_id}, mb_id={mb_id}")

        return bool(self.matriz_cpu_mb[cpu_idx][mb_idx])

    def es_compatible_gpu_gab(self, gpu_id: int, gab_id: int) -> bool:
        """Consulta O(1) usando índices de la matriz."""
        gpu_idx = self.gpu_index.get(gpu_id)
        gab_idx = self.gab_index.get(gab_id)

        if gpu_idx is None or gab_idx is None:
            raise ValueError(f"ID no encontrado → gpu_id={gpu_id}, gab_id={gab_id}")

        return bool(self.matriz_gpu_gab[gpu_idx][gab_idx])

    def motherboards_compatibles_con(self, cpu_id: int) -> list:
        """Retorna lista de Motherboards compatibles con una CPU dada."""
        cpu_idx = self.cpu_index.get(cpu_id)
        if cpu_idx is None:
            raise ValueError(f"cpu_id={cpu_id} no encontrado")

        # Operación vectorial: fila completa de la matriz
        fila = self.matriz_cpu_mb[cpu_idx]                  # array de 0s y 1s
        indices_compatibles = np.where(fila == 1)[0]        # índices donde es 1

        return [self.motherboards[i] for i in indices_compatibles]

    def gabinetes_compatibles_con(self, gpu_id: int) -> list:
        """Retorna lista de Gabinetes compatibles con una GPU dada."""
        gpu_idx = self.gpu_index.get(gpu_id)
        if gpu_idx is None:
            raise ValueError(f"gpu_id={gpu_id} no encontrado")

        fila = self.matriz_gpu_gab[gpu_idx]
        indices_compatibles = np.where(fila == 1)[0]

        return [self.gabinetes[i] for i in indices_compatibles]


# ----------------------------------------------------------
# TEST RÁPIDO AL CORRER EL ARCHIVO DIRECTAMENTE
# ----------------------------------------------------------

if __name__ == "__main__":
    matriz = MatrizCompatibilidad().construir()

    # Mostrar la matriz CPU-MB completa
    print("📊 Matriz CPU ↔ Motherboard:")
    print(matriz.matriz_cpu_mb)

    print("\n📊 Matriz GPU ↔ Gabinete:")
    print(matriz.matriz_gpu_gab)

    # Ejemplo: motherboards compatibles con la primera CPU
    primera_cpu = matriz.cpus[0]
    compatibles = matriz.motherboards_compatibles_con(primera_cpu.id)
    print(f"\n🔍 Motherboards compatibles con {primera_cpu}:")
    for mb in compatibles:
        print(f"   → {mb}")