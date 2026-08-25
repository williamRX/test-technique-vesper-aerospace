"""
Module d'exportation des résultats au format CSV.

Pourquoi le module standard `csv.DictWriter` ?
----------------------------------------------
1. Respect Strict du Format Spécifié : Garantit l'en-tête exact demandé dans le cahier des charges :
   `base,quote,daily_volatility,last_price,average_volume`
2. Zéro Dépendance Lourde : Évite d'obliger l'installation de Pandas uniquement pour
   écrire des lignes dans un CSV, réduisant le temps de démarrage du script à quelques millisecondes.
3. Écriture Atomique et Sûre : Crée automatiquement le dossier destination (`csv/`) et gère l'encodage UTF-8.
"""

import csv
import logging
from pathlib import Path

from src.config import settings
from src.models.schemas import VolatilityResult

logger = logging.getLogger(settings.PROJECT_NAME)


class VolatilityReporter:
    """
    Gestionnaire d'exportation CSV des résultats de volatilité.
    """

    CSV_HEADER = ["base", "quote", "daily_volatility", "last_price", "average_volume"]

    @classmethod
    def generate_timestamped_filepath(cls, raw_filepath: str | Path | None = None) -> Path:
        """
        Génère un chemin de fichier horodaté dans le dossier 'csv/'.

        Exemple:
            'crypto_volatility.csv' -> 'csv/crypto_volatility_20260825_143300.csv'
        """
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_path = Path(raw_filepath or settings.OUTPUT_FILE)

        # Si le chemin spécifié n'inclut pas de répertoire explicite, utiliser settings.OUTPUT_DIR ('csv')
        if input_path.parent == Path("."):
            output_dir = Path(settings.OUTPUT_DIR)
        else:
            output_dir = input_path.parent

        stem = input_path.stem
        suffix = input_path.suffix or ".csv"

        filename = f"{stem}_{timestamp}{suffix}"
        return output_dir.resolve() / filename

    @classmethod
    def export_to_csv(
        cls,
        results: list[VolatilityResult],
        output_filepath: str | Path | None = None,
        add_timestamp: bool = True,
    ) -> Path:
        """
        Exporte la liste des résultats au format CSV horodaté dans le dossier 'csv/'.

        Args:
            results (list[VolatilityResult]): Liste des résultats calculés.
            output_filepath (str | Path, optional): Chemin ou nom de fichier destination.
            add_timestamp (bool): Si True, ajoute le suffixe horodaté _YYYYMMDD_HHMMSS.

        Returns:
            Path: Chemin absolu du fichier CSV créé.
        """
        if add_timestamp:
            destination = cls.generate_timestamped_filepath(output_filepath)
        else:
            p = Path(output_filepath or settings.OUTPUT_FILE)
            if p.parent == Path("."):
                destination = (Path(settings.OUTPUT_DIR) / p).resolve()
            else:
                destination = p.resolve()

        # Création automatique du dossier 'csv/' s'il n'existe pas
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
