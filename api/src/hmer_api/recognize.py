"""Carregamento preguiçoso do Recognizer (modelo de ML) e ponte com a rota /recognize.

Mantém uma instância única (o modelo carrega uma vez). Configurável por variáveis de
ambiente HMER_CKPT / HMER_CONFIG / HMER_DEVICE.
"""

from __future__ import annotations

import os
from functools import lru_cache

from fastapi import HTTPException


@lru_cache(maxsize=1)
def get_recognizer():
    """Instancia hmer_ml.infer.Recognizer uma vez.

    Enquanto não há checkpoint (Fases 0-2), devolve um stub que retorna 501, para o
    frontend poder ser desenvolvido contra o contrato.
    """
    ckpt = os.getenv("HMER_CKPT")
    config = os.getenv("HMER_CONFIG", "ml/configs/mathwriting.yaml")
    device = os.getenv("HMER_DEVICE", "cpu")

    if not ckpt:
        return _StubRecognizer()

    # TODO(Fase 3): from hmer_ml.infer import Recognizer; return Recognizer(ckpt, config, device)
    from hmer_ml.infer import Recognizer  # noqa: F401

    raise HTTPException(status_code=501, detail="Recognizer real ainda não implementado")


class _StubRecognizer:
    def recognize(self, ink: dict, **kw) -> str:
        raise HTTPException(
            status_code=501,
            detail="Modelo não treinado ainda. Defina HMER_CKPT após a Fase 1/2.",
        )
