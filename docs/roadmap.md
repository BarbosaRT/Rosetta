# Roadmap (faseado)

Cada fase é fatiável em várias sessões de treino (checkpoint + resume). Datasets pesados
ficam fora do git.

## Fase 0 — Scaffold + fundação de dados  ← *concluída (falta validar collate com torch)*
- [x] Scaffold do monorepo (ml/api/web/schemas/docs).
- [x] **Esquema de tinta** compartilhado (`schemas/ink.schema.json`) + exemplo.
- [x] Parsing **InkML → tinta** (`ml/data/inkml.py`) + features `[T,6]`, normalize,
      resample (`ml/data/ink.py`). Validado com InkML sintético.
- [x] **Tokenizer** de LaTeX custom: tokenize/build_vocab/encode/decode + especiais;
      CLI `hmer_ml.data.build_vocab`. Round-trip testado.
- [x] `Dataset` + `collate` + `LengthBucketSampler` (`ml/data/dataset.py`);
      `prepare_sample` testável sem torch. **`collate_fn` pende validação com torch.**
- **Saída atingida:** `python -m hmer_ml.data.inkml --stats` roda; `prepare_sample`
  produz features e tokens corretos. Próximo: instalar torch e conferir shapes do batch.

## Fase 1 — Overfit (provar o seq2seq ponta a ponta)
- [ ] Encoder (BiGRU) + Transformer decoder + teacher forcing.
- [ ] **Overfitar um subconjunto minúsculo do CROHME** (dezenas de amostras) até loss ~0.
- [ ] Loop de treino: AMP, grad accum, checkpoint/resume, logging.
- **Saída:** o modelo reproduz o LaTeX das amostras de overfit → seq2seq aprende.

## Fase 2 — Escalar para MathWriting
- [ ] Treinar no CROHME completo, depois MathWriting (humanas + sintéticas).
- [ ] **Augmentation** de tinta (jitter, escala, rotação leve, dropout de pontos).
- [ ] Avaliação: **CER** e **exact match** por expressão; beam search na inferência.
- **Saída:** métricas comparáveis à literatura de HMER online num split de validação.

## Fase 3 — Inferência servida + canvas + render
- [ ] `POST /recognize` carrega checkpoint/ONNX e devolve LaTeX.
- [ ] Canvas Next.js captura PointerEvents → tinta → API → **render KaTeX**.
- [ ] `POST /evaluate` opcional: LaTeX → resultado via **SymPy**.
- **Saída:** desenhar no browser e ver LaTeX + resultado.

## Fase 4 — Extensão para reconhecimento de desenhos
- [ ] Nova **cabeça de classificação** sobre o **mesmo encoder de tinta**.
- [ ] Dataset **QuickDraw** (também tinta online).
- [ ] Config seleciona a cabeça (`head: latex` | `head: sketch_cls`).
- **Saída:** o mesmo encoder serve matemática e "o que está sendo desenhado".

## Explicitamente adiado (não implementar agora)
- Fusão multimodal (tinta + imagem renderizada).
- Refino da saída por LLM.
