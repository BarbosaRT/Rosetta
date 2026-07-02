# ADR 0006 — Encoder compartilhado + cabeças de saída plugáveis

**Status:** aceito (requisito de arquitetura)

## Contexto
Visão de longo prazo: estender o pipeline para **reconhecer desenhos** (estilo QuickDraw)
reusando a entrada de tinta e o encoder.

## Decisão
Separar explicitamente:
- **Encoder de tinta** (`model/encoder.py`) — task-agnostic, único ponto de reuso.
- **Cabeças** (`model/heads.py`):
  - `LatexHead` = Transformer decoder autorregressivo (matemática) — **agora**.
  - `SketchClsHead` = classificador de categoria (QuickDraw) — **futuro (Fase 4)**.
- `Seq2Seq`/`InkModel` (`model/seq2seq.py`) compõe `encoder + head` conforme a config
  (`head: latex | sketch_cls`).

## Justificativa
Torna a extensibilidade um **contrato de código e de config**, não uma intenção. Evita dois
modelos paralelos e mantém o encoder como ativo reutilizável.

## Consequência
Nenhum símbolo de LaTeX pode vazar para dentro do encoder. Testes garantem que
`encoder.encode(ink)` não depende da tarefa.
