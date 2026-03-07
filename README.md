# 🖥️ Almerco Expert-Build

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
├── README.md
├── .gitignore
├── requirements.txt
│
├── database/
│   ├── connection.py           # Manejador de conexión SQLite
│   ├── schema.sql              # Definición de tablas
│   ├── seed_mock.py            # Datos de prueba del catálogo
│   └── almerco.db              # Base de datos SQLite (generada localmente)
│
├── fase1_compatibilidad/
│   ├── matrix_builder.py       # Construcción de matrices NumPy
│   ├── checker.py              # Entregable: validador de builds
│   └── models/
│       └── hardware.py         # Clases de hardware (CPU, GPU, etc.)
│
├── fase2_segmentacion/
│   ├── data_builder.py         # Generador de datos de clientes
│   ├── perfiles.py             # Definición de perfiles
│   ├── segmentador.py          # Modelo K-Means
│   └── informe.py              # Entregable: reporte con gráficos
│
├── fase3_nlp/
│   ├── preprocesador.py        # Limpieza y tokenización
│   ├── extractor.py            # Extracción de entidades técnicas
│   ├── buscador.py             # Filtrado de catálogo con SciPy
│   └── motor_busqueda.py       # Entregable: búsqueda semántica
│
├── fase4_recomendador/
│   ├── reglas_obligatorias.py  # Reglas fijas de recomendación
│   ├── dataset.py              # Pares de entrenamiento PyTorch
│   ├── modelo.py               # Red neuronal feedforward
│   └── recomendador.py         # Entregable: sistema NBO completo
│
└── tests/
    └── test_fase1.py           # Tests unitarios Fase 1
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

### ✅ Fase 2 — Segmentación de Clientes por Perfil
**Estado: Completada**

Clasifica automáticamente a los clientes en perfiles según su comportamiento de navegación usando K-Means clustering.

**Herramientas:** `Scikit-learn` (K-Means), `Pandas`, `Matplotlib`

**Resultados:**
- Silhouette Score: **0.4472**
- 120 clientes Gamer — presupuesto avg $770
- 80 clientes Diseñador — presupuesto avg $1,411
- 150 clientes Oficina — presupuesto avg $351

**Entregable:** `fase2_segmentacion/informe.py`

---

### ✅ Fase 3 — Procesamiento de Lenguaje Natural
**Estado: Completada**

Motor de búsqueda semántica que interpreta consultas en lenguaje natural y las traduce en filtros técnicos sobre el catálogo.

**Herramientas:** `NLTK`, `SciPy`

**Ejemplos:**
- "quiero jugar valorant y fortnite" → Gamer → GPU alta prioridad
- "pc para diseño gráfico en photoshop" → Diseñador → CPU + RAM alta prioridad
- "computadora barata para la oficina" → Oficina → componentes económicos

**Entregable:** `fase3_nlp/motor_busqueda.py`

---

### ✅ Fase 4 — Recomendador "Next Best Offer"
**Estado: Completada**

Sistema de recomendación que combina reglas obligatorias determinísticas con una red neuronal PyTorch para sugerir componentes complementarios.

**Herramientas:** `PyTorch`

**Resultados:**
- i9-14900K → obliga refrigeración líquida 360mm + fuente 850W ✅
- RTX 4090 → obliga fuente 850W + gabinete 380mm+ ✅
- Ryzen 5 7600X → sin obligatorios, sugerencias por modelo ✅

**Entregable:** `fase4_recomendador/recomendador.py`

---

## 🗄️ Modelo de Base de Datos

| Tabla | Descripción |
|---|---|
| `categorias` | CPU, Motherboard, GPU, RAM, Gabinete, Fuente, Refrigeración, SSD |
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
git clone https://github.com/Josias45-crypto/Almerco-Expert_Build.git
cd Almerco-Expert_Build

# 2. Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\Activate.ps1       # Windows PowerShell

# 3. Instalar dependencias
pip install numpy pandas scikit-learn scipy nltk matplotlib pytest
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 4. Inicializar la base de datos
python database/connection.py

# 5. Poblar con datos de prueba
cd database
python seed_mock.py
cd ..
```

---

## ▶️ Uso por Fase

### Fase 1 — Validar compatibilidad de un build

```bash
python fase1_compatibilidad/checker.py
```

```python
from fase1_compatibilidad.checker import CompatibilityChecker

checker = CompatibilityChecker()
resultado = checker.validar(
    cpu_id=1, motherboard_id=7, gpu_id=13, gabinete_id=18
)
resultado.imprimir()
```

**Salida:**
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

### Fase 2 — Generar informe de segmentación

```bash
python fase2_segmentacion/informe.py
```

### Fase 3 — Motor de búsqueda semántica interactivo

```bash
python fase3_nlp/motor_busqueda.py --interactivo
```

```
🔍 ¿Qué PC estás buscando? → quiero jugar valorant y hacer diseño gráfico
```

### Fase 4 — Recomendador Next Best Offer

```bash
python fase4_recomendador/recomendador.py
```

**Salida:**
```
============================================================
  🖥️  Seleccionaste: Intel Core i9-14900K
  💰 Precio: $580.00
============================================================
  🔴 RECOMENDACIONES OBLIGATORIAS:
  ⚠️  CPU de alto rendimiento: refrigeración líquida 360mm obligatoria.
  ⚠️  CPU de alto rendimiento: fuente de poder 850W o más requerida.

  📦 Refrigeracion:
     → Corsair iCUE H150i Elite 360mm — $169.00
  📦 Fuente:
     → Corsair RM1000x — $189.00
     → EVGA SuperNOVA 850 G6 — $139.00

  🟡 TAMBIÉN TE PODRÍA INTERESAR:
     → [GPU] NVIDIA RTX 4090 — $1599.00
     → [Motherboard] ASUS ROG Strix Z790-E — $420.00
============================================================
```

---

## 📊 Resultados y Métricas

| Módulo | Métrica | Resultado |
|---|---|---|
| Fase 1 — Checker | Tiempo de consulta | O(1) con matrices NumPy |
| Fase 1 — Checker | Casos de prueba | 5/5 ✅ |
| Fase 2 — K-Means | Silhouette Score | 0.4472 |
| Fase 2 — K-Means | Clientes segmentados | 350 |
| Fase 3 — NLP | Intenciones en diccionario | 80+ términos |
| Fase 3 — NLP | Perfiles detectados | Gamer, Diseñador, Oficina |
| Fase 4 — NBO | Reglas obligatorias | 4 reglas activas |
| Fase 4 — NBO | Arquitectura red neuronal | 3 capas Dense + Dropout |

---

## 🛠️ Stack Tecnológico

| Herramienta | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| NumPy | Matrices binarias de compatibilidad |
| Scikit-learn | Clustering K-Means |
| NLTK + SciPy | Procesamiento de lenguaje natural |
| PyTorch | Modelo de recomendación Deep Learning |
| Pandas | Manejo y análisis de datos |
| Matplotlib | Visualización de clusters |
| SQLite | Base de datos local de desarrollo |
| Pytest | Testing unitario |
| Git + GitHub | Control de versiones |

---

## 🧪 Correr Tests

```bash
pytest tests/test_fase1.py -v
```

---

## 🌿 Ramas del Repositorio

| Rama | Descripción |
|---|---|
| `dev` | Rama principal — código completo y estable |
| `fase2` | Desarrollo Fase 2 — Segmentación K-Means |
| `fase3-nlp` | Desarrollo Fase 3 — NLP y búsqueda semántica |

---

## 👨‍💻 Desarrollado por

**Josias** — Grupo Almerco  
Departamento de Desarrollo de Software / E-commerce  
GitHub: [@Josias45-crypto](https://github.com/Josias45-crypto)

---

## 📄 Licencia

Proyecto privado — Grupo Almerco. Todos los derechos reservados.

---

## 📝 Resumen de ejecución local y errores detectados

Breve registro de las acciones que realicé para poder ejecutar todo el proyecto en mi entorno, por qué falló en tu máquina inicialmente, y cómo solucionarlo.

- Acciones realizadas localmente:
   - Creé/activé un entorno virtual (`.venv`) en la raíz del proyecto.
   - Instalé dependencias necesarias de forma incremental: `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `scipy`, `nltk` y `torch` (cuando fue necesario).
   - Forcé la salida UTF‑8 al ejecutar scripts para evitar errores de codificación con emojis (`PYTHONUTF8=1` o `python -X utf8`).
   - Ejecuté los entregables en orden: `fase1_compatibilidad/checker.py`, `fase2_segmentacion/informe.py`, `fase3_nlp/motor_busqueda.py --interactivo`.

- Errores encontrados (y causas/soluciones):
   1. `bash: sed: command not found` — Mensaje del shell MSYS/Git Bash, no de Python. Solución: instalar utilidades coreutils en MSYS2 o usar PowerShell/CMD.
   2. `ModuleNotFoundError: No module named 'numpy'` — Dependencia faltante; se resolvió instalando `numpy` en el entorno virtual.
   3. `UnicodeEncodeError` al imprimir emojis — Causa: codificación de la consola en Windows (cp1252). Solución: ejecutar con `PYTHONUTF8=1` o `python -X utf8` o reconfigurar la consola a UTF‑8.
   4. `ModuleNotFoundError: No module named 'pandas'` / `No module named 'sklearn'` / `No module named 'nltk'` — Dependencias faltantes; instalarlas vía `pip` en el venv.
   5. `nltk` downloader warnings (Zip Slip blocked) — Mensaje del downloader al intentar escribir recursos; normalmente no impide la ejecución si los recursos ya están instalados. Si hay errores, ejecutar `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"` con conexión a Internet.

- Recomendaciones para ejecutar en Git Bash (Windows):
   ```bash
   # activar venv (Git Bash)
   source .venv/Scripts/activate

   # instalar deps si faltan
   pip install -r requirements.txt

   # ejecutar cada fase (forzar UTF-8 para evitar errores con emojis)
   PYTHONUTF8=1 python fase1_compatibilidad/checker.py
   PYTHONUTF8=1 python fase2_segmentacion/informe.py
   PYTHONUTF8=1 python fase3_nlp/motor_busqueda.py --interactivo
   ```

- Notas importantes:
   - `nltk` necesita bajar recursos la primera vez (requiere conexión a Internet).
   - Si quieres evitar la advertencia de `sed` en Git Bash, instala MSYS2/coreutils o usa PowerShell.

**Nota de ejecución (solicitud del autor): 13**
