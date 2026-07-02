"""Cabeças de saída plugáveis sobre o encoder de tinta compartilhado. Ver ADR 0006.

- LatexHead     -> decoder Transformer autorregressivo (matemática) — AGORA.
- SketchClsHead -> classificador de categoria (QuickDraw) — FUTURO (Fase 4).

Ambas consomem a `memory` produzida pelo InkEncoder e NADA sabem sobre como a tinta foi
codificada. Trocar de tarefa = trocar de cabeça, não de pipeline de entrada.
"""

from __future__ import annotations

try:
    import torch.nn as nn
except ImportError:  # pragma: no cover - scaffold
    nn = None


class LatexHead(nn.Module if nn else object):
    """Transformer decoder autorregressivo → tokens de LaTeX.

    Treino: teacher forcing (feed do alvo deslocado). Inferência: beam search (infer.py).

    TODO:
      - embedding de tokens + positional encoding.
      - nn.TransformerDecoder (cross-attention na memory do encoder).
      - projeção final d_model -> vocab_size.
      - máscara causal + padding masks.
    """

    def __init__(self, d_model: int, vocab_size: int, layers: int, heads: int,
                 ff: int, dropout: float, pad_id: int):
        super().__init__()
        raise NotImplementedError

    def forward(self, memory, memory_mask, tgt_in):
        """Retorna logits [B, L, vocab]. TODO."""
        raise NotImplementedError


class SketchClsHead(nn.Module if nn else object):
    """FUTURO (Fase 4): pooling da memory + MLP → logits de categoria de desenho.

    Deixado explícito para provar que o encoder é reutilizável sem alterações.
    TODO: masked mean/attention pooling + Linear(d_model, num_classes).
    """

    def __init__(self, d_model: int, num_classes: int):
        super().__init__()
        raise NotImplementedError

    def forward(self, memory, memory_mask):
        raise NotImplementedError


def build_head(cfg, vocab_size: int | None = None, pad_id: int | None = None):
    """Fábrica de cabeça pela config (head: latex | sketch_cls)."""
    head = cfg.model.head
    if head == "latex":
        raise NotImplementedError  # return LatexHead(...)
    if head == "sketch_cls":
        raise NotImplementedError  # return SketchClsHead(...)  # Fase 4
    raise ValueError(f"model.head desconhecido: {head}")
