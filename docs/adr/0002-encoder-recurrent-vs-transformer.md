# ADR 0002 — Encoder: BiGRU por default, Transformer como alternativa escalável

**Status:** aceito (default reversível via config)

## Contexto
Encoder sobre a sequência de pontos/traços. Restrição dura: treino em **1 GPU de notebook,
VRAM ~6–8 GB**. Precisa ser reaproveitado no reconhecimento de desenhos.

## Decisão
Default = **BiGRU** (2 camadas, `d_model` moderado). Interface do encoder **desacoplada da
tarefa** (`encode(ink) -> memory, mask`), sem nada específico de LaTeX.

## Justificativa
BiGRU cabe folgado na VRAM, treina estável em sequências longas de tinta e tem menos
memória de ativação que atenção quadrática. Adequado para a fase de prova.

## Alternativa
**Transformer encoder leve** — melhor em dependências longas, mais faminto de VRAM.
Selecionável por config (`encoder.type: transformer`) para escalar na Fase 2+.
