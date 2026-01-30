"""
Service d'accès à la base de données Supabase.
"""
import logging
from typing import Optional
from dataclasses import dataclass

import streamlit as st
from supabase import create_client, Client

logger = logging.getLogger(__name__)


@dataclass
class User:
    """Représentation d'un utilisateur."""
    id: str
    email: str


@dataclass
class Watchlist:
    """Représentation d'une watchlist."""
    id: str
    user_id: str
    name: str


class DatabaseService:
    """
    Service de connexion à Supabase.
    Gère l'authentification et la connexion.
    """
    
    _instance: Optional["DatabaseService"] = None
    _client: Optional[Client] = None
    
    def __new__(cls):
        """Singleton pattern pour réutiliser la connexion."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def client(self) -> Optional[Client]:
        """Retourne le client Supabase, initialisé si nécessaire."""
        if self._client is None:
            self._client = self._init_connection()
        return self._client
    
    @property
    def is_configured(self) -> bool:
        """Vérifie si Supabase est configuré."""
        return self.client is not None
    
    @staticmethod
    @st.cache_resource
    def _init_connection() -> Optional[Client]:
        """Initialise la connexion Supabase (cachée par Streamlit)."""
        try:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
            return create_client(url, key)
        except KeyError:
            logger.warning("Configuration Supabase manquante dans secrets.toml")
            return None
        except Exception as e:
            logger.error(f"Erreur connexion Supabase: {e}")
            return None
    
    def sign_in(self, email: str, password: str) -> User:
        """
        Authentifie un utilisateur.
        
        Args:
            email: Email de l'utilisateur.
            password: Mot de passe.
            
        Returns:
            User authentifié.
            
        Raises:
            ValueError: Si l'authentification échoue ou Supabase non configuré.
        """
        if not self.is_configured:
            raise ValueError("Supabase non configuré")
        
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            user = User(id=response.user.id, email=response.user.email)
            
            # Sauvegarder les tokens de session
            self._save_session_tokens(response.session)
            
            return user
        except Exception as e:
            logger.error(f"Erreur authentification: {e}")
            raise ValueError(f"Authentification échouée: {e}")
    
    def sign_up(self, email: str, password: str) -> bool:
        """
        Crée un nouveau compte.
        
        Args:
            email: Email du nouvel utilisateur.
            password: Mot de passe.
            
        Returns:
            True si succès.
            
        Raises:
            ValueError: Si la création échoue ou Supabase non configuré.
        """
        if not self.is_configured:
            raise ValueError("Supabase non configuré")
        
        try:
            self.client.auth.sign_up({
                "email": email,
                "password": password,
            })
            return True
        except Exception as e:
            logger.error(f"Erreur création compte: {e}")
            raise ValueError(f"Création compte échouée: {e}")
    
    def sign_out(self) -> None:
        """Déconnecte l'utilisateur courant."""
        if self.is_configured:
            try:
                self.client.auth.sign_out()
            except Exception as e:
                logger.warning(f"Erreur déconnexion: {e}")
        
        # Effacer les tokens de session
        self._clear_session_tokens()
    
    def restore_session(self) -> Optional[User]:
        """
        Restaure la session utilisateur depuis les tokens sauvegardés.
        
        Returns:
            User si la session est valide, None sinon.
        """
        if not self.is_configured:
            return None
        
        # Récupérer les tokens depuis session_state (persistés via query params)
        access_token = st.session_state.get("_access_token")
        refresh_token = st.session_state.get("_refresh_token")
        
        if not access_token or not refresh_token:
            # Essayer de récupérer depuis les query params (persistance cross-refresh)
            params = st.query_params
            access_token = params.get("_at")
            refresh_token = params.get("_rt")
            
            if not access_token or not refresh_token:
                return None
        
        try:
            # Restaurer la session avec le refresh token
            response = self.client.auth.set_session(
                access_token=access_token,
                refresh_token=refresh_token,
            )
            
            if response and response.user:
                user = User(id=response.user.id, email=response.user.email)
                
                # Mettre à jour les tokens (ils peuvent avoir été rafraîchis)
                if response.session:
                    self._save_session_tokens(response.session)
                
                return user
                
        except Exception as e:
            logger.warning(f"Erreur restauration session: {e}")
            self._clear_session_tokens()
        
        return None
    
    def _save_session_tokens(self, session) -> None:
        """Sauvegarde les tokens de session."""
        if session:
            st.session_state["_access_token"] = session.access_token
            st.session_state["_refresh_token"] = session.refresh_token
            
            # Sauvegarder aussi dans query params pour persistance cross-refresh
            # Note: on utilise des noms courts pour éviter des URLs trop longues
            st.query_params["_at"] = session.access_token
            st.query_params["_rt"] = session.refresh_token
    
    def _clear_session_tokens(self) -> None:
        """Efface les tokens de session."""
        st.session_state.pop("_access_token", None)
        st.session_state.pop("_refresh_token", None)
        
        # Effacer les query params
        if "_at" in st.query_params:
            del st.query_params["_at"]
        if "_rt" in st.query_params:
            del st.query_params["_rt"]


class WatchlistService:
    """
    Service de gestion des watchlists.
    """
    
    def __init__(self, db: DatabaseService):
        """
        Initialise le service.
        
        Args:
            db: Instance de DatabaseService.
        """
        self._db = db
    
    @property
    def _client(self) -> Optional[Client]:
        return self._db.client
    
    def get_user_watchlists(self, user_id: str) -> list[Watchlist]:
        """
        Récupère les watchlists d'un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur.
            
        Returns:
            Liste des watchlists.
        """
        if not self._client:
            return []
        
        try:
            response = self._client.table("watchlists") \
                .select("*") \
                .eq("user_id", user_id) \
                .execute()
            
            return [
                Watchlist(id=row["id"], user_id=row["user_id"], name=row["name"])
                for row in response.data
            ]
        except Exception as e:
            logger.error(f"Erreur récupération watchlists: {e}")
            return []
    
    def create_watchlist(self, user_id: str, name: str) -> Optional[Watchlist]:
        """
        Crée une nouvelle watchlist.
        
        Args:
            user_id: ID de l'utilisateur.
            name: Nom de la watchlist.
            
        Returns:
            Watchlist créée ou None si erreur.
        """
        if not self._client:
            return None
        
        try:
            response = self._client.table("watchlists").insert({
                "user_id": user_id,
                "name": name,
            }).execute()
            
            if response.data:
                row = response.data[0]
                return Watchlist(id=row["id"], user_id=row["user_id"], name=row["name"])
            return None
            
        except Exception as e:
            logger.error(f"Erreur création watchlist: {e}")
            return None
    
    def delete_watchlist(self, watchlist_id: str) -> bool:
        """
        Supprime une watchlist.
        
        Args:
            watchlist_id: ID de la watchlist.
            
        Returns:
            True si succès.
        """
        if not self._client:
            return False
        
        try:
            # Supprimer d'abord les items
            self._client.table("watchlist_items") \
                .delete() \
                .eq("watchlist_id", watchlist_id) \
                .execute()
            
            # Puis la watchlist
            self._client.table("watchlists") \
                .delete() \
                .eq("id", watchlist_id) \
                .execute()
            
            return True
        except Exception as e:
            logger.error(f"Erreur suppression watchlist: {e}")
            return False
    
    def get_watchlist_items(self, watchlist_id: str) -> list[str]:
        """
        Récupère les tickers d'une watchlist.
        
        Args:
            watchlist_id: ID de la watchlist.
            
        Returns:
            Liste des tickers.
        """
        if not self._client:
            return []
        
        try:
            response = self._client.table("watchlist_items") \
                .select("ticker") \
                .eq("watchlist_id", watchlist_id) \
                .execute()
            
            return [row["ticker"] for row in response.data]
        except Exception as e:
            logger.error(f"Erreur récupération items watchlist: {e}")
            return []
    
    def add_ticker_to_watchlist(self, watchlist_id: str, ticker: str) -> bool:
        """
        Ajoute un ticker à une watchlist.
        
        Args:
            watchlist_id: ID de la watchlist.
            ticker: Symbole boursier.
            
        Returns:
            True si succès, False si déjà présent ou erreur.
        """
        if not self._client:
            return False
        
        try:
            self._client.table("watchlist_items").insert({
                "watchlist_id": watchlist_id,
                "ticker": ticker.upper(),
            }).execute()
            return True
        except Exception as e:
            # Probablement une contrainte unique violée
            logger.warning(f"Ticker {ticker} déjà dans watchlist ou erreur: {e}")
            return False
    
    def remove_ticker_from_watchlist(self, watchlist_id: str, ticker: str) -> bool:
        """
        Retire un ticker d'une watchlist.
        
        Args:
            watchlist_id: ID de la watchlist.
            ticker: Symbole boursier.
            
        Returns:
            True si succès.
        """
        if not self._client:
            return False
        
        try:
            self._client.table("watchlist_items") \
                .delete() \
                .eq("watchlist_id", watchlist_id) \
                .eq("ticker", ticker.upper()) \
                .execute()
            return True
        except Exception as e:
            logger.error(f"Erreur suppression ticker: {e}")
            return False