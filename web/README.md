# web/ — frontend Next.js (App Router)

Canvas onde a pessoa escreve matemática. Captura **PointerEvents** (x, y relativos ao
canvas + timestamp), agrupa em traços no **esquema de tinta compartilhado**, envia à API e
renderiza o LaTeX retornado com **KaTeX**.

```
app/
├── layout.tsx        # root layout
├── page.tsx          # página: canvas + resultado
└── globals.css
components/
├── InkCanvas.tsx     # captura de tinta (pointerdown/move/up → strokes)
└── LatexView.tsx     # render KaTeX + resultado
lib/
├── ink.ts            # tipos TS — espelho de schemas/ink.schema.json
└── api.ts            # fetch /recognize e /evaluate
```

## Rodar
```bash
npm install
npm run dev            # http://localhost:3000
```
`next.config.mjs` faz proxy de `/api/*` → FastAPI (`API_BASE_URL`, default :8000).

> KaTeX precisa do CSS dele. Na Fase 3, importar `katex/dist/katex.min.css` no layout
> (ou servir localmente) — deixado como TODO para não adicionar peso agora.
