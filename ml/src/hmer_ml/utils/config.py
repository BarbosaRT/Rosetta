"""Config: YAML → objeto acessível por atributo, com herança via chave `_base_`.

Simples de propósito (ADR 0006 evita Hydra por enquanto). Suporta `_base_: base.yaml`
para overrides. Ver ml/configs/.
"""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - scaffold
    yaml = None


class Config(dict):
    """dict com acesso por ponto: cfg.train.lr. Aninhado recursivamente."""

    def __getattr__(self, name):
        try:
            v = self[name]
        except KeyError as e:
            raise AttributeError(name) from e
        return Config(v) if isinstance(v, dict) else v

    def __setattr__(self, name, value):
        self[name] = value


def _deep_merge(base: dict, override: dict) -> dict:
    """Merge recursivo: override vence; dicts se fundem. TODO(tests)."""
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: str | Path) -> Config:
    """Carrega YAML resolvendo `_base_` relativo ao próprio arquivo.

    TODO: validar campos obrigatórios; permitir overrides por CLI (--set a.b=c).
    """
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    base_name = data.pop("_base_", None)
    if base_name:
        base = load_config(path.parent / base_name)
        data = _deep_merge(base, data)
    return Config(data)
