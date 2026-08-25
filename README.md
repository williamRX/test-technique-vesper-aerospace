# Test Technique - Calculateur de Volatilité Crypto / Fiat (CLI)

Ce dépôt contient l'application Python en **ligne de commande (CLI)** développée dans le cadre du test technique. Elle permet de calculer la volatilité quotidienne, le dernier prix et le volume moyen des actifs crypto par rapport à une monnaie Fiat via la bibliothèque **CCXT**.

---

## 📋 1. Contexte & Objectifs

Calculateur de la **volatilité quotidienne** des crypto-monnaies d'une plateforme d'échange (Binance/Coinbase) cotées contre une monnaie Fiat (ex: `EUR`) sur une période $N$ jours donnée via l'API **CCXT**.

---

## 🏗️ 2. Architecture & Structure du Projet

```text
.
├── pyproject.toml        # Dépendances (CCXT, Pydantic, Pytest, Ruff)
├── README.md             # Documentation principale
├── csv/                  # Rapports CSV horodatés générés
├── src/                  # Code source
│   ├── cli.py            # Interface en ligne de commande (argparse)
│   ├── config.py         # Configuration centralisée (Pydantic BaseSettings)
│   ├── main.py           # Point d'entrée script principal
│   ├── models/           # Dataclasses immuables (MarketCandle, VolatilityResult)
│   └── services/         # Services CCXT, Métriques mathématiques & Reporter CSV
├── tests/                # Suite de tests automatisés Pytest (11 tests)
└── docs/                 # Tickets de spécifications (Tickets 1 à 5)
```

---

## ⚙️ 3. Préréquis

- **Python :** `>= 3.11`

---

## 🚀 4. Installation & Démarrage Rapide

### 4.1. Activer l'environnement virtuel Python

```bash
# Activation de l'environnement virtuel (.venv)
source .venv/bin/activate

# (Si le venv n'existe pas encore sur une nouvelle machine :)
# python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

### 4.2. Lancer le calculateur de volatilité (CLI)

```bash
# Exécution par défaut (Binance, 30 jours, paires EUR)
python src/main.py

# Lister les devises de cotation disponibles sur une plateforme :
python src/main.py --list-quotes

# Exécution avec paramètres surchargés :
python src/main.py --exchange binance --quote EUR --days 30
```

---

## 🧪 5. Tests & Qualité de Code

### Exécuter les tests unitaires
```bash
pytest
```

### Vérification et formatage du code (Ruff)
```bash
# Linter
ruff check .

# Formater
ruff format .
```
