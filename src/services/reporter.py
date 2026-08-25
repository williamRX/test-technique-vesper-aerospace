"""
Module d'affichage de rapport en console et d'exportation au format CSV.

Pourquoi le module standard `csv.DictWriter` ?
----------------------------------------------
1. Respect Strict du Format Spécifié : Garantit l'en-tête exact demandé dans le cahier des charges :
   `base,quote,daily_volatility,last_price,average_volume`
2. Zéro Dépendance Lourde : Évite d'obliger l'installation de Pandas uniquement pour
   écrire 50 lignes dans un CSV, réduisant le temps de démarrage du script à quelques millisecondes.
3. Écriture Atomique et Sûre : Crée automatiquement les dossiers parents si nécessaire et gère l'encodage UTF-8.
"""

import csv
import logging
from pathlib import Path

from src.config import settings
from src.models.schemas import VolatilityResult

logger = logging.getLogger(settings.PROJECT_NAME)


class VolatilityReporter:
    """
    Gestionnaire d'exportation des résultats et d'affichage de synthèse.
    """

    CSV_HEADER = ["base", "quote", "daily_volatility", "last_price", "average_volume"]

    @classmethod
    def export_to_csv(
        cls,
        results: list[VolatilityResult],
        output_filepath: str | Path | None = None,
    ) -> Path:
        """
        Exporte la liste des résultats au format CSV selon les spécifications strictes du test.

        Args:
            results (list[VolatilityResult]): Liste des résultats calculés.
            output_filepath (str | Path, optional): Chemin du fichier CSV de sortie.

        Returns:
            Path: Chemin absolu du fichier CSV créé.
        """
        destination = Path(output_filepath or settings.OUTPUT_FILE).resolve()

        # Création automatique du dossier parent s'il n'existe pas
        destination.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Écriture de {len(results)} résultats dans le fichier CSV : {destination}")

        with open(destination, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=cls.CSV_HEADER)

            # En-tête obligatoire conforme au sujet
            writer.writeheader()

            for res in results:
                writer.writerow(res.to_csv_dict())

        logger.info(f"Export CSV réussi : {destination}")
        return destination

    @classmethod
    def print_summary_console(cls, results: list[VolatilityResult], top_n: int = 10) -> None:
        """
        Affiche une synthèse mise en forme des résultats les plus volatils dans le terminal.

        Args:
            results (list[VolatilityResult]): Liste des résultats calculés.
            top_n (int): Nombre d'actifs à afficher dans le classement.
        """
        if not results:
            print("\n⚠️ Aucun résultat à afficher.")
            return

        # Tri par volatilité quotidienne décroissante
        sorted_results = sorted(results, key=lambda x: x.daily_volatility, reverse=True)

        print("\n" + "=" * 80)
        print(
            f"📊 RÉSULTATS DE VOLATILITÉ CRYPTO / {results[0].quote} (Top {min(top_n, len(results))})"
        )
        print("=" * 80)
        print(
            f"{'BASE':<8} {'QUOTE':<6} {'DAILY VOLATILITY':<22} {'LAST PRICE':<16} {'AVG VOLUME':<16}"
        )
        print("-" * 80)

        for res in sorted_results[:top_n]:
            print(
                f"{res.base:<8} "
                f"{res.quote:<6} "
                f"{res.daily_volatility:<22.8f} "
                f"{res.last_price:<16.2f} "
                f"{res.average_volume:<16.2f}"
            )

        print("=" * 80 + "\n")
