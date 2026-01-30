"""
Service d'accès aux données de marché via yfinance.
"""
import logging
from typing import Optional
from functools import lru_cache

import yfinance as yf
import pandas as pd

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from domain.models import StockData

logger = logging.getLogger(__name__)


class MarketDataService:
    """
    Service pour récupérer les données financières d'une action.
    Encapsule les appels à yfinance avec gestion d'erreurs robuste.
    """
    
    def __init__(self, ticker: str):
        """
        Initialise le service pour un ticker donné.
        
        Args:
            ticker: Symbole boursier (ex: "AAPL", "MSFT")
        """
        self.ticker = ticker.upper()
        self._stock: Optional[yf.Ticker] = None
        self._info: Optional[dict] = None
        self._financials: Optional[pd.DataFrame] = None
        self._balance_sheet: Optional[pd.DataFrame] = None
        self._income_stmt: Optional[pd.DataFrame] = None
        self._cashflow: Optional[pd.DataFrame] = None
    
    def _load_data(self) -> None:
        """Charge toutes les données depuis yfinance."""
        if self._stock is not None:
            return
        
        logger.info(f"Chargement des données pour {self.ticker}")
        self._stock = yf.Ticker(self.ticker)
        
        # Charger toutes les données en une fois
        self._info = self._stock.info or {}
        self._financials = self._stock.financials
        self._balance_sheet = self._stock.balance_sheet
        self._income_stmt = self._stock.income_stmt
        self._cashflow = self._stock.cashflow
    
    def _safe_get(self, key: str, default=None):
        """Récupère une valeur de info de manière sécurisée."""
        self._load_data()
        return self._info.get(key, default)
    
    def _get_financial_item(
        self, 
        df: Optional[pd.DataFrame], 
        possible_names: list[str],
        default: float = 0.0
    ) -> float:
        """
        Récupère un élément financier avec plusieurs noms possibles.
        
        Args:
            df: DataFrame des données financières.
            possible_names: Liste de noms possibles pour l'élément.
            default: Valeur par défaut si non trouvé.
        
        Returns:
            Valeur de l'élément ou default.
        """
        if df is None or df.empty:
            return default
        
        for name in possible_names:
            if name in df.index:
                value = df.loc[name].iloc[0]
                if pd.notna(value):
                    return float(value)
        
        return default
    
    def get_stock_data(self) -> StockData:
        """
        Récupère toutes les données nécessaires pour l'analyse.
        
        Returns:
            StockData avec toutes les métriques.
            
        Raises:
            ValueError: Si les données minimales ne sont pas disponibles.
        """
        self._load_data()
        
        # Données de base
        name = self._safe_get("longName", self.ticker)
        if not name:
            raise ValueError(f"Impossible de charger les données pour {self.ticker}")
        
        market_cap = self._safe_get("marketCap", 0)
        if market_cap <= 0:
            market_cap = 1  # Éviter division par zéro
        
        # Calcul FCF
        fcf_yield = self._calculate_fcf_yield(market_cap)
        
        # Calcul Net Debt / EBITDA
        net_debt_ebitda = self._calculate_net_debt_ebitda()
        
        # Calcul croissance revenue
        revenue_growth, revenue_per_share = self._calculate_revenue_metrics()
        
        # Calcul couverture des intérêts
        interest_coverage = self._calculate_interest_coverage()
        
        # Calcul momentum 3 mois
        momentum_3m = self._calculate_momentum()
        
        # Données pour Shariah
        total_assets = self._get_financial_item(
            self._balance_sheet, 
            ["Total Assets"]
        )
        if total_assets <= 0:
            total_assets = 1
        
        total_debt = self._safe_get("totalDebt", 0)
        
        interest_income = self._get_financial_item(
            self._income_stmt,
            ["Interest Income", "Interest Income Non Operating", "Total Interest Income"]
        )
        
        # Actifs illiquides
        ppe = self._get_financial_item(
            self._balance_sheet,
            ["Net PPE", "Net Property, Plant And Equipment"]
        )
        goodwill = self._get_financial_item(self._balance_sheet, ["Goodwill"])
        intangibles = self._get_financial_item(
            self._balance_sheet,
            ["Intangible Assets", "Other Intangible Assets"]
        )
        inventory = self._get_financial_item(self._balance_sheet, ["Inventory"])
        illiquid_assets = ppe + goodwill + intangibles + inventory
        
        current_assets = self._get_financial_item(
            self._balance_sheet,
            ["Total Current Assets", "Current Assets"]
        )
        
        # Si pas d'actifs illiquides calculés, estimer
        if illiquid_assets == 0 and current_assets > 0:
            illiquid_assets = total_assets - current_assets
        
        # Revenus totaux
        total_revenue = self._get_financial_item(
            self._financials,
            ["Total Revenue", "Revenue"]
        )
        
        # ROE et marges
        roe_raw = self._safe_get("returnOnEquity", 0)
        roe = (roe_raw * 100) if roe_raw else 0.0
        
        margin_raw = self._safe_get("operatingMargins", 0)
        operating_margin = (margin_raw * 100) if margin_raw else 0.0
        
        return StockData(
            ticker=self.ticker,
            name=name,
            industry=self._safe_get("industry", "Unknown"),
            sector=self._safe_get("sector", "Unknown"),
            description=self._safe_get("longBusinessSummary", ""),
            currency=self._safe_get("currency", "USD"),
            current_price=self._safe_get("currentPrice", 0),
            market_cap=market_cap,
            pe_ratio=self._safe_get("trailingPE"),
            pb_ratio=self._safe_get("priceToBook"),
            peg_ratio=self._safe_get("pegRatio"),
            eps=self._safe_get("trailingEps"),
            roe=roe,
            operating_margin=operating_margin,
            fcf_yield=fcf_yield,
            current_ratio=self._safe_get("currentRatio", 0),
            debt_to_equity=self._safe_get("debtToEquity", 0),
            net_debt_ebitda=net_debt_ebitda,
            interest_coverage=interest_coverage,
            revenue_growth=revenue_growth,
            revenue_per_share=revenue_per_share,
            momentum_3m=momentum_3m,
            total_debt=total_debt,
            total_assets=total_assets,
            interest_income=interest_income,
            illiquid_assets=illiquid_assets,
            current_assets=current_assets,
            total_revenue=total_revenue,
        )
    
    def _calculate_fcf_yield(self, market_cap: float) -> float:
        """Calcule le rendement du Free Cash Flow."""
        try:
            ocf = self._get_financial_item(
                self._cashflow,
                ["Operating Cash Flow", "Total Cash From Operating Activities"]
            )
            # CapEx est généralement négatif dans yfinance
            capex = self._get_financial_item(
                self._cashflow,
                ["Capital Expenditure", "Net PPE Purchase And Sale"]
            )
            
            # FCF = OCF - |CapEx| (capex est déjà négatif donc on additionne)
            fcf = ocf + capex
            
            if market_cap > 0:
                return (fcf / market_cap) * 100
        except Exception as e:
            logger.warning(f"Erreur calcul FCF yield: {e}")
        
        return 0.0
    
    def _calculate_net_debt_ebitda(self) -> float:
        """Calcule le ratio Net Debt / EBITDA."""
        try:
            total_debt = self._safe_get("totalDebt", 0)
            cash = self._safe_get("totalCash", 0)
            ebitda = self._safe_get("ebitda", 0)
            
            if ebitda and ebitda > 0:
                return (total_debt - cash) / ebitda
        except Exception as e:
            logger.warning(f"Erreur calcul Net Debt/EBITDA: {e}")
        
        return 0.0
    
    def _calculate_revenue_metrics(self) -> tuple[float, float]:
        """Calcule la croissance des revenus et le revenu par action."""
        try:
            if self._financials is None or self._financials.empty:
                return 0.0, 0.0
            
            if "Total Revenue" not in self._financials.index:
                return 0.0, 0.0
            
            revenues = self._financials.loc["Total Revenue"]
            
            # Croissance YoY
            growth = 0.0
            if len(revenues) >= 2:
                current = revenues.iloc[0]
                previous = revenues.iloc[1]
                if previous and previous > 0:
                    growth = ((current - previous) / previous) * 100
            
            # Revenu par action
            rps = 0.0
            shares = self._safe_get("sharesOutstanding", 0)
            if shares and shares > 0 and len(revenues) > 0:
                rps = revenues.iloc[0] / shares
            
            return growth, rps
            
        except Exception as e:
            logger.warning(f"Erreur calcul revenue metrics: {e}")
            return 0.0, 0.0
    
    def _calculate_interest_coverage(self) -> float:
        """Calcule le ratio de couverture des intérêts."""
        try:
            ebit = self._get_financial_item(
                self._financials,
                ["Ebit", "Operating Income", "Earnings Before Interest and Taxes"]
            )
            
            interest_expense = self._get_financial_item(
                self._financials,
                ["Interest Expense", "Interest Expense Non Operating"]
            )
            interest_expense = abs(interest_expense)
            
            if interest_expense > 0:
                return ebit / interest_expense
            
            # Pas de dette = couverture "infinie"
            return 100.0
            
        except Exception as e:
            logger.warning(f"Erreur calcul interest coverage: {e}")
            return 0.0
    
    def _calculate_momentum(self, period: str = "3mo") -> float:
        """Calcule le momentum sur une période."""
        try:
            if self._stock is None:
                self._load_data()
            
            hist = self._stock.history(period=period)
            
            if hist.empty or len(hist) < 2:
                return 0.0
            
            start_price = hist["Close"].iloc[0]
            end_price = hist["Close"].iloc[-1]
            
            if start_price > 0:
                return ((end_price - start_price) / start_price) * 100
                
        except Exception as e:
            logger.warning(f"Erreur calcul momentum: {e}")
        
        return 0.0
    
    def get_price_history(self, period: str = "1y") -> pd.DataFrame:
        """
        Récupère l'historique des prix.
        
        Args:
            period: Période ("1mo", "3mo", "6mo", "1y", "2y", "5y")
            
        Returns:
            DataFrame avec colonnes Date, Close, et MA50.
        """
        try:
            if self._stock is None:
                self._load_data()
            
            hist = self._stock.history(period=period)
            
            if hist.empty:
                return pd.DataFrame()
            
            # Calculer MA50
            hist["MA50"] = hist["Close"].rolling(window=50).mean()
            
            return hist[["Close", "MA50"]]
            
        except Exception as e:
            logger.warning(f"Erreur récupération historique: {e}")
            return pd.DataFrame()