# schemas/ — contrato único da tinta

`ink.schema.json` (JSON Schema draft-07) é a **fonte única de verdade** do formato de tinta
que trafega entre web, api e ml. Ver [ADR 0004](../docs/adr/0004-shared-ink-schema.md).

## O que o frontend manda para a API (`POST /recognize`)

```jsonc
{
  "schema_version": "1.0",
  "width": 640,             // dimensões do canvas na captura (p/ normalização)
  "height": 360,
  "strokes": [              // 1 traço = 1 pen-down → pen-up
    { "points": [ { "x": 120.0, "y": 180.0, "t": 0 }, ... ] },
    { "points": [ ... ] }
  ]
  // "label" só existe em coleta/treino (LaTeX ground-truth); nunca na inferência
}
```

Exemplo completo em [`ink_example.json`](ink_example.json).

## Regras
- `x`, `y`: **relativos ao canvas**, em CSS px. `t`: ms desde o 1º ponto da tinta (opcional).
- Ordem dos `strokes` e dos `points` é significativa (é a trajetória temporal).
- O flag **pen-up / pen-down** é *implícito*: a fronteira entre `strokes` é um pen-up.
  As features derivadas (delta + flag de estado) são computadas em `ml/data/ink.py`.

## Espelhos (mantenha em sincronia com este arquivo)
| Camada | Arquivo |
|--------|---------|
| web    | `web/lib/ink.ts` |
| api    | `api/src/hmer_api/schemas.py` |
| ml     | `ml/src/hmer_ml/data/ink.py` |
