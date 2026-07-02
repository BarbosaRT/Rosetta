"use client";

import { useState } from "react";
import InkCanvas from "@/components/InkCanvas";
import LatexView from "@/components/LatexView";
import { recognize } from "@/lib/api";
import type { Ink } from "@/lib/ink";

type Status = "idle" | "busy" | "error";

export default function Home() {
  const [latex, setLatex] = useState<string>("");
  const [status, setStatus] = useState<Status>("idle");
  const [errorMsg, setErrorMsg] = useState<string>("");

  async function handleRecognize(ink: Ink) {
    setStatus("busy");
    setErrorMsg("");
    try {
      const { latex } = await recognize(ink);
      setLatex(latex);
      setStatus("idle");
    } catch (e) {
      const msg = (e as Error).message;
      setErrorMsg(
        msg.includes("501")
          ? "modelo ainda não carregado — defina HMER_CKPT na API"
          : `falha ao reconhecer (${msg})`
      );
      setStatus("error");
    }
  }

  return (
    <main className="page">
      <header className="masthead reveal reveal-1">
        <h1 className="wordmark">
          Rosetta<span className="dot">.</span>
        </h1>
        <span className="masthead-meta">
          tinta <span className="arrow">→</span> latex
        </span>
      </header>

      <div className="reveal reveal-2">
        <InkCanvas onRecognize={handleRecognize} busy={status === "busy"} />
        <div className={`status ${status === "error" ? "error" : ""}`} role="status">
          {status === "busy" && (
            <>
              <span className="status-dot" />
              lendo a tinta…
            </>
          )}
          {status === "error" && errorMsg}
        </div>
      </div>

      <div className="reveal reveal-3">
        <LatexView latex={latex} />
      </div>

      <footer className="colophon">
        <span>tinta online → bigru → transformer → latex</span>
        <span>projeto rosetta</span>
      </footer>
    </main>
  );
}
