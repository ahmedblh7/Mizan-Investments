import streamlit as st
import pandas as pd

# =========================================================
# 🎨 CONFIGURATION & DESIGN SYSTEM (IDENTIQUE À APP.PY)
# =========================================================
st.set_page_config(page_title="Stratégies | Mizan Investments", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    :root { --bg-dark: #0B0E13; --bg-card: rgba(28, 32, 43, 0.6); --accent-green: #00E096; --accent-gold: #E0C38C; --text-white: #FFFFFF; --text-silver: #C8CDD5; --border-subtle: rgba(255, 255, 255, 0.08); }
    .stApp { background-color: var(--bg-dark); background-image: radial-gradient(circle at 50% 0%, #151922 0%, #0B0E13 80%), url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231C202B' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E"); font-family: 'Inter', sans-serif; color: var(--text-silver); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }
    
    /* CARTES DÉTAILS */
    .strat-card { 
        background: var(--bg-card); 
        backdrop-filter: blur(12px); 
        border: 1px solid var(--border-subtle); 
        border-radius: 16px; 
        padding: 30px; 
        margin-bottom: 20px;
    }
    .strat-header {
        display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 15px;
    }
    .strat-title { font-family: 'Space Grotesk'; font-size: 1.5rem; font-weight: 700; color: white; }
    .strat-tag { padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    
    .tag-quality { background: rgba(0, 224, 150, 0.15); color: #00E096; border: 1px solid rgba(0, 224, 150, 0.3); }
    .tag-value { background: rgba(224, 195, 140, 0.15); color: #E0C38C; border: 1px solid rgba(224, 195, 140, 0.3); }
    .tag-growth { background: rgba(255, 75, 75, 0.15); color: #FF4B4B; border: 1px solid rgba(255, 75, 75, 0.3); }

    .kpi-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    
    .kpi-table th { 
        text-align: left; 
        color: #6E7687; 
        font-size: 0.85rem; 
        padding: 10px 15px; 
        border-bottom: 1px solid rgba(255,255,255,0.1); 
    }
    
    .kpi-table td { 
        padding: 12px 15px; 
        color: #C8CDD5; 
        font-size: 0.95rem; 
        border-bottom: 1px solid rgba(255,255,255,0.03); 
    }
    
    .kpi-val { font-family: 'Space Grotesk'; font-weight: 600; color: white; }
    
    .quote-box {
        font-style: italic; opacity: 0.7; border-left: 3px solid var(--accent-gold); padding-left: 15px; margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 📝 CONTENU
# =========================================================

st.markdown("# 📚 Bibliothèque des Stratégies")
st.markdown("Comprendre les modèles mathématiques derrière l'algorithme Mizan.")
st.markdown("---")

# --- STRATÉGIE 1: MIZAN STRATEGY (V7.6) ---
st.markdown("""
<div class="strat-card">
<div class="strat-header">
<div class="strat-title">💎 Mizan Strategy (Quality Growth)</div>
<div class="strat-tag tag-quality">ÉQUILIBRÉ / CASH</div>
</div>
<p><strong>Philosophie :</strong> "La Qualité à Prix Raisonnable."</p>
<p>Cette stratégie modernisée recherche l'équilibre parfait entre solidité financière et croissance. Elle s'adapte dynamiquement : elle exige un rendement cash élevé pour les entreprises matures, mais tolère un rendement plus faible pour les leaders en forte croissance, à condition que la marge opérationnelle prouve leur supériorité (Moat).</p>
<div class="quote-box">"Mieux vaut acheter une entreprise merveilleuse à un prix correct qu'une entreprise correcte à un prix merveilleux." (Warren Buffett)</div>
<table class="kpi-table">
<thead><tr><th>KPI</th><th>Cible</th><th>Pourquoi ?</th></tr></thead>
<tbody>
<tr><td><span class="kpi-val">FCF Yield</span></td><td class="kpi-val">Dynamique</td><td>> 5% si mature, > 2.5% si forte croissance (>10%/an).</td></tr>
<tr><td><span class="kpi-val">PER (P/E)</span></td><td class="kpi-val">< 25</td><td>On accepte de payer la qualité jusqu'à 25x, mais pas au-delà.</td></tr>
<tr><td><span class="kpi-val">Marge Ops</span></td><td class="kpi-val">> 15%</td><td>Preuve d'un avantage concurrentiel durable (Moat).</td></tr>
<tr><td><span class="kpi-val">Dette Nette/EBITDA</span></td><td class="kpi-val">< 3.0x</td><td>Capacité à rembourser ses dettes en moins de 3 ans.</td></tr>
</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# --- STRATÉGIE 2: MODERN GRAHAM (V7.6) ---
st.markdown("""
<div class="strat-card">
<div class="strat-header">
<div class="strat-title">🛡️ Ben Graham (Modern Value)</div>
<div class="strat-tag tag-value">DÉFENSIF / SÉCURITÉ</div>
</div>
<p><strong>Philosophie :</strong> "Sécurité et Solvabilité avant tout."</p>
<p>Une version modernisée de la stratégie "Deep Value". Nous avons supprimé le ratio P/B (obsolète pour les sociétés de services/tech) et ajouté des critères stricts de solvabilité pour éviter les "pièges de valeur" (entreprises pas chères car en faillite).</p>
<div class="quote-box">"L'essence de l'investissement est la gestion des risques, pas la gestion des rendements."</div>
<table class="kpi-table">
<thead><tr><th>KPI</th><th>Cible</th><th>Pourquoi ?</th></tr></thead>
<tbody>
<tr><td><span class="kpi-val">PER</span></td><td class="kpi-val">< 15</td><td>Discipline de prix stricte. On ne surpaie jamais.</td></tr>
<tr><td><span class="kpi-val">Interest Coverage</span></td><td class="kpi-val">> 3.0x</td><td>L'entreprise doit générer 3x plus de profits que ce que lui coûte sa dette.</td></tr>
<tr><td><span class="kpi-val">ROE</span></td><td class="kpi-val">> 8%</td><td>Minimum vital de rentabilité pour éviter les entreprises "zombies".</td></tr>
<tr><td><span class="kpi-val">Current Ratio</span></td><td class="kpi-val">> 1.5</td><td>Liquidité immédiate pour payer les factures à court terme.</td></tr>
<tr><td><span class="kpi-val">Dette/Capitaux</span></td><td class="kpi-val">< 50%</td><td>Structure financière saine, peu dépendante des banques.</td></tr>
</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# --- STRATÉGIE 3: PETER LYNCH ---
st.markdown("""
<div class="strat-card">
<div class="strat-header">
<div class="strat-title">🚀 Peter Lynch (Growth)</div>
<div class="strat-tag tag-growth">OFFENSIF / CROISSANCE</div>
</div>
<p><strong>Philosophie :</strong> "La croissance à prix raisonnable (GARP)."</p>
<p>Peter Lynch cherchait les "Tenbaggers". Il aimait les entreprises qui croissent vite, mais il utilisait le ratio PEG pour vérifier si le prix actuel justifiait cette croissance.</p>
<div class="quote-box">"Derrière chaque action, il y a une entreprise. Découvrez ce qu'elle fait."</div>
<table class="kpi-table">
<thead><tr><th>KPI</th><th>Cible</th><th>Pourquoi ?</th></tr></thead>
<tbody>
<tr><td><span class="kpi-val">PEG Ratio</span></td><td class="kpi-val">< 1.0</td><td>Le ratio PER divisé par la Croissance. < 1 signifie que la croissance est "bradée".</td></tr>
<tr><td><span class="kpi-val">Croissance CA</span></td><td class="kpi-val">> 15%</td><td>On veut une entreprise en pleine expansion, pas une qui stagne.</td></tr>
<tr><td><span class="kpi-val">PER</span></td><td class="kpi-val">< 25</td><td>Un garde-fou. Même si ça croît vite, on évite les bulles spéculatives.</td></tr>
<tr><td><span class="kpi-val">Dette/Capitaux</span></td><td class="kpi-val">< 80%</td><td>La croissance doit être organique, pas dopée par un endettement massif.</td></tr>
</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# --- SECTION SHARIAH ---
st.markdown("### 🕌 Standards Éthiques & Shariah (IFG)")
st.info("""
Toutes les stratégies ci-dessus sont filtrées par la couche de conformité suivante :
1.  **Dette portant intérêts** < 33% de la Capitalisation Boursière.
2.  **Actifs portant intérêts** (Cash placé) < 33% de la Capitalisation Boursière.
3.  **Revenus basés sur Intérêts** (Riba) < 5% du Chiffre d'Affaires total.
4.  **Vérification Politique** : Exclusion des entreprises listées sur l'API de Boycott.
""")