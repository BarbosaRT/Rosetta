// Tipos de tinta — espelho de schemas/ink.schema.json (ADR 0004).
// Mantenha em sincronia com api/schemas.py e ml/data/ink.py.

export interface Point {
  x: number; // relativo ao canvas (CSS px)
  y: number;
  t?: number; // ms desde o 1º ponto da tinta
}

export interface Stroke {
  points: Point[];
}

export interface Ink {
  schema_version?: string; // "1.0"
  width?: number; // dimensões do canvas na captura (p/ normalização no ML)
  height?: number;
  strokes: Stroke[];
  label?: string; // só em coleta/treino; nunca na inferência
}

export const SCHEMA_VERSION = "1.0";

export function emptyInk(width: number, height: number): Ink {
  return { schema_version: SCHEMA_VERSION, width, height, strokes: [] };
}
