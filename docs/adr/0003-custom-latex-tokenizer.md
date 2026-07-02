# ADR 0003 — Tokenizer de LaTeX custom (vocab do dataset)

**Status:** aceito

## Contexto
Precisamos tokenizar LaTeX normalizado para o decoder autorregressivo.

## Decisão
**Tokenizer custom** com vocabulário derivado do dataset: símbolos matemáticos + tokens
sintáticos (`\frac`, `^`, `_`, `{`, `}`, `\int`, gregas, ...) + especiais
`<pad> <bos> <eos> <unk>`. Isolado em `ml/tokenizer/latex_tokenizer.py`.

## Justificativa
LaTeX de matemática tem um conjunto de tokens fechado e bem definido (MathWriting: 244
símbolos + 10 sintáticos). Controle total do vocab evita quebrar `\frac` em subpalavras e
mantém CER/exact-match interpretáveis.

## Alternativa
**SentencePiece/BPE** — útil só se o vocab explodir ou virar texto livre. Mantido em
aberto; a interface do tokenizer (`encode`/`decode`/`vocab_size`) permite trocar depois.
