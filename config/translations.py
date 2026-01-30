"""
Système de traduction pour l'internationalisation.
"""
from dataclasses import dataclass
from typing import Literal

Language = Literal["en", "fr"]
SUPPORTED_LANGUAGES: list[Language] = ["en", "fr"]


@dataclass(frozen=True)
class Translations:
    """Conteneur immutable pour les traductions."""
    
    # Sidebar
    sidebar_title: str
    sidebar_subtitle: str
    analyze_btn: str
    search_placeholder: str
    no_result: str
    select_stock: str
    crunching: str
    
    # Hero
    hero_title: str
    hero_sub: str
    
    # Search
    search_title: str
    methodology: str
    
    # Verdict
    verdict_halal_title: str
    verdict_halal_desc: str
    verdict_haram_title: str
    verdict_haram_desc: str
    
    # Tabs
    tab_fund: str
    tab_shariah: str
    tab_exit: str
    
    # Metrics
    company: str
    price: str
    mcap: str
    momentum: str
    
    # Strategy
    strategy_label: str
    strat_name_mizan: str
    strat_name_graham: str
    strat_name_lynch: str
    strategy_active: str
    bullets_mizan: str
    bullets_graham: str
    bullets_shariah: str
    
    # Shariah checks
    act_check: str
    inc_haram: str
    debt: str
    real_assets: str
    cash_cap: str
    boycott_check: str
    
    # Charts
    chart_title: str
    dynamic_targets: str
    tp1_safety: str
    tp2_euphoria: str
    trend_ma50: str
    mizan_score: str
    
    # Watchlist
    watchlist_title: str
    watchlist_empty: str
    watchlist_add: str
    watchlist_create: str
    watchlist_save: str
    
    # Auth
    login: str
    signup: str
    logout: str
    email: str
    password: str
    login_success: str
    signup_success: str


_TRANSLATIONS: dict[Language, Translations] = {
    "en": Translations(
        sidebar_title="Mizan Inv.",
        sidebar_subtitle="Institutional Grade Analysis",
        analyze_btn="INITIATE SCAN",
        search_placeholder="Search ticker...",
        no_result="No asset found.",
        select_stock="Select Asset",
        crunching="Processing...",
        hero_title="Take your wealth<br>to the next level.",
        hero_sub="Manage. Analyze. Dominate.",
        search_title="ASSET INTELLIGENCE",
        methodology="Proprietary Algorithm",
        verdict_halal_title="COMPLIANT ASSET",
        verdict_halal_desc="Meets quantitative Shariah standards.",
        verdict_haram_title="NON-COMPLIANT",
        verdict_haram_desc="Failed checks: ",
        tab_fund="STRATEGY AUDIT",
        tab_shariah="COMPLIANCE",
        tab_exit="EXIT PLAN",
        company="Issuer",
        price="Spot Price",
        mcap="Market Cap",
        momentum="Momentum (3M)",
        strategy_label="STRATEGY SELECTION",
        strat_name_mizan="Mizan Strategy (Quality Growth)",
        strat_name_graham="Ben Graham (Modern Value)",
        strat_name_lynch="Peter Lynch (Growth)",
        strategy_active="Active Strategy:",
        bullets_mizan="• Dynamic FCF Yield<br>• P/E < 25<br>• Margin > 15%",
        bullets_graham="• P/E < 15<br>• Interest Cov > 3x<br>• ROE > 8%",
        bullets_shariah="• Debt < 33%<br>• Interest < 5%<br>• Real Assets > 20%",
        act_check="Activity",
        inc_haram="Interest Inc.",
        debt="Leverage",
        real_assets="Real Assets",
        cash_cap="Liquidity",
        boycott_check="Boycott",
        chart_title="Price Action (1Y)",
        dynamic_targets="🎯 Dynamic Targets",
        tp1_safety="TP1 (Safety)",
        tp2_euphoria="TP2 (Euphoria)",
        trend_ma50="Trend (MA50)",
        mizan_score="Mizan Quality Score",
        watchlist_title="My Watchlists",
        watchlist_empty="No lists created.",
        watchlist_add="Add to Watchlist",
        watchlist_create="Create new list",
        watchlist_save="Save stock",
        login="Login",
        signup="Sign Up",
        logout="Log out",
        email="Email",
        password="Password",
        login_success="Welcome!",
        signup_success="Account created! Check your emails.",
    ),
    "fr": Translations(
        sidebar_title="Mizan Inv.",
        sidebar_subtitle="Analyse de niveau institutionnel",
        analyze_btn="LANCER LE SCAN",
        search_placeholder="Rechercher...",
        no_result="Aucun actif trouvé.",
        select_stock="Sélectionner l'actif",
        crunching="Traitement...",
        hero_title="Votre patrimoine passe<br>au niveau supérieur.",
        hero_sub="Gérez. Analysez. Dominez.",
        search_title="INTELLIGENCE D'ACTIF",
        methodology="Algorithme Propriétaire",
        verdict_halal_title="ACTIF CONFORME",
        verdict_halal_desc="Respecte les standards Shariah.",
        verdict_haram_title="NON-CONFORME",
        verdict_haram_desc="Échecs : ",
        tab_fund="AUDIT STRATÉGIQUE",
        tab_shariah="CONFORMITÉ",
        tab_exit="PLAN DE SORTIE",
        company="Émetteur",
        price="Prix Spot",
        mcap="Capitalisation",
        momentum="Momentum 3M",
        strategy_label="SÉLECTION STRATÉGIE",
        strat_name_mizan="Stratégie Mizan (Qualité/Croissance)",
        strat_name_graham="Ben Graham (Modern Value)",
        strat_name_lynch="Peter Lynch (Croissance)",
        strategy_active="Stratégie Active :",
        bullets_mizan="• Rendement FCF Dynamique<br>• PER < 25<br>• Marge > 15%",
        bullets_graham="• PER < 15<br>• Couv. Intérêts > 3x<br>• ROE > 8%",
        bullets_shariah="• Dette < 33%<br>• Intérêts < 5%<br>• Actifs Réels > 20%",
        act_check="Activité",
        inc_haram="Revenus Intérêts",
        debt="Levier",
        real_assets="Actifs Réels",
        cash_cap="Liquidité",
        boycott_check="Boycott",
        chart_title="Action des Prix (1 An)",
        dynamic_targets="🎯 Objectifs Dynamiques",
        tp1_safety="TP1 (Sécurité)",
        tp2_euphoria="TP2 (Euphorie)",
        trend_ma50="Tendance (MA50)",
        mizan_score="Score Qualité Mizan",
        watchlist_title="Mes Watchlists",
        watchlist_empty="Aucune liste créée.",
        watchlist_add="Ajouter à une Watchlist",
        watchlist_create="Créer une nouvelle liste",
        watchlist_save="Sauvegarder l'action",
        login="Connexion",
        signup="Créer un compte",
        logout="Se déconnecter",
        email="Email",
        password="Mot de passe",
        login_success="Bienvenue !",
        signup_success="Compte créé ! Vérifiez vos emails.",
    ),
}


def get_translation(lang: Language) -> Translations:
    """Récupère les traductions pour une langue donnée."""
    if lang not in _TRANSLATIONS:
        raise ValueError(f"Langue non supportée: {lang}. Langues disponibles: {SUPPORTED_LANGUAGES}")
    return _TRANSLATIONS[lang]