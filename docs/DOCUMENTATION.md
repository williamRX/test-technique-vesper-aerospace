# Documentation Technique & Fonctionnelle - Calculateur de Volatilité Crypto / Fiat

Bienvenue dans la documentation complète du projet **Crypto Volatility Calculator**. Ce document détaille l'architecture, les spécifications mathématiques, les choix techniques et le guide d'utilisation.

---

## 📌 1. Vue d'Ensemble & Objectifs Métier

L'application est un outil en ligne de commande (CLI) autonome développé en Python. Son objectif principal est d'analyser la **volatilité quotidienne**, le **dernier prix d'échange** et le **volume moyen** des crypto-monnaies disponibles sur une plateforme d'échange (ex: Binance ou Coinbase) cotées contre une monnaie Fiat cible (ex: `EUR` ou `USD`) sur une période d'analyse de $N$ jours.

### Exigences clés respectées :
- Connexion aux API publiques via **CCXT** sans aucune clé d'API requise.
- Exécution non-interactive pilotée par configuration et arguments CLI.
- Suivi d'activité en temps réel via des logs consoles horodatés.
- Génération d'un rapport CSV horodaté préservé dans le dossier `csv/` sous le format strict :
  `base,quote,daily_volatility,last_price,average_volume`

---

## 🏛️ 2. Architecture & Design Patterns

Le projet suit les principes de la **Clean Architecture** (Service-Oriented) :

```text
Test Technique/
├── pyproject.toml        # Dépendances (CCXT, Pydantic, Pytest, Ruff) & Config outillage
├── README.md             # Documentation d'accueil et Quickstart
├── csv/                  # Dossier de destination des rapports CSV horodatés
├── docs/                 # Documentation technique et tickets de spécification
│   ├── DOCUMENTATION.md  # Documentation technique globale
│   ├── ticket-1-config-and-cli.md
│   ├── ticket-2-data-fetching-ccxt.md
│   ├── ticket-3-volatility-engine.md
│   ├── ticket-4-reporting-and-csv.md
│   └── ticket-5-testing-and-validation.md
├── src/                  # Code source modulé
│   ├── cli.py            # Interface CLI (argparse, gestion d'erreurs et exit codes)
│   ├── config.py         # Configuration centralisée (Pydantic BaseSettings v2)
│   ├── main.py           # Point d'entrée script principal
│   ├── models/
│   │   └── schemas.py    # Dataclasses immuables (@dataclass(slots=True, frozen=True))
│   └── services/
│       ├── exchange.py   # Client CCXT dynamique avec RateLimiter & pauses de sécurité
│       ├── metrics.py    # Moteur mathématique de calcul de la variance et volatilité
│       └── reporter.py   # Exportateur CSV atomique horodaté
└── tests/                # Suite de tests automatisés (11 tests Pytest)
    ├── conftest.py
    ├── test_config.py
    ├── test_exchange.py
    ├── test_main.py
    ├── test_metrics.py
    └── test_reporter.py
```

---

## 📐 3. Spécifications Mathématiques

Pour chaque paire crypto/fiat analysée sur une période de $N$ jours (avec $N$ bougies journalières OHLCV) :

### 3.1. Rendements Journaliers ($R_t$)
Variation relative du prix de clôture ($P_t$) sur $M = N - 1$ intervalles quotidiens :
$$R_t = \frac{P_t - P_{t-1}}{P_{t-1}}$$

### 3.2. Moyenne des Rendements ($\bar{R}$)
$$\bar{R} = \frac{1}{M} \sum_{t=1}^{M} R_t$$

### 3.3. Variance Échantillonnée ($\text{Variance}$)
Calcul de l'écart-type échantillonnel non biaisé avec diviseur $M - 1$ (degrés de liberté) :
$$\text{Variance} = \frac{1}{M - 1} \sum_{t=1}^{M} (R_t - \bar{R})^2$$

### 3.4. Volatilité Quotidienne ($\sigma_{daily}$)
$$\sigma_{daily} = \sqrt{\text{Variance}}$$

### 3.5. Dernier Prix (`last_price`) & Volume Moyen (`average_volume`)
- **Dernier Prix** : Prix de clôture de la toute dernière bougie complète disponible ($P_{dernier}$).
- **Volume Moyen** : Moyenne arithmétique des volumes de transactions sur les $N$ jours :
  $$\bar{V} = \frac{1}{N} \sum_{t=1}^{N} V_t$$

---

## ⚙️ 4. Stratégie de Configuration & Gestion des Cas Limites

### 4.1. Single Source of Truth (`src/config.py`)
Utilisation de `Pydantic BaseSettings v2` pour centraliser la configuration :
- `EXCHANGE` : `'binance'` (par défaut)
- `QUOTE_CURRENCY` : `'EUR'` (par défaut)
- `DAYS_PERIOD` : `30` jours (par défaut)
- `OUTPUT_DIR` : `'csv'` (par défaut)
- `OUTPUT_FILE` : `'crypto_volatility.csv'` (par défaut)
- `STRICT_DATA_CHECK` : `True` (Option A)
- `RATE_LIMIT_DELAY` : `0.1` seconde

### 4.2. Option A (Strict Data Check)
Si une crypto a moins de $N$ jours d'historique (token listé récemment ou bougies manquantes) :
- En mode **Strict (`True`)** : La paire est ignorée avec un log `WARNING` afin de garantir une comparabilité rigoureuse sur $N$ jours uniformes.
- En mode **Tolérant (`False`)** : La volatilité est calculée sur le nombre de bougies disponibles dès lors qu'il y en a au moins 2.

### 4.3. Resilience API & Protection Anti-Bannissement IP
1. `enableRateLimit=True` actif sur le client CCXT.
2. Pause explicite `RATE_LIMIT_DELAY = 0.1s` entre chaque appel d'historique.
3. Capture propre de `KeyboardInterrupt` (`Ctrl+C`) sans stacktrace.

---

## 🚀 5. Guide d'Utilisation

### Activation de l'environnement virtuel :
```bash
source .venv/bin/activate
```

### Commandes usuelles :
```bash
# Exécution par défaut (Binance, 30 jours, paires EUR)
python src/main.py

# Lister les devises de cotation (Quotes) disponibles sur une plateforme :
python src/main.py --list-quotes
python src/main.py --exchange coinbase --list-quotes

# Exécution surchargée :
python src/main.py --exchange binance --quote USD --days 14
```

---

## 🧪 6. Qualité de Code & Tests Automatisés

- **Tests unitaires et d'intégration** : 11 tests automatisés avec Pytest et Mocks CCXT (`unittest.mock`) exécutés en 0.26s.
- **Linter & Formateur** : Validation par **Ruff** sans aucun avertissement ni erreur de style (conforme PEP8).
- **Resolution PYTHONPATH** : Bloc dynamique dans `src/main.py` et `src/cli.py` garantissant l'exécution sans erreur depuis n'importe quel sous-dossier.
