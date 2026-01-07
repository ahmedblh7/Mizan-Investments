import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import plotly.graph_objects as go

# =========================================================
# 🎨 CONFIGURATION & DESIGN SYSTEM (FINANCE BRO - DARK LUXURY)
# =========================================================
st.set_page_config(page_title="FinanceBro", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* VARIABLES */
    :root {
        --bg-dark: #0B0E13;
        --bg-card: rgba(28, 32, 43, 0.6);
        --accent-green: #00E096;
        --accent-gold: #E0C38C;
        --text-white: #FFFFFF;
        --text-silver: #C8CDD5;
        --border-subtle: rgba(255, 255, 255, 0.08);
    }

    /* 1. RESET & FOND GLOBAL */
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 50% 0%, #151922 0%, #0B0E13 80%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231C202B' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        font-family: 'Inter', sans-serif;
        color: var(--text-silver);
    }

    /* 2. SIDEBAR PERSONNALISÉE (NOUVEAU DESIGN) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B0E13 0%, #161b26 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    .sidebar-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 5px;
        display: flex; 
        align-items: center; 
        gap: 10px;
    }
    .sidebar-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #6E7687;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }

    /* Styles des Expanders dans la Sidebar (Minimaliste) */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        border-color: var(--accent-green) !important;
        color: var(--accent-green) !important;
    }
    [data-testid="stSidebar"] .streamlit-expanderContent {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: none !important;
        padding-left: 15px !important;
        border-left: 2px solid var(--accent-green) !important;
    }
    .checklist-item {
        font-size: 0.8rem;
        color: #C8CDD5;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Logos Partenaires */
    .partner-logos {
        display: flex;
        gap: 15px;
        margin-top: 10px;
        opacity: 0.5;
        filter: grayscale(100%);
        transition: all 0.5s ease;
    }
    .partner-logos:hover {
        opacity: 1;
        filter: grayscale(0%);
    }

    /* Cacher le label du selectbox langue */
    [data-testid="stSidebar"] .stSelectbox label { display: none; }

    /* 3. TYPOGRAPHIE GENERALE */
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }
    h1 { font-weight: 700 !important; color: var(--text-white); }
    h2 { font-weight: 600 !important; color: var(--text-white); }
    p, div, span { font-family: 'Inter', sans-serif; }

    /* 4. CARTES KPI (GLASSMORPHISM) */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 224, 150, 0.3);
        box-shadow: 0 10px 30px rgba(0, 224, 150, 0.1);
    }

    .kpi-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6E7687;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-white);
        margin-bottom: 4px;
    }

    .kpi-target {
        font-size: 0.85rem;
        color: #555;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* COULEURS DYNAMIQUES */
    .val-green { color: var(--accent-green); text-shadow: 0 0 15px rgba(0, 224, 150, 0.4); }
    .val-gold { color: var(--accent-gold); text-shadow: 0 0 15px rgba(224, 195, 140, 0.3); }
    .val-red { color: #FF4B4B; text-shadow: 0 0 15px rgba(255, 75, 75, 0.3); }

    /* 5. INPUTS & BUTTONS */
    .stTextInput > div > div > input {
        background-color: #0F1218;
        color: white;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 12px;
        font-family: 'Space Grotesk';
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-green);
        box-shadow: 0 0 0 1px var(--accent-green);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00E096 0%, #00B075 100%);
        color: #0B0E13;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 224, 150, 0.4);
        color: black;
    }

    /* 6. TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #6E7687;
        font-family: 'Space Grotesk';
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1C202B;
        color: var(--accent-gold);
        border: 1px solid rgba(224, 195, 140, 0.2);
    }

    /* 7. VERDICT BOX */
    .verdict-box {
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 20px;
        border: 1px solid;
        backdrop-filter: blur(10px);
    }
    .verdict-halal {
        background: linear-gradient(90deg, rgba(0, 224, 150, 0.1) 0%, rgba(0,0,0,0) 100%);
        border-color: rgba(0, 224, 150, 0.3);
    }
    .verdict-haram {
        background: linear-gradient(90deg, rgba(255, 75, 75, 0.1) 0%, rgba(0,0,0,0) 100%);
        border-color: rgba(255, 75, 75, 0.3);
    }

    /* METRICS TOP */
    [data-testid="stMetricLabel"] { font-family: 'Inter'; color: #6E7687; font-size: 0.9rem; }
    [data-testid="stMetricValue"] { font-family: 'Space Grotesk'; color: white; font-size: 1.8rem; font-weight: 600; }
    [data-testid="stMetricDelta"] { font-family: 'Space Grotesk'; }

</style>
""", unsafe_allow_html=True)

# =========================================================
# 🚫 BLACKLIST (ACTIVITÉS)
# =========================================================
SECTOR_BLACKLIST = [
    'Banks', 'Insurance', 'Capital Markets', 'Credit Services', 'Mortgage',
    'Beverages - Wineries & Distilleries', 'Beverages - Brewers',
    'Tobacco', 'Gambling', 'Casinos', 'Resorts & Casinos', 'Defense'
]
KEYWORD_BLACKLIST = [
    'alcohol', 'liquor', 'wine', 'beer', 'brewery', 'pork', 'gambling', 'casino', 
    'betting', 'tobacco', 'interest', 'lending', 'banking', 'adult'
]

# =========================================================
# 💾 STATE
# =========================================================
if 'active_ticker' not in st.session_state:
    st.session_state.active_ticker = None

def trigger_analysis(ticker):
    st.session_state.active_ticker = ticker

# =========================================================
# 🌍 TRADUCTIONS
# =========================================================
TRANSLATIONS = {
    'en': {
        'sidebar_title': "FinanceBro", 'sidebar_subtitle': "Institutional Grade Analysis",
        'sidebar_tip': "Enter a ticker to start.", 'methodology': "Proprietary Algorithm",
        'strat_fin': "Value & Growth Check", 'strat_shariah': "Islamic Finance Check",
        'search_title': "ASSET INTELLIGENCE", 'search_placeholder': "Search ticker (e.g. AAPL, TSLA...)",
        'select_stock': "Select Asset", 'analyze_btn': "INITIATE SCAN",
        'crunching': "Processing Data Streams...", 'no_result': "No asset found.",
        'verdict_halal_title': "COMPLIANT ASSET", 'verdict_halal_desc': "This asset meets all quantitative criteria defined by IFG standards.",
        'verdict_haram_title': "NON-COMPLIANT", 'verdict_haram_desc': "Failed checks: ",
        'tab_fund': "FUNDAMENTALS", 'tab_shariah': "COMPLIANCE", 'tab_exit': "STRATEGY",
        'company': "Issuer", 'company_help': "Official registered name.",
        'price': "Spot Price", 'price_help': "Real-time market price.",
        'mcap': "Market Cap", 'mcap_help': "Total value of all shares.",
        'momentum': "3M Momentum", 'momentum_help': "Price trend over last 3 months.",
        'per': "P/E Ratio", 'per_help': "Price-to-Earnings.", 'per_target': "Target < 12",
        'fcf_yield': "FCF Yield", 'fcf_help': "Free Cash Flow Yield.", 'fcf_target': "Target > 5%",
        'roe': "ROE", 'roe_help': "Return on Equity.", 'roe_target': "Target > 10%",
        'margin': "Ops Margin", 'margin_help': "Operating Margin.", 'margin_target': "Target > 14%",
        'solvency': "Net Debt/EBITDA", 'solvency_help': "Solvency Ratio.", 'solvency_target': "Safe < 3.0",
        'growth': "Rev Growth", 'growth_help': "Year-over-Year Revenue Growth.", 'growth_target': "Positive",
        'act_check': "Activity Scan", 'act_check_help': "Automated screening.",
        'inc_haram': "Impure Income", 'inc_haram_help': "Non-compliant income.", 'inc_target': "Limit < 5%",
        'debt': "Leverage", 'debt_help': "Interest-bearing debt vs Assets.", 'debt_target': "Limit < 33%",
        'real_assets': "Real Assets", 'real_assets_help': "Tangible assets ratio.", 'real_target': "Min > 20%",
        'cash_cap': "Liquidity Check", 'cash_target': "Cash < Market Cap",
        'boycott_check': "Boycott Check", 'boycott_help': "Checks against Boycott Israeli Businesses API.", 'boycott_target': "Not Listed",
        'target1': "Take Profit 1 (20%)", 'target2': "Exit All", 'chart_title': "Price Action (1Y)"
    },
    'fr': {
        'sidebar_title': "FinanceBro", 'sidebar_subtitle': "Analyse de niveau institutionnel",
        'sidebar_tip': "Entrez un ticker pour commencer.", 'methodology': "Algorithme Propriétaire",
        'strat_fin': "Analyse Valeur & Croissance", 'strat_shariah': "Filtre Finance Islamique",
        'search_title': "ASSET INTELLIGENCE", 'search_placeholder': "Rechercher (ex: LVMH...)",
        'select_stock': "Sélectionner l'actif", 'analyze_btn': "LANCER LE SCAN",
        'crunching': "Traitement des données...", 'no_result': "Aucun actif trouvé.",
        'verdict_halal_title': "ACTIF CONFORME", 'verdict_halal_desc': "Cet actif respecte les standards IFG.",
        'verdict_haram_title': "NON-CONFORME", 'verdict_haram_desc': "Critères échoués : ",
        'tab_fund': "FONDAMENTAUX", 'tab_shariah': "CONFORMITÉ", 'tab_exit': "STRATÉGIE",
        'company': "Émetteur", 'company_help': "Nom officiel enregistré.",
        'price': "Prix Spot", 'price_help': "Prix actuel du marché.",
        'mcap': "Capitalisation", 'mcap_help': "Valeur totale des actions.",
        'momentum': "Momentum 3M", 'momentum_help': "Tendance du prix sur 3 mois.",
        'per': "PER", 'per_help': "Ratio Cours/Bénéfice.", 'per_target': "Cible < 12",
        'fcf_yield': "Rendement FCF", 'fcf_help': "La vraie rentabilité cash.", 'fcf_target': "Cible > 5%",
        'roe': "ROE", 'roe_help': "Rentabilité des Capitaux Propres.", 'roe_target': "Cible > 10%",
        'margin': "Marge Ops", 'margin_help': "Marge Opérationnelle.", 'margin_target': "Cible > 14%",
        'solvency': "Dette Nette/EBITDA", 'solvency_help': "Solvabilité.", 'solvency_target': "Sûr < 3.0",
        'growth': "Croissance CA", 'growth_help': "Croissance annuelle.", 'growth_target': "Positive",
        'act_check': "Scan Activité", 'act_check_help': "Analyse sectorielle.",
        'inc_haram': "Revenus Impurs", 'inc_haram_help': "Revenus intérêts.", 'inc_target': "Limite < 5%",
        'debt': "Levier", 'debt_help': "Dette vs Actifs.", 'debt_target': "Limite < 33%",
        'real_assets': "Actifs Réels", 'real_assets_help': "Actifs tangibles.", 'real_target': "Min > 20%",
        'cash_cap': "Liquidité", 'cash_target': "Cash < Market Cap",
        'boycott_check': "Check Boycott", 'boycott_help': "Vérifie l'API Boycott Israeli Businesses.", 'boycott_target': "Non Listé",
        'target1': "Prise de Profit 1 (20%)", 'target2': "Sortie Totale", 'chart_title': "Action des Prix (1 An)"
    }
}

# =========================================================
# 🧠 BACKEND (LOGIQUE)
# =========================================================
class FinanceBroAgent:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.financials = self.stock.financials
        self.balance_sheet = self.stock.balance_sheet
        self.income_stmt = self.stock.income_stmt
        self.cashflow = self.stock.cashflow
        self.data = {}
        
    def _safe_get(self, key, default=None):
        return self.info.get(key, default)

    def _get_item(self, df, items_list):
        if df is None or df.empty: return 0
        for item in items_list:
            if item in df.index:
                return df.loc[item].iloc[0]
        return 0

    def collect_data(self):
        # BASIC
        self.data['name'] = self._safe_get('longName', self.ticker)
        self.data['sector'] = self._safe_get('sector', 'Unknown')
        self.data['industry'] = self._safe_get('industry', 'Unknown')
        self.data['description'] = self._safe_get('longBusinessSummary', '')
        self.data['current_price'] = self._safe_get('currentPrice', 0)
        self.data['currency'] = self._safe_get('currency', 'USD')
        self.data['market_cap'] = self._safe_get('marketCap', 1)

        # VALUATION
        self.data['per'] = self._safe_get('trailingPE')
        self.data['eps'] = self._safe_get('trailingEps')
        self.data['roe'] = self._safe_get('returnOnEquity', 0) * 100
        self.data['ops_margin'] = self._safe_get('operatingMargins', 0) * 100
        
        # FCF YIELD
        try:
            ocf = self._get_item(self.cashflow, ['Operating Cash Flow', 'Total Cash From Operating Activities'])
            capex = self._get_item(self.cashflow, ['Capital Expenditure', 'Net PPE Purchase And Sale'])
            fcf = ocf + capex 
            self.data['fcf_yield'] = (fcf / self.data['market_cap']) * 100
        except: self.data['fcf_yield'] = 0

        # SOLVENCY
        try:
            total_debt = self._safe_get('totalDebt', 0)
            cash = self._safe_get('totalCash', 0)
            net_debt = total_debt - cash
            ebitda = self._safe_get('ebitda', 1)
            self.data['net_debt_ebitda'] = net_debt / ebitda if ebitda else 0
        except: self.data['net_debt_ebitda'] = 0

        # MOMENTUM
        try:
            hist = self.stock.history(period="3mo")
            if not hist.empty:
                start = hist['Close'].iloc[0]
                end = hist['Close'].iloc[-1]
                self.data['momentum_3m'] = ((end - start) / start) * 100
            else: self.data['momentum_3m'] = 0
        except: self.data['momentum_3m'] = 0

        # SHARIAH DATA
        self.data['total_debt'] = self._safe_get('totalDebt', 0)
        self.data['total_assets'] = self._get_item(self.balance_sheet, ['Total Assets'])
        if self.data['total_assets'] == 0: self.data['total_assets'] = 1

        self.data['interest_income'] = self._get_item(self.income_stmt, ['Interest Income', 'Interest Income Non Operating', 'Total Interest Income'])

        ppe = self._get_item(self.balance_sheet, ['Net PPE', 'Net Property, Plant And Equipment'])
        goodwill = self._get_item(self.balance_sheet, ['Goodwill'])
        intangibles = self._get_item(self.balance_sheet, ['Intangible Assets', 'Other Intangible Assets'])
        inventory = self._get_item(self.balance_sheet, ['Inventory'])
        
        self.data['illiquid_assets'] = ppe + goodwill + intangibles + inventory
        self.data['current_assets'] = self._get_item(self.balance_sheet, ['Total Current Assets', 'Current Assets'])
        
        if self.data['illiquid_assets'] == 0 and self.data['current_assets'] > 0:
             self.data['illiquid_assets'] = self.data['total_assets'] - self.data['current_assets']

    def check_business_activity(self):
        industry = str(self.data['industry']).lower()
        sector = str(self.data['sector']).lower()
        description = str(self.data['description']).lower()
        
        detected_issues = []
        for bad_sector in SECTOR_BLACKLIST:
            if bad_sector.lower() in industry or bad_sector.lower() in sector:
                detected_issues.append(f"Sector: {bad_sector}")
        if not detected_issues:
            for keyword in KEYWORD_BLACKLIST:
                if f" {keyword} " in f" {description} ":
                    detected_issues.append(f"Keyword: {keyword}")
                    break
        
        if detected_issues: return False, ", ".join(detected_issues)
        return True, "OK"

    def check_boycott_status(self):
        """Vérifie l'API de boycott pour le nom de l'entreprise"""
        try:
            # 1. Nettoyage du nom (ex: "Apple Inc." -> "Apple") pour meilleure recherche
            raw_name = self.data['name']
            clean_name = raw_name.replace(" Inc.", "").replace(" Corporation", "").replace(" Corp.", "").replace(" Ltd.", "").replace(" PLC", "").split(" - ")[0].strip()
            
            # 2. Appel API
            url = f"https://api.boycottisraeli.biz/v1/search/{clean_name}"
            r = requests.get(url, timeout=3) # Timeout court pour ne pas bloquer l'app
            
            if r.status_code == 200:
                results = r.json()
                # Si la liste n'est pas vide, l'entreprise est listée
                if len(results) > 0:
                    return True, results # True = Boycotté
            return False, []
        except:
            return False, [] # En cas d'erreur ou timeout, on assume "pas trouvé"

    def calculate_shariah_ratios(self):
        d = self.data
        ratio_haram = (d['interest_income'] / d['total_revenue']) * 100 if 'total_revenue' in d else 0
        ratio_debt = (d['total_debt'] / d['total_assets']) * 100
        ratio_illiquid = (d['illiquid_assets'] / d['total_assets']) * 100
        is_liquid_ok = d['current_assets'] < d['market_cap']
        
        is_activity_halal, activity_msg = self.check_business_activity()
        is_boycotted, boycott_data = self.check_boycott_status()

        failures = []
        if not is_activity_halal: failures.append(f"Activity ({activity_msg})")
        if is_boycotted: failures.append("Boycott List Detected") # Ajout à la liste des échecs
        
        if ratio_haram >= 5: failures.append("Interest Income > 5%")
        if ratio_debt >= 33: failures.append("Debt > 33%")
        if ratio_illiquid <= 20: failures.append("Real Assets < 20%")
        if not is_liquid_ok: failures.append("Cash > Market Cap")
        
        return {
            "haram_ratio": ratio_haram, "debt_ratio": ratio_debt, "illiquid_ratio": ratio_illiquid,
            "liquid_ok": is_liquid_ok, "activity_ok": is_activity_halal, "activity_msg": activity_msg,
            "is_boycotted": is_boycotted,
            "status": "HALAL" if not failures else "HARAM", "details": failures
        }

def search_symbol(query):
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        if 'quotes' in data and len(data['quotes']) > 0: return data['quotes']
    except: return []
    return []

def kpi_card(label, value_str, target_text, is_success, help_text, is_warning=False):
    """Carte KPI stylisée Dark Luxury"""
    if is_warning: color_class = "val-gold"
    else: color_class = "val-green" if is_success else "val-red"
    
    icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>"""
    
    html = f"""
    <div class="glass-card">
        <div>
            <div class="kpi-title">
                {label}
                <span title="{help_text}" style="cursor:help; opacity:0.6;">{icon_svg}</span>
            </div>
            <div class="kpi-value {color_class}">{value_str}</div>
        </div>
        <div class="kpi-target">
            <span style="opacity:0.5;">Goal:</span> {target_text}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# 📱 FRONTEND (LAYOUT FINANCE BRO AVEC NOUVEAU MENU)
# =========================================================

# --- SIDEBAR (MISE A JOUR) ---
with st.sidebar:
    # 1. En-tête stylisé
    st.markdown("""
        <div class="sidebar-title">
            <span style="color:#00E096;">🛡️</span> FINANCE BRO
        </div>
        <div class="sidebar-subtitle">Institutional Grade Analysis</div>
    """, unsafe_allow_html=True)

    # 2. Sélecteur Langue (Sans label visible grâce au CSS)
    lang_choice = st.selectbox("Language", ["English", "Français"], key="lang", label_visibility="collapsed")
    lang = 'en' if lang_choice == "English" else 'fr'
    t = TRANSLATIONS[lang]

    st.markdown("---")
    
    # 3. Méthodologie (Expanders stylisés)
    st.markdown(f"<div style='margin-bottom:10px; font-weight:600; font-size:0.8rem; color:#E0E0E0;'>{t['methodology'].upper()}</div>", unsafe_allow_html=True)
    
    with st.expander(f"📈 {t['strat_fin']}", expanded=True):
        st.markdown("""
        <div class="checklist-item">✅ FCF Yield > 5% <span style="color:#F59E0B; font-size:10px; margin-left:5px;">(Golden Rule)</span></div>
        <div class="checklist-item">✅ P/E Ratio < 12</div>
        <div class="checklist-item">✅ Debt/EBITDA < 3</div>
        """, unsafe_allow_html=True)

    with st.expander(f"☪️ {t['strat_shariah']}"):
        st.markdown("""
        <div class="checklist-item">🔹 Interest Income < 5%</div>
        <div class="checklist-item">🔹 Total Debt < 33%</div>
        <div class="checklist-item">🔹 Real Assets > 20%</div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 4. Footer (Logos fonctionnels via Clearbit)
    st.markdown("<div style='font-size:0.75rem; color:#6E7687; margin-bottom:10px; letter-spacing:1px;'>DATA SOURCES & PARTNERS</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="partner-logos">
        <img src="https://logo.clearbit.com/yahoo.com" width="24" title="Yahoo Finance">
       <img src="https://logo.clearbit.com/bloomberg.com" width="24" title="Bloomberg Terminals">
        <img src="https://logo.clearbit.com/nasdaq.com" width="24" title="Nasdaq">
    </div>
    <div style="margin-top:30px; font-size:0.6rem; color:#444;">
        v5.2 • Secured by SSL
    </div>
    """, unsafe_allow_html=True)

# --- HERO & SEARCH ---
st.markdown(f"""
<div style="margin-bottom: 40px;">
    <h1 style="font-size: 3.5rem; line-height: 1.1;">Votre patrimoine passe<br>au niveau supérieur.</h1>
    <p style="font-size: 1.2rem; color: #00E096; font-family: 'Space Grotesk'; margin-top:10px;">Gérez. Analysez. Dominez.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"### {t['search_title']}")
search_col1, search_col2 = st.columns([2, 1])

input_ticker = None
with search_col1: 
    search_query = st.text_input("Search", placeholder=t['search_placeholder'], label_visibility="collapsed")
with search_col2:
    if search_query:
        results = search_symbol(search_query)
        if results:
            options = {f"{r['shortname']} ({r['symbol']})": r['symbol'] for r in results if 'shortname' in r}
            selected_label = st.selectbox("Select", options.keys(), label_visibility="collapsed")
            input_ticker = options[selected_label]
        else: st.selectbox("Select", [t['no_result']], disabled=True, label_visibility="collapsed")
    else: st.selectbox("Select", [t['select_stock']], disabled=True, label_visibility="collapsed")

st.markdown("###")
if st.button(t['analyze_btn'], type="primary", use_container_width=True, disabled=not input_ticker):
    trigger_analysis(input_ticker)

# --- DASHBOARD ---
if st.session_state.active_ticker:
    ticker_to_analyze = st.session_state.active_ticker
    with st.spinner(t['crunching']):
        try:
            agent = FinanceBroAgent(ticker_to_analyze)
            agent.collect_data()
            d = agent.data
            shariah = agent.calculate_shariah_ratios()

            st.markdown("---")
            
            # TOP METRICS
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(t['company'], d['name'], help=t['company_help'])
            m2.metric(t['price'], f"{d['current_price']} {d['currency']}", help=t['price_help'])
            m3.metric(t['mcap'], f"{d['market_cap']/1e9:.1f}B", help=t['mcap_help'])
            
            mom = d['momentum_3m']
            m4.metric(t['momentum'], f"{mom:.2f}%", delta="Trend", delta_color="normal" if mom > 0 else "inverse", help=t['momentum_help'])
            
            st.markdown("###")

            # VERDICT BANNER
            if shariah['status'] == "HALAL":
                st.markdown(f"""<div class="verdict-box verdict-halal"><div style="font-size:2rem; text-shadow: 0 0 20px #00E096;">🛡️</div><div><div style="font-weight:700; font-size:1.2rem; font-family:'Space Grotesk'; color:#00E096;">{t['verdict_halal_title']}</div><div style="font-size:0.9rem; opacity:0.8;">{t['verdict_halal_desc']}</div></div></div>""", unsafe_allow_html=True)
            else:
                fail_txt = t['verdict_haram_desc'] + ", ".join(shariah['details'])
                st.markdown(f"""<div class="verdict-box verdict-haram"><div style="font-size:2rem; text-shadow: 0 0 20px #FF4B4B;">🚫</div><div><div style="font-weight:700; font-size:1.2rem; font-family:'Space Grotesk'; color:#FF4B4B;">{t['verdict_haram_title']}</div><div style="font-size:0.9rem; opacity:0.8;">{fail_txt}</div></div></div>""", unsafe_allow_html=True)

            # TABS
            tab1, tab2, tab3 = st.tabs([t['tab_fund'], t['tab_shariah'], t['tab_exit']])

            # --- TAB 1 : FUNDAMENTALS ---
            with tab1:
                st.markdown("#### VALUATION & EFFICIENCY")
                c1, c2, c3, c4 = st.columns(4)
                
                with c1:
                    per = d['per'] if d['per'] else 0
                    kpi_card(t['per'], f"{per:.1f}x", t['per_target'], (0 < per < 12), t['per_help'])
                with c2:
                    fcf = d['fcf_yield']
                    kpi_card(t['fcf_yield'], f"{fcf:.2f}%", t['fcf_target'], (fcf > 5), t['fcf_help'], is_warning=(2 < fcf <= 5))
                with c3:
                    roe = d['roe']
                    kpi_card(t['roe'], f"{roe:.1f}%", t['roe_target'], (roe > 10), t['roe_help'])
                with c4:
                    solv = d['net_debt_ebitda']
                    kpi_card(t['solvency'], f"{solv:.1f}x", t['solvency_target'], (solv < 3.0), t['solvency_help'])

            # --- TAB 2 : SHARIAH & ETHICS ---
            with tab2:
                st.markdown("#### ISLAMIC & ETHICAL SCREENING")
                
                # PREMIERE LIGNE : QUALITATIF (Boycott + Secteur)
                cs_a, cs_b = st.columns(2)
                
                with cs_a:
                    # CARTE BOYCOTT (NEW)
                    is_boycotted = shariah['is_boycotted']
                    status_text = "LISTED (AVOID)" if is_boycotted else "SAFE"
                    # is_success est True si NON boycotté
                    kpi_card(t['boycott_check'], status_text, t['boycott_target'], (not is_boycotted), t['boycott_help'])
                
                with cs_b:
                    is_act_good = shariah['activity_ok']
                    msg = "APPROVED" if is_act_good else "RESTRICTED"
                    kpi_card(t['act_check'], msg, d['industry'][:20]+"...", is_act_good, t['act_check_help'])

                st.markdown("---")
                
                # DEUXIEME LIGNE : QUANTITATIF (Ratios)
                cs1, cs2, cs3, cs4 = st.columns(4)
                
                with cs1:
                    val = shariah['haram_ratio']
                    kpi_card(t['inc_haram'], f"{val:.2f}%", t['inc_target'], (val < 5), t['inc_haram_help'])
                with cs2:
                    val = shariah['debt_ratio']
                    kpi_card(t['debt'], f"{val:.1f}%", t['debt_target'], (val < 33), t['debt_help'])
                with cs3:
                    val = shariah['illiquid_ratio']
                    kpi_card(t['real_assets'], f"{val:.1f}%", t['real_target'], (val > 20), t['real_assets_help'])
                with cs4:
                    is_liquid_ok = shariah['liquid_ok']
                    kpi_card(t['cash_cap'], "PASS" if is_liquid_ok else "FAIL", t['cash_target'], is_liquid_ok, t['cash_target'])

            # --- TAB 3 : EXIT ---
            with tab3:
                if d['eps'] and d['eps'] > 0:
                    t15 = d['eps'] * 15
                    t20 = d['eps'] * 20
                    hist = agent.stock.history(period="1y")
                    
                    # Graphique Plotly Style Dark
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Price', 
                                             line=dict(color='#00E096', width=2), fill='tozeroy', fillcolor='rgba(0, 224, 150, 0.05)'))
                    
                    # Lignes de cibles
                    fig.add_hline(y=t15, line_dash="dot", line_color="#E0C38C", annotation_text="TP1 (x15)", annotation_font_color="#E0C38C")
                    fig.add_hline(y=t20, line_dash="dot", line_color="#FF4B4B", annotation_text="TP2 (x20)", annotation_font_color="#FF4B4B")
                    
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        margin=dict(l=10, r=10, t=30, b=10),
                        font=dict(family="Space Grotesk"),
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col_ex1, col_ex2 = st.columns(2)
                    col_ex1.markdown(f"<div style='color:#E0C38C; font-family:Space Grotesk;'>🎯 {t['target1']} : <b>{t15:.2f} {d['currency']}</b></div>", unsafe_allow_html=True)
                    col_ex2.markdown(f"<div style='color:#FF4B4B; font-family:Space Grotesk;'>🚀 {t['target2']} : <b>{t20:.2f} {d['currency']}</b></div>", unsafe_allow_html=True)
                else: st.warning("EPS Data missing.")
                
        except Exception as e: st.error(f"Error: {e}")
elif not st.session_state.active_ticker:
    st.markdown(f"""
    <div style="margin-top:50px; text-align:center; opacity:0.5;">
        <p>FinanceBro Protocol v5.2 • Powered by IFG & Boycott API</p>
    </div>
    """, unsafe_allow_html=True)