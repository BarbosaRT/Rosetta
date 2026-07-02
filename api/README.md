# api/ — serviço FastAPI

Ponte entre o canvas (web) e o modelo (ml).

## Endpoints
| Método | Rota         | Entrada                          | Saída                          |
|--------|--------------|----------------------------------|--------------------------------|
| POST   | `/recognize` | tinta (esquema compartilhado)    | `{ "latex": "x^2" }`           |
| POST   | `/evaluate`  | `{ "latex": "1+1" }` (opcional)  | `{ "result": "2", ... }` SymPy |
| GET    | `/health`    | —                                | `{ "status": "ok" }`           |

O corpo de `/recognize` segue **`schemas/ink.schema.json`** (espelhado em `schemas.py`).

## Rodar
```bash
uv run uvicorn hmer_api.main:app --reload --port 8000
```

O modelo é carregado no startup via `hmer_ml.infer.Recognizer` (checkpoint/ONNX). Sem
checkpoint treinado ainda → endpoints devolvem stub/501 até a Fase 3.
