"""
Interface en ligne de commande (CLI) pour l'exécution du calculateur de volatilité Crypto/Fiat.
"""

import argparse
import sys
from pathlib import Path

# Résolution automatique du PYTHONPATH pour permettre l'exécution 'python -m src.cli' ou 'python src/cli.py'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import logger, settings
from src.services.exchange import CryptoExchangeService
from src.services.metrics import compute_pair_metrics
from src.services.reporter import VolatilityReporter


def run_pipeline(
    exchange_id: str | None = None,
    quote_currency: str | None = None,
    days_period: int | None = None,
    output_file: str | None = None,
) -> int:
    """
    Exécute le pipeline complet de collecte, calcul et exportation de la volatilité.

    Returns:
        int: Exit code (0 = Succès, 1 = Erreur).
    """
    selected_exchange = (exchange_id or settings.EXCHANGE).lower()
    selected_quote = (quote_currency or settings.QUOTE_CURRENCY).upper()
    selected_days = days_period or settings.DAYS_PERIOD
    selected_output = output_file or settings.OUTPUT_FILE

    logger.info("=" * 60)
    logger.info("🚀 DÉMARRAGE DU CALCULATEUR DE VOLATILITÉ CRYPTO / FIAT")
    logger.info(f"   • Exchange : {selected_exchange}")
    logger.info(f"   • Devise Fiat : {selected_quote}")
    logger.info(f"   • Période d'analyse : {selected_days} jours")
    logger.info(f"   • Fichier de sortie : {selected_output}")
    logger.info("=" * 60)

    try:
        # 1. Initialisation de l'exchange CCXT
        exchange_service = CryptoExchangeService(exchange_id=selected_exchange)

        # 2. Récupération des paires Fiat disponibles (ex: 'BTC/EUR', 'ETH/EUR')
        fiat_pairs = exchange_service.fetch_fiat_pairs(quote_currency=selected_quote)

        if not fiat_pairs:
            logger.error(
                f"Aucune paire Spot active trouvée pour la cotation '{selected_quote}' sur {selected_exchange}."
            )
            return 1

        results = []
        total_pairs = len(fiat_pairs)

        # 3. Boucle de collecte et calcul avec suivi d'activité console
        logger.info(f"Début du traitement des {total_pairs} paires...")

        for idx, symbol in enumerate(fiat_pairs, start=1):
            logger.info(f"[{idx}/{total_pairs}] Collecte des données pour {symbol}...")

            # Récupération des bougies journalières
            candles = exchange_service.fetch_ohlcv_candles(
                symbol=symbol,
                days_period=selected_days,
            )

            # Calcul des métriques (Volatilité, Last Price, Volume Moyen)
            metrics_result = compute_pair_metrics(
                symbol=symbol,
                candles=candles,
                required_days=selected_days,
            )

            if metrics_result is not None:
                results.append(metrics_result)

        # 4. Exportation et synthèse
        if not results:
            logger.warning("Aucun résultat valide n'a pu être calculé sur l'ensemble des paires.")
            return 1

        VolatilityReporter.export_to_csv(results=results, output_filepath=selected_output)

        logger.info(f"✅ Traitement terminé avec succès ! {len(results)} paires analysées.")
        return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠️ Interruption par l'utilisateur (Ctrl+C). Arrêt propre du script.")
        return 130
    except Exception as e:
        logger.critical(f"❌ Erreur critique durant l'exécution du pipeline : {e}", exc_info=True)
        return 1


def main() -> None:
    """
    Parser d'arguments de la ligne de commande.
    """
    parser = argparse.ArgumentParser(
        description="Calculateur de Volatilité Crypto asset vs Fiat currency (CCXT & Python)."
    )
    parser.add_argument(
        "--list-quotes",
        action="store_true",
        help="Affiche la liste de toutes les devises de cotation (Fiat/Stablecoins) disponibles sur l'exchange.",
    )
    parser.add_argument(
        "--exchange",
        type=str,
        default=settings.EXCHANGE,
        help=f"Plateforme d'échange (defaut: {settings.EXCHANGE})",
    )
    parser.add_argument(
        "--quote",
        type=str,
        default=settings.QUOTE_CURRENCY,
        help=f"Devise Fiat de référence (defaut: {settings.QUOTE_CURRENCY})",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=settings.DAYS_PERIOD,
        help=f"Nombre de jours d'historique (defaut: {settings.DAYS_PERIOD})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=settings.OUTPUT_FILE,
        help=f"Fichier de sortie CSV (defaut: {settings.OUTPUT_FILE})",
    )

    args = parser.parse_args()

    if args.list_quotes:
        exchange_service = CryptoExchangeService(exchange_id=args.exchange)
        quotes = exchange_service.get_available_fiat_quotes()
        print(f"\n🌍 Devises de cotation (Quotes) disponibles sur '{args.exchange.lower()}' ({len(quotes)} trouvées) :")
        print(", ".join(quotes))
        print()
        sys.exit(0)

    exit_code = run_pipeline(
        exchange_id=args.exchange,
        quote_currency=args.quote,
        days_period=args.days,
        output_file=args.output,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
