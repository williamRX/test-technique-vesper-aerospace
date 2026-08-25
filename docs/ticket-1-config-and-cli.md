# Ticket 1 : Configuration et Ligne de Commande (CLI)

## Status: Draft
## Priority: High

### 🎯 Objectif
Permettre à l'utilisateur de configurer l'exécution du script via des constantes, des variables d'environnement ou des arguments de ligne de commande sans interface graphique (GUI).

### 📋 Spécifications Fonctionnelles
1. **Paramètres requis** :
   - `EXCHANGE` : Nom de la plateforme d'échange (par défaut `coinbase` ou `binance`).
   - `QUOTE_CURRENCY` : Devise Fiat de référence (ex: `EUR`, `USD`).
   - `DAYS_PERIOD` : Nombre de jours d'historique pour le calcul de la volatilité (ex: `30` jours).
   - `OUTPUT_FILE` : Chemin du fichier CSV de sortie (ex: `crypto_volatility.csv`).

2. **Mode de fonctionnement** :
   - Lecture automatique des paramètres depuis un fichier `.env` ou `src/config.py`.
   - Optionnel : Surcharge par arguments de ligne de commande (`argparse` ou `click` / `typer`).

### 📦 LIVRABLES ATTENDUS
- Module `src/config.py` mis à jour avec les paramètres requis.
- Point d'entrée scriptable exécutable via terminal : `python -m src.cli` ou `python src/main.py`.

### 🧪 Critères d'Acceptation
- Le script démarre en ligne de commande sans blocage ni demande d'interaction utilisateur (non-interactif).
- Si les paramètres sont modifiés dans `config.py` ou via l'environnement, le script adapte immédiatement son comportement.
