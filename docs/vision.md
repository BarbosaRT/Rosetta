# Visão

## O produto
A pessoa **escreve matemática à mão** num canvas; o sistema devolve a expressão em
**LaTeX normalizado** e, quando fizer sentido, o **resultado calculado**. Referência de
experiência: "Math Notes" do iPad.

## Escopo de reconhecimento (do simples ao complexo)
- **Aritmética:** `+ - × ÷`, frações, parênteses, potências, raízes, igualdade.
- **Cálculo e além:** integrais, derivadas, somatórios, limites, letras gregas,
  subscritos/sobrescritos, notação de conjunto.

## Princípio de arquitetura: entrada e encoder agnósticos à tarefa
```
        tinta online (traços/pontos)
                  │
        ┌─────────▼──────────┐
        │  ENCODER DE TINTA  │   (compartilhado, task-agnostic)
        └─────────┬──────────┘
                  │  representação latente
        ┌─────────┴───────────────────────┐
        ▼                                  ▼
 ┌─────────────┐                   ┌────────────────────┐
 │ CABEÇA 1    │                   │ CABEÇA 2 (futuro)  │
 │ decoder     │                   │ classificador de    │
 │ LaTeX (seq) │                   │ desenho (QuickDraw) │
 └─────────────┘                   └────────────────────┘
```
O **esquema de tinta** e o **encoder** não sabem se a tarefa é matemática ou desenho.
Trocar de tarefa = trocar a **cabeça**, não o pipeline de entrada. Isso é requisito, não
"talvez um dia" — ver [`adr/0006-pluggable-heads.md`](adr/0006-pluggable-heads.md).

## Decisões fixas (não reabrir sem perguntar)
1. Entrada = **tinta online** (point/stroke-based), não imagem. Render→imagem é upgrade
   multimodal **futuro**, não caminho principal.
2. Saída = **LaTeX normalizado**.
3. Full-stack monorepo: PyTorch + FastAPI + Next.js.
4. Treino **só local** (ASUS TUF F16, VRAM ~6–8 GB) → tudo dimensionado p/ caber.
5. Extensibilidade p/ desenhos é **requisito de arquitetura**.

## Anotado como futuro (não implementar agora)
- Fusão multimodal (tinta + imagem renderizada).
- Refino da saída por LLM.
