"""
Module de configuration centralisé de l'application.
"""

import logging
import sys

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Paramètres globaux de l'application pour le calcul de la volatilité Crypto/Fiat.
    """

    # Nom de la plateforme d'échange CCXT ('binance', 'coinbase', etc.)
    EXCHANGE: str = Field(
        default="binance",
        description="Plateforme d'échange crypto CCXT à utiliser.",
    )

    # Devise Fiat de cotation cible ('EUR', 'USD', etc.)
    QUOTE_CURRENCY: str = Field(
        default="EUR",
        description="Devise Fiat de référence pour filtrer les paires (ex: EUR).",
    )

    # Période d'analyse en jours
    DAYS_PERIOD: int = Field(
        default=30,
        ge=2,
        description="Nombre de jours d'historique d'analyse (minimum 2 jours pour calculer une variance).",
    )

    # Dossier et fichier de sortie CSV
    OUTPUT_DIR: str = Field(
        default="csv",
        description="Répertoire de stockage des rapports CSV horodatés.",
    )

    OUTPUT_FILE: str = Field(
        default="crypto_volatility.csv",
        description="Nom de base du fichier CSV destination.",
    )

    # Gestion des cas limites (Option A: Strict = ignorer les paires avec < DAYS_PERIOD bougies)
    STRICT_DATA_CHECK: bool = Field(
        default=True,
        description="Si True, ignore les paires n'ayant pas la totalité des jours d'historique requis.",
    )

    # Délai de sécurité en secondes entre chaque appel API (en plus du rateLimiter CCXT)
    RATE_LIMIT_DELAY: float = Field(
        default=0.1,
        ge=0.0,
        description="Pause explicite (en s) entre chaque requête HTTP pour garantir zéro bannissement IP.",
    )

    # Configuration de l'application
    PROJECT_NAME: str = "Crypto Volatility Calculator"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        extra="ignore",
    )


# Instance globale unique des paramètres
settings = Settings()

# Configuration du format et du niveau des logs console
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(settings.PROJECT_NAME)
