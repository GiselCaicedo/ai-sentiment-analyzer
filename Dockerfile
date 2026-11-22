# Runs the web page with the live analyzer. The first run downloads the model (~500 MB).
FROM python:3.11-slim
WORKDIR /app
ENV HF_HOME=/models HOST=0.0.0.0
COPY requirements.txt pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
COPY data ./data
COPY web ./web
EXPOSE 8000
CMD ["python", "-m", "sentiment_analyzer.server"]
