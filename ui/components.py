"""
Composants UI réutilisables pour l'application Mizan.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from domain.models import StrategyCheckResult, ShariahResult
from config.translations import Translations
from ui.styles import COLORS


def render_kpi_card(
    label: str,
    value: str,
    target: str,
    passed: bool,
) -> None:
    """
    Affiche une carte KPI avec indicateur de succès/échec.
    
    Args:
        label: Libellé du KPI.
        value: Valeur affichée.
        target: Cible ou seuil.
        passed: Si le critère est validé.
    """
    color_class = "val-green" if passed else "val-red"
    
    html = f"""
    <div class="glass-card">
        <div>
            <div class="kpi-title">{label}</div>
            <div class="kpi-value {color_class}">{value}</div>
        </div>
        <div class="kpi-target">
            <span style="opacity:0.5;">Target:</span> {target}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_strategy_results(results: list[StrategyCheckResult]) -> None:
    """
    Affiche les résultats d'une stratégie sous forme de grille de KPIs.
    
    Args:
        results: Liste des résultats de critères.
    """
    cols = st.columns(4)
    
    for i, check in enumerate(results):
        with cols[i % 4]:
            render_kpi_card(
                label=check.name,
                value=check.value,
                target=check.target,
                passed=check.passed,
            )


def render_verdict_box(
    shariah_result: ShariahResult,
    translations: Translations,
) -> None:
    """
    Affiche la boîte de verdict Shariah.
    
    Args:
        shariah_result: Résultat de l'analyse Shariah.
        translations: Traductions à utiliser.
    """
    if shariah_result.is_compliant:
        html = f"""
        <div class="verdict-box verdict-halal">
            <div style="font-size:2rem; text-shadow: 0 0 20px #00E096;">⚖️</div>
            <div>
                <div style="font-weight:700; font-size:1.2rem; font-family:'Space Grotesk'; color:#00E096;">
                    {translations.verdict_halal_title}
                </div>
                <div style="font-size:0.9rem; opacity:0.8;">
                    {translations.verdict_halal_desc}
                </div>
            </div>
        </div>
        """
    else:
        failures_text = translations.verdict_haram_desc + ", ".join(shariah_result.failures)
        html = f"""
        <div class="verdict-box verdict-haram">
            <div style="font-size:2rem; text-shadow: 0 0 20px #FF4B4B;">🚫</div>
            <div>
                <div style="font-weight:700; font-size:1.2rem; font-family:'Space Grotesk'; color:#FF4B4B;">
                    {translations.verdict_haram_title}
                </div>
                <div style="font-size:0.9rem; opacity:0.8;">
                    {failures_text}
                </div>
            </div>
        </div>
        """
    
    st.markdown(html, unsafe_allow_html=True)


def render_quality_gauge(
    score: int,
    is_compliant: bool,
    title: str = "Quality Score",
) -> None:
    """
    Affiche un cercle de score interactif et animé.
    
    Args:
        score: Score de 0 à 100.
        is_compliant: Si l'actif est conforme Shariah.
        title: Titre du score.
    """
    # Couleur basée sur le score et la conformité
    if not is_compliant:
        main_color = COLORS["accent_red"]
        glow_color = "rgba(255, 75, 75, 0.4)"
    elif score >= 70:
        main_color = COLORS["accent_green"]
        glow_color = "rgba(0, 224, 150, 0.4)"
    elif score >= 50:
        main_color = COLORS["accent_gold"]
        glow_color = "rgba(224, 195, 140, 0.4)"
    else:
        main_color = "#FF8C42"  # Orange
        glow_color = "rgba(255, 140, 66, 0.4)"
    
    # Calcul du pourcentage pour le cercle (circumference = 2 * PI * radius)
    # Radius = 54, donc circumference ≈ 339.29
    circumference = 339.29
    stroke_dashoffset = circumference - (circumference * score / 100)
    
    # Générer un ID unique pour l'animation
    import random
    unique_id = f"score_{random.randint(1000, 9999)}"
    
    html = f"""
    <style>
        .score-circle-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        
        .score-circle {{
            position: relative;
            width: 140px;
            height: 140px;
        }}
        
        .score-circle svg {{
            transform: rotate(-90deg);
            width: 140px;
            height: 140px;
        }}
        
        .score-circle .bg {{
            fill: none;
            stroke: rgba(255, 255, 255, 0.08);
            stroke-width: 8;
        }}
        
        .score-circle .progress-{unique_id} {{
            fill: none;
            stroke: {main_color};
            stroke-width: 8;
            stroke-linecap: round;
            stroke-dasharray: {circumference};
            stroke-dashoffset: {circumference};
            filter: drop-shadow(0 0 8px {glow_color});
            animation: fill-{unique_id} 1.5s ease-out forwards;
        }}
        
        @keyframes fill-{unique_id} {{
            0% {{
                stroke-dashoffset: {circumference};
            }}
            100% {{
                stroke-dashoffset: {stroke_dashoffset};
            }}
        }}
        
        .score-value-container {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }}
        
        .score-value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: {main_color};
            text-shadow: 0 0 20px {glow_color};
            line-height: 1;
        }}
        
        .score-percent {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.9rem;
            color: {COLORS["text_muted"]};
            margin-top: 2px;
        }}
        
        .score-title {{
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: {COLORS["text_muted"]};
            margin-top: 12px;
            text-align: center;
        }}
        
        .score-circle:hover .progress-{unique_id} {{
            filter: drop-shadow(0 0 15px {glow_color}) drop-shadow(0 0 30px {glow_color});
            transition: filter 0.3s ease;
        }}
        
        .score-circle:hover .score-value {{
            text-shadow: 0 0 30px {glow_color};
            transition: text-shadow 0.3s ease;
        }}
    </style>
    
    <div class="score-circle-container">
        <div class="score-circle">
            <svg viewBox="0 0 120 120">
                <circle class="bg" cx="60" cy="60" r="54"/>
                <circle class="progress-{unique_id}" cx="60" cy="60" r="54"/>
            </svg>
            <div class="score-value-container">
                <div class="score-value">{score}</div>
                <div class="score-percent">/ 100</div>
            </div>
        </div>
        <div class="score-title">{title}</div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def render_price_chart(
    price_history: pd.DataFrame,
    tp1: float,
    tp2: float,
    currency: str,
    title: str = "Price Action (1Y)",
) -> go.Figure:
    """
    Crée un graphique de prix avec objectifs.
    
    Args:
        price_history: DataFrame avec colonnes Close et MA50.
        tp1: Premier objectif de prix.
        tp2: Deuxième objectif de prix.
        currency: Devise.
        title: Titre du graphique.
        
    Returns:
        Figure Plotly.
    """
    fig = go.Figure()
    
    # Ligne de prix
    fig.add_trace(go.Scatter(
        x=price_history.index,
        y=price_history["Close"],
        mode="lines",
        name="Price",
        line=dict(color=COLORS["accent_green"], width=2),
    ))
    
    # Moyenne mobile 50 jours
    if "MA50" in price_history.columns:
        fig.add_trace(go.Scatter(
            x=price_history.index,
            y=price_history["MA50"],
            mode="lines",
            name="Trend (MA50)",
            line=dict(color=COLORS["text_muted"], width=1, dash="solid"),
            opacity=0.5,
        ))
    
    # Objectifs de prix
    if tp1 > 0:
        fig.add_hline(
            y=tp1,
            line_dash="dot",
            line_color=COLORS["accent_gold"],
            annotation_text="TP1",
            annotation_font_color=COLORS["accent_gold"],
        )
    
    if tp2 > 0:
        fig.add_hline(
            y=tp2,
            line_dash="dot",
            line_color=COLORS["accent_red"],
            annotation_text="TP2",
            annotation_font_color=COLORS["accent_red"],
        )
    
    fig.update_layout(
        template="plotly_dark",
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=450,
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(family="Space Grotesk"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
    )
    
    return fig


def render_shariah_checks(
    shariah_result: ShariahResult,
    industry: str,
    translations: Translations,
) -> None:
    """
    Affiche les vérifications Shariah détaillées.
    
    Args:
        shariah_result: Résultat de l'analyse.
        industry: Industrie de l'entreprise.
        translations: Traductions.
    """
    # Première ligne : Boycott et Activité
    col_a, col_b = st.columns(2)
    
    with col_a:
        render_kpi_card(
            label=translations.boycott_check,
            value="LISTED" if shariah_result.is_boycotted else "SAFE",
            target="Not Listed",
            passed=not shariah_result.is_boycotted,
        )
    
    with col_b:
        activity_status = "RESTRICTED" if not shariah_result.is_activity_compliant else "APPROVED"
        # Tronquer l'industrie si trop longue
        industry_display = industry[:15] + "..." if len(industry) > 15 else industry
        render_kpi_card(
            label=translations.act_check,
            value=activity_status,
            target=industry_display,
            passed=shariah_result.is_activity_compliant,
        )
    
    st.markdown("---")
    
    # Deuxième ligne : Ratios
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_kpi_card(
            label=translations.inc_haram,
            value=f"{shariah_result.interest_income_ratio:.2f}%",
            target="< 5%",
            passed=shariah_result.interest_income_ratio < 5,
        )
    
    with col2:
        render_kpi_card(
            label=translations.debt,
            value=f"{shariah_result.debt_ratio:.1f}%",
            target="< 33%",
            passed=shariah_result.debt_ratio < 33,
        )
    
    with col3:
        render_kpi_card(
            label=translations.real_assets,
            value=f"{shariah_result.illiquid_assets_ratio:.1f}%",
            target="> 20%",
            passed=shariah_result.illiquid_assets_ratio > 20,
        )
    
    with col4:
        render_kpi_card(
            label=translations.cash_cap,
            value="PASS" if shariah_result.is_liquid_ok else "FAIL",
            target="Cash < Cap",
            passed=shariah_result.is_liquid_ok,
        )