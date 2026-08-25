"""
Module de calculs financiers et de métriques de volatilité.
"""

import logging
import math

from src.config import settings
from src.models.schemas import MarketCandle, VolatilityResult

logger = logging.getLogger(settings.PROJECT_NAME)


def calculate_daily_returns(prices: list[float]) -> list[float]:
    """
    Calcule la série des rendements relatifs quotidiens à partir des prix de clôture.

    Formule:
        R_t = (P_t - P_{t-1}) / P_{t-1}

    Args:
        prices (list[float]): Liste ordonnée des prix de clôture.

    Returns:
        list[float]: Liste des M = (len(prices) - 1) rendements.
    """
    if len(prices) < 2:
        return []

    returns = []
    for i in range(1, len(prices)):
        prev_price = prices[i - 1]
        curr_price = prices[i]

        if prev_price <= 0:
            continue

        ret = (curr_price - prev_price) / prev_price
        returns.append(ret)

    return returns


def calculate_sample_variance(data: list[float]) -> float:
    """
    Calcule la variance échantillonnée d'une série numérique (diviseur M - 1).

    Args:
        data (list[float]): Liste de valeurs numériques (ex: rendements).

    Returns:
        float: Variance de l'échantillon.
    """
    n = len(data)
    if n < 2:
        return 0.0

    mean_val = sum(data) / n
    squared_diff_sum = sum((x - mean_val) ** 2 for x in data)

    # Diviseur (n - 1) pour l'écart-type échantillonnel non biaisé
    return squared_diff_sum / (n - 1)


def calculate_daily_volatility(returns: list[float]) -> float:
    """
    Calcule la volatilité quotidienne = sqrt(Variance des rendements).

    Args:
        returns (list[float]): Série des rendements journaliers.

    Returns:
        float: Volatilité quotidienne (ex: 0.03308 pour 3.308%).
    """
    variance = calculate_sample_variance(returns)
    return math.sqrt(variance)


def compute_pair_metrics(
    symbol: str,
    candles: list[MarketCandle],
    required_days: int | None = None,
    strict_check: bool | None = None,
) -> VolatilityResult | None:
    """
    Calcule l'ensemble des métriques d'une paire crypto/fiat (Volatilité, Dernier Prix, Volume Moyen).

    Args:
        symbol (str): Symbole du marché (ex: 'BTC/EUR').
        candles (list[MarketCandle]): Historique des bougies.
        required_days (int, optional): Nombre de jours requis.
        strict_check (bool, optional): Si True (Option A), invalide les séries incompletes.

    Returns:
        VolatilityResult | None: Objet résultat ou None si la série est insuffisante.
    """
    target_days = required_days or settings.DAYS_PERIOD
    is_strict = settings.STRICT_DATA_CHECK if strict_check is None else strict_check

    # Extraction des paires Base / Quote (ex: 'BTC/EUR' -> base='BTC', quote='EUR')
    parts = symbol.split("/")
    if len(parts) == 2:
        base_curr, quote_curr = parts[0], parts[1]
    else:
        base_curr, quote_curr = symbol, settings.QUOTE_CURRENCY

    # Validation Option A (Strict Data Check)
    if len(candles) < target_days:
        if is_strict:
            logger.warning(
                f"[{symbol}] Ignoré (Option A) : {len(candles)} bougies disponibles sur {target_days} requises."
            )
            return None
        elif len(candles) < 2:
            logger.warning(
                f"[{symbol}] Ignoré : Historique insuffisant (< 2 bougies) pour calculer une variance."
            )
            return None

    # Extraction des séries de prix de clôture et de volumes
    close_prices = [c.close for c in candles]
    volumes = [c.volume for c in candles]

    # 1. Rendements & Volatilité Quotidienne = sqrt(Variance)
    returns = calculate_daily_returns(close_prices)
    if not returns:
        return None

    daily_vol = calculate_daily_volatility(returns)

    # 2. Dernier Prix de clôture (Last Price)
    last_price = close_prices[-1]

    # 3. Volume moyen quotidien (Average Volume)
    average_volume = sum(volumes) / len(volumes)

    return VolatilityResult(
        base=base_curr,
        quote=quote_curr,
        daily_volatility=daily_vol,
        last_price=last_price,
        average_volume=average_volume,
    )
