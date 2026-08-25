# Ticket 5 : Tests Unitaires et Validation d'Intégration

## Status: Draft
## Priority: Medium

### 🎯 Objectif
Garantir la fiabilité du projet par des tests automatisés (Pytest), en mockant les appels d'API externes pour éviter d'être dépendant du réseau lors de la suite de tests.

### 📋 Spécifications Fonctionnelles
1. **Tests Mathématiques (`tests/test_metrics.py`)** :
   - Tester le calcul de la volatilité, du dernier prix et du volume moyen avec des séries de prix connues (ex: séries constantes, séries avec volatilité connue).

2. **Tests de Collecte (`tests/test_exchange.py`)** :
   - Mocker l'exchange CCXT avec `unittest.mock` ou `pytest-mock` pour tester le filtrage des paires et la gestion des erreurs sans faire de requêtes HTTP réelles.

3. **Test d'Intégration du CSV (`tests/test_reporter.py`)** :
   - Vérifier qu'un fichier CSV valide est correctement créé et lisible avec la structure de colonnes exacte.

### 📦 LIVRABLES ATTENDUS
- Nouveaux fichiers de test sous `tests/`.
- Execution réussie de `pytest`.

### 🧪 Critères d'Acceptation
- Succès à 100% de `pytest`.
- Couverture de code décente sur la partie calculs financiers et génération CSV.
