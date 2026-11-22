# Web page with the live analyzer. Used locally (docker compose) and on Hugging Face Spaces.
FROM python:3.11-slim

# Hugging Face Spaces runs the container as user 1000
RUN useradd -m -u 1000 user
WORKDIR /app

COPY requirements.txt pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt \
    && chown user /app

USER user
ENV HF_HOME=/home/user/models HOST=0.0.0.0

# Download the model while building, so the app starts fast
RUN python -c "from sentiment_analyzer.analyzer import get_model; get_model()"

COPY --chown=user data ./data
COPY --chown=user web ./web

EXPOSE 8000
CMD ["python", "-m", "sentiment_analyzer.server"]
