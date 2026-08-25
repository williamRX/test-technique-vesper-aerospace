from fastapi import FastAPI

from src.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Socle API de base pour test technique",
)


@app.get("/")
def read_root():
    """Route racine d'accueil."""
    return {
        "message": "Bienvenue sur le service Test Technique API",
        "status": "ready",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Endpoint de santé pour la supervision ou conteneurisation."""
    return {"status": "ok", "version": settings.VERSION}
