# Image de base Python 3.11 légère
FROM python:3.11-slim

# Configuration des variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# Copie et installation des dépendances
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copie du code source
COPY src/ ./src/

# Port exposé pour l'API
EXPOSE 8000

# Commande de démarrage par défaut (FastAPI via Uvicorn)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
