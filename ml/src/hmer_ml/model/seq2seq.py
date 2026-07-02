"""InkModel = encoder de tinta (compartilhado) + cabeça (plugável). Ver ADR 0006.

Este é o único lugar que junta encoder + head. `build_model(cfg)` lê a config e monta a
combinação certa (head: latex agora; sketch_cls na Fase 4) — sem que o encoder saiba da
tarefa.
"""

from __future__ import annotations

try:
    import torch.nn as nn
except ImportError:  # pragma: no cover - scaffold
    nn = None

from .encoder import build_encoder
from .heads import build_head


class InkModel(nn.Module if nn else object):
    def __init__(self, encoder, head):
        super().__init__()
        self.encoder = encoder
        self.head = head

    def forward(self, batch):
        """Fluxo genérico: encode a tinta, depois aplica a cabeça.

        TODO:
          memory, mmask = self.encoder(batch["src"], batch["src_mask"])
          - head latex:      return self.head(memory, mmask, batch["tgt_in"])  # logits
          - head sketch_cls: return self.head(memory, mmask)                    # logits cls
        """
        raise NotImplementedError


def build_model(cfg, vocab_size: int | None = None, pad_id: int | None = None) -> InkModel:
    """Monta o modelo a partir da config. Ponto único de composição encoder+head."""
    encoder = build_encoder(cfg)
    head = build_head(cfg, vocab_size=vocab_size, pad_id=pad_id)
    return InkModel(encoder, head)
