# Test Technique - Backend & Data Shell

Ce dépôt contient le projet développé dans le cadre du test technique. Il est pré-configuré avec une architecture modulaire en Python 3.11+, un outillage de qualité (Pytest, Ruff) et une conteneurisation Docker.

---

## 📋 1. Contexte & Objectifs

> *Section à compléter durant l'exercice.*

- **Sujet / Problématique :** [Description du problème]
- **Objectifs principaux :**
  - [ ] Objectif 1
  - [ ] Objectif 2
  - [ ] Objectif 3

---

## 🏗️ 2. Architecture & Structure du Projet

```text
.
├── Dockerfile            # Containerisation du service
├── pyproject.toml        # Dépendances & configuration outils (Ruff, Pytest)
├── README.md             # Documentation principale
├── src/                  # Code source de l'application / scripts
│   ├── config.py         # Configuration globale & logging
│   └── main.py           # Coquille API (FastAPI)
├── tests/                # Suite de tests unitaires et d'intégration
│   ├── conftest.py       # Fixtures Pytest
│   └── test_main.py      # Validation de l'API
└── docs/                 # Documentation complémentaire ou schémas
```

---

## ⚙️ 3. Préréquis

- **Python :** `>= 3.11`
- **Docker :** Optional (pour la conteneurisation)
- **macOS / Linux / Windows**

---

## 🚀 4. Installation & Démarrage Rapide

### 4.1. Environnement virtuel Python

```bash
# 1. Création du venv
python3 -m venv .venv

# 2. Activation du venv (macOS / Linux)
source .venv/bin/activate

# 3. Installation des dépendances et outils dev
pip install -e ".[dev]"
```

### 4.2. Démarrage de l'API (FastAPI)

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
