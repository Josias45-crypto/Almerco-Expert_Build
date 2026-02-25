# database/seed_mock.py
# ============================================================
# Poblar la base de datos con datos de prueba realistas
# Catálogo simulado de Grupo Almerco
# ============================================================

from connection import get_connection
import json


# ------------------------------------------------------------
# DATOS MOCK
# ------------------------------------------------------------

CATEGORIAS = [
    ("CPU",           "Procesadores"),
    ("Motherboard",   "Tarjetas madre"),
    ("GPU",           "Tarjetas gráficas"),
    ("RAM",           "Memoria RAM"),
    ("Gabinete",      "Cases / Gabinetes"),
    ("Fuente",        "Fuentes de poder"),
    ("Refrigeracion", "Sistemas de enfriamiento"),
]

SOCKETS = ["LGA1700", "LGA1200", "AM5", "AM4"]

# specs guardadas como JSON
PRODUCTOS = [
    # --- CPUs ---
    (
        "CPU", "Intel", "Core i9-14900K", 580.00, 10,
        {"socket": "LGA1700", "tdp_w": 125, "nucleos": 24}
    ),
    (
        "CPU", "Intel", "Core i7-14700K", 380.00, 15,
        {"socket": "LGA1700", "tdp_w": 125, "nucleos": 20}
    ),
    (
        "CPU", "Intel", "Core i5-14600K", 240.00, 20,
        {"socket": "LGA1700", "tdp_w": 125, "nucleos": 14}
    ),
    (
        "CPU", "AMD", "Ryzen 9 7950X", 550.00, 8,
        {"socket": "AM5", "tdp_w": 170, "nucleos": 16}
    ),
    (
        "CPU", "AMD", "Ryzen 7 7700X", 300.00, 12,
        {"socket": "AM5", "tdp_w": 105, "nucleos": 8}
    ),
    (
        "CPU", "AMD", "Ryzen 5 7600X", 190.00, 18,
        {"socket": "AM5", "tdp_w": 105, "nucleos": 6}
    ),

    # --- Motherboards ---
    (
        "Motherboard", "ASUS", "ROG Strix Z790-E", 420.00, 8,
        {"socket": "LGA1700", "chipset": "Z790", "form_factor": "ATX"}
    ),
    (
        "Motherboard", "MSI", "MAG Z790 Tomahawk", 280.00, 12,
        {"socket": "LGA1700", "chipset": "Z790", "form_factor": "ATX"}
    ),
    (
        "Motherboard", "Gigabyte", "B760M DS3H", 130.00, 20,
        {"socket": "LGA1700", "chipset": "B760", "form_factor": "mATX"}
    ),
    (
        "Motherboard", "ASUS", "ROG Crosshair X670E", 450.00, 6,
        {"socket": "AM5", "chipset": "X670E", "form_factor": "ATX"}
    ),
    (
        "Motherboard", "MSI", "MEG X670E ACE", 400.00, 7,
        {"socket": "AM5", "chipset": "X670E", "form_factor": "ATX"}
    ),
    (
        "Motherboard", "Gigabyte", "B650M DS3H", 140.00, 15,
        {"socket": "AM5", "chipset": "B650", "form_factor": "mATX"}
    ),

    # --- GPUs ---
    (
        "GPU", "NVIDIA", "RTX 4090", 1599.00, 5,
        {"largo_mm": 336, "vram_gb": 24, "tdp_w": 450}
    ),
    (
        "GPU", "NVIDIA", "RTX 4070 Ti", 799.00, 10,
        {"largo_mm": 285, "vram_gb": 12, "tdp_w": 285}
    ),
    (
        "GPU", "NVIDIA", "RTX 4060", 299.00, 20,
        {"largo_mm": 240, "vram_gb": 8, "tdp_w": 115}
    ),
    (
        "GPU", "AMD", "RX 7900 XTX", 899.00, 7,
        {"largo_mm": 287, "vram_gb": 24, "tdp_w": 355}
    ),
    (
        "GPU", "AMD", "RX 7700 XT", 349.00, 14,
        {"largo_mm": 267, "vram_gb": 12, "tdp_w": 245}
    ),

    # --- Gabinetes ---
    (
        "Gabinete", "Lian Li", "PC-O11 Dynamic EVO", 149.00, 10,
        {"max_gpu_largo_mm": 420, "form_factor": "Mid Tower"}
    ),
    (
        "Gabinete", "NZXT", "H510", 79.00, 15,
        {"max_gpu_largo_mm": 381, "form_factor": "Mid Tower"}
    ),
    (
        "Gabinete", "Fractal Design", "Torrent", 179.00, 8,
        {"max_gpu_largo_mm": 461, "form_factor": "Mid Tower"}
    ),
    (
        "Gabinete", "Cooler Master", "Q300L", 49.00, 20,
        {"max_gpu_largo_mm": 360, "form_factor": "mATX"}
    ),

    # --- Fuentes ---
    (
        "Fuente", "Corsair", "RM1000x", 189.00, 10,
        {"watts": 1000, "certificacion": "80+ Gold", "modular": True}
    ),
    (
        "Fuente", "EVGA", "SuperNOVA 850 G6", 139.00, 15,
        {"watts": 850, "certificacion": "80+ Gold", "modular": True}
    ),
    (
        "Fuente", "Seasonic", "Focus GX-650", 99.00, 18,
        {"watts": 650, "certificacion": "80+ Gold", "modular": True}
    ),
    (
        "Fuente", "Thermaltake", "Smart 500W", 45.00, 25,
        {"watts": 500, "certificacion": "80+ White", "modular": False}
    ),

    # --- Refrigeración ---
    (
        "Refrigeracion", "Corsair", "iCUE H150i Elite 360mm", 169.00, 8,
        {"tipo": "liquida", "radiador_mm": 360, "sockets": ["LGA1700", "AM5"]}
    ),
    (
        "Refrigeracion", "NZXT", "Kraken X63 280mm", 129.00, 10,
        {"tipo": "liquida", "radiador_mm": 280, "sockets": ["LGA1700", "AM5"]}
    ),
    (
        "Refrigeracion", "be quiet!", "Dark Rock Pro 4", 89.00, 12,
        {"tipo": "aire", "tdp_max_w": 250, "sockets": ["LGA1700", "AM5", "AM4"]}
    ),
    (
        "Refrigeracion", "Cooler Master", "Hyper 212", 35.00, 30,
        {"tipo": "aire", "tdp_max_w": 150, "sockets": ["LGA1700", "AM5", "AM4"]}
    ),
]


# ------------------------------------------------------------
# FUNCIONES
# ------------------------------------------------------------

def seed_categorias(conn):
    cursor = conn.cursor()
    for nombre, descripcion in CATEGORIAS:
        cursor.execute(
            "INSERT OR IGNORE INTO categorias (nombre, descripcion) VALUES (?, ?)",
            (nombre, descripcion)
        )
    print(f"  ✅ Categorías insertadas: {len(CATEGORIAS)}")


def seed_sockets(conn):
    cursor = conn.cursor()
    for socket in SOCKETS:
        cursor.execute(
            "INSERT OR IGNORE INTO sockets (nombre) VALUES (?)",
            (socket,)
        )
    print(f"  ✅ Sockets insertados: {len(SOCKETS)}")


def seed_productos(conn):
    cursor = conn.cursor()
    count = 0

    for cat_nombre, marca, modelo, precio, stock, specs in PRODUCTOS:

        # Obtener id de categoría
        cursor.execute("SELECT id FROM categorias WHERE nombre = ?", (cat_nombre,))
        row = cursor.fetchone()
        if not row:
            print(f"  ⚠️  Categoría no encontrada: {cat_nombre}")
            continue

        categoria_id = row["id"]
        specs_json   = json.dumps(specs)

        cursor.execute("""
            INSERT OR IGNORE INTO productos
                (categoria_id, marca, modelo, precio, stock, specs)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (categoria_id, marca, modelo, precio, stock, specs_json))

        count += 1

    print(f"  ✅ Productos insertados: {count}")


def seed_dimensiones(conn):
    """
    Extrae largo_mm de los specs de las GPUs y lo guarda en dimensiones_fisicas.
    """
    cursor = conn.cursor()
    count  = 0

    cursor.execute("""
        SELECT p.id, p.specs
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE c.nombre = 'GPU'
    """)
    gpus = cursor.fetchall()

    for gpu in gpus:
        specs = json.loads(gpu["specs"])
        largo = specs.get("largo_mm")
        if largo:
            cursor.execute("""
                INSERT OR IGNORE INTO dimensiones_fisicas (producto_id, largo_mm)
                VALUES (?, ?)
            """, (gpu["id"], largo))
            count += 1

    # También para gabinetes guardamos su capacidad máxima
    cursor.execute("""
        SELECT p.id, p.specs
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE c.nombre = 'Gabinete'
    """)
    gabinetes = cursor.fetchall()

    for gab in gabinetes:
        specs = json.loads(gab["specs"])
        max_largo = specs.get("max_gpu_largo_mm")
        if max_largo:
            cursor.execute("""
                INSERT OR IGNORE INTO dimensiones_fisicas (producto_id, largo_mm)
                VALUES (?, ?)
            """, (gab["id"], max_largo))
            count += 1

    print(f"  ✅ Dimensiones físicas insertadas: {count}")


def seed_compatibilidad_cpu_mb(conn):
    """
    Genera la matriz de compatibilidad CPU <-> Motherboard
    basada en el socket de cada uno.
    """
    cursor = conn.cursor()
    count  = 0

    # Traer todas las CPUs con su socket
    cursor.execute("""
        SELECT p.id, p.specs FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE c.nombre = 'CPU'
    """)
    cpus = cursor.fetchall()

    # Traer todas las Motherboards con su socket
    cursor.execute("""
        SELECT p.id, p.specs FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE c.nombre = 'Motherboard'
    """)
    motherboards = cursor.fetchall()

    for cpu in cpus:
        cpu_specs  = json.loads(cpu["specs"])
        cpu_socket = cpu_specs.get("socket")

        for mb in motherboards:
            mb_specs  = json.loads(mb["specs"])
            mb_socket = mb_specs.get("socket")

            compatible = 1 if cpu_socket == mb_socket else 0

            cursor.execute("""
                INSERT OR IGNORE INTO compatibilidad_cpu_motherboard
                    (cpu_id, motherboard_id, compatible)
                VALUES (?, ?, ?)
            """, (cpu["id"], mb["id"], compatible))
            count += 1

    print(f"  ✅ Filas de compatibilidad CPU-MB generadas: {count}")


def seed_compatibilidad_gpu_gabinete(conn):
    """
    Genera la matriz de compatibilidad GPU <-> Gabinete
    basada en dimensiones físicas.
    """
    cursor = conn.cursor()
    count  = 0

    cursor.execute("""
        SELECT p.id, d.largo_mm FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        JOIN dimensiones_fisicas d ON d.producto_id = p.id
        WHERE c.nombre = 'GPU'
    """)
    gpus = cursor.fetchall()

    cursor.execute("""
        SELECT p.id, p.specs FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE c.nombre = 'Gabinete'
    """)
    gabinetes = cursor.fetchall()

    for gpu in gpus:
        for gab in gabinetes:
            gab_specs  = json.loads(gab["specs"])
            max_largo  = gab_specs.get("max_gpu_largo_mm", 0)
            gpu_largo  = gpu["largo_mm"]
            compatible = 1 if gpu_largo <= max_largo else 0
            espacio    = round(max_largo - gpu_largo, 2)

            cursor.execute("""
                INSERT OR IGNORE INTO compatibilidad_gpu_gabinete
                    (gpu_id, gabinete_id, compatible, espacio_libre_mm)
                VALUES (?, ?, ?, ?)
            """, (gpu["id"], gab["id"], compatible, espacio))
            count += 1

    print(f"  ✅ Filas de compatibilidad GPU-Gabinete generadas: {count}")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    print("\n🚀 Iniciando seed de base de datos Almerco...\n")

    with get_connection() as conn:
        seed_categorias(conn)
        seed_sockets(conn)
        seed_productos(conn)
        seed_dimensiones(conn)
        seed_compatibilidad_cpu_mb(conn)
        seed_compatibilidad_gpu_gabinete(conn)

    print("\n✅ Seed completado exitosamente.\n")