# Test Technique - Backend & Data Shell

Ce dépôt contient le projet développé dans le cadre du test technique. Il est pré-configuré avec une architecture modulaire en Python 3.11+, un outillage de qualité (Pytest, Ruff) et une conteneurisation Docker.

---

## 📋 1. Contexte & Objectifs

Calculateur de la **volatilité quotidienne** des crypto-monnaies d'une plateforme d'échange (Binance/Coinbase) cotées contre une monnaie Fiat (ex: `EUR`) sur une période $N$ jours donnée via l'API **CCXT**.

---

## 🏗️ 2. Architecture & Structure du Projet

```text
.
├── Dockerfile            # Containerisation du service
├── pyproject.toml        # Dépendances (CCXT, FastAPI, Pytest, Ruff)
├── README.md             # Documentation principale
├── src/                  # Code source
│   ├── cli.py            # Point d'entrée CLI
│   ├── config.py         # Settings & Logging Pydantic v2
│   ├── main.py           # Point d'entrée script & API
│   ├── models/           # Dataclasses immuables (MarketCandle, VolatilityResult)
│   └── services/         # Services CCXT, Métriques mathématiques & Reporter CSV
├── tests/                # Suite de tests Pytest (11 tests)
└── docs/                 # Tickets de spécifications (Tickets 1 à 5)
```

---

## ⚙️ 3. Préréquis

- **Python :** `>= 3.11`
- **Docker :** Optionnel (pour la conteneurisation)

---

## 🚀 4. Installation & Démarrage Rapide

### 4.1. Activer l'environnement virtuel Python

Le dossier du venv s'appelle **`.venv`** (avec un point au début) :

```bash
# 1. Activation de l'environnement virtuel (macOS / Linux)
source .venv/bin/activate

# (Si le venv n'existe pas encore sur une nouvelle machine :)
# python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

### 4.2. Lancer le calculateur de volatilité (CLI)

Une fois l'environnement `.venv` activé :

```bash
# Exécution par défaut (Binance, 30 jours, paires EUR)
python src/main.py

# Ou avec des paramètres surchargés :
python src/main.py --days 30 --quote EUR --output crypto_volatility.csv
```

```bash
# Lancer le serveur de développement Uvicorn
uvicorn src.main:app --reload --port 8000
```
L'API sera disponible sur :
- Application : `http://localhost:8000`
- Documentation interactive (Swagger UI) : `http://localhost:8000/docs`

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

---

## 🐳 6. Conteneurisation (Docker)

```bash
# Build de l'image
docker build -t test-technique:latest .

# Lancement du conteneur
docker run -p 8000:8000 test-technique:latest
```

---

## 📌 7. Décisions Techniques & Arbitrages

> *Section réservée aux explications d'architecture, de choix d'algorithmes ou de modèles de données lors de la restitution.*

- **Choix 1 :** ...
- **Choix 2 :** ...
