🖥️ Almerco Expert-Build

> **Asistente de Ventas Inteligente y Validador de Compatibilidad**  
> Proyecto desarrollado para **Grupo Almerco** — Departamento de Desarrollo de Software / E-commerce

---

## 📋 Descripción General

Almerco Expert-Build es un sistema de inteligencia artificial aplicado al e-commerce de hardware para PC. Su objetivo principal es **reducir las devoluciones por incompatibilidad** y **aumentar el ticket promedio** mediante un motor que valida que todas las piezas de una PC seleccionada por el cliente sean compatibles entre sí, y que además recomiende componentes complementarios de forma inteligente.

El sistema se compone de cuatro fases progresivas, cada una construida sobre la anterior, que juntas forman un asistente de ventas completo.

---

## 🎯 Objetivos de Negocio

- Eliminar devoluciones causadas por incompatibilidad de hardware (socket incorrecto, GPU que no entra en el gabinete, fuente insuficiente, etc.)
- Aumentar el ticket promedio mediante recomendaciones inteligentes de componentes complementarios
- Personalizar la experiencia de compra según el perfil del cliente (Gamer, Diseñador, Usuario de Oficina)
- Procesar búsquedas en lenguaje natural para facilitar la navegación del catálogo

---

## 🏗️ Arquitectura del Proyecto

```
almerco-expert-build/
│
├── README.md                          # Este archivo
├── .gitignore                         # Archivos ignorados por Git
├── requirements.txt                   # Dependencias Python
│
├── database/                          # Capa de datos
│   ├── connection.py                  # Manejador de conexión SQLite
│   ├── schema.sql                     # Definición de tablas
│   ├── seed_mock.py                   # Datos de prueba del catálogo
│   └── almerco.db                     # Base de datos SQLite (generada)
│
├── fase1_compatibilidad/              # Motor de Compatibilidad Matricial
│   ├── __init__.py
│   ├── matrix_builder.py              # Construcción de matrices NumPy
│   ├── checker.py                     # Entregable: validador de builds
│   └── models/
│       ├── __init__.py
│       └── hardware.py                # Clases de hardware (CPU, GPU, etc.)
│
├── fase2_segmentacion/                # Segmentación de Clientes (K-Means)
│   └── __init__.py
│
├── fase3_nlp/                         # Procesamiento de Lenguaje Natural
│   └── __init__.py
│
├── fase4_recomendador/                # Recomendador Deep Learning
│   └── __init__.py
│
└── tests/
    └── test_fase1.py                  # Tests unitarios Fase 1
```

---

## 🔧 Fases de Implementación

### ✅ Fase 1 — Motor de Compatibilidad Matricial
**Estado: Completada**

Valida que las piezas seleccionadas por el cliente sean físicamente y eléctricamente compatibles entre sí. Utiliza matrices binarias de NumPy para lograr consultas en tiempo O(1).

**Herramientas:** `NumPy`, `SQLite`, `Python dataclasses`

**Validaciones implementadas:**
- CPU ↔ Motherboard (compatibilidad de socket: LGA1700, AM5, AM4, etc.)
- GPU ↔ Gabinete (dimensiones físicas en milímetros)

**Entregable:** `fase1_compatibilidad/checker.py`

---

### 🔜 Fase 2 — Segmentación de Clientes por Perfil
**Estado: Pendiente**

Clasifica automáticamente a los clientes en perfiles según su comportamiento de navegación y compras anteriores usando algoritmos de clustering no supervisado.

**Herramientas:** `Scikit-learn` (K-Means)

**Perfiles a detectar:** Gamer, Diseñador Gráfico, Usuario de Oficina

**Entregable:** Informe de perfiles de cliente de Grupo Almerco

---

### 🔜 Fase 3 — Procesamiento de Lenguaje Natural
**Estado: Pendiente**

Motor de búsqueda semántica que interpreta consultas en lenguaje natural como *"Busco una PC potente para renderizar video 4K"* y las traduce en filtros técnicos sobre el catálogo.

**Herramientas:** `NLTK`, `SciPy`

**Ejemplo:** "renderizar" → prioridad en CPU y RAM → filtra catálogo automáticamente

**Entregable:** Módulo de búsqueda semántica

---

### 🔜 Fase 4 — Recomendador "Next Best Offer"
**Estado: Pendiente**

Sistema de recomendación basado en Deep Learning que sugiere componentes complementarios obligatorios y opcionales según la selección del cliente.

**Herramientas:** `PyTorch` / `Keras`

**Ejemplo:** Si el cliente elige un i9-14900K → el sistema recomienda obligatoriamente refrigeración líquida 360mm y fuente de más de 850W.

**Entregable:** Motor de recomendación NBO

---

## 🗄️ Modelo de Base de Datos

La base de datos SQLite contiene las siguientes tablas:

| Tabla | Descripción |
|---|---|
| `categorias` | CPU, Motherboard, GPU, RAM, Gabinete, Fuente, Refrigeración |
| `productos` | Catálogo completo con specs en formato JSON |
| `sockets` | Tipos de socket: LGA1700, AM5, AM4, LGA1200 |
| `compatibilidad_cpu_motherboard` | Matriz de compatibilidad CPU ↔ Motherboard |
| `dimensiones_fisicas` | Dimensiones en mm de GPUs y Gabinetes |
| `compatibilidad_gpu_gabinete` | Matriz de compatibilidad GPU ↔ Gabinete |

---

## ⚙️ Instalación y Configuración

### Pre-requisitos

- Python 3.10 o superior
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/practicas-josias/Almerco-Expert-Build.git
cd almerco-expert-build

# 2. Crear y activar el entorno virtual
python -m venv venv
source venv/Scripts/activate   # Windows
source venv/bin/activate        # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Inicializar la base de datos
python database/connection.py

# 5. Poblar con datos de prueba
cd database
python seed_mock.py
cd ..
```

---

## ▶️ Uso

### Validar compatibilidad de un build

```python
from fase1_compatibilidad.checker import CompatibilityChecker

checker = CompatibilityChecker()

resultado = checker.validar(
    cpu_id         = 1,    # Intel Core i9-14900K
    motherboard_id = 7,    # ASUS ROG Strix Z790-E
    gpu_id         = 13,   # NVIDIA RTX 4090
    gabinete_id    = 18,   # Lian Li PC-O11 Dynamic EVO
)

resultado.imprimir()
```

**Salida esperada:**
```
=======================================================
       RESULTADO DE COMPATIBILIDAD - ALMERCO
=======================================================
📦 Build seleccionado:
   CPU: Intel Core i9-14900K [LGA1700]
   Motherboard: ASUS ROG Strix Z790-E [LGA1700 | Z790]
   GPU: NVIDIA RTX 4090 [336mm | 24GB]
   Gabinete: Lian Li PC-O11 Dynamic EVO [Max GPU: 420mm]
-------------------------------------------------------
✅ BUILD COMPATIBLE — ¡Todas las piezas encajan!
=======================================================
```

### Correr los tests

```bash
pytest tests/test_fase1.py -v
```

---

## 🛠️ Stack Tecnológico

| Herramienta | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| NumPy | Matrices binarias de compatibilidad |
| Scikit-learn | Clustering K-Means (Fase 2) |
| NLTK + SciPy | Procesamiento de lenguaje natural (Fase 3) |
| PyTorch / Keras | Modelo de recomendación Deep Learning (Fase 4) |
| SQLite | Base de datos local de desarrollo |
| Pytest | Testing unitario |
| Git + GitHub | Control de versiones |

---

## 📦 Dependencias

```
numpy==1.26.4
pandas==2.2.2
scikit-learn==1.4.2
nltk==3.8.1
scipy==1.13.0
torch==2.3.0
SQLAlchemy==2.0.30
pytest==8.2.0
python-dotenv==1.0.1
```

---

## 🌿 Ramas del Repositorio

| Rama | Descripción |
|---|---|
| `main` | Código estable y aprobado |
| `dev` | Rama principal de desarrollo activo |

---

## 👨‍💻 Desarrollado por

**Josias** — Grupo Almerco  
Departamento de Desarrollo de Software / E-commerce

---

## 📄 Licencia

Proyecto privado — Grupo Almerco. Todos los derechos reservados.
