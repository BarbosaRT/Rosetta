"""Checkpoint com resume — treinos são fatiados em várias sessões (restrição de hardware).

Salva modelo + otimizador + scheduler + scaler(AMP) + passo/época + config + vocab, para
retomar bit-a-bit. Ver docs/roadmap.md (Fase 1).
"""

from __future__ import annotations

from pathlib import Path


def save_checkpoint(path: str | Path, *, model, optimizer, scheduler, scaler, step: int,
                    epoch: int, cfg, extra: dict | None = None) -> None:
    """Salva estado completo p/ resume atômico.

    TODO: torch.save de state_dicts; escrita atômica (arquivo temporário + os.replace).
    """
    raise NotImplementedError


def load_checkpoint(path: str | Path, *, model, optimizer=None, scheduler=None, scaler=None):
    """Carrega estado; retorna (step, epoch). optimizer/scheduler opcionais (só inferência).

    TODO: torch.load(map_location); carregar state_dicts existentes.
    """
    raise NotImplementedError


def latest_checkpoint(dirpath: str | Path) -> Path | None:
    """Retorna o checkpoint mais recente do diretório, ou None. TODO."""
    raise NotImplementedError
