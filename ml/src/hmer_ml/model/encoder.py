"""Encoder de tinta — AGNÓSTICO À TAREFA. Único ponto de reuso entre matemática e desenhos.

REGRA (ADR 0006): nenhum símbolo de LaTeX / conceito de tarefa pode entrar aqui. A
interface é `forward(features, mask) -> (memory, memory_mask)`. Serve tanto ao decoder
LaTeX quanto, no futuro, ao classificador de desenhos.
"""

from __future__ import annotations

try:
    import torch.nn as nn
except ImportError:  # pragma: no cover - scaffold
    nn = None


class InkEncoder(nn.Module if nn else object):
    """Base comum. Implementações concretas: BiGRUEncoder, TransformerInkEncoder."""

    def forward(self, features, mask):
        raise NotImplementedError


class BiGRUEncoder(InkEncoder):
    """Encoder recorrente (default). Cabe folgado em VRAM ~6-8 GB. Ver ADR 0002.

    TODO:
      - projeção linear in_features -> d_model.
      - nn.GRU(bidirectional=True, num_layers, dropout).
      - projetar hidden*2 -> d_model se bidirecional.
      - respeitar padding (pack_padded_sequence).
    """

    def __init__(self, in_features: int, d_model: int, hidden: int, layers: int,
                 dropout: float, bidirectional: bool = True):
        super().__init__()
        raise NotImplementedError


class TransformerInkEncoder(InkEncoder):
    """Alternativa escalável (mais VRAM). Selecionada por config encoder.type=transformer.

    TODO: projeção in_features->d_model + positional encoding + nn.TransformerEncoder.
    """

    def __init__(self, in_features: int, d_model: int, layers: int, heads: int,
                 ff: int, dropout: float):
        super().__init__()
        raise NotImplementedError


def build_encoder(cfg) -> InkEncoder:
    """Fábrica: escolhe a implementação pela config (bigru | transformer)."""
    etype = cfg.model.encoder.type
    if etype == "bigru":
        raise NotImplementedError  # return BiGRUEncoder(...)
    if etype == "transformer":
        raise NotImplementedError  # return TransformerInkEncoder(...)
    raise ValueError(f"encoder.type desconhecido: {etype}")
