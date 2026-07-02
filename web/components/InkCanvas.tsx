"use client";

import { useCallback, useRef, useState } from "react";
import { emptyInk, type Ink, type Point, type Stroke } from "@/lib/ink";

interface Props {
  width: number;
  height: number;
  onRecognize: (ink: Ink) => void;
}

/**
 * Canvas de tinta online.
 *
 * Captura PointerEvents e agrupa em traços no esquema de tinta compartilhado:
 *   pointerdown -> começa um novo Stroke
 *   pointermove -> adiciona Point (x,y relativos ao canvas, t = ms desde o 1º ponto)
 *   pointerup   -> fecha o Stroke
 *
 * A captura é a "verdade"; o <canvas> é só desenho. Assim o payload enviado ao ML é
 * exatamente a trajetória (ADR 0001/0004). Desenho e envio estão implementados aqui;
 * o reconhecimento real depende do modelo (Fase 3).
 */
export default function InkCanvas({ width, height, onRecognize }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const inkRef = useRef<Ink>(emptyInk(width, height));
  const drawingRef = useRef(false);
  const t0Ref = useRef<number>(0);
  const [dirty, setDirty] = useState(false);

  const toPoint = useCallback((e: React.PointerEvent): Point => {
    const rect = canvasRef.current!.getBoundingClientRect();
    if (t0Ref.current === 0) t0Ref.current = performance.now();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
      t: Math.round(performance.now() - t0Ref.current),
    };
  }, []);

  const drawSegment = (a: Point, b: Point) => {
    const ctx = canvasRef.current!.getContext("2d")!;
    ctx.strokeStyle = "#111";
    ctx.lineWidth = 2.5;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  };

  const onPointerDown = (e: React.PointerEvent) => {
    e.currentTarget.setPointerCapture(e.pointerId);
    drawingRef.current = true;
    const stroke: Stroke = { points: [toPoint(e)] };
    inkRef.current.strokes.push(stroke);
    setDirty(true);
  };

  const onPointerMove = (e: React.PointerEvent) => {
    if (!drawingRef.current) return;
    const stroke = inkRef.current.strokes.at(-1)!;
    const prev = stroke.points.at(-1)!;
    const p = toPoint(e);
    stroke.points.push(p);
    drawSegment(prev, p);
  };

  const onPointerUp = (e: React.PointerEvent) => {
    drawingRef.current = false;
    e.currentTarget.releasePointerCapture(e.pointerId);
  };

  const clear = () => {
    const ctx = canvasRef.current!.getContext("2d")!;
    ctx.clearRect(0, 0, width, height);
    inkRef.current = emptyInk(width, height);
    t0Ref.current = 0;
    setDirty(false);
  };

  return (
    <div>
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        className="canvas-surface"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerLeave={onPointerUp}
      />
      <div style={{ marginTop: 12, display: "flex", gap: 8 }}>
        <button onClick={() => onRecognize(inkRef.current)} disabled={!dirty}>
          Reconhecer
        </button>
        <button onClick={clear}>Limpar</button>
      </div>
    </div>
  );
}
