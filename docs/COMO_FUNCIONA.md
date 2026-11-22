# Cómo funciona (guía para estudiar y explicar)

## La idea en una frase

El dataset vive en `data/sample_reviews.csv`. Al abrir la página, el servidor lo lee, clasifica cada
reseña con un modelo pre-entrenado de Hugging Face, cuenta los resultados con Pandas y la página los
dibuja. Además hay un campo libre para escribir una reseña y **clasificarla** o **agregarla al dataset**.

```
data/sample_reviews.csv
        │
        ▼
analyzer.py   1. load_reviews   (Pandas lee el CSV)
              2. get_model      (carga RoBERTa)
              3. classify       (el modelo etiqueta cada reseña)
              4. summarize      (Pandas cuenta)
              +  to_markdown    (reporte final)
        │
        ▼
server.py     GET  /api/report    → analiza el dataset
              POST /api/classify  → clasifica 1 reseña (no se guarda)
              POST /api/add       → agrega 1 reseña al CSV y vuelve a analizar
        │
        ▼
web/          la página muestra el reporte y tiene el campo libre
```

## El dataset: `data/sample_reviews.csv`

80 reseñas inventadas de un café, de 8 productos. Columnas:
`review_id, date, product, rating, review_text, true_label`.
`true_label` es la etiqueta que puso una persona; sirve para medir qué tan bien acierta el modelo.

## `analyzer.py` — las 4 tareas del enunciado

| Función | Qué hace | Qué decir si te preguntan |
|---|---|---|
| `load_reviews()` | Lee el CSV con `pd.read_csv`, quita espacios, reseñas vacías y repetidas | Limpieza básica con Pandas (`str.strip`, `drop_duplicates`) |
| `add_review(text, product)` | Agrega una fila al final del CSV (`to_csv(mode="a")`) | Le pone id siguiente y fecha de hoy. No tiene `true_label`, así que no cuenta para la precisión. No deja repetir reseñas |
| `get_model()` | Carga el modelo con `pipeline("text-classification", ...)` | Es **pre-entrenado**: no lo entrenamos, solo lo usamos. Se carga una vez y se guarda en `_model` |
| `classify(reviews)` | Pasa todas las reseñas al modelo y agrega `sentiment` y `confidence` | `confidence` es la probabilidad que el modelo le da a su respuesta (0 a 1) |
| `classify_text(text)` | Clasifica una sola reseña escrita por el usuario | Usa `classify` por dentro; no guarda nada |
| `summarize(scored)` | `value_counts` para contar, porcentajes, `crosstab` por producto, precisión | Precisión = % de reseñas (con etiqueta humana) donde el modelo coincide |
| `to_markdown(summary)` | Escribe el reporte en Markdown | Es el "customer feedback analysis report" que pide el enunciado |
| `analyze()` | Une todo: cargar → clasificar → contar → reporte | La usa el servidor |

`python -m sentiment_analyzer.analyzer` guarda `web/data/report.json` (lo que se ve en GitHub Pages)
y `reports/feedback_report.md`.

## `server.py` — el puente entre la página y el modelo

- Usa `http.server`, que viene con Python (no hay que instalar nada).
- Sirve los archivos de `web/` y tiene las 3 rutas `/api/` del diagrama.
- Si la reseña viene vacía o repetida responde error 400 con un mensaje claro.

## `web/` — la página

- `index.html`: el campo libre (texto + producto + botones **Classify** y **Add to dataset**) y las
  zonas de resultados.
- `app.js`:
  - Al abrir: `fetch("api/report")` y `show(report)`. Sin servidor, usa `data/report.json`.
  - **Classify** → `post("api/classify")` y muestra p. ej. "Negative · 78% confidence".
  - **Add to dataset** → `post("api/add")` y vuelve a dibujar todo con el reporte nuevo.
  - `show` dibuja tarjetas, barras (ancho = porcentaje), tabla por producto, tabla de reseñas
    (la más nueva arriba) y el botón para descargar el reporte.
- `styles.css`: colores en variables (`--positive`, `--neutral`, `--negative`).

## Preguntas probables

- **¿Por qué no entrenaron un modelo?** El enunciado pide uno pre-entrenado. RoBERTa ya fue
  entrenado con millones de tweets para clasificar sentimiento en 3 clases.
- **¿Dónde está Pandas?** Leer y escribir el CSV, limpiar, contar (`value_counts`), tabla por
  producto (`crosstab`) y precisión (comparar dos columnas y sacar `mean`).
- **¿Qué tan bueno es?** 86,2 % de acierto en las 80 reseñas. Falla más con sarcasmo y reseñas mixtas.
- **¿Por qué la reseña agregada no cambia la precisión?** No tiene etiqueta humana para comparar.
- **¿Por qué hace falta un servidor?** El modelo corre en Python; el navegador no puede ejecutarlo.
- **¿Cómo prueban sin descargar el modelo?** `classify` recibe el modelo como argumento; los tests
  le pasan `fake_model`, una función que imita al modelo, y usan una copia temporal del CSV.

## Para dejar el dataset como estaba

Las reseñas agregadas quedan al final del CSV. Para borrarlas: elimina esas líneas, o
`git checkout data/sample_reviews.csv`.
