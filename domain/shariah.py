"""
Analyseur de conformité Shariah.
Implémente les règles AAOIFI pour le screening d'actions.
"""
from dataclasses import dataclass
import logging

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from domain.models import StockData, ShariahResult
from config.settings import (
    Settings,
    SECTOR_BLACKLIST,
    KEYWORD_BLACKLIST,
)

logger = logging.getLogger(__name__)


class ShariahAnalyzer:
    """
    Analyse la conformité Shariah d'une action.
    
    Basé sur les standards AAOIFI (Accounting and Auditing Organization 
    for Islamic Financial Institutions).
    """
    
    def __init__(self, boycott_checker: callable = None):
        """
        Initialise l'analyseur.
        
        Args:
            boycott_checker: Fonction optionnelle pour vérifier le statut boycott.
                            Signature: (company_name: str) -> bool
        """
        self._boycott_checker = boycott_checker
    
    def analyze(self, stock: StockData) -> ShariahResult:
        """
        Analyse complète de conformité Shariah.
        
        Args:
            stock: Données de l'action à analyser.
            
        Returns:
            ShariahResult avec tous les détails de conformité.
        """
        failures: list[str] = []
        
        # 1. Vérification de l'activité commerciale
        is_activity_ok, activity_issue = self._check_business_activity(stock)
        if not is_activity_ok:
            failures.append("Activity")
            logger.info(f"{stock.ticker}: Activité non conforme - {activity_issue}")
        
        # 2. Vérification du boycott
        is_boycotted = self._check_boycott_status(stock.name)
        if is_boycotted:
            failures.append("Boycott Listed")
            logger.info(f"{stock.ticker}: Entreprise boycottée")
        
        # 3. Ratio de revenus d'intérêts (< 5%)
        interest_ratio = stock.interest_income_ratio
        if interest_ratio >= Settings.MAX_INTEREST_INCOME_RATIO:
            failures.append(f"Interest > {Settings.MAX_INTEREST_INCOME_RATIO}%")
            logger.info(f"{stock.ticker}: Intérêts {interest_ratio:.1f}% >= {Settings.MAX_INTEREST_INCOME_RATIO}%")
        
        # 4. Ratio de dette (< 33%)
        debt_ratio = stock.debt_ratio
        if debt_ratio >= Settings.MAX_DEBT_RATIO:
            failures.append(f"Debt > {Settings.MAX_DEBT_RATIO}%")
            logger.info(f"{stock.ticker}: Dette {debt_ratio:.1f}% >= {Settings.MAX_DEBT_RATIO}%")
        
        # 5. Ratio d'actifs réels/illiquides (> 20%)
        illiquid_ratio = stock.illiquid_assets_ratio
        if illiquid_ratio <= Settings.MIN_REAL_ASSETS_RATIO:
            failures.append(f"Real Assets < {Settings.MIN_REAL_ASSETS_RATIO}%")
            logger.info(f"{stock.ticker}: Actifs réels {illiquid_ratio:.1f}% <= {Settings.MIN_REAL_ASSETS_RATIO}%")
        
        # 6. Vérification liquidité (actifs courants < capitalisation)
        is_liquid_ok = stock.is_liquid_ok
        if not is_liquid_ok:
            failures.append("Cash > Cap")
            logger.info(f"{stock.ticker}: Actifs courants > capitalisation")
        
        return ShariahResult(
            interest_income_ratio=interest_ratio,
            debt_ratio=debt_ratio,
            illiquid_assets_ratio=illiquid_ratio,
            is_liquid_ok=is_liquid_ok,
            is_activity_compliant=is_activity_ok,
            activity_issue=activity_issue,
            is_boycotted=is_boycotted,
            failures=failures,
        )
    
    def _check_business_activity(self, stock: StockData) -> tuple[bool, str]:
        """
        Vérifie si l'activité de l'entreprise est conforme.
        
        Returns:
            Tuple (is_compliant, issue_description)
        """
        industry_lower = stock.industry.lower()
        sector_lower = stock.sector.lower()
        description_lower = stock.description.lower()
        
        # Vérification des secteurs blacklistés
        for blacklisted in SECTOR_BLACKLIST:
            if blacklisted in industry_lower or blacklisted in sector_lower:
                return False, f"Sector: {blacklisted.title()}"
        
        # Vérification des mots-clés dans la description
        for keyword in KEYWORD_BLACKLIST:
            # Recherche du mot entier (avec espaces)
            if f" {keyword} " in f" {description_lower} ":
                return False, f"Keyword: {keyword}"
        
        return True, "OK"
    
    def _check_boycott_status(self, company_name: str) -> bool:
        """
        Vérifie si l'entreprise est sur une liste de boycott.
        
        Returns:
            True si l'entreprise est boycottée.
        """
        if self._boycott_checker is None:
            return False
        
        try:
            return self._boycott_checker(company_name)
        except Exception as e:
            logger.warning(f"Erreur vérification boycott pour {company_name}: {e}")
            return False