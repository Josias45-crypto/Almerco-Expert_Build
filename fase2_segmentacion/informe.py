# fase2_segmentacion/informe.py
# ============================================================
# ENTREGABLE FASE 2 — Informe de Perfiles de Cliente
# Genera un reporte completo de la segmentación K-Means
# ============================================================

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

ROOT_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE2_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, FASE2_DIR)

from fase2_segmentacion.segmentador import SegmentadorClientes
from fase2_segmentacion.perfiles import PERFILES, FEATURE_NOMBRES

# Carpeta donde se guardan los reportes
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# COLORES POR PERFIL
# ------------------------------------------------------------

COLORES = {
    "Gamer":     "#e74c3c",
    "Disenador": "#9b59b6",
    "Oficina":   "#3498db",
}


# ------------------------------------------------------------
# GENERADOR DE INFORME
# ------------------------------------------------------------

class InformeSegmentacion:

    def __init__(self):
        self.segmentador = SegmentadorClientes()
        self.segmentador.entrenar()
        self.df = self.segmentador.df_result

    # ----------------------------------------------------------
    # 1. RESUMEN EN CONSOLA
    # ----------------------------------------------------------

    def imprimir_resumen(self):
        print("\n" + "="*60)
        print("   INFORME DE SEGMENTACIÓN — GRUPO ALMERCO")
        print(f"   Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("="*60)

        for perfil_nombre, perfil in PERFILES.items():
            subset = self.df[self.df["perfil_asignado"] == perfil_nombre]
            if subset.empty:
                continue

            print(f"\n{'─'*60}")
            print(f"  👤 Perfil: {perfil_nombre}")
            print(f"  {perfil.descripcion}")
            print(f"{'─'*60}")
            print(f"  Total clientes   : {len(subset)}")
            print(f"  Presupuesto avg  : ${subset['presupuesto'].mean():.2f}")
            print(f"  Presupuesto rango: ${subset['presupuesto'].min():.0f} — ${subset['presupuesto'].max():.0f}")
            print(f"  Interés GPU avg  : {subset['interes_gpu'].mean():.2f}")
            print(f"  Interés CPU avg  : {subset['interes_cpu'].mean():.2f}")
            print(f"  Interés RAM avg  : {subset['interes_ram'].mean():.2f}")
            print(f"  Categorías clave : {', '.join(perfil.categorias_clave)}")

        print("\n" + "="*60)

    # ----------------------------------------------------------
    # 2. GRÁFICO 1 — Distribución de clientes por perfil
    # ----------------------------------------------------------

    def grafico_distribucion(self):
        conteo = self.df["perfil_asignado"].value_counts()
        colores = [COLORES[p] for p in conteo.index]

        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.bar(conteo.index, conteo.values, color=colores, edgecolor="white", linewidth=1.5)

        # Etiquetas encima de cada barra
        for bar, valor in zip(bars, conteo.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                    str(valor), ha="center", va="bottom", fontweight="bold", fontsize=12)

        ax.set_title("Distribución de Clientes por Perfil", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Perfil", fontsize=12)
        ax.set_ylabel("Cantidad de Clientes", fontsize=12)
        ax.set_ylim(0, conteo.max() + 30)
        ax.spines[["top", "right"]].set_visible(False)

        plt.tight_layout()
        ruta = os.path.join(OUTPUT_DIR, "grafico_distribucion.png")
        plt.savefig(ruta, dpi=150)
        plt.close()
        print(f"  ✅ Gráfico guardado: {ruta}")

    # ----------------------------------------------------------
    # 3. GRÁFICO 2 — Radar de intereses por perfil
    # ----------------------------------------------------------

    def grafico_radar(self):
        import numpy as np

        categorias   = ["GPU", "CPU", "RAM", "Refrigeración", "Fuente"]
        n_categorias = len(categorias)
        angulos      = [n / float(n_categorias) * 2 * 3.14159 for n in range(n_categorias)]
        angulos     += angulos[:1]  # cerrar el polígono

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

        for perfil_nombre in PERFILES:
            subset = self.df[self.df["perfil_asignado"] == perfil_nombre]
            if subset.empty:
                continue

            valores = [
                subset["interes_gpu"].mean(),
                subset["interes_cpu"].mean(),
                subset["interes_ram"].mean(),
                subset["interes_refrig"].mean(),
                subset["interes_fuente"].mean(),
            ]
            valores += valores[:1]

            ax.plot(angulos, valores, color=COLORES[perfil_nombre], linewidth=2, label=perfil_nombre)
            ax.fill(angulos, valores, color=COLORES[perfil_nombre], alpha=0.15)

        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=11)
        ax.set_ylim(0, 1)
        ax.set_title("Intereses por Perfil de Cliente", fontsize=14, fontweight="bold", pad=20)
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

        plt.tight_layout()
        ruta = os.path.join(OUTPUT_DIR, "grafico_radar.png")
        plt.savefig(ruta, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  ✅ Gráfico guardado: {ruta}")

    # ----------------------------------------------------------
    # 4. EXPORTAR CSV
    # ----------------------------------------------------------

    def exportar_csv(self):
        ruta = os.path.join(OUTPUT_DIR, "clientes_segmentados.csv")
        self.df.to_csv(ruta, index=False)
        print(f"  ✅ CSV exportado: {ruta}")

    # ----------------------------------------------------------
    # GENERAR TODO
    # ----------------------------------------------------------

    def generar(self):
        print("\n📊 Generando informe completo...\n")
        self.imprimir_resumen()
        self.grafico_distribucion()
        self.grafico_radar()
        self.exportar_csv()
        print("\n✅ Informe generado exitosamente.\n")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    informe = InformeSegmentacion()
    informe.generar()