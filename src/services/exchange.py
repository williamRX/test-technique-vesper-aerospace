"""
Service de connexion et de collecte de données de marché via la bibliothèque CCXT.

Pourquoi ce design de service autonome ?
---------------------------------------
1. Decouplage total des APIs externes : La logique propre aux spécificités de CCXT
   est encapsulée ici. Si l'API d'un exchange change ou nécessite un retry custom,
   seul ce module est impacté.
2. Resilience & Rate Limiting (`enableRateLimit=True`) : Les exchanges crypto appliquent des
   quotas stricts de requêtes HTTP. CCXT gère automatiquement les délais d'attente
   (`time.sleep`) pour éviter le bannissement d'IP lors de la boucle sur des dizaines de paires.
3. Instanciation Dynamique : L'exchange n'est pas hardcodé ; il est instancié dynamiquement
   via `getattr(ccxt, exchange_name)()` pour permettre la bascule entre Binance, Coinbase, etc.
"""

import logging

import ccxt

from src.config import settings
from src.models.schemas import MarketCandle

logger = logging.getLogger(settings.PROJECT_NAME)


class CryptoExchangeService:
    """
    Service d'interaction avec les API publiques d'échange crypto via CCXT.
    """

    def __init__(self, exchange_id: str | None = None):
        """
        Initialise l'instance CCXT pour l'exchange spécifié.

        Args:
            exchange_id (str, optional): Nom CCXT de la plateforme (ex: 'binance', 'coinbase').
                                         Par défaut, utilise `settings.EXCHANGE`.
        """
        self.exchange_name = (exchange_id or settings.EXCHANGE).lower()

        if not hasattr(ccxt, self.exchange_name):
            raise ValueError(
                f"L'exchange '{self.exchange_name}' n'est pas pris en charge par CCXT. "
                f"Veuillez choisir parmi la liste compatible (ex: 'binance', 'coinbase')."
            )

        # Instanciation dynamique avec activation du rate limiter intégré CCXT
        exchange_class = getattr(ccxt, self.exchange_name)
        self.client: ccxt.Exchange = exchange_class(
            {
                "enableRateLimit": True,
                "timeout": 15000,  # 15 secondes max par requête
            }
        )
        logger.info(f"Service Exchange initialisé pour '{self.exchange_name}' (RateLimit actif).")

    def fetch_fiat_pairs(self, quote_currency: str | None = None) -> list[str]:
        """
        Récupère toutes les paires Spot actives associées à une devise Fiat de cotation.

        Args:
            quote_currency (str, optional): Monnaie Fiat cible (ex: 'EUR').

        Returns:
            list[str]: Liste des symboles de marché (ex: ['BTC/EUR', 'ETH/EUR']).
        """
        target_quote = (quote_currency or settings.QUOTE_CURRENCY).upper()
        logger.info(
            f"Chargement des marchés sur {self.exchange_name} pour la devise Fiat '{target_quote}'..."
        )

        try:
            markets = self.client.load_markets()
        except (ccxt.NetworkError, ccxt.ExchangeError) as e:
            logger.error(f"Échec lors du chargement des marchés CCXT sur {self.exchange_name}: {e}")
            raise

        fiat_symbols = []
        for symbol, market in markets.items():
            # Filtrage strict : paires actives + marché Spot + quote matching Fiat
            is_active = market.get("active", True)
            is_spot = market.get("spot", True) or market.get("type") == "spot"
            market_quote = market.get("quote", "").upper()

            if is_active and is_spot and market_quote == target_quote:
                fiat_symbols.append(symbol)

        logger.info(
            f"{len(fiat_symbols)} paires Spot actives trouvées pour la cotation '{target_quote}'."
        )
        return sorted(fiat_symbols)

    def fetch_ohlcv_candles(
        self,
        symbol: str,
        days_period: int | None = None,
        timeframe: str = "1d",
    ) -> list[MarketCandle]:
        """
        Récupère l'historique des bougies OHLCV pour un symbole donné.

        Args:
            symbol (str): Symbole du marché (ex: 'BTC/EUR').
            days_period (int, optional): Nombre de jours d'historique.
            timeframe (str): Résolution temporelle (par défaut '1d' = bougies journalières).

        Returns:
            list[MarketCandle]: Liste des bougies typées ordonnées chronologiquement.
        """
        limit = days_period or settings.DAYS_PERIOD

        try:
            # Appel API CCXT public
            raw_candles = self.client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except ccxt.RateLimitExceeded as e:
            logger.warning(f"Rate limit atteint sur {symbol}: {e}. Attente...")
            return []
        except (ccxt.NetworkError, ccxt.ExchangeError) as e:
            logger.warning(f"Impossible de récupérer l'historique OHLCV pour {symbol}: {e}")
            return []

        if not raw_candles:
            return []

        # Conversion en objets immuables MarketCandle
        candles = []
        for candle in raw_candles:
            # Structure brute CCXT: [timestamp, open, high, low, close, volume]
            if len(candle) >= 6 and None not in candle[:6]:
                candles.append(
                    MarketCandle(
                        timestamp=int(candle[0]),
                        open=float(candle[1]),
                        high=float(candle[2]),
                        low=float(candle[3]),
                        close=float(candle[4]),
                        volume=float(candle[5]),
                    )
                )

        return candles
