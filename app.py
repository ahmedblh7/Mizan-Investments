"""
Mizan Investments - Application principale.

Point d'entrée Streamlit pour l'analyse d'investissements conformes Shariah.
"""
import streamlit as st

import sys
from pathlib import Path

# Ajouter le répertoire racine au path pour les imports
ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import Settings
from config.translations import get_translation, Language, SUPPORTED_LANGUAGES
from services.database import DatabaseService, WatchlistService
from services.external_apis import SymbolSearchService
from domain.strategies import AVAILABLE_STRATEGIES
from ui.styles import apply_custom_styles
from ui.pages.analysis import render_analysis_page


# =========================================================
# 🎨 CONFIGURATION PAGE
# =========================================================
st.set_page_config(
    page_title=Settings.APP_NAME,
    page_icon=Settings.APP_ICON,
    layout="wide",
)

apply_custom_styles()


# =========================================================
# 🔐 INITIALISATION SESSION STATE
# =========================================================
def init_session_state() -> None:
    """Initialise les variables de session."""
    if "user" not in st.session_state:
        st.session_state.user = None
    if "active_ticker" not in st.session_state:
        st.session_state.active_ticker = None
    if "selected_strategy" not in st.session_state:
        st.session_state.selected_strategy = "Mizan"
    if "language" not in st.session_state:
        st.session_state.language = "en"
    if "_session_restored" not in st.session_state:
        st.session_state._session_restored = False


init_session_state()


# =========================================================
# 🗄️ SERVICES
# =========================================================
db_service = DatabaseService()
watchlist_service = WatchlistService(db_service)
search_service = SymbolSearchService()


# =========================================================
# 🔄 RESTAURATION DE SESSION
# =========================================================
def restore_user_session() -> None:
    """Restaure la session utilisateur si des tokens existent."""
    if st.session_state._session_restored:
        return
    
    st.session_state._session_restored = True
    
    if st.session_state.user is None:
        restored_user = db_service.restore_session()
        if restored_user:
            st.session_state.user = restored_user


# Restaurer la session au chargement
restore_user_session()


# =========================================================
# 📱 SIDEBAR
# =========================================================
def render_sidebar() -> Language:
    """
    Affiche la sidebar avec authentification et paramètres.
    
    Returns:
        Code langue sélectionné.
    """
    with st.sidebar:
        st.markdown(f"### {Settings.APP_ICON} {Settings.APP_NAME}")
        
        # Bloc authentification
        if st.session_state.user is None:
            _render_auth_forms()
        else:
            _render_user_panel()
        
        st.markdown("---")
        
        # Sélection langue
        lang_options = {"English": "en", "Français": "fr"}
        selected_lang_display = st.selectbox(
            "Language",
            options=list(lang_options.keys()),
            key="lang_select",
            label_visibility="collapsed",
        )
        lang: Language = lang_options[selected_lang_display]
        st.session_state.language = lang
        
        # Sélection stratégie
        t = get_translation(lang)
        st.markdown(f"**{t.strategy_label}**")
        
        strategy_names = {
            "Mizan": t.strat_name_mizan,
            "Graham": t.strat_name_graham,
            "Lynch": t.strat_name_lynch,
        }
        reverse_map = {v: k for k, v in strategy_names.items()}
        
        selected_display = st.selectbox(
            "Strategy",
            options=list(strategy_names.values()),
            key="strategy_select",
            label_visibility="collapsed",
        )
        st.session_state.selected_strategy = reverse_map[selected_display]
        
        # Description stratégie
        with st.expander(t.strat_name_mizan):
            st.markdown(
                f"<div style='font-size:13px; color:#C8CDD5;'>{t.bullets_mizan}</div>",
                unsafe_allow_html=True,
            )
        
        return lang


def _render_auth_forms() -> None:
    """Affiche les formulaires de connexion/inscription."""
    if not db_service.is_configured:
        st.info("💡 Configure Supabase in secrets.toml to enable auth.")
        return
    
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
    
    with login_tab:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Se connecter", type="primary", key="login_btn"):
            if email and password:
                try:
                    user = db_service.sign_in(email, password)
                    st.session_state.user = user
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Veuillez remplir tous les champs.")
    
    with signup_tab:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        
        if st.button("Créer un compte", key="signup_btn"):
            if email and password:
                try:
                    db_service.sign_up(email, password)
                    st.success("Compte créé ! Vérifiez vos emails.")
                except ValueError as e:
                    st.error(str(e))
            else:
                st.warning("Veuillez remplir tous les champs.")


def _render_user_panel() -> None:
    """Affiche le panneau utilisateur connecté."""
    user = st.session_state.user
    st.success(f"👋 {user.email}")
    
    # Watchlists
    st.markdown("### 📂 Mes Watchlists")
    watchlists = watchlist_service.get_user_watchlists(user.id)
    
    if watchlists:
        selected_list = st.selectbox(
            "Voir une liste",
            options=[w.name for w in watchlists],
            key="view_watchlist",
            label_visibility="collapsed",
        )
        
        # Trouver l'ID de la liste sélectionnée
        selected_watchlist = next(w for w in watchlists if w.name == selected_list)
        items = watchlist_service.get_watchlist_items(selected_watchlist.id)
        
        if items:
            for ticker in items:
                if st.button(f"🔎 {ticker}", key=f"wl_btn_{ticker}", use_container_width=True):
                    st.session_state.active_ticker = ticker
                    st.rerun()
        else:
            st.caption("Liste vide.")
    else:
        st.caption("Aucune liste créée.")
    
    st.markdown("---")
    
    if st.button("Se déconnecter", key="logout_btn"):
        db_service.sign_out()
        st.session_state.user = None
        st.rerun()


# =========================================================
# 🏠 CONTENU PRINCIPAL
# =========================================================
def render_main_content(lang: Language) -> None:
    """Affiche le contenu principal."""
    t = get_translation(lang)
    
    # Hero section
    st.markdown(
        f"""
        <div style="margin-bottom: 40px;">
            <h1 style="font-size: 3.5rem; line-height: 1.1;">{t.hero_title}</h1>
            <p style="font-size: 1.2rem; color: #00E096; font-family: 'Space Grotesk'; margin-top:10px;">
                {t.hero_sub}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Barre de recherche
    col_search, col_select = st.columns([2, 1])
    
    with col_search:
        search_query = st.text_input(
            "Search",
            placeholder=t.search_placeholder,
            label_visibility="collapsed",
        )
    
    input_ticker = None
    with col_select:
        if search_query:
            results = search_service.search(search_query)
            if results:
                options = {f"{r.name} ({r.symbol})": r.symbol for r in results}
                selected = st.selectbox(
                    "Select",
                    options=list(options.keys()),
                    label_visibility="collapsed",
                )
                input_ticker = options[selected]
            else:
                st.selectbox(
                    "Select",
                    options=[t.no_result],
                    disabled=True,
                    label_visibility="collapsed",
                )
        else:
            st.selectbox(
                "Select",
                options=[t.select_stock],
                disabled=True,
                label_visibility="collapsed",
            )
    
    st.markdown("###")
    
    # Bouton d'analyse
    if st.button(
        t.analyze_btn,
        type="primary",
        use_container_width=True,
        disabled=not input_ticker,
    ):
        st.session_state.active_ticker = input_ticker
    
    # Affichage de l'analyse
    if st.session_state.active_ticker:
        _render_analysis_with_watchlist(t)
    else:
        # Message par défaut
        st.markdown(
            f"""
            <div style="margin-top:50px; text-align:center; opacity:0.5;">
                <p>{Settings.APP_NAME} v{Settings.VERSION}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_analysis_with_watchlist(t) -> None:
    """Affiche l'analyse avec option d'ajout à watchlist."""
    ticker = st.session_state.active_ticker
    
    # Bouton d'ajout à watchlist
    st.markdown("###")
    if st.session_state.user:
        with st.popover(f"⭐ {t.watchlist_add}", use_container_width=True):
            watchlists = watchlist_service.get_user_watchlists(st.session_state.user.id)
            
            if watchlists:
                list_options = {w.name: w.id for w in watchlists}
                selected_list = st.selectbox(
                    "Choisir une liste :",
                    options=list(list_options.keys()),
                )
                
                if st.button(t.watchlist_save, type="primary"):
                    success = watchlist_service.add_ticker_to_watchlist(
                        list_options[selected_list],
                        ticker,
                    )
                    if success:
                        st.toast(f"{ticker} sauvegardé !", icon="⭐")
                    else:
                        st.toast(f"{ticker} est déjà dans cette liste.", icon="⚠️")
            else:
                st.info(t.watchlist_empty)
            
            st.markdown("---")
            
            new_list_name = st.text_input(
                t.watchlist_create,
                placeholder="Ex: Tech, Halal...",
            )
            if st.button("Créer la liste"):
                if new_list_name:
                    result = watchlist_service.create_watchlist(
                        st.session_state.user.id,
                        new_list_name,
                    )
                    if result:
                        st.toast(f"Liste '{new_list_name}' créée !", icon="✅")
                        st.rerun()
    else:
        st.info("💡 Connectez-vous pour sauvegarder cette action.")
    
    # Rendu de l'analyse
    render_analysis_page(
        ticker=ticker,
        strategy_name=st.session_state.selected_strategy,
        translations=t,
    )


# =========================================================
# 🚀 MAIN
# =========================================================
def main() -> None:
    """Point d'entrée principal."""
    lang = render_sidebar()
    render_main_content(lang)


if __name__ == "__main__":
    main()