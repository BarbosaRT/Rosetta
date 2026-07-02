// Cliente da API. Passa pelo proxy /api/* (ver next.config.mjs).
import type { Ink } from "./ink";

export interface RecognizeResponse {
  latex: string;
}

export interface EvaluateResponse {
  result?: string;
  error?: string;
}

export async function recognize(ink: Ink): Promise<RecognizeResponse> {
  const res = await fetch("/api/recognize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ink),
  });
  if (!res.ok) {
    // 501 enquanto o modelo não está treinado (stub da API) — tratar na UI.
    throw new Error(`recognize falhou: ${res.status}`);
  }
  return res.json();
}

export async function evaluate(latex: string): Promise<EvaluateResponse> {
  const res = await fetch("/api/evaluate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ latex }),
  });
  if (!res.ok) throw new Error(`evaluate falhou: ${res.status}`);
  return res.json();
}
