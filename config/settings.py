"""
Configuration centralisée de l'application Mizan.
"""
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(frozen=True)
class Settings:
    """Configuration immutable de l'application."""
    
    APP_NAME: ClassVar[str] = "Mizan Investments"
    APP_ICON: ClassVar[str] = "⚖️"
    VERSION: ClassVar[str] = "2.0.0"
    
    # Seuils Shariah
    MAX_DEBT_RATIO: ClassVar[float] = 33.0
    MAX_INTEREST_INCOME_RATIO: ClassVar[float] = 5.0
    MIN_REAL_ASSETS_RATIO: ClassVar[float] = 20.0
    
    # Seuils stratégies
    MIZAN_MAX_PE: ClassVar[float] = 25.0
    MIZAN_MIN_MARGIN: ClassVar[float] = 15.0
    MIZAN_MAX_NET_DEBT_EBITDA: ClassVar[float] = 3.0
    MIZAN_FCF_YIELD_GROWTH: ClassVar[float] = 2.5
    MIZAN_FCF_YIELD_MATURE: ClassVar[float] = 5.0
    
    GRAHAM_MAX_PE: ClassVar[float] = 15.0
    GRAHAM_MIN_CURRENT_RATIO: ClassVar[float] = 1.5
    GRAHAM_MAX_DEBT_EQUITY: ClassVar[float] = 50.0
    GRAHAM_MIN_INTEREST_COVERAGE: ClassVar[float] = 3.0
    GRAHAM_MIN_ROE: ClassVar[float] = 8.0
    
    LYNCH_MAX_PEG: ClassVar[float] = 1.0
    LYNCH_MIN_GROWTH: ClassVar[float] = 15.0
    LYNCH_MAX_DEBT_EQUITY: ClassVar[float] = 80.0
    LYNCH_MAX_PE: ClassVar[float] = 25.0
    
    # API externes
    BOYCOTT_API_URL: ClassVar[str] = "https://api.boycottisraeli.biz/v1/search"
    BOYCOTT_API_TIMEOUT: ClassVar[int] = 3
    
    YAHOO_SEARCH_URL: ClassVar[str] = "https://query2.finance.yahoo.com/v1/finance/search"


# Secteurs non conformes Shariah
SECTOR_BLACKLIST: set[str] = {
    "banks",
    "insurance",
    "capital markets",
    "credit services",
    "mortgage",
    "beverages - wineries & distilleries",
    "beverages - brewers",
    "tobacco",
    "gambling",
    "casinos",
    "defense",
    "adult entertainment",
}

# Mots-clés non conformes dans les descriptions
KEYWORD_BLACKLIST: set[str] = {
    "alcohol",
    "liquor",
    "wine",
    "beer",
    "brewery",
    "pork",
    "gambling",
    "casino",
    "betting",
    "tobacco",
    "adult entertainment",
    "pornography",
}