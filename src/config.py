"""
Module de configuration centralisé de l'application.

Pourquoi Pydantic BaseSettings (model_config = SettingsConfigDict(...)) ?
-------------------------------------------------------------------------
1. Validation automatique des types à l'exécution : Empêche les erreurs silencieuses
   si un utilisateur passe un nombre de jours négatif ou une chaîne invalide.
2. Découplage de la configuration : Permet de surcharger chaque paramètre via :
   - Des variables d'environnement (ex: EXPORT_QUOTE_CURRENCY="USD")
   - Un fichier .env local
   - Des paramètres passés en ligne de commande (CLI)
3. Pattern 'Single Source of Truth' : Évite de hardcoder des constantes éparpillées
   dans les différents modules de l'application.
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

    # Chemin du fichier CSV généré en sortie
    OUTPUT_FILE: str = Field(
        default="crypto_volatility.csv",
        description="Fichier CSV destination des résultats de volatilité.",
    )

    # Gestion des cas limites (Option A: Strict = ignorer les paires avec < DAYS_PERIOD bougies)
    STRICT_DATA_CHECK: bool = Field(
        default=True,
        description="Si True, ignore les paires n'ayant pas la totalité des jours d'historique requis.",
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
