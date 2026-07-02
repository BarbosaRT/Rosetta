"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { emptyInk, type Ink, type Point, type Stroke } from "@/lib/ink";

interface Props {
  onRecognize: (ink: Ink) => void;
  busy?: boolean;
}

const PEN_COLOR = "#2a3670"; // tinta azul-preta (--pen)
const PEN_WIDTH = 2.25;
const ASPECT = 0.52; // altura = largura * ASPECT

/**
 * Folha de escrita (canvas de tinta online).
 *
 * A captura é a "verdade"; o <canvas> é só desenho (ADR 0001/0004):
 *   pointerdown → novo Stroke · pointermove → Point {x, y, t} · pointerup → fecha.
 *
 * Extras de qualidade: nitidez em HiDPI (devicePixelRatio), redesenho a partir da
 * própria tinta (permite desfazer e redimensionar sem perder traços).
 */
export default function InkCanvas({ onRecognize, busy = false }: Props) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const inkRef = useRef<Ink>(emptyInk(0, 0));
  const drawingRef = useRef(false);
  const t0Ref = useRef<number>(0);
  const [strokeCount, setStrokeCount] = useState(0);

  const ctx = () => canvasRef.current!.getContext("2d")!;

  /** Redesenha toda a tinta (fonte da verdade) no canvas. */
  const redraw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const c = ctx();
    const dpr = window.devicePixelRatio || 1;
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.clearRect(0, 0, canvas.width / dpr, canvas.height / dpr);
    c.strokeStyle = PEN_COLOR;
    c.lineWidth = PEN_WIDTH;
    c.lineCap = "round";
    c.lineJoin = "round";
    for (const s of inkRef.current.strokes) {
      if (s.points.length === 0) continue;
      c.beginPath();
      c.moveTo(s.points[0].x, s.points[0].y);
      for (const p of s.points.slice(1)) c.lineTo(p.x, p.y);
      if (s.points.length === 1) c.lineTo(s.points[0].x + 0.1, s.points[0].y);
      c.stroke();
    }
  }, []);

  /** Dimensiona o canvas para o wrapper, com nitidez HiDPI, e redesenha. */
  const resize = useCallback(() => {
    const wrap = wrapRef.current;
    const canvas = canvasRef.current;
    if (!wrap || !canvas) return;
    const w = wrap.clientWidth;
    const h = Math.round(w * ASPECT);
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    canvas.style.height = `${h}px`;
    if (inkRef.current.strokes.length === 0) {
      inkRef.current = emptyInk(w, h);
    }
    redraw();
  }, [redraw]);

  useEffect(() => {
    resize();
    const ro = new ResizeObserver(resize);
    if (wrapRef.current) ro.observe(wrapRef.current);
    return () => ro.disconnect();
  }, [resize]);

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
    const c = ctx();
    c.strokeStyle = PEN_COLOR;
    c.lineWidth = PEN_WIDTH;
    c.lineCap = "round";
    c.beginPath();
    c.moveTo(a.x, a.y);
    c.lineTo(b.x, b.y);
    c.stroke();
  };

  const onPointerDown = (e: React.PointerEvent) => {
    e.currentTarget.setPointerCapture(e.pointerId);
    drawingRef.current = true;
    const stroke: Stroke = { points: [toPoint(e)] };
    inkRef.current.strokes.push(stroke);
    setStrokeCount(inkRef.current.strokes.length);
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

  const undo = () => {
    inkRef.current.strokes.pop();
    setStrokeCount(inkRef.current.strokes.length);
    if (inkRef.current.strokes.length === 0) t0Ref.current = 0;
    redraw();
  };

  const clear = () => {
    const wrap = wrapRef.current!;
    inkRef.current = emptyInk(wrap.clientWidth, Math.round(wrap.clientWidth * ASPECT));
    t0Ref.current = 0;
    setStrokeCount(0);
    redraw();
  };

  const hasInk = strokeCount > 0;

  return (
    <div ref={wrapRef} className="sheet-wrap">
      <canvas
        ref={canvasRef}
        className="sheet"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerLeave={onPointerUp}
      />
      <div className={`sheet-hint ${hasInk ? "hidden" : ""}`}>
        escreva uma expressão aqui
      </div>
      <div className="toolbar">
        <div className="toolbar-group">
          <button className="btn btn-ghost" onClick={undo} disabled={!hasInk || busy}>
            ← desfazer
          </button>
          <button className="btn btn-ghost" onClick={clear} disabled={!hasInk || busy}>
            limpar
          </button>
        </div>
        <button
          className="btn btn-primary"
          onClick={() => onRecognize(inkRef.current)}
          disabled={!hasInk || busy}
        >
          {busy ? "reconhecendo…" : "reconhecer →"}
        </button>
      </div>
    </div>
  );
}
