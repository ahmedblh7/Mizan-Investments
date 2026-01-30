"""
Stratégies d'investissement.
Implémente différentes approches (Mizan, Graham, Lynch).
"""
from abc import ABC, abstractmethod
from typing import Type

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from domain.models import StockData, StrategyCheckResult, StrategyResult
from config.settings import Settings


class Strategy(ABC):
    """Interface abstraite pour les stratégies d'investissement."""
    
    name: str
    description: str
    
    @abstractmethod
    def evaluate(self, stock: StockData) -> StrategyResult:
        """
        Évalue une action selon les critères de la stratégie.
        
        Args:
            stock: Données de l'action.
            
        Returns:
            StrategyResult avec les détails de l'évaluation.
        """
        pass
    
    @staticmethod
    def _format_pe(pe: float | None) -> str:
        """Formate le ratio P/E pour affichage."""
        if pe is None or pe <= 0:
            return "N/A"
        return f"{pe:.2f}"
    
    @staticmethod
    def _format_percent(value: float) -> str:
        """Formate une valeur en pourcentage."""
        return f"{value:.1f}%"
    
    @staticmethod
    def _format_ratio(value: float) -> str:
        """Formate un ratio."""
        return f"{value:.2f}"


class MizanStrategy(Strategy):
    """
    Stratégie Mizan : Quality Growth.
    
    Focus sur :
    - FCF Yield dynamique (adapté à la croissance)
    - Valorisation raisonnable (P/E < 25)
    - Marges opérationnelles solides (> 15%)
    - Solvabilité (Net Debt/EBITDA < 3)
    """
    
    name = "Mizan"
    description = "Quality Growth - Focus on sustainable quality at reasonable prices"
    
    def evaluate(self, stock: StockData) -> StrategyResult:
        checks: list[StrategyCheckResult] = []
        
        # 1. FCF Yield dynamique
        is_growth_stock = stock.revenue_growth > 10
        target_fcf = Settings.MIZAN_FCF_YIELD_GROWTH if is_growth_stock else Settings.MIZAN_FCF_YIELD_MATURE
        fcf_target_desc = f"> {target_fcf}% ({'Growth' if is_growth_stock else 'Mature'})"
        
        checks.append(StrategyCheckResult(
            name="FCF Yield",
            value=self._format_percent(stock.fcf_yield),
            target=fcf_target_desc,
            passed=stock.fcf_yield > target_fcf,
        ))
        
        # 2. P/E Ratio
        pe_value = stock.pe_ratio if stock.pe_ratio and stock.pe_ratio > 0 else 999
        checks.append(StrategyCheckResult(
            name="P/E",
            value=self._format_pe(stock.pe_ratio),
            target=f"< {Settings.MIZAN_MAX_PE}",
            passed=pe_value < Settings.MIZAN_MAX_PE,
        ))
        
        # 3. Marge opérationnelle
        checks.append(StrategyCheckResult(
            name="Op. Margin",
            value=self._format_percent(stock.operating_margin),
            target=f"> {Settings.MIZAN_MIN_MARGIN}%",
            passed=stock.operating_margin > Settings.MIZAN_MIN_MARGIN,
        ))
        
        # 4. Solvabilité
        checks.append(StrategyCheckResult(
            name="Net Debt/EBITDA",
            value=f"{stock.net_debt_ebitda:.2f}x",
            target=f"< {Settings.MIZAN_MAX_NET_DEBT_EBITDA}x",
            passed=stock.net_debt_ebitda < Settings.MIZAN_MAX_NET_DEBT_EBITDA,
        ))
        
        return StrategyResult(strategy_name=self.name, checks=checks)


class GrahamStrategy(Strategy):
    """
    Stratégie Ben Graham : Modern Value.
    
    Focus sur :
    - Valorisation stricte (P/E < 15)
    - Liquidité (Current Ratio > 1.5)
    - Faible endettement (D/E < 50%)
    - Couverture des intérêts (> 3x)
    - Rentabilité (ROE > 8%)
    """
    
    name = "Graham"
    description = "Modern Value - Margin of safety with quality focus"
    
    def evaluate(self, stock: StockData) -> StrategyResult:
        checks: list[StrategyCheckResult] = []
        
        # 1. P/E Ratio
        pe_value = stock.pe_ratio if stock.pe_ratio and stock.pe_ratio > 0 else 999
        checks.append(StrategyCheckResult(
            name="P/E",
            value=self._format_pe(stock.pe_ratio),
            target=f"< {Settings.GRAHAM_MAX_PE}",
            passed=pe_value < Settings.GRAHAM_MAX_PE,
        ))
        
        # 2. Current Ratio
        checks.append(StrategyCheckResult(
            name="Current Ratio",
            value=self._format_ratio(stock.current_ratio),
            target=f"> {Settings.GRAHAM_MIN_CURRENT_RATIO}",
            passed=stock.current_ratio > Settings.GRAHAM_MIN_CURRENT_RATIO,
        ))
        
        # 3. Debt/Equity
        de_value = stock.debt_to_equity if stock.debt_to_equity else 999
        checks.append(StrategyCheckResult(
            name="Debt/Equity",
            value=f"{de_value:.0f}%",
            target=f"< {Settings.GRAHAM_MAX_DEBT_EQUITY}%",
            passed=de_value < Settings.GRAHAM_MAX_DEBT_EQUITY,
        ))
        
        # 4. Interest Coverage
        checks.append(StrategyCheckResult(
            name="Interest Coverage",
            value=f"{stock.interest_coverage:.1f}x",
            target=f"> {Settings.GRAHAM_MIN_INTEREST_COVERAGE}x",
            passed=stock.interest_coverage > Settings.GRAHAM_MIN_INTEREST_COVERAGE,
        ))
        
        # 5. ROE
        checks.append(StrategyCheckResult(
            name="ROE",
            value=self._format_percent(stock.roe),
            target=f"> {Settings.GRAHAM_MIN_ROE}%",
            passed=stock.roe > Settings.GRAHAM_MIN_ROE,
        ))
        
        return StrategyResult(strategy_name=self.name, checks=checks)


class LynchStrategy(Strategy):
    """
    Stratégie Peter Lynch : Growth.
    
    Focus sur :
    - PEG attractif (< 1.0)
    - Forte croissance (> 15%)
    - Endettement modéré (D/E < 80%)
    - Valorisation raisonnable (P/E < 25)
    """
    
    name = "Lynch"
    description = "Growth - GARP (Growth at Reasonable Price)"
    
    def evaluate(self, stock: StockData) -> StrategyResult:
        checks: list[StrategyCheckResult] = []
        
        # 1. PEG Ratio
        peg_value = stock.peg_ratio if stock.peg_ratio is not None else 999
        peg_display = f"{peg_value:.2f}" if stock.peg_ratio is not None else "N/A"
        checks.append(StrategyCheckResult(
            name="PEG",
            value=peg_display,
            target=f"< {Settings.LYNCH_MAX_PEG}",
            passed=peg_value < Settings.LYNCH_MAX_PEG,
        ))
        
        # 2. Revenue Growth
        checks.append(StrategyCheckResult(
            name="Revenue Growth",
            value=self._format_percent(stock.revenue_growth),
            target=f"> {Settings.LYNCH_MIN_GROWTH}%",
            passed=stock.revenue_growth > Settings.LYNCH_MIN_GROWTH,
        ))
        
        # 3. Debt/Equity
        de_value = stock.debt_to_equity if stock.debt_to_equity else 999
        checks.append(StrategyCheckResult(
            name="Debt/Equity",
            value=f"{de_value:.0f}%",
            target=f"< {Settings.LYNCH_MAX_DEBT_EQUITY}%",
            passed=de_value < Settings.LYNCH_MAX_DEBT_EQUITY,
        ))
        
        # 4. P/E Ratio
        pe_value = stock.pe_ratio if stock.pe_ratio and stock.pe_ratio > 0 else 999
        checks.append(StrategyCheckResult(
            name="P/E",
            value=self._format_pe(stock.pe_ratio),
            target=f"< {Settings.LYNCH_MAX_PE}",
            passed=pe_value < Settings.LYNCH_MAX_PE,
        ))
        
        return StrategyResult(strategy_name=self.name, checks=checks)


# Registre des stratégies disponibles
AVAILABLE_STRATEGIES: dict[str, Type[Strategy]] = {
    "Mizan": MizanStrategy,
    "Graham": GrahamStrategy,
    "Lynch": LynchStrategy,
}


def get_strategy(name: str) -> Strategy:
    """
    Factory pour obtenir une instance de stratégie.
    
    Args:
        name: Nom de la stratégie ("Mizan", "Graham", "Lynch")
        
    Returns:
        Instance de la stratégie.
        
    Raises:
        ValueError: Si la stratégie n'existe pas.
    """
    if name not in AVAILABLE_STRATEGIES:
        available = ", ".join(AVAILABLE_STRATEGIES.keys())
        raise ValueError(f"Stratégie '{name}' inconnue. Disponibles: {available}")
    
    return AVAILABLE_STRATEGIES[name]()