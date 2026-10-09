# SETUP.md — Qué descargar y cómo arrancar con Claude Code + GitHub

Verifica siempre las instrucciones oficiales más recientes (docs.claude.com) porque los comandos de instalación pueden cambiar.

## 1. Cuentas necesarias

- **GitHub** (cuenta personal o la del Tec). Crea el repo como **privado**.
- **Claude** con plan que incluya Claude Code (Pro/Max/Team o API con créditos).
- **Overleaf** (si el paper será en LaTeX; muchas conferencias IEEE/Springer dan plantilla).
- **Zotero** (gestor de referencias; exporta a `references.bib`).
- Acceso a **Teams / Living Lab** y a **RetroBit** (ya los tienes por el equipo).

## 2. Software a instalar

| Herramienta | Para qué | Notas |
|---|---|---|
| **Git** | Control de versiones | git-scm.com |
| **GitHub CLI (`gh`)** | Crear repo, PRs, autenticación desde terminal | `gh auth login` |
| **Python 3.11 o 3.12** | Pipeline de datos y modelos | evita versiones muy nuevas si TensorFlow/PyTorch aún no las soportan |
| **uv** (recomendado) o venv | Entornos y dependencias reproducibles | docs.astral.sh/uv |
| **VS Code** | Editor | extensiones: Python, Jupyter, Ruff, GitLens |
| **Claude Code** | Agente de código en terminal / IDE | instalador nativo o npm (ver docs); requiere Node.js solo si usas la vía npm |
| **Node.js LTS** | Solo si instalas Claude Code con npm | nodejs.org |
| **LaTeX** (opcional) | Compilar el paper local | TeX Live / MiKTeX, o simplemente usa Overleaf |

Hardware: el SRS (RNF-05) exige que todo corra en un equipo estándar. Un LSTM por variable sobre series de sensores corre en CPU; GPU es opcional.

## 3. Librerías de Python (se fijan en `pyproject.toml`)

- Datos: `pandas`, `numpy`, `pyarrow`, `pyyaml`, `pandera` (validación de esquema)
- Series de tiempo: `statsmodels` (SARIMA), `prophet` (alternativa; puede dar problemas de instalación en Windows, SARIMA es la opción más sencilla), `pmdarima` (opcional)
- Deep learning: `torch` (recomendado) o `tensorflow`
- ML auxiliar: `scikit-learn`
- Visualización: `matplotlib`, `seaborn`, `plotly` (dashboard opcional)
- Calidad: `pytest`, `ruff`, `pre-commit`
- Notebooks: `jupyterlab`

## 4. Pasos para arrancar

```bash
# 1. Crear el repo privado desde terminal
gh auth login
mkdir skiliket-eq9-alerta-predictiva && cd skiliket-eq9-alerta-predictiva
git init
gh repo create skiliket-eq9-alerta-predictiva --private --source=. --remote=origin

# 2. Copiar CLAUDE.md y SETUP.md a la raíz, luego:
git add CLAUDE.md SETUP.md
git commit -m "docs: add master CLAUDE.md and setup guide"
git push -u origin main

# 3. Entorno Python
uv init --python 3.12      # o: python -m venv .venv
uv add pandas numpy pyarrow pyyaml pandera statsmodels scikit-learn torch matplotlib seaborn
uv add --dev pytest ruff pre-commit jupyterlab

# 4. Abrir Claude Code dentro del repo
claude
```

Primer prompt sugerido dentro de Claude Code:

> Lee CLAUDE.md y propón la estructura de carpetas de la sección 5 y un `.gitignore` que excluya datos crudos y credenciales. No crees nada hasta que yo confirme.

## 5. Archivos que debes meter al repo (carpeta `docs/`)

Copia al repo, **sin datos sensibles**, el SRS (`docs/SRS.md`, idealmente convertido a Markdown), el documento de calendario de SKILIKET, la propuesta original de Néstor y los reportes semanales de RetroBit. Claude Code puede leerlos como contexto.

## 6. Datos

- Pide al Equipo 7 un exporte **acotado** primero (una variable, pocos dispositivos).
- Guárdalo en `data/raw/` (ignorado por Git). Documenta en `docs/decisiones.md` de dónde vino, fecha y alcance.
- Si no puedes subir datos a GitHub, compártelos por la carpeta de Teams y deja un script `scripts/download_data.md` con instrucciones.

## 7. Buenas prácticas con Claude Code

- Trabaja por **tareas pequeñas ligadas al SRS** ("implementa RF-ING-01 y RF-ING-03").
- Pídele que **planee antes de ejecutar** en cambios grandes.
- Revisa cada diff antes de commitear; tú eres responsable de lo que firma el paper.
- Nunca pegues credenciales, tokens ni datos personales en el chat.
- Actualiza la lista de pendientes en `CLAUDE.md` cada semana.
- Usa un chat/sesión por tema (datos, modelos, reglas, paper) para mantener contexto limpio.

## 8. Orden sugerido de trabajo (dada la fecha actual, Semana 6)

1. Esta semana: repo + estructura + Introducción del paper (borrador en `paper/01_introduction.md`).
2. Semana 7: lectura de normas → `configs/rules.yaml` con umbrales y citas; revisión de literatura.
3. Semana 8: metodología y métricas; ingesta + preprocesamiento + baseline funcionando.
4. Semana 9: LSTM, comparación y validación de reglas; resultados y discusión.
5. Semana 10: conclusiones y Manual de Procesos.
6. Semana 11: revisión y envío. Semana 12: póster.

**Alerta:** el calendario del SRS preveía EDA y baseline en la Semana 5. Confirma con tu equipo y mentor en qué punto estás realmente, porque el tiempo restante es corto.
