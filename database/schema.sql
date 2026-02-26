-- ============================================================
-- ALMERCO EXPERT-BUILD | Schema de Base de Datos
-- Versión: 1.0
-- Descripción: Modelo relacional para el motor de compatibilidad
-- ============================================================

-- ------------------------------------------------------------
-- TABLA: categorias
-- Ej: CPU, Motherboard, GPU, RAM, Gabinete, Fuente, Refrigeración
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorias (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL UNIQUE,
    descripcion TEXT
);

-- ------------------------------------------------------------
-- TABLA: productos
-- Catálogo general de hardware
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id    INTEGER NOT NULL,
    marca           TEXT NOT NULL,
    modelo          TEXT NOT NULL,
    precio          REAL NOT NULL,
    stock           INTEGER DEFAULT 0,
    activo          INTEGER DEFAULT 1,  -- 1 = activo, 0 = inactivo
    specs           TEXT,               -- JSON con especificaciones técnicas
    creado_en       TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- ------------------------------------------------------------
-- TABLA: sockets
-- Ej: LGA1700, AM5, AM4
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sockets (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre  TEXT NOT NULL UNIQUE   -- Ej: 'LGA1700', 'AM5'
);

-- ------------------------------------------------------------
-- TABLA: compatibilidad_cpu_motherboard
-- Matriz binaria: qué CPU es compatible con qué Motherboard
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS compatibilidad_cpu_motherboard (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_id          INTEGER NOT NULL,
    motherboard_id  INTEGER NOT NULL,
    compatible      INTEGER DEFAULT 1,  -- 1 = compatible, 0 = no compatible
    nota            TEXT,               -- Ej: 'Requiere actualización de BIOS'

    FOREIGN KEY (cpu_id)         REFERENCES productos(id),
    FOREIGN KEY (motherboard_id) REFERENCES productos(id),
    UNIQUE(cpu_id, motherboard_id)
);

-- ------------------------------------------------------------
-- TABLA: dimensiones_fisicas
-- Para validar GPU vs espacio en Gabinete
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dimensiones_fisicas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL UNIQUE,
    largo_mm    REAL,   -- longitud en milímetros (clave para GPU)
    ancho_mm    REAL,
    alto_mm     REAL,

    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- ------------------------------------------------------------
-- TABLA: compatibilidad_gpu_gabinete
-- Validación física: ¿entra la GPU en el gabinete?
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS compatibilidad_gpu_gabinete (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    gpu_id          INTEGER NOT NULL,
    gabinete_id     INTEGER NOT NULL,
    compatible      INTEGER DEFAULT 1,
    espacio_libre_mm REAL,  -- margen que queda después de instalar la GPU

    FOREIGN KEY (gpu_id)      REFERENCES productos(id),
    FOREIGN KEY (gabinete_id) REFERENCES productos(id),
    UNIQUE(gpu_id, gabinete_id)
);