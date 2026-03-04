# app.py
import streamlit as st
import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT_DIR, "database"))
sys.path.insert(0, ROOT_DIR)

st.set_page_config(
    page_title="Almerco Expert-Build",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS PERSONALIZADO
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

/* ── FONDO GENERAL ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #030712;
    color: #e2e8f0;
    font-family: 'Rajdhani', sans-serif;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139,92,246,0.06) 0%, transparent 60%),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 60px,
            rgba(0,212,255,0.015) 60px,
            rgba(0,212,255,0.015) 61px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 60px,
            rgba(0,212,255,0.015) 60px,
            rgba(0,212,255,0.015) 61px
        );
    pointer-events: none;
    z-index: 0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #060b18 100%) !important;
    border-right: 1px solid rgba(0,212,255,0.15) !important;
}

[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, #8b5cf6, transparent);
}

/* ── TÍTULOS ── */
h1 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 900 !important;
    font-size: 2.2rem !important;
    background: linear-gradient(135deg, #00d4ff 0%, #8b5cf6 50%, #06ffa5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px !important;
    margin-bottom: 0.2rem !important;
}

h2, h3 {
    font-family: 'Orbitron', monospace !important;
    color: #00d4ff !important;
    letter-spacing: 1px !important;
}

/* ── CARDS / MÉTRICAS ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(0,212,255,0.05), rgba(139,92,246,0.05));
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 1rem 1.5rem !important;
    position: relative;
    overflow: hidden;
}

[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00d4ff, #8b5cf6);
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    color: #00d4ff !important;
    font-size: 2rem !important;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
}

/* ── BOTONES ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(139,92,246,0.1)) !important;
    border: 1px solid rgba(0,212,255,0.4) !important;
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,212,255,0.25), rgba(139,92,246,0.25)) !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.3), 0 0 40px rgba(0,212,255,0.1) !important;
    transform: translateY(-1px) !important;
}

/* ── SELECTBOX / INPUTS ── */
.stSelectbox > div > div,
.stTextInput > div > div > input {
    background: rgba(0,212,255,0.05) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 10px rgba(0,212,255,0.2) !important;
}

/* ── SLIDER ── */
.stSlider > div > div > div {
    background: rgba(0,212,255,0.2) !important;
}

.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #00d4ff, #8b5cf6) !important;
}

/* ── ALERTS ── */
.stSuccess {
    background: rgba(6,255,165,0.08) !important;
    border: 1px solid rgba(6,255,165,0.3) !important;
    border-radius: 8px !important;
    color: #06ffa5 !important;
}

.stError {
    background: rgba(255,60,60,0.08) !important;
    border: 1px solid rgba(255,60,60,0.3) !important;
    border-radius: 8px !important;
}

.stWarning {
    background: rgba(255,170,0,0.08) !important;
    border: 1px solid rgba(255,170,0,0.3) !important;
    border-radius: 8px !important;
}

.stInfo {
    background: rgba(0,212,255,0.06) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: rgba(0,212,255,0.05) !important;
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    color: #00d4ff !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,212,255,0.15) !important;
    border-radius: 8px !important;
}

/* ── RADIO SIDEBAR ── */
.stRadio > div {
    gap: 0.3rem !important;
}

.stRadio > div > label {
    background: rgba(0,212,255,0.03) !important;
    border: 1px solid rgba(0,212,255,0.1) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-family: 'Rajdhani', sans-serif !important;
    color: #94a3b8 !important;
    transition: all 0.2s ease !important;
}

.stRadio > div > label:hover {
    border-color: rgba(0,212,255,0.4) !important;
    color: #00d4ff !important;
}

/* ── DIVISOR ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent) !important;
    margin: 1.5rem 0 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #030712; }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("""
<div style="text-align:center; padding: 1rem 0 0.5rem;">
    <div style="font-family:'Orbitron',monospace; font-size:1.1rem; font-weight:900;
                background:linear-gradient(135deg,#00d4ff,#8b5cf6);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        ALMERCO
    </div>
    <div style="font-family:'Rajdhani',sans-serif; font-size:0.7rem;
                color:#475569; letter-spacing:3px; text-transform:uppercase;">
        EXPERT-BUILD
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "MÓDULOS",
    [
        "⬡  Inicio",
        "⬡  Compatibilidad",
        "⬡  Segmentación",
        "⬡  Búsqueda NLP",
        "⬡  Recomendador NBO",
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-family:'Rajdhani',sans-serif; font-size:0.7rem;
            color:#334155; text-align:center; letter-spacing:2px;">
    GRUPO ALMERCO © 2026
</div>
""", unsafe_allow_html=True)


# ============================================================
# INICIO
# ============================================================

if "Inicio" in pagina:
    st.markdown("""
    <div style="margin-bottom:0.5rem;">
        <span style="font-family:'Rajdhani',sans-serif; font-size:0.8rem;
                     color:#475569; letter-spacing:4px; text-transform:uppercase;">
            GRUPO ALMERCO — SISTEMA DE VENTAS INTELIGENTE
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.title("EXPERT-BUILD")

    st.markdown("""
    <p style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; color:#64748b;
              letter-spacing:1px; margin-bottom:2rem;">
        Motor de compatibilidad · Segmentación inteligente · NLP · Deep Learning
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Productos", "29")
    with col2:
        st.metric("Clientes", "350")
    with col3:
        st.metric("Intenciones NLP", "80+")
    with col4:
        st.metric("Reglas NBO", "4")

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(0,212,255,0.05),rgba(0,212,255,0.02));
                    border:1px solid rgba(0,212,255,0.2); border-radius:12px; padding:1.5rem;
                    border-top:2px solid #00d4ff;">
            <div style="font-family:'Orbitron',monospace; font-size:0.65rem; color:#00d4ff;
                        letter-spacing:2px; margin-bottom:0.8rem;">FASE 01</div>
            <div style="font-family:'Orbitron',monospace; font-size:0.9rem; color:#e2e8f0;
                        margin-bottom:0.8rem;">COMPATIBILIDAD</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.9rem; color:#64748b;">
                Valida CPU, Motherboard, GPU y Gabinete usando matrices binarias NumPy en tiempo O(1).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(139,92,246,0.05),rgba(139,92,246,0.02));
                    border:1px solid rgba(139,92,246,0.2); border-radius:12px; padding:1.5rem;
                    border-top:2px solid #8b5cf6;">
            <div style="font-family:'Orbitron',monospace; font-size:0.65rem; color:#8b5cf6;
                        letter-spacing:2px; margin-bottom:0.8rem;">FASE 02</div>
            <div style="font-family:'Orbitron',monospace; font-size:0.9rem; color:#e2e8f0;
                        margin-bottom:0.8rem;">SEGMENTACIÓN</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.9rem; color:#64748b;">
                Clasifica clientes en Gamer, Diseñador u Oficina mediante K-Means clustering.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(6,255,165,0.05),rgba(6,255,165,0.02));
                    border:1px solid rgba(6,255,165,0.2); border-radius:12px; padding:1.5rem;
                    border-top:2px solid #06ffa5;">
            <div style="font-family:'Orbitron',monospace; font-size:0.65rem; color:#06ffa5;
                        letter-spacing:2px; margin-bottom:0.8rem;">FASE 03</div>
            <div style="font-family:'Orbitron',monospace; font-size:0.9rem; color:#e2e8f0;
                        margin-bottom:0.8rem;">BÚSQUEDA NLP</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.9rem; color:#64748b;">
                Interpreta consultas en lenguaje natural y filtra el catálogo automáticamente.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(255,170,0,0.05),rgba(255,170,0,0.02));
                    border:1px solid rgba(255,170,0,0.2); border-radius:12px; padding:1.5rem;
                    border-top:2px solid #ffaa00;">
            <div style="font-family:'Orbitron',monospace; font-size:0.65rem; color:#ffaa00;
                        letter-spacing:2px; margin-bottom:0.8rem;">FASE 04</div>
            <div style="font-family:'Orbitron',monospace; font-size:0.9rem; color:#e2e8f0;
                        margin-bottom:0.8rem;">RECOMENDADOR</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.9rem; color:#64748b;">
                Sugiere componentes obligatorios y complementarios con Deep Learning PyTorch.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# COMPATIBILIDAD
# ============================================================

elif "Compatibilidad" in pagina:
    st.markdown('<span style="font-family:Orbitron,monospace;font-size:0.7rem;color:#00d4ff;letter-spacing:3px;">FASE 01</span>', unsafe_allow_html=True)
    st.title("COMPATIBILIDAD")
    st.markdown('<p style="color:#64748b;font-family:Rajdhani,sans-serif;">Selecciona los componentes y valida si son compatibles entre sí.</p>', unsafe_allow_html=True)
    st.markdown("---")

    from fase1_compatibilidad.checker import CompatibilityChecker
    from database.connection import get_connection

    @st.cache_resource
    def cargar_checker():
        return CompatibilityChecker()

    checker = cargar_checker()

    def get_cat(cat):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT p.id, p.marca, p.modelo, p.precio
                FROM productos p JOIN categorias c ON p.categoria_id=c.id
                WHERE c.nombre=? AND p.activo=1
            """, (cat,))
            return cur.fetchall()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div style="color:#00d4ff;font-family:Orbitron,monospace;font-size:0.7rem;letter-spacing:2px;margin-bottom:0.5rem;">CPU</div>', unsafe_allow_html=True)
        cpus = get_cat("CPU")
        cpu_op = {f"{r['marca']} {r['modelo']} — ${r['precio']}": r['id'] for r in cpus}
        cpu_sel = st.selectbox("CPU", list(cpu_op.keys()), label_visibility="collapsed")

        st.markdown('<div style="color:#00d4ff;font-family:Orbitron,monospace;font-size:0.7rem;letter-spacing:2px;margin:1rem 0 0.5rem;">MOTHERBOARD</div>', unsafe_allow_html=True)
        mbs = get_cat("Motherboard")
        mb_op = {f"{r['marca']} {r['modelo']} — ${r['precio']}": r['id'] for r in mbs}
        mb_sel = st.selectbox("MB", list(mb_op.keys()), label_visibility="collapsed")

    with col2:
        st.markdown('<div style="color:#00d4ff;font-family:Orbitron,monospace;font-size:0.7rem;letter-spacing:2px;margin-bottom:0.5rem;">GPU</div>', unsafe_allow_html=True)
        gpus = get_cat("GPU")
        gpu_op = {f"{r['marca']} {r['modelo']} — ${r['precio']}": r['id'] for r in gpus}
        gpu_sel = st.selectbox("GPU", list(gpu_op.keys()), label_visibility="collapsed")

        st.markdown('<div style="color:#00d4ff;font-family:Orbitron,monospace;font-size:0.7rem;letter-spacing:2px;margin:1rem 0 0.5rem;">GABINETE</div>', unsafe_allow_html=True)
        gabs = get_cat("Gabinete")
        gab_op = {f"{r['marca']} {r['modelo']} — ${r['precio']}": r['id'] for r in gabs}
        gab_sel = st.selectbox("GAB", list(gab_op.keys()), label_visibility="collapsed")

    st.markdown("---")

    if st.button("⚡  VALIDAR COMPATIBILIDAD", use_container_width=True):
        resultado = checker.validar(
            cpu_id=cpu_op[cpu_sel],
            motherboard_id=mb_op[mb_sel],
            gpu_id=gpu_op[gpu_sel],
            gabinete_id=gab_op[gab_sel],
        )

        if resultado.es_valido:
            st.success("✅  BUILD COMPATIBLE — Todas las piezas encajan perfectamente.")
        else:
            st.error("❌  BUILD INCOMPATIBLE")
            for e in resultado.errores:
                st.error(e)

        for adv in resultado.advertencias:
            st.warning(adv)


# ============================================================
# SEGMENTACIÓN
# ============================================================

elif "Segmentación" in pagina:
    st.markdown('<span style="font-family:Orbitron,monospace;font-size:0.7rem;color:#8b5cf6;letter-spacing:3px;">FASE 02</span>', unsafe_allow_html=True)
    st.title("SEGMENTACIÓN")
    st.markdown('<p style="color:#64748b;font-family:Rajdhani,sans-serif;">Clasifica el perfil de un cliente según su nivel de interés en cada componente.</p>', unsafe_allow_html=True)
    st.markdown("---")

    from fase2_segmentacion.segmentador import SegmentadorClientes

    @st.cache_resource
    def cargar_seg():
        s = SegmentadorClientes()
        s.entrenar()
        return s

    seg = cargar_seg()

    col1, col2 = st.columns(2)
    with col1:
        gpu    = st.slider("🎮  Interés en GPU",            0.0, 1.0, 0.5, 0.05)
        cpu    = st.slider("💻  Interés en CPU",            0.0, 1.0, 0.5, 0.05)
        ram    = st.slider("🧠  Interés en RAM",            0.0, 1.0, 0.5, 0.05)
    with col2:
        refrig = st.slider("❄️  Interés en Refrigeración", 0.0, 1.0, 0.5, 0.05)
        fuente = st.slider("⚡  Interés en Fuente",         0.0, 1.0, 0.5, 0.05)
        presup = st.slider("💰  Presupuesto (USD)",          100, 3000, 800, 50)

    st.markdown("---")

    if st.button("🔍  CLASIFICAR CLIENTE", use_container_width=True):
        perfil = seg.predecir({
            "interes_gpu": gpu, "interes_cpu": cpu, "interes_ram": ram,
            "interes_refrig": refrig, "interes_fuente": fuente, "presupuesto": presup,
        })

        colores  = {"Gamer": "#ff3c3c", "Disenador": "#8b5cf6", "Oficina": "#00d4ff"}
        iconos   = {"Gamer": "🔴", "Disenador": "🟣", "Oficina": "🔵"}
        descrip  = {
            "Gamer"    : "Alto rendimiento en videojuegos. GPU es la prioridad máxima.",
            "Disenador": "Diseño gráfico y renderizado. CPU y RAM son fundamentales.",
            "Oficina"  : "Uso cotidiano y productividad. Precio y eficiencia ante todo.",
        }
        color = colores.get(perfil, "#00d4ff")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{color}10,{color}05);
                    border:1px solid {color}40; border-left:4px solid {color};
                    border-radius:12px; padding:1.5rem; margin-top:1rem;">
            <div style="font-family:'Orbitron',monospace; font-size:0.7rem;
                        color:{color}; letter-spacing:3px; margin-bottom:0.5rem;">
                PERFIL DETECTADO
            </div>
            <div style="font-family:'Orbitron',monospace; font-size:1.8rem;
                        color:{color}; margin-bottom:0.5rem;">
                {iconos.get(perfil,'')} {perfil.upper()}
            </div>
            <div style="font-family:'Rajdhani',sans-serif; color:#94a3b8; font-size:1rem;">
                {descrip.get(perfil,'')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.7rem;color:#8b5cf6;letter-spacing:2px;margin-bottom:1rem;">DISTRIBUCIÓN DE CLIENTES</div>', unsafe_allow_html=True)
    resumen = seg.resumen()
    st.dataframe(resumen, use_container_width=True)


# ============================================================
# BÚSQUEDA NLP
# ============================================================

elif "NLP" in pagina:
    st.markdown('<span style="font-family:Orbitron,monospace;font-size:0.7rem;color:#06ffa5;letter-spacing:3px;">FASE 03</span>', unsafe_allow_html=True)
    st.title("BÚSQUEDA NLP")
    st.markdown('<p style="color:#64748b;font-family:Rajdhani,sans-serif;">Escribe en lenguaje natural. El sistema detecta tus intenciones y filtra el catálogo.</p>', unsafe_allow_html=True)
    st.markdown("---")

    from fase3_nlp.buscador import Buscador

    @st.cache_resource
    def cargar_buscador():
        return Buscador()

    buscador = cargar_buscador()

    ejemplos = [
        "PC potente para renderizar 4K",
        "Computadora barata para oficina",
        "Gaming y streaming",
        "Diseño gráfico en Photoshop",
        "Programar y correr Docker",
    ]

    st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.7rem;color:#06ffa5;letter-spacing:2px;margin-bottom:0.8rem;">¿QUÉ PC ESTÁS BUSCANDO?</div>', unsafe_allow_html=True)
    consulta = st.text_input("", placeholder="Ej: quiero jugar valorant y hacer streaming...", label_visibility="collapsed")

    st.markdown('<div style="font-family:Rajdhani,sans-serif;font-size:0.8rem;color:#475569;letter-spacing:2px;margin:0.8rem 0 0.5rem;">EJEMPLOS RÁPIDOS</div>', unsafe_allow_html=True)
    cols = st.columns(len(ejemplos))
    for i, ej in enumerate(ejemplos):
        if cols[i].button(ej, key=f"ej{i}"):
            consulta = ej

    if consulta:
        resultado = buscador.buscar(consulta)
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            perfil = resultado['perfil_detectado']
            colores_p = {"Gamer": "#ff3c3c", "Disenador": "#8b5cf6", "Oficina": "#00d4ff"}
            c = colores_p.get(perfil, "#00d4ff")
            st.markdown(f'<div style="font-family:Rajdhani,sans-serif;font-size:1rem;color:#94a3b8;">Perfil detectado: <span style="color:{c};font-family:Orbitron,monospace;font-size:0.8rem;">{perfil}</span></div>', unsafe_allow_html=True)
        with col2:
            intenciones = ', '.join(resultado['intenciones']) if resultado['intenciones'] else 'ninguna'
            st.markdown(f'<div style="font-family:Rajdhani,sans-serif;font-size:1rem;color:#94a3b8;">Intenciones: <span style="color:#06ffa5;">{intenciones}</span></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.7rem;color:#06ffa5;letter-spacing:2px;margin-bottom:1rem;">PRODUCTOS RECOMENDADOS</div>', unsafe_allow_html=True)

        for categoria, datos in resultado["resultados_por_categoria"].items():
            if datos["productos"]:
                with st.expander(f"📦  {categoria}  —  Prioridad: {datos['prioridad']}", expanded=True):
                    for p in datos["productos"]:
                        st.markdown(f"**{p['marca']} {p['modelo']}** — `${p['precio']:.2f}`")


# ============================================================
# RECOMENDADOR NBO
# ============================================================

elif "NBO" in pagina:
    st.markdown('<span style="font-family:Orbitron,monospace;font-size:0.7rem;color:#ffaa00;letter-spacing:3px;">FASE 04</span>', unsafe_allow_html=True)
    st.title("RECOMENDADOR NBO")
    st.markdown('<p style="color:#64748b;font-family:Rajdhani,sans-serif;">Selecciona un producto y recibe recomendaciones obligatorias y complementarias.</p>', unsafe_allow_html=True)
    st.markdown("---")

    from fase4_recomendador.recomendador import RecomendadorNBO
    from database.connection import get_connection

    @st.cache_resource
    def cargar_rec():
        return RecomendadorNBO()

    rec = cargar_rec()

    def get_todos():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT p.id, p.marca, p.modelo, p.precio, c.nombre as categoria
                FROM productos p JOIN categorias c ON p.categoria_id=c.id
                WHERE p.activo=1 ORDER BY c.nombre, p.precio DESC
            """)
            return cur.fetchall()

    prods   = get_todos()
    opciones = {f"[{r['categoria']}]  {r['marca']} {r['modelo']} — ${r['precio']}": r['id'] for r in prods}

    st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.7rem;color:#ffaa00;letter-spacing:2px;margin-bottom:0.5rem;">SELECCIONA UN PRODUCTO</div>', unsafe_allow_html=True)
    prod_sel = st.selectbox("", list(opciones.keys()), label_visibility="collapsed")

    if st.button("🎯  VER RECOMENDACIONES", use_container_width=True):
        resultado = rec.recomendar(opciones[prod_sel])

        if "error" in resultado:
            st.error(resultado["error"])
        else:
            prod = resultado["producto_seleccionado"]
            st.markdown(f"""
            <div style="background:rgba(255,170,0,0.05);border:1px solid rgba(255,170,0,0.2);
                        border-left:4px solid #ffaa00;border-radius:12px;padding:1.2rem;margin-bottom:1.5rem;">
                <div style="font-family:'Orbitron',monospace;font-size:0.65rem;color:#ffaa00;letter-spacing:2px;">PRODUCTO SELECCIONADO</div>
                <div style="font-family:'Orbitron',monospace;font-size:1.1rem;color:#e2e8f0;margin-top:0.3rem;">
                    {prod['marca']} {prod['modelo']}
                </div>
                <div style="font-family:'Rajdhani',sans-serif;color:#64748b;">${prod['precio']:.2f} — {prod['categoria']}</div>
            </div>
            """, unsafe_allow_html=True)

            if resultado["obligatorios"]:
                st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.7rem;color:#ff3c3c;letter-spacing:2px;margin-bottom:0.8rem;">🔴 OBLIGATORIO</div>', unsafe_allow_html=True)
                for msg in resultado["mensajes"]:
                    st.warning(msg)
                for r in resultado["obligatorios"]:
                    st.markdown(f'<div style="font-family:Orbitron,monospace;font-size:0.65rem;color:#ff3c3c;letter-spacing:1px;margin:0.8rem 0 0.3rem;">📦 {r["categoria"]}</div>', unsafe_allow_html=True)
                    for p in r["productos"]:
                        st.markdown(f"**{p['marca']} {p['modelo']}** — `${p['precio']:.2f}`")
            else:
                st.success("✅  Sin recomendaciones obligatorias para este producto.")

            if resultado["sugeridos"]:
                st.markdown("---")
                st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.7rem;color:#ffaa00;letter-spacing:2px;margin-bottom:0.8rem;">🟡 TAMBIÉN TE PODRÍA INTERESAR</div>', unsafe_allow_html=True)
                cols = st.columns(len(resultado["sugeridos"]))
                for i, s in enumerate(resultado["sugeridos"]):
                    with cols[i]:
                        st.metric(s["categoria"], f"${s['precio']:.2f}")
                        st.markdown(f"**{s['marca']}** {s['modelo']}")