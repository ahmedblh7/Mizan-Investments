"""
Modèles de données pour l'application Mizan.
Utilise des dataclasses pour la clarté et l'immutabilité.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StockData:
    """Données financières d'une action."""
    
    ticker: str
    name: str
    industry: str
    sector: str
    description: str
    currency: str
    
    # Prix et valorisation
    current_price: float
    market_cap: float
    pe_ratio: Optional[float]
    pb_ratio: Optional[float]
    peg_ratio: Optional[float]
    eps: Optional[float]
    
    # Rentabilité
    roe: float
    operating_margin: float
    fcf_yield: float
    
    # Solvabilité
    current_ratio: float
    debt_to_equity: float
    net_debt_ebitda: float
    interest_coverage: float
    
    # Croissance
    revenue_growth: float
    revenue_per_share: float
    momentum_3m: float
    
    # Données Shariah
    total_debt: float
    total_assets: float
    interest_income: float
    illiquid_assets: float
    current_assets: float
    total_revenue: float
    
    @property
    def debt_ratio(self) -> float:
        """Ratio dette/actifs en pourcentage."""
        if self.total_assets <= 0:
            return 0.0
        return (self.total_debt / self.total_assets) * 100
    
    @property
    def interest_income_ratio(self) -> float:
        """Ratio revenus d'intérêts/revenus totaux en pourcentage."""
        if self.total_revenue <= 0:
            return 0.0
        return (self.interest_income / self.total_revenue) * 100
    
    @property
    def illiquid_assets_ratio(self) -> float:
        """Ratio actifs illiquides/actifs totaux en pourcentage."""
        if self.total_assets <= 0:
            return 0.0
        return (self.illiquid_assets / self.total_assets) * 100
    
    @property
    def is_liquid_ok(self) -> bool:
        """Vérifie si les actifs courants sont inférieurs à la capitalisation."""
        return self.current_assets < self.market_cap


@dataclass(frozen=True)
class StrategyCheckResult:
    """Résultat d'un critère de stratégie."""
    
    name: str
    value: str
    target: str
    passed: bool


@dataclass
class StrategyResult:
    """Résultat complet d'une évaluation de stratégie."""
    
    strategy_name: str
    checks: list[StrategyCheckResult] = field(default_factory=list)
    
    @property
    def score(self) -> int:
        """Score de 0 à 100 basé sur le nombre de critères validés."""
        if not self.checks:
            return 0
        passed = sum(1 for check in self.checks if check.passed)
        return int((passed / len(self.checks)) * 100)
    
    @property
    def passed_count(self) -> int:
        """Nombre de critères validés."""
        return sum(1 for check in self.checks if check.passed)
    
    @property
    def total_count(self) -> int:
        """Nombre total de critères."""
        return len(self.checks)


@dataclass
class ShariahResult:
    """Résultat de l'analyse de conformité Shariah."""
    
    # Ratios calculés
    interest_income_ratio: float
    debt_ratio: float
    illiquid_assets_ratio: float
    is_liquid_ok: bool
    
    # Vérifications
    is_activity_compliant: bool
    activity_issue: str
    is_boycotted: bool
    
    # Résultat final
    failures: list[str] = field(default_factory=list)
    
    @property
    def is_compliant(self) -> bool:
        """Indique si l'actif est conforme Shariah."""
        return len(self.failures) == 0
    
    @property
    def status(self) -> str:
        """Statut textuel de conformité."""
        return "HALAL" if self.is_compliant else "HARAM"


@dataclass
class AnalysisResult:
    """Résultat complet d'une analyse."""
    
    stock_data: StockData
    shariah_result: ShariahResult
    strategy_result: StrategyResult
    
    @property
    def is_investable(self) -> bool:
        """Indique si l'actif est investissable (conforme + bon score)."""
        return self.shariah_result.is_compliant and self.strategy_result.score >= 50