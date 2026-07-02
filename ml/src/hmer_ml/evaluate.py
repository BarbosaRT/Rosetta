"""Avaliação: CER (character error rate) e exact match por expressão.

Alinhado à literatura de HMER online. Ver docs/roadmap.md (Fase 2).

Uso:
  uv run python -m hmer_ml.evaluate --config configs/mathwriting.yaml --ckpt <path>
"""

from __future__ import annotations

import argparse

from .utils.config import load_config


def char_error_rate(pred: str, gold: str) -> float:
    """Distância de edição (Levenshtein) normalizada pelo comprimento do gold.

    TODO: implementar edit distance (DP). Definir tokenização do CER (por caractere vs
    por token LaTeX) e documentar a escolha.
    """
    raise NotImplementedError


def exact_match(pred: str, gold: str) -> bool:
    """Igualdade após normalização de LaTeX (espaços, chaves redundantes).

    TODO: normalizar antes de comparar; reutilizar o normalizador do tokenizer.
    """
    raise NotImplementedError


def evaluate(cfg, ckpt: str) -> dict:
    """Roda inferência sobre o split e agrega métricas.

    TODO:
      - carregar tokenizer + modelo (checkpoint).
      - DataLoader do split (eval.split).
      - beam search por amostra (infer.py) → predição.
      - agregar CER médio e exact-match rate; retornar dict de métricas.
    """
    raise NotImplementedError


def main() -> None:
    ap = argparse.ArgumentParser(description="Avaliação HMER (CER, exact match)")
    ap.add_argument("--config", required=True)
    ap.add_argument("--ckpt", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    metrics = evaluate(cfg, args.ckpt)
    print(metrics)


if __name__ == "__main__":
    main()
