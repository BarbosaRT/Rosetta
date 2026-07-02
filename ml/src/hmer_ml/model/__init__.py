"""Modelo: encoder de tinta compartilhado + cabeças plugáveis. Ver ADR 0006."""

from .seq2seq import InkModel, build_model

__all__ = ["InkModel", "build_model"]
