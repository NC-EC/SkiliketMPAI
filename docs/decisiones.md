# Registro de decisiones (ADR ligero)

> Cada decisión relevante del proyecto (horizonte, frecuencia, norma adoptada,
> baseline elegido, framework, etc.) se documenta aquí con fecha y motivo.
> Ver CLAUDE.md sección 10.

## Formato

```
## AAAA-MM-DD — Título corto de la decisión
- Contexto:
- Decisión:
- Motivo:
- Alternativas consideradas:
```

## 2026-10-08 — Estructura inicial del repositorio

- Contexto: el repo solo tenía `CLAUDE.md`, `README.md` y `SETUP.md`; no había
  código ni estructura de carpetas.
- Decisión: crear la estructura propuesta en `CLAUDE.md` sección 5
  (`configs/`, `data/`, `src/skiliket_eq9/`, `notebooks/`, `tests/`,
  `reports/`, `paper/`, `poster/`, `docs/`, `scripts/`), un `.gitignore`
  que excluye `data/raw`, `data/interim`, `data/processed` y `models/`, y un
  `pyproject.toml` base sin dependencias fijadas todavía.
- Motivo: dejar el repo listo para empezar a trabajar en el pipeline sin
  bloquear ninguna decisión de contenido (umbrales, horizonte, baseline, etc.)
  que corresponde tomar en las Semanas 7-8.
- Alternativas consideradas: ninguna; es la estructura que el propio
  `CLAUDE.md` ya proponía.
