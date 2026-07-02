"""Loop de treino do seq2seq (teacher forcing).

Respeita a restrição de 1 GPU de notebook (VRAM ~6-8 GB):
  - AMP (mixed precision)          -> train.amp
  - acumulação de gradiente        -> train.grad_accum
  - bucketing/padding por compr.   -> train.bucket_by_length
  - checkpoint + resume            -> checkpoint.resume

Uso:
  uv run python -m hmer_ml.train --config configs/overfit_crohme.yaml   # Fase 1
  uv run python -m hmer_ml.train --config configs/mathwriting.yaml      # Fase 2
"""

from __future__ import annotations

import argparse

from .utils.config import load_config


def train(cfg) -> None:
    """Orquestra o treino.

    Esqueleto pretendido (Fase 1):
      1. seed everything; escolher device (cuda se disponível).
      2. tokenizer: carregar vocab (ou build_vocab na 1ª vez) → vocab_size, pad_id.
      3. HMERDataset + DataLoader (collate_fn, LengthBucketSampler se bucket_by_length).
      4. build_model(cfg, vocab_size, pad_id).to(device).
      5. otimizador (AdamW) + scheduler (warmup) + GradScaler(enabled=amp).
      6. resume opcional (checkpoint.resume / latest_checkpoint).
      7. laço época→passo:
           - autocast(enabled=amp): logits = model(batch)
           - loss = cross_entropy(logits, tgt_out, ignore_index=pad, label_smoothing)
           - loss/grad_accum; scaler.scale().backward(); a cada grad_accum passos:
             grad_clip, scaler.step, scaler.update, optimizer.zero_grad, scheduler.step
           - salvar checkpoint a cada save_every_steps.
    TODO: implementar na Fase 1. Meta imediata: overfitar o subset e loss→~0.
    """
    raise NotImplementedError


def main() -> None:
    ap = argparse.ArgumentParser(description="Treino HMER online")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    train(cfg)


if __name__ == "__main__":
    main()
