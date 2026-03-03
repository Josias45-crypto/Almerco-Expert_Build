# fase4_recomendador/modelo.py
# ============================================================
# Red neuronal PyTorch para recomendación de productos
# Arquitectura: Autoencoder simple
# ============================================================

import sys
import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

ROOT_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FASE4_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, FASE4_DIR)

from dataset import DatasetRecomendador


# ------------------------------------------------------------
# ARQUITECTURA DE LA RED NEURONAL
# ------------------------------------------------------------

class RecomendadorNet(nn.Module):
    """
    Red neuronal feedforward para recomendación.

    Entrada : vector one-hot del producto seleccionado
    Salida  : vector de probabilidades sobre todos los productos

    Arquitectura:
        Input(n_productos) → Dense(128) → ReLU → Dropout
        → Dense(64) → ReLU
        → Dense(n_productos) → Sigmoid
    """

    def __init__(self, n_productos: int):
        super(RecomendadorNet, self).__init__()

        self.red = nn.Sequential(
            nn.Linear(n_productos, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, n_productos),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.red(x)


# ------------------------------------------------------------
# ENTRENADOR
# ------------------------------------------------------------

class EntrenadorModelo:
    """
    Entrena la red neuronal y guarda el modelo.
    """

    def __init__(self, n_epochs: int = 50, lr: float = 0.001):
        self.n_epochs  = n_epochs
        self.lr        = lr
        self.dataset   = DatasetRecomendador()
        self.modelo    = RecomendadorNet(self.dataset.n_productos)
        self.criterio  = nn.BCELoss()
        self.optimizador = optim.Adam(self.modelo.parameters(), lr=self.lr)
        self.historial_loss = []

    def entrenar(self) -> "EntrenadorModelo":
        """Entrena el modelo con los pares generados."""
        print("\n🧠 Entrenando modelo de recomendación...\n")

        df = self.dataset.generar_pares(n_muestras=1000)
        X, y = self.dataset.preparar_tensores(df)

        self.modelo.train()

        for epoch in range(self.n_epochs):
            # Forward pass
            prediccion = self.modelo(X)
            loss       = self.criterio(prediccion, y)

            # Backward pass
            self.optimizador.zero_grad()
            loss.backward()
            self.optimizador.step()

            self.historial_loss.append(loss.item())

            if (epoch + 1) % 10 == 0:
                print(f"  Epoch {epoch+1:3d}/{self.n_epochs} — Loss: {loss.item():.6f}")

        print(f"\n  ✅ Entrenamiento completo.")
        print(f"  ✅ Loss inicial : {self.historial_loss[0]:.6f}")
        print(f"  ✅ Loss final   : {self.historial_loss[-1]:.6f}")

        return self

    def guardar(self, ruta: str = None):
        """Guarda el modelo entrenado en disco."""
        if ruta is None:
            ruta = os.path.join(FASE4_DIR, "modelo_entrenado.pt")

        torch.save({
            "model_state_dict"    : self.modelo.state_dict(),
            "n_productos"         : self.dataset.n_productos,
            "id_a_idx"            : self.dataset.id_a_idx,
            "idx_a_id"            : self.dataset.idx_a_id,
        }, ruta)
        print(f"  ✅ Modelo guardado en: {ruta}")

    def cargar(self, ruta: str = None):
        """Carga un modelo previamente entrenado."""
        if ruta is None:
            ruta = os.path.join(FASE4_DIR, "modelo_entrenado.pt")

        checkpoint = torch.load(ruta, weights_only=False)
        self.modelo = RecomendadorNet(checkpoint["n_productos"])
        self.modelo.load_state_dict(checkpoint["model_state_dict"])
        self.dataset.id_a_idx = checkpoint["id_a_idx"]
        self.dataset.idx_a_id = checkpoint["idx_a_id"]
        print(f"  ✅ Modelo cargado desde: {ruta}")
        return self

    def predecir(self, producto_id: int, top_n: int = 5) -> list:
        """
        Dado un producto_id retorna los top_n productos recomendados.
        """
        self.modelo.eval()

        idx = self.dataset.id_a_idx.get(producto_id)
        if idx is None:
            raise ValueError(f"producto_id={producto_id} no encontrado.")

        # Vector one-hot del producto
        x = torch.zeros(self.dataset.n_productos)
        x[idx] = 1.0

        with torch.no_grad():
            probabilidades = self.modelo(x.unsqueeze(0)).squeeze()

        # Ordenar por probabilidad descendente
        indices_top = torch.argsort(probabilidades, descending=True)

        recomendaciones = []
        for i in indices_top:
            i = i.item()
            if i == idx:
                continue  # No recomendar el mismo producto

            prod_id = self.dataset.idx_a_id.get(i)
            prod    = next((p for p in self.dataset.productos if p["id"] == prod_id), None)

            if prod:
                recomendaciones.append({
                    "id"          : prod["id"],
                    "marca"       : prod["marca"],
                    "modelo"      : prod["modelo"],
                    "categoria"   : prod["categoria"],
                    "precio"      : prod["precio"],
                    "probabilidad": round(probabilidades[i].item(), 4),
                })

            if len(recomendaciones) >= top_n:
                break

        return recomendaciones


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    entrenador = EntrenadorModelo(n_epochs=50)
    entrenador.entrenar()
    entrenador.guardar()

    print("\n🔍 Predicciones para Intel Core i9-14900K (id=1):")
    recs = entrenador.predecir(producto_id=1, top_n=5)
    for r in recs:
        print(f"   → [{r['categoria']}] {r['marca']} {r['modelo']} — ${r['precio']} (prob: {r['probabilidad']})")