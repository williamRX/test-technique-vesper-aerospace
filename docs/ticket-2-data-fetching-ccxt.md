# Ticket 2 : Collecte des Données de Marché via CCXT

## Status: Draft
## Priority: High

### 🎯 Objectif
Se connecter à l'API publique d'une plateforme d'échange (Coinbase ou Binance) via la bibliothèque **CCXT** pour lister les paires de cryptomonnaies actives contre la monnaie Fiat choisie et récupérer leur historique de prix journalier (OHLCV).

### 📋 Spécifications Fonctionnelles
1. **Initialisation CCXT** :
   - Instancier l'exchange choisi (`ccxt.coinbase()` ou `ccxt.binance()`) avec `enableRateLimit=True`.
   - Pas besoin de clés d'API (utilisation exclusive des endpoints publics).

2. **Filtrage des Marchés** :
   - Charger la liste des marchés avec `fetch_markets()`.
   - Filtrer pour ne conserver que les paires spot actives dont la monnaie de cotation (`quote`) correspond au paramètre `QUOTE_CURRENCY` (ex: `BTC/EUR`, `ETH/EUR`).

3. **Récupération des Bougies (OHLCV)** :
   - Pour chaque paire sélectionnée, récupérer l'historique sur la période demandée (`DAYS_PERIOD`) à la résolution journalière (`timeframe='1d'`).
   - Gérer proprement les erreurs réseau, le rate limiting et les paires sans données suffisantes.

### 📦 LIVRABLES ATTENDUS
- Module `src/services/exchange.py` avec des fonctions de fetch autonomes.
- Structure de données de retour propre (ex: DataFrame pandas ou liste de dicts avec timestamps, prix de clôture `close`, et volume `volume`).

### 🧪 Critères d'Acceptation
- Capable de lister toutes les paires `*/EUR` ou `*/USD` de la plateforme.
- Récupération d'au moins $N$ bougies journalières par paire.
- Résilience face aux erreurs d'API (retry ou ignorer la paire si données insuffisantes).
