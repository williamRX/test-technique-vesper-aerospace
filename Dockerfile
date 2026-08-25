# Image de base Python 3.11 légère
FROM python:3.11-slim

# Configuration des variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# Copie et installation des dépendances du projet
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copie du code source et des fichiers de spécifications
COPY src/ ./src/
COPY README.md .

# Commande d'exécution par défaut (CLI Volatilité)
CMD ["python", "src/main.py"]
