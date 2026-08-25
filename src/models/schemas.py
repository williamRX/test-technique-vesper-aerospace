"""
Module des schémas de données et Data Transfer Objects (DTO).
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class MarketCandle:
    """
    Représente une bougie de marché OHLCV (Open, High, Low, Close, Volume) journalière.

    Attributs:
        timestamp (int): Timestamp Unix en millisecondes.
        open (float): Prix d'ouverture de la journée.
        high (float): Prix le plus haut atteint dans la journée.
        low (float): Prix le plus bas atteint dans la journée.
        close (float): Prix de clôture de la journée.
        volume (float): Volume de transactions échangé dans la journée.
    """

    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(slots=True, frozen=True)
class VolatilityResult:
    """
    Contient le résultat du calcul de volatilité et des métriques pour une paire donnée.

    Conforme aux exigences d'export CSV du test technique :
    `base,quote,daily_volatility,last_price,average_volume`

    Attributs:
        base (str): Symbole de la crypto-monnaie (ex: 'BTC').
        quote (str): Devise Fiat de cotation (ex: 'EUR').
        daily_volatility (float): Volatilité quotidienne (Racine carrée de la Variance des rendements).
        last_price (float): Dernier prix de clôture disponible.
        average_volume (float): Volume quotidien moyen sur la période N jours.
    """

    base: str
    quote: str
    daily_volatility: float
    last_price: float
    average_volume: float

    def to_csv_dict(self) -> dict[str, str | float]:
        """
        Convertit l'objet en dictionnaire formaté pour l'écriture CSV.

        Pourquoi cette méthode ?
        Isoler le formatage d'export dans le modèle évite d'éparpiller la logique de
        mise en forme dans les différents reporters.
        """
        return {
            "base": self.base,
            "quote": self.quote,
            "daily_volatility": self.daily_volatility,
            "last_price": self.last_price,
            "average_volume": self.average_volume,
        }
