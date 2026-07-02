"""App FastAPI: monta rotas e carrega o modelo no startup.

Fase 0/scaffold: as rotas existem e validam o contrato, mas devolvem 501 até haver
checkpoint treinado (Fase 3).
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .evaluate import evaluate_latex
from .recognize import get_recognizer
from .schemas import (
    EvaluateRequest,
    EvaluateResponse,
    Ink,
    RecognizeResponse,
)

app = FastAPI(title="HMER API", version="0.0.0")

# CORS liberado p/ o dev do Next.js (localhost:3000). Restringir em produção.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/recognize", response_model=RecognizeResponse)
def recognize(ink: Ink) -> RecognizeResponse:
    """Tinta → LaTeX. Delega ao Recognizer (hmer_ml.infer)."""
    recognizer = get_recognizer()
    latex = recognizer.recognize(ink.model_dump())
    return RecognizeResponse(latex=latex)


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest) -> EvaluateResponse:
    """LaTeX → resultado numérico/simbólico via SymPy (opcional)."""
    return evaluate_latex(req.latex)
