# Plan de desarrollo – AI Sentiment Analyzer (Project 19)

> El plan está en español para Gisel. **Todo lo que se entrega (código, README, interfaz, dataset y PPT) va en inglés**, porque el curso es en inglés.

## 1. Problema y objetivos

**Problem statement:** A café chain receives hundreds of customer reviews and cannot read them all. It needs to know quickly how many are positive, negative or neutral, which products drive complaints, and how sentiment changes over time.

**Objetivos:**
1. Cargar reseñas de ejemplo desde un CSV con Pandas.
2. Clasificar cada reseña con un modelo preentrenado de Hugging Face (positive / neutral / negative + confianza).
3. Calcular conteos y porcentajes de sentimiento con Pandas, en total, por producto y por mes.
4. Medir qué tan bien acierta el modelo comparándolo con etiquetas hechas a mano (accuracy y matriz de confusión).
5. Generar un **reporte de análisis de feedback** (el "expected output"), publicado en GitHub Pages.

**Fecha:** demo el **sábado 21-nov-2026 a las 7:30 p. m. hora Bogotá**. Dejar todo publicado y la PPT lista el viernes.

## 2. Decisiones clave

| Decisión | Elección | Por qué |
|---|---|---|
| Modelo | `cardiffnlp/twitter-roberta-base-sentiment-latest` | Preentrenado, gratis y **con clase neutral** (el escenario la pide). Unos 500 MB; se descarga la primera vez. |
| Dónde corre el modelo | En local (CLI de Python) | GitHub Pages solo sirve archivos estáticos, no ejecuta Python. |
| Despliegue | GitHub Pages con el **reporte estático** (`web/`), que lee el `report.json` generado por Python | Cumple "deploy with GitHub Pages" sin servidor. |
| Demo en vivo | App Streamlit local: escribir una reseña y ver su sentimiento al instante | Muestra el modelo funcionando en clase. |
| Dataset | `data/sample_reviews.csv`, **80 reseñas escritas para el proyecto** (cafetería ficticia "Bean & Leaf") con columna `true_label` puesta a mano | Cumple "sample dataset with source details" sin problemas de licencia y permite medir el acierto. |

## 3. Requisitos

### 3.1 Funcionales

| ID | Requisito |
|----|-----------|
| RF-01 | Cargar un CSV con `review_id, date, product, rating, review_text, true_label`. Validar columnas y quitar filas con texto vacío o duplicado (se informa cuántas). |
| RF-02 | Clasificar todas las reseñas en lotes (batch de 16), truncando a 512 tokens. Agregar `sentiment` y `confidence`. |
| RF-03 | Calcular con Pandas: conteo y % por sentimiento; distribución por producto; tendencia mensual; confianza promedio por clase; las 3 reseñas más positivas y las 3 más negativas. |
| RF-04 | Evaluación: accuracy, matriz de confusión (`pd.crosstab`) y lista de reseñas mal clasificadas. |
| RF-05 | Comparar con las estrellas: % de reseñas de 1–2 estrellas que el modelo marcó como no negativas (señal de sarcasmo o texto mixto). |
| RF-06 | Exportar `web/data/report.json`, `web/data/reviews_scored.csv`, `reports/feedback_report.md` y `reports/charts/*.png` (matplotlib, para la PPT). |
| RF-07 | Sitio estático: tarjetas de resumen, barras por sentimiento, barras apiladas por producto, línea mensual, matriz de confusión y tabla de reseñas con filtro por sentimiento/producto y búsqueda de texto. |
| RF-08 | Streamlit: un cuadro de texto → sentimiento + confianza; y una opción para subir un CSV y descargar el resultado. |
| RF-09 | CLI: `python -m sentiment_analyzer.cli --input <csv> --out <dir> [--limit N]`. |

### 3.2 No funcionales
- Funciona en CPU. Clasificar 80 reseñas tarda menos de 1 minuto después de la primera descarga.
- Las pruebas no descargan el modelo (usan `FakeClassifier`).
- El sitio es accesible (tabla con encabezados, filtros con etiquetas, contraste AA) y responsive.
- Sin claves de API.

## 4. Arquitectura

Sigue la "Suggested Project Architecture" del documento del profesor (Frontend → Python application → AI model layer → Data layer → Git/GitHub):

```
data/sample_reviews.csv
        │  (Data layer: CSV)
        ▼
sentiment_analyzer (Python application: Pandas + NumPy)
  data_loader ─► classifier ─► analysis ─► evaluation ─► report
                    │ (AI model layer: Hugging Face pipeline)
                    ▼
web/data/report.json + reviews_scored.csv      reports/feedback_report.md + charts/*.png
        │                                               │
        ▼                                               ▼
web/ (Frontend: HTML/CSS/JS) ──► GitHub Pages          PPT
app/streamlit_app.py ──► demo local en vivo
```

### 4.1 Estructura de carpetas

```
03_GenAI_Sentiment_Analyzer/
├── AGENTS.md
├── README.md
├── requirements.txt
├── pyproject.toml              # ruff + pytest config, package metadata
├── .gitignore
├── data/
│   ├── sample_reviews.csv
│   └── DATA_SOURCE.md          # explains the dataset was written for this project
├── src/sentiment_analyzer/
│   ├── __init__.py
│   ├── config.py               # MODEL_NAME, BATCH_SIZE, LABELS, paths
│   ├── data_loader.py          # load_reviews(path) -> DataFrame (validate + clean)
│   ├── classifier.py           # Prediction dataclass, SentimentClassifier
│   ├── analysis.py             # sentiment_counts, by_product, monthly_trend, top_reviews...
│   ├── evaluation.py           # accuracy, confusion_matrix, misclassified, rating_mismatch
│   ├── charts.py               # matplotlib PNGs for the report/PPT
│   ├── report.py               # build_report_dict, write_json, write_markdown
│   └── cli.py                  # argparse entry point
├── app/
│   └── streamlit_app.py
├── tests/
│   ├── conftest.py             # small DataFrame + FakeClassifier
│   ├── test_data_loader.py
│   ├── test_analysis.py
│   ├── test_evaluation.py
│   └── test_report.py
├── reports/                    # generated
├── web/
│   ├── index.html
│   ├── styles.css
│   ├── app.js                  # fetch + render
│   ├── charts.js               # SVG bar/line helpers
│   └── data/                   # generated report.json, reviews_scored.csv
├── presentation/
│   └── OUTLINE.md              # slide-by-slide content for the PPT
└── .github/workflows/pages.yml # deploys web/ to GitHub Pages
```

### 4.2 Contrato de `report.json`

```json
{
  "generated_at": "2026-11-19T15:00:00",
  "model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
  "total_reviews": 80,
  "rows_dropped": 0,
  "counts": {"positive": 0, "neutral": 0, "negative": 0},
  "percentages": {"positive": 0.0, "neutral": 0.0, "negative": 0.0},
  "avg_confidence": {"positive": 0.0, "neutral": 0.0, "negative": 0.0},
  "by_product": [{"product": "Latte", "positive": 0, "neutral": 0, "negative": 0}],
  "monthly": [{"month": "2026-08", "positive": 0, "neutral": 0, "negative": 0}],
  "evaluation": {"accuracy": 0.0, "confusion_matrix": {"labels": [], "matrix": [[]]}, "misclassified": []},
  "rating_mismatch_pct": 0.0,
  "top_positive": [{"review_id": 1, "text": "", "confidence": 0.0}],
  "top_negative": [],
  "reviews": [{"review_id": 1, "date": "", "product": "", "rating": 5, "text": "", "sentiment": "", "confidence": 0.0, "true_label": ""}]
}
```

### 4.3 Dataset de ejemplo (instrucciones para generarlo)

- 80 filas, fechas entre ago. y nov. de 2026, 8 productos (Latte, Espresso, Cold Brew, Croissant, Bagel, Matcha, Muffin, Sandwich).
- Una mezcla aproximada de 45 % positivas, 25 % neutrales y 30 % negativas, con reseñas de 1 a 4 frases.
- Incluir a propósito unas 6 reseñas difíciles: sarcasmo ("Great, another 20-minute wait"), opiniones mixtas y negaciones. Sirven para hablar de las limitaciones.
- Hacer que un producto tenga más quejas (por ejemplo, Sandwich) y que haya un mes con un pico negativo (por ejemplo, octubre, "new staff"). Así el reporte cuenta una historia.
- `rating` debe ser coherente con `true_label` salvo en las reseñas sarcásticas.

## 5. Interfaz del reporte (web/)

Una sola página con estas secciones, de arriba abajo: resumen (total, % por sentimiento y accuracy), barras por sentimiento, sentimiento por producto, tendencia mensual, "What customers love / complain about" (las top 3 de cada lado), evaluación del modelo (matriz y reseñas mal clasificadas) y una tabla de reseñas con filtros. Pie de página con el modelo usado, la fecha de generación y las limitaciones.

**Dirección visual (para unslop):** un reporte editorial sobrio, como un informe impreso de una consultora pequeña. Usa fondo claro y tipografía con carácter para los títulos. Los tres colores de sentimiento son apagados y se usan **solo** en los datos. El protagonista es el gráfico por producto. Sin gradientes ni emojis.

## 6. Fases de desarrollo

### Fase 1 – Datos y núcleo (≈ 3 h)
- [ ] `requirements.txt`, `pyproject.toml`, `.gitignore` y el dataset con su `DATA_SOURCE.md`.
- [ ] `data_loader`, `analysis` y `evaluation` con sus pruebas usando un DataFrame pequeño fijo.
- **Acepta si:** `pytest` pasa.

### Fase 2 – Modelo y CLI (≈ 2 h)
- [ ] `classifier` (pipeline de transformers, mapeo de etiquetas a positive/neutral/negative, lotes), `report`, `charts` y `cli`.
- **Acepta si:** la CLI genera los archivos de RF-06 y `feedback_report.md` se lee bien.

### Fase 3 – Sitio estático y despliegue (≈ 3 h)
- [ ] `web/` según la sección 5, consultando modern-web-guidance para la tabla, los filtros y la accesibilidad.
- [ ] Workflow de GitHub Pages que publica `web/`.
- **Acepta si:** el enlace público muestra el reporte con los datos reales.

### Fase 4 – Demo en vivo (≈ 1 h)
- [ ] `streamlit_app.py` (RF-08), con el modelo cacheado usando `st.cache_resource`.
- **Acepta si:** clasifica una frase escrita en menos de 2 s después de cargar.

### Fase 5 – Pulido, README y PPT (≈ 2 h)
- [ ] Pasada con **unslop** sobre `web/`.
- [ ] README con todo lo que pide el checklist del profe: problema, instalación, herramientas, funciones, capturas, resultados de pruebas, limitaciones y enlace.
- [ ] `presentation/OUTLINE.md` (ver sección 7) y capturas en `reports/screenshots/`.

## 7. Contenido de la PPT (10 diapositivas, en inglés)

1. Title: *AI Sentiment Analyzer – Understanding Customer Feedback with Transformers*, con nombre y fecha.
2. Problem: demasiadas reseñas para leerlas a mano.
3. Objectives: los 5 objetivos de la sección 1.
4. Technologies: Python, Pandas, NumPy, Hugging Face Transformers (RoBERTa), Matplotlib, Streamlit, GitHub Pages.
5. Architecture: el diagrama de la sección 4.
6. Implementation: carga → limpieza → clasificación en lotes → análisis con Pandas (con un fragmento corto de `groupby`).
7. Results: porcentajes, producto con más quejas y pico mensual (gráficos de `reports/charts/`).
8. Model evaluation: accuracy, matriz de confusión y un ejemplo de sarcasmo mal clasificado.
9. Live demo + deployment: enlace de GitHub Pages y app Streamlit.
10. Limitations & next steps: sarcasmo, solo inglés, dataset pequeño; siguientes pasos: modelo multilingüe, reseñas reales, aspect-based sentiment.

## 8. Limitaciones conocidas (para el README y la PPT)

- El modelo fue entrenado con tweets, así que puede fallar con sarcasmo y con reseñas mixtas.
- Solo funciona en inglés.
- El dataset es pequeño y escrito a mano, así que la accuracy es indicativa y no es un benchmark.
- El sitio publicado muestra un análisis ya calculado; la clasificación en vivo solo corre en local con Streamlit.
