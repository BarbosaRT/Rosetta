r"""Tokenizer de LaTeX custom — vocabulário derivado do dataset.

Símbolos matemáticos + tokens sintáticos (\frac, ^, _, {, }, \int, gregas, ...) +
especiais <pad> <bos> <eos> <unk>. Isolado para poder trocar por SentencePiece depois
sem tocar no resto (ADR 0003). A interface pública (build_vocab/encode/decode/vocab_size)
é o contrato estável. Sem dependências pesadas — testável em qualquer ambiente.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PAD, BOS, EOS, UNK = "<pad>", "<bos>", "<eos>", "<unk>"
DEFAULT_SPECIALS = (PAD, BOS, EOS, UNK)

# Ordem importa (alternância de regex é gulosa da esquerda p/ direita):
#   1. comando com nome:     \frac \int \alpha \left  ...
#   2. comando de 1 símbolo: \{ \} \| \, \; \%  (barra + um não-letra)
#   3. qualquer caractere não-espaço isolado: + - = ^ _ { } ( ) dígitos letras
_TOKEN_RE = re.compile(r"\\[a-zA-Z]+|\\.|[^\s]")


class LatexTokenizer:
    def __init__(self, stoi: dict[str, int] | None = None, specials=DEFAULT_SPECIALS):
        self.specials = tuple(specials)
        self.stoi: dict[str, int] = dict(stoi) if stoi else {}
        self.itos: dict[int, str] = {i: s for s, i in self.stoi.items()}

    # --- ids de tokens especiais (usados por modelo/loss/inferência) ---
    @property
    def pad_id(self) -> int:
        return self.stoi[PAD]

    @property
    def bos_id(self) -> int:
        return self.stoi[BOS]

    @property
    def eos_id(self) -> int:
        return self.stoi[EOS]

    @property
    def unk_id(self) -> int:
        return self.stoi[UNK]

    def vocab_size(self) -> int:
        return len(self.stoi)

    # --- tokenização ---
    @staticmethod
    def tokenize(latex: str) -> list[str]:
        r"""Quebra uma string LaTeX em tokens.

        Regras:
          - `\comando` (letras) vira 1 token: `\frac`, `\alpha`, `\int`, `\left`.
          - `\` + 1 não-letra vira 1 token: `\{`, `\}`, `\,`, `\%`.
          - cada outro caractere não-espaço vira 1 token: `^ _ { } ( ) + - = 0 x`.
          - espaços em branco são separadores (descartados).
        """
        return _TOKEN_RE.findall(latex)

    def build_vocab(self, latex_strings, min_freq: int = 1) -> "LatexTokenizer":
        """Constrói stoi/itos a partir do corpus de labels.

        Especiais recebem os primeiros ids (0..len-1), fixos. Os demais tokens entram
        ordenados por frequência decrescente (e alfabética p/ desempate → determinístico).
        """
        counter: Counter[str] = Counter()
        for s in latex_strings:
            counter.update(self.tokenize(s))

        stoi: dict[str, int] = {tok: i for i, tok in enumerate(self.specials)}
        # ordena por (-freq, token) para reprodutibilidade entre execuções
        for tok, freq in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])):
            if freq < min_freq or tok in stoi:
                continue
            stoi[tok] = len(stoi)

        self.stoi = stoi
        self.itos = {i: s for s, i in stoi.items()}
        return self

    def encode(self, latex: str, add_special: bool = True) -> list[int]:
        """LaTeX → ids. Com add_special, envolve em <bos> ... <eos>."""
        if not self.stoi:
            raise RuntimeError("vocabulário vazio — chame build_vocab() ou load() antes")
        unk = self.unk_id
        ids = [self.stoi.get(tok, unk) for tok in self.tokenize(latex)]
        if add_special:
            ids = [self.bos_id, *ids, self.eos_id]
        return ids

    def decode(self, ids, strip_special: bool = True) -> str:
        """ids → LaTeX. Remove especiais e junta tokens com espaço.

        Junta com espaço (perde a formatação original, mas mantém o LaTeX válido e é o
        formato esperado por normalização/CER). Para na 1ª ocorrência de <eos>.
        """
        special_ids = {self.stoi[s] for s in self.specials if s in self.stoi}
        eos = self.stoi.get(EOS)
        toks: list[str] = []
        for i in ids:
            i = int(i)
            if eos is not None and i == eos:
                break
            if strip_special and i in special_ids:
                continue
            toks.append(self.itos.get(i, UNK))
        return " ".join(toks)

    # --- persistência ---
    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(
            json.dumps({"specials": list(self.specials), "stoi": self.stoi}, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str | Path) -> "LatexTokenizer":
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(stoi=d["stoi"], specials=tuple(d.get("specials", DEFAULT_SPECIALS)))
