# Ticket 4 : Affichage Console et Exportation CSV

## Status: Draft
## Priority: High

### 🎯 Objectif
Afficher en direct la progression du traitement dans le terminal et exporter le tableau de résultat final dans un fichier CSV strictement conforme aux exigences du sujet.

### 📋 Spécifications Fonctionnelles
1. **Logging en Direct (Console)** :
   - Afficher l'activité en temps réel avec horodatage ou barre de progression (ex: `[INFO] Récupération des marchés pour Coinbase...`, `[INFO] [12/150] Traitement de BTC/EUR...`).

2. **Structure exacte du CSV de Sortie** :
   Le fichier CSV généré doit avoir l'en-tête exact suivant :
   ```csv
   base,quote,daily_volatility,last_price,average_volume
   ```

3. **Exemple de données CSV attendues** :
   ```csv
   BTC,EUR,3.3084702888119626,35617.08,1694.0949196774188
   ETH,EUR,3.1123116046847192,2360.35,23870.74
   ```

### 📦 LIVRABLES ATTENDUS
- Module `src/services/reporter.py` pour l'exportation CSV et la mise en forme.
- Intégration du système de logs `logging` ou `rich`.

### 🧪 Critères d'Acceptation
- Le fichier CSV généré respecte à la lettre les 5 noms de colonnes : `base`, `quote`, `daily_volatility`, `last_price`, `average_volume`.
- L'affichage console montre clairement la progression de la collecte sans spammer le terminal.
