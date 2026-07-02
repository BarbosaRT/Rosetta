import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import "katex/dist/katex.min.css";

// Display editorial (variável) + mono técnico — a voz "caderno de matemática".
// Self-hosted (app/fonts) para o build não depender de rede.
const fraunces = localFont({
  src: [
    { path: "./fonts/fraunces-normal-300-700.woff2", weight: "300 700", style: "normal" },
    { path: "./fonts/fraunces-italic-300-700.woff2", weight: "300 700", style: "italic" },
  ],
  variable: "--font-fraunces",
});

const plexMono = localFont({
  src: [
    { path: "./fonts/plex-normal-400.woff2", weight: "400", style: "normal" },
    { path: "./fonts/plex-normal-500.woff2", weight: "500", style: "normal" },
  ],
  variable: "--font-plex",
});

export const metadata: Metadata = {
  title: "Rosetta — escrita à mão → LaTeX",
  description: "Escreva matemática à mão e obtenha LaTeX.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={`${fraunces.variable} ${plexMono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
