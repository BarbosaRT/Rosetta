"""Blocos de decodificação reutilizados por LatexHead.

Separado de heads.py para manter a cabeça enxuta e permitir reuso (ex.: futuras cabeças
seq2seq para outras notações). Ver ADR 0006.
"""

from __future__ import annotations

try:
    import torch.nn as nn
except ImportError:  # pragma: no cover - scaffold
    nn = None


class PositionalEncoding(nn.Module if nn else object):
    """Positional encoding senoidal (ou aprendido). TODO."""

    def __init__(self, d_model: int, max_len: int = 4096):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError


def causal_mask(size: int):
    """Máscara triangular p/ atenção autorregressiva. TODO (torch.triu)."""
    raise NotImplementedError
