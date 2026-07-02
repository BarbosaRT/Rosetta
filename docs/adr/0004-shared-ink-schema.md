# ADR 0004 — Esquema de tinta compartilhado como fonte única

**Status:** aceito

## Contexto
Web captura tinta, API recebe, ML treina/infere. Se cada camada definir seu formato, elas
divergem e treino/inferência deixam de casar.

## Decisão
Um **JSON Schema único** em `schemas/ink.schema.json` define a tinta (traços = listas de
pontos `{x, y, t}`). Espelhado em:
- **web:** `web/lib/ink.ts` (tipos TS)
- **api:** `api/src/hmer_api/schemas.py` (Pydantic)
- **ml:** `ml/src/hmer_ml/data/ink.py` (dataclass + features)

Alinhado ao **InkML** para que o parser de treino produza exatamente a mesma estrutura que
o frontend envia na inferência.

## Consequência
Mudou o contrato? Atualiza-se o `.json` e os três espelhos. `schema_version` versiona o
formato. Encoder e schema permanecem **agnósticos à tarefa** (serve desenhos também).
