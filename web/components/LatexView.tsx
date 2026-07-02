"use client";

import { useEffect, useRef, useState } from "react";
import katex from "katex";
import { evaluate } from "@/lib/api";

interface Props {
  latex: string;
}

/** Resultado: LaTeX renderizado (KaTeX), código-fonte copiável e avaliação via SymPy. */
export default function LatexView({ latex }: Props) {
  const renderRef = useRef<HTMLDivElement>(null);
  const [result, setResult] = useState<string>("");
  const [evalError, setEvalError] = useState<string>("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    setResult("");
    setEvalError("");
    if (!renderRef.current) return;
    if (!latex) {
      renderRef.current.innerHTML = "";
      return;
    }
    try {
      katex.render(latex, renderRef.current, { throwOnError: false, displayMode: true });
      renderRef.current.classList.remove("result-appear");
      void renderRef.current.offsetWidth; // reinicia a animação
      renderRef.current.classList.add("result-appear");
    } catch {
      renderRef.current.textContent = latex; // fallback: código cru
    }
  }, [latex]);

  async function onEvaluate() {
    setEvalError("");
    try {
      const r = await evaluate(latex);
      if (r.result) setResult(r.result);
      else setEvalError(r.error ?? "sem resultado");
    } catch (e) {
      setEvalError((e as Error).message);
    }
  }

  async function onCopy() {
    try {
      await navigator.clipboard.writeText(latex);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard indisponível — silencioso */
    }
  }

  return (
    <section className="result">
      <p className="result-label">resultado</p>

      <div className="result-render" ref={renderRef} />
      {!latex && (
        <p className="result-empty">o LaTeX reconhecido aparecerá aqui —</p>
      )}

      {latex && (
        <>
          <div className="code-row">
            <code>{latex}</code>
            <button className="btn-copy" onClick={onCopy}>
              {copied ? "copiado ✓" : "copiar"}
            </button>
          </div>

          <div className="eval-row">
            <button className="btn btn-ghost" onClick={onEvaluate}>
              calcular
            </button>
            {result && <span className="eval-result">= {result}</span>}
            {evalError && <span className="eval-error">{evalError}</span>}
          </div>
        </>
      )}
    </section>
  );
}
