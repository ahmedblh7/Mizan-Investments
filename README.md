# ⚖️ Mizan Investments

**Institutional Grade Asset Intelligence & Ethical Screening.**
*Analyze. Screen. Dominate.*

Mizan Investments est un terminal d'analyse financière "Dark Luxury" conçu pour les investisseurs exigeants. Il combine l'analyse fondamentale rigoureuse (Value/Growth) avec un filtrage éthique strict (Shariah Compliant & Boycott Check).

---

## 🚀 Fonctionnalités Clés

* **📊 Scanner Fondamental :** Analyse en temps réel via l'API Yahoo Finance.
* **🕌 Conformité Éthique (Shariah) :**
    * Dette < 33% de la Capitalisation.
    * Revenus basés sur Intérêts (Riba) < 5%.
    * Ratio Liquidité & Actifs Réels.
    * **Boycott Check :** Vérification automatique via API externe.
* **🧠 3 Stratégies Algorithmiques :** Moteurs de notation propriétaires (voir ci-dessous).
* **🎯 Smart Exit Plan :**
    * Calcul dynamique des cibles de prix (TP1/TP2).
    * **Mode Hybride :** Bascule automatiquement sur le P/S (Price-to-Sales) si l'entreprise est déficitaire, ou le P/E si elle est rentable.
    * **Tendance :** Surveillance de la cassure via Moyenne Mobile 50.
* **🌍 Bilingue :** Interface complète en Anglais et Français.

---

## 📚 Les Stratégies (Moteurs v7.9)

| Stratégie | Profil | Critères Clés (Mis à jour) |
| :--- | :--- | :--- |
| **💎 Mizan Strategy** | *Quality Growth* | • **FCF Yield Dynamique** (>2.5% si croissance, >5% sinon)<br>• **P/E < 25** (Qualité à prix raisonnable)<br>• **Marge Ops > 15%** (Avantage concurrentiel) |
| **🛡️ Modern Graham** | *Safe Value* | • **P/E < 15** (Discipline stricte)<br>• **Interest Coverage > 3x** (Solvabilité)<br>• **ROE > 8%** (Rentabilité minimale)<br>• *Pas de filtre P/B (Obsolète)* |
| **🚀 Peter Lynch** | *Aggressive Growth* | • **PEG Ratio < 1.0** (La croissance est "gratuite")<br>• **Croissance > 15%**<br>• Dette/Capitaux < 80% |

---

## 🛠️ Installation & Démarrage

   ```bash
   git clone https://github.com/ahmedblh7/mizan-investments.git
   cd mizan-investments
   pip install -r requirements.txt


python -m venv venv
venv\Scripts\activate
streamlit run app.py

git add .
git commit -m "Update"
git push