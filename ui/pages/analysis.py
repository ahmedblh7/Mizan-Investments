"""
Page d'analyse principale.
"""
import streamlit as st

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from domain.models import StockData, ShariahResult, StrategyResult
from domain.shariah import ShariahAnalyzer
from domain.strategies import get_strategy
from services.market_data import MarketDataService
from services.external_apis import BoycottChecker
from config.translations import Translations
from ui.components import (
    render_verdict_box,
    render_quality_gauge,
    render_strategy_results,
    render_shariah_checks,
    render_price_chart,
)


def render_analysis_page(
    ticker: str,
    strategy_name: str,
    translations: Translations,
) -> None:
    """
    Affiche la page d'analyse complète pour un ticker.
    
    Args:
        ticker: Symbole boursier.
        strategy_name: Nom de la stratégie à appliquer.
        translations: Traductions à utiliser.
    """
    with st.spinner(translations.crunching):
        try:
            # Charger les données
            market_service = MarketDataService(ticker)
            stock_data = market_service.get_stock_data()
            
            # Analyse Shariah
            boycott_checker = BoycottChecker()
            shariah_analyzer = ShariahAnalyzer(
                boycott_checker=boycott_checker.is_boycotted
            )
            shariah_result = shariah_analyzer.analyze(stock_data)
            
            # Analyse stratégie
            strategy = get_strategy(strategy_name)
            strategy_result = strategy.evaluate(stock_data)
            
            # Affichage
            _render_header(stock_data, translations)
            _render_verdict_and_score(shariah_result, strategy_result, translations)
            _render_tabs(
                stock_data, 
                shariah_result, 
                strategy_result, 
                market_service,
                translations,
            )
            
        except ValueError as e:
            st.error(f"Erreur: {e}")
        except Exception as e:
            st.error(f"Erreur inattendue: {e}")


def _render_header(stock_data: StockData, translations: Translations) -> None:
    """Affiche l'en-tête avec les métriques principales."""
    st.markdown("---")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(translations.company, stock_data.name)
    m2.metric(
        translations.price, 
        f"{stock_data.current_price} {stock_data.currency}"
    )
    m3.metric(
        translations.mcap, 
        f"{stock_data.market_cap / 1e9:.1f}B"
    )
    m4.metric(
        translations.momentum,
        f"{stock_data.momentum_3m:.2f}%",
        delta_color="normal" if stock_data.momentum_3m > 0 else "inverse",
    )
    
    st.markdown("###")


def _render_verdict_and_score(
    shariah_result: ShariahResult,
    strategy_result: StrategyResult,
    translations: Translations,
) -> None:
    """Affiche le verdict Shariah et le score qualité."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_verdict_box(shariah_result, translations)
    
    with col2:
        render_quality_gauge(
            score=strategy_result.score,
            is_compliant=shariah_result.is_compliant,
            title=translations.mizan_score,
        )


def _render_tabs(
    stock_data: StockData,
    shariah_result: ShariahResult,
    strategy_result: StrategyResult,
    market_service: MarketDataService,
    translations: Translations,
) -> None:
    """Affiche les onglets d'analyse."""
    tab1, tab2, tab3 = st.tabs([
        translations.tab_fund,
        translations.tab_shariah,
        translations.tab_exit,
    ])
    
    with tab1:
        render_strategy_results(strategy_result.checks)
    
    with tab2:
        render_shariah_checks(
            shariah_result,
            stock_data.industry,
            translations,
        )
    
    with tab3:
        _render_exit_plan(stock_data, market_service, translations)


def _render_exit_plan(
    stock_data: StockData,
    market_service: MarketDataService,
    translations: Translations,
) -> None:
    """Affiche le plan de sortie avec graphique et objectifs."""
    price_history = market_service.get_price_history("1y")
    
    if price_history.empty:
        st.warning("Insufficient data for chart.")
        return
    
    # Calculer les objectifs basés sur EPS ou Revenue per Share
    tp1, tp2 = 0.0, 0.0
    
    if stock_data.eps and stock_data.eps > 0:
        # Objectifs basés sur P/E cible
        tp1 = stock_data.eps * 15  # P/E conservateur
        tp2 = stock_data.eps * 25  # P/E optimiste
    elif stock_data.revenue_per_share > 0:
        # Objectifs basés sur P/S cible
        tp1 = stock_data.revenue_per_share * 6
        tp2 = stock_data.revenue_per_share * 10
    
    if tp1 > 0:
        # Graphique
        fig = render_price_chart(
            price_history,
            tp1,
            tp2,
            stock_data.currency,
            translations.chart_title,
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Métriques d'objectifs
        st.markdown(f"#### {translations.dynamic_targets}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric(translations.tp1_safety, f"{tp1:.2f} {stock_data.currency}")
        c2.metric(translations.tp2_euphoria, f"{tp2:.2f} {stock_data.currency}")
        
        # Vérification tendance MA50
        if "MA50" in price_history.columns:
            ma50_series = price_history["MA50"].dropna()
            if not ma50_series.empty:
                ma50_val = ma50_series.iloc[-1]
                is_broken = stock_data.current_price < ma50_val
                c3.metric(
                    translations.trend_ma50,
                    "BROKEN" if is_broken else "INTACT",
                    f"{ma50_val:.2f}",
                    delta_color="inverse" if is_broken else "normal",
                )
    else:
        st.warning("Insufficient data for price targets.")