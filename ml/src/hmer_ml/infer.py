"""Inferência: tinta (Ink / dict do esquema compartilhado) → LaTeX. Usado pela API.

Beam search sobre a LatexHead. Mantém a MESMA representação de tinta do treino (parse →
features), garantindo consistência treino/inferência (ADR 0004).
"""

from __future__ import annotations

from .data.ink import Ink


class Recognizer:
    """Carrega tokenizer + modelo uma vez e reconhece tinta sob demanda.

    A API instancia isto no startup (carregando checkpoint ou ONNX) e chama `.recognize`.
    """

    def __init__(self, ckpt_path: str, config_path: str, device: str = "cpu"):
        # TODO: load_config; carregar tokenizer (vocab); build_model + load_checkpoint;
        #       model.eval(); mover p/ device. Opcional: caminho ONNX Runtime.
        self.ckpt_path = ckpt_path
        self.config_path = config_path
        self.device = device

    def recognize(self, ink: Ink | dict, beam_size: int = 4, max_len: int = 256) -> str:
        """Retorna o LaTeX reconhecido.

        TODO:
          - aceitar dict do esquema → Ink.from_dict.
          - normalize/resample + ink_to_features → tensor [1, T, F].
          - encoder → memory; beam_search(head, memory, bos/eos) → ids.
          - tokenizer.decode(ids) → LaTeX.
        """
        raise NotImplementedError


def beam_search(head, memory, memory_mask, *, bos_id: int, eos_id: int,
                beam_size: int, max_len: int):
    """Beam search autorregressivo genérico sobre uma cabeça seq. TODO."""
    raise NotImplementedError
