"""
Point d'entrée principal de l'application.

Permet soit :
1. Le lancement en ligne de commande (CLI) via `python src/main.py` ou `python -m src.cli`.
2. L'exposition d'une API REST optionnelle via FastAPI pour l'intégration web / microservice.
"""

import sys
from pathlib import Path

# Résolution automatique du PYTHONPATH pour permettre l'exécution 'python src/main.py'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI

from src.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Service de calcul de volatilité des actifs crypto par rapport à une monnaie Fiat.",
)


@app.get("/")
def read_root():
    """Endpoint racine d'information."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "exchange_default": settings.EXCHANGE,
        "quote_default": settings.QUOTE_CURRENCY,
        "days_period": settings.DAYS_PERIOD,
        "status": "ready",
    }


@app.get("/health")
def health_check():
    """Endpoint de santé pour supervision / Docker / K8s."""
    return {"status": "ok", "version": settings.VERSION}


if __name__ == "__main__":
    from src.cli import main

    sys.exit(main())
