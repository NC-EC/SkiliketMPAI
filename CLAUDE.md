# CLAUDE.md — Alerta Ambiental Predictiva (SKILIKET · Equipo 9)

> Documento maestro para Claude Code. Léelo completo al iniciar cada sesión. Si algo aquí contradice una instrucción puntual del usuario, pregunta antes de actuar.

## 1. Contexto del proyecto

- **Marco:** SKILIKET Living Lab, Tecnológico de Monterrey, Campus Guadalajara. Proyecto Solidario de Servicio Social (semestre agosto–diciembre 2026). No es una materia: lo que se entrega debe servirle de verdad al siguiente equipo.
- **Equipo 9 — Alerta Ambiental Predictiva.** Integrantes: Néstor Cáceres (ITC, líder del proyecto, compartido con Equipo 4) e integrante de Ciencia de Datos.
- **Reto:** modelo de IA predictiva que *anticipe* (no solo detecte) cuándo las variables ambientales de SKILIKET cruzarán umbrales de riesgo, más un motor de recomendaciones de salud física con reglas trazables a normativa oficial.
- **Variables objetivo (7):** CO2, temperatura, humedad, TVOC, ruido, radiación UV, AQI-UBA.
- **Enfoque técnico:** forecasting de series de tiempo. Baseline estadístico (SARIMA o Prophet) vs. deep learning (LSTM), con la misma partición temporal y las mismas métricas. Motor de reglas basado en OMS, NOM-025-STPS, EPA y ASHRAE.
- **Entregables del semestre:**
  1. Paper para una conferencia indexada en Scopus o journal afín (**envío en Semana 11, jueves 12 nov 2026**).
  2. Póster del Simposio (síntesis visual del paper; Simposio sábado 21 nov 2026; arte final viernes 20 nov).
  3. Manual de Procesos (reentrenamiento del modelo + actualización de reglas; borrador Semana 10, cierre del 23 nov al 4 dic).
  4. Pipeline reproducible en este repositorio.
- **Éxito del semestre (SRS §7):** una comparación *honesta* baseline vs. LSTM sobre datos reales y un paper enviado, aunque el LSTM no gane.

## 2. Reglas de oro (no negociables)

1. **Nunca inventes datos, resultados, métricas, referencias ni citas.** Si algo no existe todavía, escribe `TODO` o `[POR CONFIRMAR]`. Las referencias bibliográficas solo se agregan si el usuario las aportó o si se verificaron con una fuente consultable.
2. **Los datos crudos son de solo lectura.** Viven en `data/raw/`, nunca se modifican ni se suben a GitHub. Toda transformación ocurre en el pipeline y es repetible (RD-03, RNF-07).
3. **Sin fuga de información:** partición temporal estricta (ningún dato de prueba anterior a uno de entrenamiento); los parámetros de normalización se calculan solo con el set de entrenamiento (RF-MOD-04, RF-PRE-05).
4. **Reproducibilidad:** semillas fijas, versiones de librerías fijadas, configuración en archivos YAML, no valores en el código (RNF-01, RNF-04).
5. **Trazabilidad normativa:** ninguna regla del motor existe sin ID, severidad, recomendación y cita (documento, sección o tabla). Si dos normas difieren, se documenta cuál se adopta y por qué (RM-04).
6. **Sin diagnóstico médico.** Las recomendaciones se limitan a acciones de salud física y ambientales: ventilar, hidratarse, reducir exposición (RM-03).
7. **Privacidad:** los datos ambientales no llevan datos personales; cualquier dato de salud del Equipo 10 se usa solo agregado y con su consentimiento (RNF-08). Repo **privado**.
8. **Honestidad en el paper:** reporta limitaciones, resultados negativos y que el LSTM puede perder contra el baseline. Si el histórico es corto, dilo.
9. **Antes de cambios grandes** (cambiar de framework, reestructurar carpetas, borrar archivos, reescribir una sección del paper), propón un plan y espera confirmación.
10. **Idioma:** documentación y conversación en español; código, nombres de variables y commits en inglés; el paper en el idioma que exija la conferencia elegida (probablemente inglés).

## 3. Estado actual y pendientes abiertos

Fecha de referencia al crear este documento: **jueves 8 oct 2026 (entrega de la Semana 6: Introducción + sesión intermedia con el mentor).**

Pendientes (actualizar esta lista conforme se resuelvan):

- [ ] Viabilidad confirmada con el Dr. Rasikh Tariq (CA-01)
- [ ] Alcance real de datos: periodo, número de dispositivos, ubicaciones (RD-01)
- [ ] Mentor de referencia asignado
- [ ] Conferencia/journal destino elegido y su fecha límite (CA-02)
- [ ] Horizonte de predicción y frecuencia de remuestreo fijados
- [ ] Umbrales de riesgo con fuente normativa (Semana 7)
- [ ] Definir si se suman más estudiantes al equipo
- [ ] Confirmar estado real de CA-04 (EDA + primer baseline), previsto para la Semana 5

> Claude: al inicio de cada sesión, pregunta al usuario qué ítems de esta lista cambiaron y actualízala.

## 4. Calendario restante (misiones semanales)

Cada misión se lanza el viernes y se entrega el jueves siguiente.

| Sem | Entrega | Misión | Criterio SRS |
|---|---|---|---|
| 6 | 8 oct | Introducción del paper + sesión intermedia (corte) | CA-05 |
| 7 | 15 oct | Marco conceptual, antecedentes, revisión de literatura; **definir umbrales normativos** | CA-06 |
| 8 | 22 oct | Metodología, partición train/test, métricas | CA-07 |
| 9 | 29 oct | LSTM entrenado, comparación con baseline, reglas validadas con casos reales; resultados y discusión (borrador) | CA-08 |
| 10 | 5 nov | Conclusiones + borrador del Manual de Procesos | CA-09 |
| 11 | 12 nov | Revisión final y **ENVÍO del paper** | CA-10 |
| 12 | 19 nov | Póster y ensayo (arte final 20 nov) | CA-11 |
| — | 21 nov | Simposio SKILIKET Otoño 2026 | — |
| — | 23 nov–4 dic | Cierre: Manual de Procesos definitivo | — |

Cada semana también aplica: reporte de avance (Word/PDF) cargado en RetroBit por el líder en turno antes de la reunión; video corto de inicio y fin de sesión en Teams; avances en el chat y en la carpeta Living Lab de Teams.

## 5. Arquitectura del pipeline (5 etapas)

```
1. Ingesta  →  2. Preprocesamiento  →  3. Modelado  →  4. Motor de reglas  →  5. Salida
 (Equipo 7)                                               (Equipo 10: evidencia)   (Equipo 4: futuro)
```

Estructura de repositorio propuesta:

```
skiliket-eq9-alerta-predictiva/
├── CLAUDE.md                  # este archivo
├── README.md
├── pyproject.toml             # dependencias fijadas (uv o pip)
├── .gitignore                 # incluye data/raw, data/processed, models, .env
├── configs/
│   ├── pipeline.yaml          # horizonte, frecuencia de remuestreo, semillas, rutas
│   └── rules.yaml             # reglas normativas (ID, variable, umbral, severidad, recomendación, cita)
├── data/
│   ├── raw/                   # SOLO LECTURA, no versionado
│   ├── interim/
│   └── processed/
├── src/skiliket_eq9/
│   ├── ingestion/             # RF-ING: carga, validación, inventario de dispositivos
│   ├── preprocessing/         # RF-PRE: limpieza, faltantes, remuestreo, features, escalado, EDA
│   ├── models/                # RF-MOD: baseline (SARIMA/Prophet), LSTM, evaluación, cruce de umbral
│   ├── rules/                 # RF-REC: motor de reglas
│   └── output/                # RF-SAL: CSV/JSON, gráficas, tablas del paper
├── notebooks/                 # exploración (no lógica de producción)
├── tests/                     # pytest
├── reports/
│   ├── figures/               # regenerables con un comando
│   └── tables/
├── paper/                     # LaTeX o Markdown del paper, bib, secciones por semana
├── poster/
├── docs/
│   ├── SRS.md                 # versión viva del SRS
│   ├── manual_de_procesos.md
│   ├── decisiones.md          # registro de decisiones (ADR ligero)
│   └── retrobit/              # reportes semanales
└── scripts/                   # run_pipeline.sh, make_figures.sh
```

Si el repo aún no tiene esta estructura, propónla y créala solo tras confirmación.

## 6. Requisitos clave del SRS (resumen operativo)

- **Prioridad Alta = necesario para el paper.** Atiende primero RF-ING-01/02/03, RF-PRE-01/02/03/05/06, RF-MOD-01 a 06, RF-REC-01/02/05/06, RF-SAL-01/02.
- **Ingesta:** inventario automático de dispositivos (ubicación, periodo, # observaciones); registros inválidos a un reporte, no entran al pipeline.
- **Preprocesamiento:** limpieza de duplicados y fuera de rango físico; faltantes con estrategia documentada y % antes/después; remuestreo a frecuencia común configurable; features (rezagos, medias móviles, hora/estacionalidad) versionadas.
- **Modelado:** baseline y LSTM por variable (o multivariable); horizonte como parámetro; estimación del instante de cruce de umbral o "sin cruce"; tabla comparativa por variable y modelo; guardar modelos, parámetros y semillas.
- **Métricas:** MAE, RMSE (obligatorias); MAPE/sMAPE (propuesta); para detección de cruce: precisión, exhaustividad y anticipación en minutos/horas (propuesta). No fijar metas numéricas de error hasta ver el histórico.
- **Motor de reglas:** cada regla = ID, variable, condición, severidad, recomendación, cita. Toda predicción que cruza umbral dispara ≥1 regla; si ninguna aplica, se registra. La salida incluye ID de regla y fuente.
- **Salida:** CSV/JSON con esquema documentado e independiente de herramientas del equipo; gráficas pronóstico vs. observado; tablas y figuras del paper regenerables con un comando.
- **Fuera de alcance:** UI productiva, streaming/tiempo real, dispositivos fuera del campus (Distrito Tec, TecMilenio Zacatecas), integración con la app del Equipo 4.

Fuentes normativas candidatas (por confirmar): CO2, temperatura y humedad → ASHRAE (temperatura también NOM-025-STPS); TVOC → OMS/EPA; ruido y UV → OMS; AQI-UBA → EPA/OMS. **Los umbrales se definen en la Semana 7 leyendo las normas; no los asumas de memoria.**

## 7. Convenciones de código

- Python 3.11+. Gestor de dependencias: `uv` (o `venv` + pip). Fijar versiones.
- Framework de deep learning: **PyTorch** por defecto (TensorFlow solo si el equipo decide cambiar; registrar en `docs/decisiones.md`).
- Estilo: `ruff` (lint + format), type hints en funciones públicas, docstrings breves.
- Módulos por etapa, sin lógica de negocio en notebooks.
- Todo parámetro (horizonte, frecuencia, semillas, rutas, umbrales) viene de `configs/`.
- Pruebas con `pytest` para: validación de esquema, ausencia de fuga train/test, motor de reglas (toda regla tiene cita), reproducibilidad de un experimento pequeño.
- Un experimento = un comando: `python -m skiliket_eq9.run --config configs/pipeline.yaml`.
- Commits pequeños, en inglés, formato `tipo: descripción` (`feat:`, `fix:`, `docs:`, `data:`, `exp:`, `paper:`).
- Ramas: `main` estable; trabajo en `feat/...`, `paper/...`, `exp/...` con PR y revisión del otro integrante (RNF-03).
- Nunca hacer `git push --force` a `main`. Nunca commitear datos crudos, credenciales o `.env`.

## 8. Flujo de trabajo del paper

- El paper vive en `paper/` y se escribe **progresivamente**, una sección por misión semanal (el proceso es parte de la evaluación).
- Estructura base: Introducción → Marco conceptual/antecedentes → Metodología → Resultados y discusión → Conclusiones.
- Cada afirmación factual lleva cita; las referencias van en `paper/references.bib`. Marca `[CITA PENDIENTE]` si no hay fuente.
- Las tablas y figuras se generan desde `reports/` con scripts, no a mano.
- Antecedentes SKILIKET que se pueden citar (confirmar datos antes de usar): Sanabria-Z et al. (JISEM 2025); Mercado-Rojas et al. (IEEE RITA 2025, "Framework for AI Integration in Citizen Science"); Ruiz-López et al. (IEEE ISEC 2025). Equipo 10: estudio piloto de calidad del aire interior y atención (Karen Tapia et al.).
- Antes de generar texto del paper, pregunta qué sección toca y revisa el borrador previo para mantener coherencia.
- Cuando el usuario elija conferencia/journal, adapta plantilla (IEEE, Springer, ACM, etc.) y respeta límite de páginas y fecha de envío.

## 9. Coordinación con otros equipos

- **Equipo 7 (Plataforma Federada):** fuente de los exportes históricos. Pedir primero un exporte acotado (R03).
- **Equipo 10 (Salud y Calidad del Aire):** protocolo de recolección y evidencia biológica (cuestionario de Síndrome del Edificio Enfermo, prueba D2-R). Revisar con ellos antes de usar cualquier dato de salud.
- **Equipo 4 (App gamificada + RetroBit):** futuro consumidor del esquema de salida. Néstor comparte carga con ellos: no sobrecargar.

## 10. Cómo debe trabajar Claude en este repo

- Antes de programar, lee `docs/SRS.md`, `configs/` y la lista de pendientes (§3).
- Para tareas nuevas, indica qué requisito del SRS (RF-/RNF-/RD-/RM-) y qué criterio de aceptación (CA-) atiende.
- Si faltan datos reales, trabaja con datos sintéticos **claramente etiquetados como sintéticos** y nunca los uses para resultados del paper.
- Al terminar una tarea: resumen breve de qué cambió, cómo ejecutarlo/verificarlo y qué sigue.
- Mantén `docs/decisiones.md` al día con cada decisión relevante (horizonte, frecuencia, norma adoptada, baseline elegido).
- Si una instrucción implica algo irreversible o ambiguo, pregunta primero.
