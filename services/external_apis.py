"""
Services d'accès aux APIs externes.
"""
import logging
from typing import Optional
from dataclasses import dataclass

import requests

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import Settings

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Résultat de recherche de symbole."""
    symbol: str
    name: str
    exchange: str
    type: str


class BoycottChecker:
    """
    Service de vérification du statut boycott d'une entreprise.
    """
    
    def __init__(self, timeout: int = Settings.BOYCOTT_API_TIMEOUT):
        """
        Initialise le checker.
        
        Args:
            timeout: Timeout des requêtes en secondes.
        """
        self._timeout = timeout
        self._base_url = Settings.BOYCOTT_API_URL
    
    def is_boycotted(self, company_name: str) -> bool:
        """
        Vérifie si une entreprise est sur la liste de boycott.
        
        Args:
            company_name: Nom de l'entreprise.
            
        Returns:
            True si l'entreprise est listée.
        """
        # Nettoyer le nom
        clean_name = self._clean_company_name(company_name)
        
        if not clean_name:
            return False
        
        try:
            url = f"{self._base_url}/{clean_name}"
            response = requests.get(url, timeout=self._timeout)
            
            if response.status_code == 200:
                data = response.json()
                return len(data) > 0
            
            return False
            
        except requests.Timeout:
            logger.warning(f"Timeout vérification boycott pour {company_name}")
            return False
        except requests.RequestException as e:
            logger.warning(f"Erreur vérification boycott: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur inattendue vérification boycott: {e}")
            return False
    
    @staticmethod
    def _clean_company_name(name: str) -> str:
        """Nettoie le nom d'entreprise pour la recherche."""
        if not name:
            return ""
        
        # Retirer les suffixes courants
        clean = name.replace(" Inc.", "")
        clean = clean.replace(" Inc", "")
        clean = clean.replace(" Corporation", "")
        clean = clean.replace(" Corp.", "")
        clean = clean.replace(" Corp", "")
        clean = clean.replace(" Ltd.", "")
        clean = clean.replace(" Ltd", "")
        clean = clean.replace(" LLC", "")
        clean = clean.replace(" PLC", "")
        clean = clean.replace(" N.V.", "")
        clean = clean.replace(" S.A.", "")
        
        # Prendre la première partie si tiret
        if " - " in clean:
            clean = clean.split(" - ")[0]
        
        return clean.strip()


class SymbolSearchService:
    """
    Service de recherche de symboles boursiers via Yahoo Finance.
    """
    
    def __init__(self, timeout: int = 5):
        """
        Initialise le service.
        
        Args:
            timeout: Timeout des requêtes en secondes.
        """
        self._timeout = timeout
        self._base_url = Settings.YAHOO_SEARCH_URL
        self._headers = {"User-Agent": "Mozilla/5.0"}
    
    def search(self, query: str, max_results: int = 10) -> list[SearchResult]:
        """
        Recherche des symboles correspondant à une requête.
        
        Args:
            query: Terme de recherche.
            max_results: Nombre maximum de résultats.
            
        Returns:
            Liste de résultats de recherche.
        """
        if not query or len(query) < 1:
            return []
        
        try:
            response = requests.get(
                self._base_url,
                params={"q": query},
                headers=self._headers,
                timeout=self._timeout,
            )
            
            if response.status_code != 200:
                logger.warning(f"Erreur recherche Yahoo: {response.status_code}")
                return []
            
            data = response.json()
            quotes = data.get("quotes", [])
            
            results: list[SearchResult] = []
            for quote in quotes[:max_results]:
                # Ne garder que les éléments avec un nom
                if "shortname" not in quote or "symbol" not in quote:
                    continue
                
                results.append(SearchResult(
                    symbol=quote["symbol"],
                    name=quote.get("shortname", quote["symbol"]),
                    exchange=quote.get("exchange", "Unknown"),
                    type=quote.get("quoteType", "Unknown"),
                ))
            
            return results
            
        except requests.Timeout:
            logger.warning("Timeout recherche symbole")
            return []
        except requests.RequestException as e:
            logger.warning(f"Erreur recherche symbole: {e}")
            return []
        except Exception as e:
            logger.error(f"Erreur inattendue recherche symbole: {e}")
            return []