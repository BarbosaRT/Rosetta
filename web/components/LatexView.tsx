"use client";

import { useEffect, useRef, useState } from "react";
import katex from "katex";
import { evaluate } from "@/lib/api";

interface Props {
  latex: string;
}

/** Renderiza o LaTeX reconhecido com KaTeX e oferece avaliar via SymPy (opcional). */
export default function LatexView({ latex }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const [result, setResult] = useState<string>("");

  useEffect(() => {
    if (!ref.current) return;
    if (!latex) {
      ref.current.innerHTML = "";
      return;
    }
    try {
      katex.render(latex, ref.current, { throwOnError: false, displayMode: true });
    } catch {
      ref.current.textContent = latex; // fallback: mostra o código cru
    }
  }, [latex]);

  async function onEvaluate() {
    // TODO(Fase 3): habilitar quando /evaluate estiver implementado com SymPy.
    try {
      const r = await evaluate(latex);
      setResult(r.result ?? r.error ?? "");
    } catch (e) {
      setResult((e as Error).message);
    }
  }

  return (
    <section style={{ marginTop: 16 }}>
      <div
        ref={ref}
        style={{ minHeight: 48, background: "var(--panel)", borderRadius: 8, padding: 12 }}
      />
      {latex && (
        <div style={{ marginTop: 8 }}>
          <code style={{ opacity: 0.7 }}>{latex}</code>
          <div style={{ marginTop: 8 }}>
            <button onClick={onEvaluate}>Calcular (SymPy)</button>
            {result && <span style={{ marginLeft: 8 }}>= {result}</span>}
          </div>
        </div>
      )}
    </section>
  );
}
