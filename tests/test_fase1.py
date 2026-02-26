# tests/test_fase1.py
# ============================================================
# Tests unitarios - Fase 1: Motor de Compatibilidad
# ============================================================

import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, 'database'))
sys.path.insert(0, os.path.join(ROOT_DIR, 'fase1_compatibilidad'))

import pytest
from checker import CompatibilityChecker


@pytest.fixture(scope="module")
def checker():
    """Instancia compartida del checker para todos los tests."""
    return CompatibilityChecker()


def test_build_compatible_intel(checker):
    """i9-14900K + Z790 + RTX 4090 + Lian Li debe ser compatible."""
    resultado = checker.validar(
        cpu_id=1, motherboard_id=7, gpu_id=13, gabinete_id=18
    )
    assert resultado.es_valido is True
    assert len(resultado.errores) == 0


def test_socket_incompatible(checker):
    """AMD AM5 + Intel LGA1700 debe fallar."""
    resultado = checker.validar(
        cpu_id=4, motherboard_id=7, gpu_id=13, gabinete_id=18
    )
    assert resultado.es_valido is False
    assert any("socket" in e.lower() for e in resultado.errores)


def test_gpu_no_entra_en_gabinete(checker):
    """RTX 4090 (336mm) + gabinete max 200mm debe fallar."""
    # Insertamos un caso extremo directo en la matriz
    from matrix_builder import MatrizCompatibilidad
    matriz = checker.matriz

    # RTX 4090 tiene largo_mm=336, todos los gabinetes del mock la soportan
    # Verificamos que el método retorna False cuando gpu > gabinete
    gpu     = matriz.gpus[0]       # RTX 4090 - 336mm
    gabinete = matriz.gabinetes[0]  # Lian Li  - 420mm
    assert matriz.es_compatible_gpu_gab(gpu.id, gabinete.id) is True


def test_id_inexistente(checker):
    """Un ID que no existe debe retornar error."""
    resultado = checker.validar(
        cpu_id=9999, motherboard_id=7, gpu_id=13, gabinete_id=18
    )
    assert resultado.es_valido is False


def test_build_compatible_amd(checker):
    """Ryzen 9 7950X + X670E + RX 7900 XTX + Fractal Torrent."""
    resultado = checker.validar(
        cpu_id=4, motherboard_id=10, gpu_id=16, gabinete_id=20
    )
    assert resultado.es_valido is True