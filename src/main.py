"""
Point d'entrée principal de l'application en ligne de commande (CLI).

Permet le lancement direct via :
    python src/main.py
ou
    python src/main.py --days 30 --quote EUR --output crypto_volatility.csv
"""

import sys
from pathlib import Path

# Résolution automatique du PYTHONPATH pour le lancement 'python src/main.py'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cli import main

if __name__ == "__main__":
    sys.exit(main())
