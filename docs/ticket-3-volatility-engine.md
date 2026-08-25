# Ticket 3 : Moteur de Calcul de Volatilité et Indicateurs

## Status: Draft
## Priority: High

### 🎯 Objectif
Implémenter la logique mathématique pour calculer la volatilité quotidienne, le dernier prix et le volume moyen sur la période spécifiée pour chaque paire crypto/fiat.

### 📋 Formules et Spécifications Mathématiques
1. **Rendements Journaliers ($R_t$)** :
   Calculer la variation relative du prix de clôture ($P_t$) jour par jour :
   $$R_t = \frac{P_t - P_{t-1}}{P_{t-1}}$$
   *(ou Rendement Logarithmique : $R_t = \ln(P_t / P_{t-1})$)*

2. **Moyenne des Rendements ($\bar{R}$)** :
   $$\bar{R} = \frac{1}{M} \sum_{t=1}^{M} R_t$$
   *(où $M = N - 1$ est le nombre de rendements calculés sur la période)*

3. **Volatilité Quotidienne ($\sigma_{daily}$)** :
   Calcul de l'écart-type échantillonnel des rendements journaliers :
   $$\sigma_{daily} = \sqrt{\frac{1}{M - 1} \sum_{t=1}^{M} (R_t - \bar{R})^2}$$

4. **Dernier Prix (`last_price`)** :
   Prix de clôture de la toute dernière bougie complète disponible ($P_{dernier}$).

5. **Volume Moyen (`average_volume`)** :
   Moyenne arithmétique des volumes de transaction quotidiens sur la période :
   $$V_{moyen} = \frac{1}{N} \sum_{t=1}^{N} V_t$$

### 📦 LIVRABLES ATTENDUS
- Module `src/services/metrics.py` réutilisable (calculs via `numpy` / `pandas` ou fonctions pure Python).

### 🧪 Critères d'Acceptation
- Fonction de calcul testée unitairement avec des valeurs d'entrée contrôlées.
- Gestion des cas limites (ex: nombre de prix insuffisant $< 2$, volume nul).
