# ADR 0005 — Gerenciamento de dependências Python com uv (workspace)

**Status:** aceito

## Decisão
**uv** com **workspace** na raiz (`pyproject.toml`), membros `ml/` e `api/`. Cada pacote
tem seu `pyproject.toml`; o lockfile é compartilhado e reprodutível.

## Justificativa
Rápido, resolve o monorepo Python num só ambiente, lockfile determinístico — importa para
retomar treinos idênticos entre sessões no mesmo notebook.

## Alternativa
**Poetry** (mais lento, ergonomia de workspace inferior) ou **pip + venv** (sem lock
robusto). Trocar depois é possível: dependências ficam declaradas nos `pyproject.toml`.
