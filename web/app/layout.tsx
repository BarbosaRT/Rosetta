import type { Metadata } from "next";
import "./globals.css";
// TODO(Fase 3): import "katex/dist/katex.min.css"; para estilizar o render do LaTeX.

export const metadata: Metadata = {
  title: "HMER — Math Notes",
  description: "Escreva matemática à mão e obtenha LaTeX.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
