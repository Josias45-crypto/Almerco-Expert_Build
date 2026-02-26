# fase2_segmentacion/segmentador.py
# ============================================================
# Aplica K-Means clustering para segmentar clientes
# Herramienta: Scikit-learn
# ============================================================

import sys
import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

ROOT_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE2_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, FASE2_DIR)

from fase2_segmentacion.data_builder import cargar_datos_mock
from fase2_segmentacion.perfiles import clasificar_cluster, obtener_perfil, FEATURE_NOMBRES


# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------

N_CLUSTERS   = 3       # Gamer, Diseñador, Oficina
RANDOM_STATE = 42      # Reproducibilidad


# ------------------------------------------------------------
# CLASE PRINCIPAL
# ------------------------------------------------------------

class SegmentadorClientes:
    """
    Aplica K-Means sobre los datos de comportamiento
    y clasifica cada cliente en un perfil.
    """

    def __init__(self, n_clusters: int = N_CLUSTERS):
        self.n_clusters = n_clusters
        self.scaler     = StandardScaler()
        self.modelo     = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
        self.df         = None
        self.df_result  = None
        self.centroides = None
        self.mapa_cluster_perfil = {}   # cluster_id → nombre perfil

    # ----------------------------------------------------------
    # ENTRENAMIENTO
    # ----------------------------------------------------------

    def entrenar(self, df: pd.DataFrame = None) -> "SegmentadorClientes":
        """
        Carga datos, escala features, aplica K-Means
        y mapea cada cluster a un perfil de cliente.
        """
        # Cargar datos si no se pasan
        if df is None:
            df = cargar_datos_mock()
        self.df = df.copy()

        print("🔧 Entrenando modelo K-Means...\n")

        # 1. Extraer solo las features numéricas
        X = self.df[FEATURE_NOMBRES + ["presupuesto"]].values

        # 2. Escalar los datos (importante para K-Means)
        X_scaled = self.scaler.fit_transform(X)

        # 3. Aplicar K-Means
        self.df["cluster"] = self.modelo.fit_predict(X_scaled)

        # 4. Calcular centroides en escala original
        self.centroides = self.scaler.inverse_transform(self.modelo.cluster_centers_)

        # 5. Mapear cada cluster a un perfil
        self._mapear_clusters_a_perfiles()

        # 6. Asignar nombre de perfil a cada cliente
        self.df["perfil_asignado"] = self.df["cluster"].map(self.mapa_cluster_perfil)

        # 7. Calcular métricas
        score = silhouette_score(X_scaled, self.df["cluster"])
        print(f"  ✅ Silhouette Score: {score:.4f}  (entre -1 y 1, más alto es mejor)")
        print(f"  ✅ Clusters encontrados: {self.n_clusters}")
        print(f"  ✅ Clientes procesados: {len(self.df)}\n")

        self.df_result = self.df
        return self

    def _mapear_clusters_a_perfiles(self):
        """
        Compara cada centroide con los perfiles definidos
        y asigna el perfil más cercano a cada cluster.
        """
        features_con_presupuesto = FEATURE_NOMBRES + ["presupuesto"]

        for cluster_id in range(self.n_clusters):
            centroide_valores = self.centroides[cluster_id]
            centroide_dict    = dict(zip(features_con_presupuesto, centroide_valores))

            # clasificar_cluster solo usa FEATURE_NOMBRES (sin presupuesto)
            perfil = clasificar_cluster(centroide_dict)
            self.mapa_cluster_perfil[cluster_id] = perfil

        print("  📊 Mapeo cluster → perfil:")
        for cluster_id, perfil in self.mapa_cluster_perfil.items():
            print(f"     Cluster {cluster_id} → {perfil}")
        print()

    # ----------------------------------------------------------
    # PREDICCIÓN
    # ----------------------------------------------------------

    def predecir(self, datos_cliente: dict) -> str:
        """
        Dado un dict con el comportamiento de un cliente nuevo,
        retorna el perfil que le corresponde.

        Args:
            datos_cliente: {
                'interes_gpu': 0.9,
                'interes_cpu': 0.7,
                'interes_ram': 0.6,
                'interes_refrig': 0.7,
                'interes_fuente': 0.8,
                'presupuesto': 1200
            }

        Returns:
            Nombre del perfil: 'Gamer', 'Disenador' o 'Oficina'
        """
        features = FEATURE_NOMBRES + ["presupuesto"]
        X_nuevo  = np.array([[datos_cliente[f] for f in features]])
        X_scaled = self.scaler.transform(X_nuevo)
        cluster  = self.modelo.predict(X_scaled)[0]
        return self.mapa_cluster_perfil[cluster]

    # ----------------------------------------------------------
    # RESUMEN
    # ----------------------------------------------------------

    def resumen(self) -> pd.DataFrame:
        """Retorna estadísticas por perfil asignado."""
        if self.df_result is None:
            raise RuntimeError("Primero debes llamar a entrenar()")

        resumen = self.df_result.groupby("perfil_asignado").agg(
            total_clientes  = ("cliente_id", "count"),
            presupuesto_avg = ("presupuesto", "mean"),
            presupuesto_min = ("presupuesto", "min"),
            presupuesto_max = ("presupuesto", "max"),
            interes_gpu_avg = ("interes_gpu", "mean"),
            interes_cpu_avg = ("interes_cpu", "mean"),
            interes_ram_avg = ("interes_ram", "mean"),
        ).round(3)

        return resumen


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    segmentador = SegmentadorClientes()
    segmentador.entrenar()

    print("📊 Resumen por perfil:\n")
    print(segmentador.resumen().to_string())

    # Predicción de un cliente nuevo
    print("\n🔍 Predicción cliente nuevo (perfil esperado: Gamer):")
    perfil = segmentador.predecir({
        "interes_gpu":    0.90,
        "interes_cpu":    0.70,
        "interes_ram":    0.65,
        "interes_refrig": 0.70,
        "interes_fuente": 0.75,
        "presupuesto":    1400,
    })
    print(f"   → Perfil asignado: {perfil}")

    print("\n🔍 Predicción cliente nuevo (perfil esperado: Oficina):")
    perfil = segmentador.predecir({
        "interes_gpu":    0.15,
        "interes_cpu":    0.40,
        "interes_ram":    0.35,
        "interes_refrig": 0.20,
        "interes_fuente": 0.30,
        "presupuesto":    350,
    })
    print(f"   → Perfil asignado: {perfil}")