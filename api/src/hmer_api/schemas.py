"""Modelos Pydantic — espelho de schemas/ink.schema.json (ADR 0004).

Mantenha em sincronia com o JSON Schema e com web/lib/ink.ts e ml/data/ink.py.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float
    y: float
    t: float | None = Field(default=None, description="ms desde o 1º ponto da tinta")


class Stroke(BaseModel):
    points: list[Point] = Field(min_length=1)


class Ink(BaseModel):
    """Corpo de POST /recognize. Igual ao contrato compartilhado."""

    schema_version: str = "1.0"
    width: float | None = None
    height: float | None = None
    strokes: list[Stroke]
    label: str | None = None  # ignorado na inferência


class RecognizeResponse(BaseModel):
    latex: str


class EvaluateRequest(BaseModel):
    latex: str


class EvaluateResponse(BaseModel):
    result: str | None = None
    error: str | None = None
