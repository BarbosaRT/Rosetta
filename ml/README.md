# ml/ — pacote de Machine Learning

Pipeline de HMER online: **InkML → tinta → tensores → seq2seq → LaTeX**.

```
src/hmer_ml/
├── data/         # parsing InkML, esquema de tinta, dataset, augmentation
├── tokenizer/    # tokenizer de LaTeX custom (isolado)
├── model/        # encoder (compartilhado) + heads plugáveis + seq2seq
├── utils/        # config (YAML→dataclass), checkpoint/resume
├── train.py      # loop de treino (AMP, grad accum, resume)
├── evaluate.py   # CER + exact match, beam search
└── infer.py      # tinta → LaTeX (usado pela API)
configs/          # base.yaml, overfit_crohme.yaml, mathwriting.yaml
tests/            # smoke test do formato/shapes
```

## Comandos (uma vez implementado)
```bash
uv run python -m hmer_ml.data.inkml --stats data/crohme/train   # Fase 0
uv run python -m hmer_ml.train --config configs/overfit_crohme.yaml  # Fase 1
uv run python -m hmer_ml.evaluate --config configs/mathwriting.yaml  # Fase 2
```

## Restrições de hardware (ASUS TUF F16, VRAM ~6–8 GB)
Modelo compacto por default, **AMP**, **acumulação de gradiente**, **bucketing/padding**
por comprimento, **checkpoint com resume**. Escalar via config, não via edição de código.
