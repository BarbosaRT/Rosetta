# ADR 0001 — Entrada é tinta online, não imagem

**Status:** aceito (decisão fixa do projeto)

## Contexto
HMER pode consumir imagem rasterizada (offline) ou trajetória da caneta (online).

## Decisão
Entrada = **tinta online**: sequência de traços/pontos `{x, y, t}`. O modelo consome a
trajetória diretamente, no espírito do HMER online.

## Consequência
- Precisamos de features de online handwriting: `(x,y)` normalizados, `(dx,dy)`, flag pen.
- Datasets em **InkML** (MathWriting, CROHME) encaixam naturalmente.
- Render tinta→imagem fica como **upgrade multimodal futuro**, não caminho principal.
