# fase1_compatibilidad/models/hardware.py
# ============================================================
# Modelos de datos para el Motor de Compatibilidad
# Representan las entidades de hardware del catálogo Almerco
# ============================================================

import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CPU:
    id:       int
    marca:    str
    modelo:   str
    precio:   float
    socket:   str
    tdp_w:    int
    nucleos:  int

    @staticmethod
    def from_db_row(row) -> "CPU":
        """Construye un CPU desde una fila de la base de datos."""
        specs = json.loads(row["specs"])
        return CPU(
            id      = row["id"],
            marca   = row["marca"],
            modelo  = row["modelo"],
            precio  = row["precio"],
            socket  = specs.get("socket", ""),
            tdp_w   = specs.get("tdp_w", 0),
            nucleos = specs.get("nucleos", 0),
        )

    def __str__(self):
        return f"{self.marca} {self.modelo} [{self.socket}]"


@dataclass
class Motherboard:
    id:          int
    marca:       str
    modelo:      str
    precio:      float
    socket:      str
    chipset:     str
    form_factor: str

    @staticmethod
    def from_db_row(row) -> "Motherboard":
        specs = json.loads(row["specs"])
        return Motherboard(
            id          = row["id"],
            marca       = row["marca"],
            modelo      = row["modelo"],
            precio      = row["precio"],
            socket      = specs.get("socket", ""),
            chipset     = specs.get("chipset", ""),
            form_factor = specs.get("form_factor", ""),
        )

    def __str__(self):
        return f"{self.marca} {self.modelo} [{self.socket} | {self.chipset}]"


@dataclass
class GPU:
    id:       int
    marca:    str
    modelo:   str
    precio:   float
    largo_mm: float
    vram_gb:  int
    tdp_w:    int

    @staticmethod
    def from_db_row(row) -> "GPU":
        specs = json.loads(row["specs"])
        return GPU(
            id       = row["id"],
            marca    = row["marca"],
            modelo   = row["modelo"],
            precio   = row["precio"],
            largo_mm = specs.get("largo_mm", 0),
            vram_gb  = specs.get("vram_gb", 0),
            tdp_w    = specs.get("tdp_w", 0),
        )

    def __str__(self):
        return f"{self.marca} {self.modelo} [{self.largo_mm}mm | {self.vram_gb}GB]"


@dataclass
class Gabinete:
    id:               int
    marca:            str
    modelo:           str
    precio:           float
    max_gpu_largo_mm: float
    form_factor:      str

    @staticmethod
    def from_db_row(row) -> "Gabinete":
        specs = json.loads(row["specs"])
        return Gabinete(
            id               = row["id"],
            marca            = row["marca"],
            modelo           = row["modelo"],
            precio           = row["precio"],
            max_gpu_largo_mm = specs.get("max_gpu_largo_mm", 0),
            form_factor      = specs.get("form_factor", ""),
        )

    def __str__(self):
        return f"{self.marca} {self.modelo} [Max GPU: {self.max_gpu_largo_mm}mm]"


@dataclass
class Fuente:
    id:            int
    marca:         str
    modelo:        str
    precio:        float
    watts:         int
    certificacion: str
    modular:       bool

    @staticmethod
    def from_db_row(row) -> "Fuente":
        specs = json.loads(row["specs"])
        return Fuente(
            id            = row["id"],
            marca         = row["marca"],
            modelo        = row["modelo"],
            precio        = row["precio"],
            watts         = specs.get("watts", 0),
            certificacion = specs.get("certificacion", ""),
            modular       = specs.get("modular", False),
        )

    def __str__(self):
        return f"{self.marca} {self.modelo} [{self.watts}W | {self.certificacion}]"


@dataclass
class Refrigeracion:
    id:          int
    marca:       str
    modelo:      str
    precio:      float
    tipo:        str
    radiador_mm: Optional[int]
    tdp_max_w:   Optional[int]
    sockets:     list = field(default_factory=list)

    @staticmethod
    def from_db_row(row) -> "Refrigeracion":
        specs = json.loads(row["specs"])
        return Refrigeracion(
            id          = row["id"],
            marca       = row["marca"],
            modelo      = row["modelo"],
            precio      = row["precio"],
            tipo        = specs.get("tipo", ""),
            radiador_mm = specs.get("radiador_mm"),
            tdp_max_w   = specs.get("tdp_max_w"),
            sockets     = specs.get("sockets", []),
        )

    def __str__(self):
        detalle = f"{self.radiador_mm}mm" if self.tipo == "liquida" else f"{self.tdp_max_w}W TDP"
        return f"{self.marca} {self.modelo} [{self.tipo} | {detalle}]"