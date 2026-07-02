"""Avaliação opcional de LaTeX via SymPy: LaTeX → resultado.

Usado por POST /evaluate. Melhor esforço: nem toda expressão é avaliável (ex.: integrais
indefinidas retornam forma simbólica; expressões inválidas retornam erro amigável).
"""

from __future__ import annotations

from .schemas import EvaluateResponse


def evaluate_latex(latex: str) -> EvaluateResponse:
    """Converte LaTeX → expressão SymPy e tenta simplificar/calcular.

    TODO(Fase 3):
      - sympy.parsing.latex.parse_latex(latex)  (requer antlr4 runtime).
      - simplify / evalf conforme o tipo; formatar de volta.
      - capturar exceções → EvaluateResponse(error=...).
    """
    try:
        # from sympy.parsing.latex import parse_latex
        # expr = parse_latex(latex)
        # return EvaluateResponse(result=str(sympy.simplify(expr)))
        return EvaluateResponse(error="não implementado (Fase 3)")
    except Exception as e:  # pragma: no cover - scaffold
        return EvaluateResponse(error=str(e))
