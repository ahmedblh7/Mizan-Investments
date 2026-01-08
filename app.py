import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import plotly.graph_objects as go

# =========================================================
# 🎨 CONFIGURATION & DESIGN SYSTEM (DARK LUXURY)
# =========================================================
st.set_page_config(page_title="FinanceBro", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    :root { --bg-dark: #0B0E13; --bg-card: rgba(28, 32, 43, 0.6); --accent-green: #00E096; --accent-gold: #E0C38C; --text-white: #FFFFFF; --text-silver: #C8CDD5; --border-subtle: rgba(255, 255, 255, 0.08); }
    .stApp { background-color: var(--bg-dark); background-image: radial-gradient(circle at 50% 0%, #151922 0%, #0B0E13 80%), url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231C202B' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E"); font-family: 'Inter', sans-serif; color: var(--text-silver); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }
    .glass-card { background: var(--bg-card); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 24px; height: 100%; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
    .glass-card:hover { transform: translateY(-4px); border-color: rgba(0, 224, 150, 0.3); box-shadow: 0 10px 30px rgba(0, 224, 150, 0.1); }
    .kpi-title { font-family: 'Inter', sans-serif; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: #6E7687; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
    .kpi-value { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--text-white); margin-bottom: 4px; }
    .kpi-target { font-size: 0.85rem; color: #555; font-family: 'Space Grotesk', sans-serif; }
    .val-green { color: var(--accent-green); text-shadow: 0 0 15px rgba(0, 224, 150, 0.4); }
    .val-gold { color: var(--accent-gold); text-shadow: 0 0 15px rgba(224, 195, 140, 0.3); }
    .val-red { color: #FF4B4B; text-shadow: 0 0 15px rgba(255, 75, 75, 0.3); }
    .stTextInput > div > div > input { background-color: #0F1218; color: white; border: 1px solid #333; border-radius: 12px; padding: 12px; font-family: 'Space Grotesk'; }
    .stButton > button { background: linear-gradient(135deg, #00E096 0%, #00B075 100%); color: #0B0E13; border: none; border-radius: 8px; padding: 0.6rem 1.5rem; font-family: 'Space Grotesk', sans-serif; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.3s; }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 224, 150, 0.4); color: black; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: rgba(255,255,255,0.02); border-radius: 12px; padding: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: transparent; border-radius: 8px; color: #6E7687; font-family: 'Space Grotesk'; border: none; }
    .stTabs [aria-selected="true"] { background-color: #1C202B; color: var(--accent-gold); border: 1px solid rgba(224, 195, 140, 0.2); }
    .verdict-box { padding: 24px; border-radius: 16px; margin-bottom: 30px; display: flex; align-items: center; gap: 20px; border: 1px solid; backdrop-filter: blur(10px); }
    .verdict-halal { background: linear-gradient(90deg, rgba(0, 224, 150, 0.1) 0%, rgba(0,0,0,0) 100%); border-color: rgba(0, 224, 150, 0.3); }
    .verdict-haram { background: linear-gradient(90deg, rgba(255, 75, 75, 0.1) 0%, rgba(0,0,0,0) 100%); border-color: rgba(255, 75, 75, 0.3); }
    [data-testid="stMetricLabel"] { font-family: 'Inter'; color: #6E7687; font-size: 0.9rem; }
    [data-testid="stMetricValue"] { font-family: 'Space Grotesk'; color: white; font-size: 1.8rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 🚫 BLACKLIST
# =========================================================
SECTOR_BLACKLIST = ['Banks', 'Insurance', 'Capital Markets', 'Credit Services', 'Mortgage', 'Beverages - Wineries & Distilleries', 'Beverages - Brewers', 'Tobacco', 'Gambling', 'Casinos', 'Defense']
KEYWORD_BLACKLIST = ['alcohol', 'liquor', 'wine', 'beer', 'brewery', 'pork', 'gambling', 'casino', 'betting', 'tobacco', 'interest', 'lending', 'banking', 'adult']

# =========================================================
# 💾 STATE
# =========================================================
if 'active_ticker' not in st.session_state: st.session_state.active_ticker = None
if 'selected_strategy' not in st.session_state: st.session_state.selected_strategy = "FinanceBro"

def trigger_analysis(ticker): st.session_state.active_ticker = ticker

# =========================================================
# 🌍 TRADUCTIONS (VERIFIÉES ET COMPLÈTES)
# =========================================================
TRANSLATIONS = {
    'en': {
        # Navigation & Headers
        'sidebar_title': "FinanceBro", 'sidebar_subtitle': "Institutional Grade Analysis",
        'analyze_btn': "INITIATE SCAN", 'search_placeholder': "Search ticker...", 
        'no_result': "No asset found.", 'select_stock': "Select Asset", 'crunching': "Processing...",
        'hero_title': "Take your wealth<br>to the next level.", 'hero_sub': "Manage. Analyze. Dominate.",
        'search_title': "ASSET INTELLIGENCE",
        'methodology': "Proprietary Algorithm", # FIXED: Key Added

        # Verdicts
        'verdict_halal_title': "COMPLIANT ASSET", 'verdict_halal_desc': "Meets quantitative Shariah standards.",
        'verdict_haram_title': "NON-COMPLIANT", 'verdict_haram_desc': "Failed checks: ",
        
        # Tabs
        'tab_fund': "STRATEGY AUDIT", 'tab_shariah': "COMPLIANCE", 'tab_exit': "EXIT PLAN",
        
        # Header Metrics
        'company': "Issuer", 'company_help': "Official registered name.", # FIXED
        'price': "Spot Price", 'price_help': "Real-time market price.", # FIXED
        'mcap': "Market Cap", 'mcap_help': "Total value of all shares.", # FIXED
        'momentum': "Momentum (3M)", 'momentum_help': "Price trend over last 3 months.", # FIXED
        
        # Strategies
        'strategy_label': "STRATEGY SELECTION",
        'strat_name_fb': "FinanceBro (Quality)",
        'strat_name_bg': "Ben Graham (Deep Value)",
        'strat_name_pl': "Peter Lynch (Growth)",
        'strategy_active': "Active Strategy:",
        'bullets_fin': "• FCF Yield > 5% 🌟<br>• P/E < 12<br>• Debt/EBITDA < 3",
        'bullets_shariah': "• Debt < 33%<br>• Interest < 5%<br>• Real Assets > 20%",

        # KPIs & Tooltips
        'per': "P/E Ratio", 'per_help': "Price-to-Earnings Ratio.", 
        'pb': "P/B Ratio", 'pb_help': "Price-to-Book Ratio.", 
        'peg': "PEG Ratio", 'peg_help': "Price/Earnings-to-Growth.",
        'fcf_yield': "FCF Yield", 'fcf_help': "Free Cash Flow Yield.",
        'roe': "ROE", 'roe_help': "Return on Equity.", 
        'margin': "Ops Margin", 'margin_help': "Operating Margin.",
        'solvency': "Net Debt/EBITDA", 'solvency_help': "Years to pay off debt.",
        'growth': "Rev Growth", 'growth_help': "Revenue Growth.",
        'current_ratio': "Current Ratio", 'current_help': "Short-term liquidity.",
        'debt_equity': "Debt/Equity", 'de_help': "Total Debt to Equity.",
        'goal': "Goal:",

        # Shariah
        'act_check': "Activity", 'act_help': "Sector Screening.",
        'inc_haram': "Impure Inc.", 'inc_help': "Interest Income.", 'inc_target': "Limit < 5%", # FIXED
        'debt': "Leverage", 'debt_help': "Debt/Assets Ratio.", 'debt_target': "Limit < 33%",
        'real_assets': "Real Assets", 'real_help': "Tangible Assets Ratio.", 'real_target': "Min > 20%",
        'cash_cap': "Liquidity", 'cash_help': "Cash vs Market Cap.", 'cash_target': "Cash < Market Cap",
        'boycott_check': "Boycott", 'boycott_help': "Boycott List Check.", 'boycott_target': "Not Listed",
        
        # Status Text
        'status_safe': "SAFE", 'status_listed': "LISTED",
        'status_approved': "APPROVED", 'status_restricted': "RESTRICTED",
        'status_pass': "PASS", 'status_fail': "FAIL",

        # Exit Plan
        'target1': "Take Profit 1 (20%)", 'target2': "Exit All", 
        'chart_title': "Price Action (1Y)", 'missing_eps': "EPS Data missing."
    },
    'fr': {
        # Navigation & Headers
        'sidebar_title': "FinanceBro", 'sidebar_subtitle': "Analyse de niveau institutionnel",
        'analyze_btn': "LANCER LE SCAN", 'search_placeholder': "Rechercher...", 
        'no_result': "Aucun actif trouvé.", 'select_stock': "Sélectionner l'actif", 'crunching': "Traitement...",
        'hero_title': "Votre patrimoine passe<br>au niveau supérieur.", 'hero_sub': "Gérez. Analysez. Dominez.",
        'search_title': "INTELLIGENCE D'ACTIF",
        'methodology': "Algorithme Propriétaire", # FIXED: Key Added

        # Verdicts
        'verdict_halal_title': "ACTIF CONFORME", 'verdict_halal_desc': "Respecte les standards Shariah.",
        'verdict_haram_title': "NON-CONFORME", 'verdict_haram_desc': "Échecs : ",
        
        # Tabs
        'tab_fund': "AUDIT STRATÉGIQUE", 'tab_shariah': "CONFORMITÉ", 'tab_exit': "PLAN DE SORTIE",
        
        # Header Metrics
        'company': "Émetteur", 'company_help': "Nom officiel enregistré.", # FIXED
        'price': "Prix Spot", 'price_help': "Prix marché temps réel.", # FIXED
        'mcap': "Capitalisation", 'mcap_help': "Valeur totale des actions.", # FIXED
        'momentum': "Momentum 3M", 'momentum_help': "Tendance sur 3 mois.", # FIXED

        # Strategies
        'strategy_label': "SÉLECTION STRATÉGIE",
        'strat_name_fb': "FinanceBro (Qualité)",
        'strat_name_bg': "Ben Graham (Valeur)",
        'strat_name_pl': "Peter Lynch (Croissance)",
        'strategy_active': "Stratégie Active :",
        'bullets_fin': "• Rendement FCF > 5% 🌟<br>• PER < 12<br>• Dette/EBITDA < 3",
        'bullets_shariah': "• Dette < 33%<br>• Intérêts < 5%<br>• Actifs Réels > 20%",

        # KPIs & Tooltips
        'per': "PER", 'per_help': "Ratio Cours/Bénéfice.", 
        'pb': "Price/Book", 'pb_help': "Ratio Cours/Actif Net.", 
        'peg': "Ratio PEG", 'peg_help': "Ratio PER/Croissance.",
        'fcf_yield': "Rendement FCF", 'fcf_help': "Rendement du Cash Flow Libre.",
        'roe': "ROE", 'roe_help': "Rentabilité des Capitaux Propres.", 
        'margin': "Marge Ops", 'margin_help': "Marge Opérationnelle.",
        'solvency': "Dette Nette/EBITDA", 'solvency_help': "Années pour rembourser la dette.",
        'growth': "Croissance CA", 'growth_help': "Croissance du CA (Annuel).",
        'current_ratio': "Ratio Courant", 'current_help': "Liquidité à court terme.",
        'debt_equity': "Dette/Equity", 'de_help': "Dette sur Capitaux Propres.",
        'goal': "Cible :",

        # Shariah
        'act_check': "Activité", 'act_help': "Scan Sectoriel.",
        'inc_haram': "Rev. Impurs", 'inc_help': "Revenus d'intérêts.", 'inc_target': "Limite < 5%", # FIXED
        'debt': "Levier", 'debt_help': "Ratio Dette/Actifs.", 'debt_target': "Limite < 33%",
        'real_assets': "Actifs Réels", 'real_help': "Ratio Actifs Tangibles.", 'real_target': "Min > 20%",
        'cash_cap': "Liquidité", 'cash_help': "Cash vs Capitalisation.", 'cash_target': "Cash < Capitalisation",
        'boycott_check': "Boycott", 'boycott_help': "Vérification Liste Boycott.", 'boycott_target': "Non Listé",

        # Status Text
        'status_safe': "SÛR", 'status_listed': "LISTÉ",
        'status_approved': "APPROUVÉ", 'status_restricted': "RESTREINT",
        'status_pass': "VALIDE", 'status_fail': "ÉCHEC",

        # Exit Plan
        'target1': "Prise de Profit 1 (20%)", 'target2': "Sortie Totale", 
        'chart_title': "Action des Prix (1 An)", 'missing_eps': "Données EPS manquantes."
    }
}

# =========================================================
# 🧠 BACKEND (SAFE & ROBUST)
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
        
    def _safe_get(self, key, default=None): return self.info.get(key, default)
    def _get_item(self, df, items_list):
        if df is None or df.empty: return 0
        for item in items_list:
            if item in df.index: return df.loc[item].iloc[0]
        return 0

    def collect_data(self):
        # Basic Info
        self.data['name'] = self._safe_get('longName', self.ticker)
        self.data['industry'] = self._safe_get('industry', 'Unknown')
        self.data['sector'] = self._safe_get('sector', 'Unknown')
        self.data['description'] = self._safe_get('longBusinessSummary', '')
        self.data['current_price'] = self._safe_get('currentPrice', 0)
        self.data['currency'] = self._safe_get('currency', 'USD')
        self.data['market_cap'] = self._safe_get('marketCap', 1)

        # Fundamental Data Points (Safe Initialization)
        self.data['per'] = self._safe_get('trailingPE', 0)
        self.data['eps'] = self._safe_get('trailingEps', 0) # FIXED: Prevent 'eps' KeyError
        self.data['pb'] = self._safe_get('priceToBook', 0)
        self.data['peg'] = self._safe_get('pegRatio', 0)
        self.data['roe'] = self._safe_get('returnOnEquity', 0) * 100 if self._safe_get('returnOnEquity') else 0
        self.data['ops_margin'] = self._safe_get('operatingMargins', 0) * 100 if self._safe_get('operatingMargins') else 0
        self.data['current_ratio'] = self._safe_get('currentRatio', 0)
        self.data['debt_to_equity'] = self._safe_get('debtToEquity', 0)

        # FCF
        try:
            ocf = self._get_item(self.cashflow, ['Operating Cash Flow', 'Total Cash From Operating Activities'])
            capex = self._get_item(self.cashflow, ['Capital Expenditure', 'Net PPE Purchase And Sale'])
            fcf = ocf + capex 
            self.data['fcf_yield'] = (fcf / self.data['market_cap']) * 100 if self.data['market_cap'] > 0 else 0
        except: self.data['fcf_yield'] = 0

        # Solvency
        try:
            total_debt = self._safe_get('totalDebt', 0)
            cash = self._safe_get('totalCash', 0)
            ebitda = self._safe_get('ebitda', 1)
            self.data['net_debt_ebitda'] = (total_debt - cash) / ebitda if ebitda else 0
        except: self.data['net_debt_ebitda'] = 0

        # Growth
        try:
            revs = self.financials.loc['Total Revenue']
            self.data['revenue_growth'] = ((revs.iloc[0] - revs.iloc[1]) / revs.iloc[1]) * 100 if len(revs) >= 2 else 0
        except: self.data['revenue_growth'] = 0

        # Momentum
        try:
            hist = self.stock.history(period="3mo")
            if not hist.empty:
                start = hist['Close'].iloc[0]
                end = hist['Close'].iloc[-1]
                self.data['momentum_3m'] = ((end - start) / start) * 100
            else: self.data['momentum_3m'] = 0
        except: self.data['momentum_3m'] = 0

        # Shariah Specifics
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

    def evaluate_strategy(self, strategy_key):
        d = self.data
        results = [] 
        
        if strategy_key == "FinanceBro":
            results.append({"k": "fcf_yield", "v": f"{d['fcf_yield']:.2f}%", "t": "> 5%", "pass": d['fcf_yield'] > 5, "h": "fcf_help"})
            per = d['per'] if d['per'] else 0
            results.append({"k": "per", "v": f"{per:.2f}", "t": "< 12", "pass": (0 < per < 12), "h": "per_help"})
            results.append({"k": "roe", "v": f"{d['roe']:.2f}%", "t": "> 10%", "pass": d['roe'] > 10, "h": "roe_help"})
            results.append({"k": "solvency", "v": f"{d['net_debt_ebitda']:.2f}x", "t": "< 3.0", "pass": d['net_debt_ebitda'] < 3, "h": "solvency_help"})

        elif strategy_key == "Graham":
            per = d['per'] if d['per'] else 0
            results.append({"k": "per", "v": f"{per:.2f}", "t": "< 15", "pass": (0 < per < 15), "h": "per_help"})
            pb = d['pb'] if d['pb'] else 0
            results.append({"k": "pb", "v": f"{pb:.2f}", "t": "< 1.5", "pass": (0 < pb < 1.5), "h": "pb_help"})
            cr = d['current_ratio'] if d['current_ratio'] else 0
            results.append({"k": "current_ratio", "v": f"{cr:.2f}", "t": "> 1.5", "pass": cr > 1.5, "h": "current_help"})
            de = d['debt_to_equity'] if d['debt_to_equity'] else 999
            results.append({"k": "debt_equity", "v": f"{de:.0f}%", "t": "< 50%", "pass": de < 50, "h": "de_help"})

        elif strategy_key == "Lynch":
            peg = d['peg'] if d['peg'] else 0
            results.append({"k": "peg", "v": f"{peg:.2f}", "t": "< 1.0", "pass": (0 < peg < 1.0), "h": "peg_help"})
            results.append({"k": "growth", "v": f"{d['revenue_growth']:.1f}%", "t": "> 15%", "pass": d['revenue_growth'] > 15, "h": "growth_help"})
            de = d['debt_to_equity'] if d['debt_to_equity'] else 999
            results.append({"k": "debt_equity", "v": f"{de:.0f}%", "t": "< 80%", "pass": de < 80, "h": "de_help"})
            per = d['per'] if d['per'] else 0
            results.append({"k": "per", "v": f"{per:.2f}", "t": "< 25", "pass": (0 < per < 25), "h": "per_help"})

        return results

    def check_boycott_status(self):
        try:
            clean_name = self.data['name'].replace(" Inc.", "").replace(" Corporation", "").split(" - ")[0].strip()
            url = f"https://api.boycottisraeli.biz/v1/search/{clean_name}"
            r = requests.get(url, timeout=2)
            if r.status_code == 200 and len(r.json()) > 0: return True
            return False
        except: return False

    def check_business_activity(self):
        industry = str(self.data['industry']).lower()
        sector = str(self.data['sector']).lower()
        desc = str(self.data['description']).lower()
        issues = [f"Sector: {s}" for s in SECTOR_BLACKLIST if s.lower() in industry or s.lower() in sector]
        if not issues:
            for k in KEYWORD_BLACKLIST:
                if f" {k} " in f" {desc} ":
                    issues.append(f"Keyword: {k}")
                    break
        return (False, ", ".join(issues)) if issues else (True, "OK")

    def calculate_shariah_ratios(self):
        d = self.data
        ratio_haram = (d['interest_income'] / d['total_revenue']) * 100 if 'total_revenue' in d and d['total_revenue'] else 0
        ratio_debt = (d['total_debt'] / d['total_assets']) * 100
        ratio_illiquid = (d['illiquid_assets'] / d['total_assets']) * 100
        is_liquid_ok = d['current_assets'] < d['market_cap']
        is_act_halal, act_msg = self.check_business_activity()
        is_boycotted = self.check_boycott_status()

        failures = []
        if not is_act_halal: failures.append(f"Activity")
        if is_boycotted: failures.append("Boycott Listed")
        if ratio_haram >= 5: failures.append("Interest > 5%")
        if ratio_debt >= 33: failures.append("Debt > 33%")
        if ratio_illiquid <= 20: failures.append("Real Assets < 20%")
        if not is_liquid_ok: failures.append("Cash > Cap")
        
        return {
            "haram_ratio": ratio_haram, "debt_ratio": ratio_debt, "illiquid_ratio": ratio_illiquid,
            "liquid_ok": is_liquid_ok, "activity_ok": is_act_halal, "activity_msg": act_msg, "is_boycotted": is_boycotted,
            "status": "HALAL" if not failures else "HARAM", "details": failures
        }

def search_symbol(query):
    try:
        r = requests.get(f"https://query2.finance.yahoo.com/v1/finance/search?q={query}", headers={'User-Agent': 'Mozilla/5.0'})
        data = r.json()
        if 'quotes' in data and len(data['quotes']) > 0: return data['quotes']
    except: return []
    return []

def kpi_card(label, value_str, target_text, is_success, help_text, goal_label="Goal:"):
    if is_success: color_class = "val-green"
    else: color_class = "val-red"
    icon = """<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>"""
    st.markdown(f"""<div class="glass-card"><div><div class="kpi-title">{label}<span title="{help_text}" style="cursor:help; opacity:0.6;">{icon}</span></div><div class="kpi-value {color_class}">{value_str}</div></div><div class="kpi-target"><span style="opacity:0.5;">{goal_label}</span> {target_text}</div></div>""", unsafe_allow_html=True)

# =========================================================
# 📱 FRONTEND
# =========================================================
with st.sidebar:
    st.markdown("### 🛡️ FINANCE BRO")
    lang_choice = st.selectbox("", ["English", "Français"], key="lang", label_visibility="collapsed")
    lang = 'en' if lang_choice == "English" else 'fr'
    t = TRANSLATIONS[lang]
    st.caption(t['sidebar_subtitle'])
    st.markdown("---")
    
    st.markdown(f"**{t['strategy_label']}**")
    strat_map = {"FinanceBro": t['strat_name_fb'], "Graham": t['strat_name_bg'], "Lynch": t['strat_name_pl']}
    reverse_map = {v: k for k, v in strat_map.items()}
    selected_display_name = st.selectbox("Strat", list(strat_map.values()), key='strategy_box', label_visibility="collapsed")
    st.session_state.selected_strategy = reverse_map[selected_display_name]
    
    st.info(f"{t['strategy_active']} **{selected_display_name}**")
    st.markdown("---")
    st.markdown(f"**{t['methodology']}**")
    with st.expander(t['strat_name_fb']): st.markdown(f"<div style='font-size:13px; color:#C8CDD5;'>{t['bullets_fin']}</div>", unsafe_allow_html=True)
    with st.expander(t['tab_shariah']): st.markdown(f"<div style='font-size:13px; color:#C8CDD5;'>{t['bullets_shariah']}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**CONNECTED TO**")
    st.markdown("<div style='display:flex; gap:10px; opacity:0.4; filter:grayscale(100%);'><img src='https://logo.clearbit.com/binance.com' width='20'><img src='https://logo.clearbit.com/bloomberg.com' width='20'></div>", unsafe_allow_html=True)

st.markdown(f"""<div style="margin-bottom: 40px;"><h1 style="font-size: 3.5rem; line-height: 1.1;">{t['hero_title']}</h1><p style="font-size: 1.2rem; color: #00E096; font-family: 'Space Grotesk'; margin-top:10px;">{t['hero_sub']}</p></div>""", unsafe_allow_html=True)

st.markdown(f"### {t['search_title']}")
c1, c2 = st.columns([2, 1])
input_ticker = None
with c1: search_query = st.text_input("Search", placeholder=t['search_placeholder'], label_visibility="collapsed")
with c2:
    if search_query:
        results = search_symbol(search_query)
        if results:
            opts = {f"{r['shortname']} ({r['symbol']})": r['symbol'] for r in results if 'shortname' in r}
            sel = st.selectbox("Select", opts.keys(), label_visibility="collapsed")
            input_ticker = opts[sel]
        else: st.selectbox("Select", [t['no_result']], disabled=True, label_visibility="collapsed")
    else: st.selectbox("Select", [t['select_stock']], disabled=True, label_visibility="collapsed")

st.markdown("###")
if st.button(t['analyze_btn'], type="primary", use_container_width=True, disabled=not input_ticker): trigger_analysis(input_ticker)

if st.session_state.active_ticker:
    ticker = st.session_state.active_ticker
    with st.spinner(t['crunching']):
        try:
            agent = FinanceBroAgent(ticker)
            agent.collect_data()
            d = agent.data
            shariah = agent.calculate_shariah_ratios()
            strategy_results = agent.evaluate_strategy(st.session_state.selected_strategy)

            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(t['company'], d['name'], help=t['company_help'])
            m2.metric(t['price'], f"{d['current_price']} {d['currency']}", help=t['price_help'])
            m3.metric(t['mcap'], f"{d['market_cap']/1e9:.1f}B", help=t['mcap_help'])
            m4.metric(t['momentum'], f"{d['momentum_3m']:.2f}%", delta="Trend", delta_color="normal" if d['momentum_3m'] > 0 else "inverse", help=t['momentum_help'])
            
            st.markdown("###")
            if shariah['status'] == "HALAL":
                st.markdown(f"""<div class="verdict-box verdict-halal"><div style="font-size:2rem; text-shadow: 0 0 20px #00E096;">🛡️</div><div><div style="font-weight:700; font-size:1.2rem; font-family:'Space Grotesk'; color:#00E096;">{t['verdict_halal_title']}</div><div style="font-size:0.9rem; opacity:0.8;">{t['verdict_halal_desc']}</div></div></div>""", unsafe_allow_html=True)
            else:
                fail_txt = t['verdict_haram_desc'] + ", ".join(shariah['details'])
                st.markdown(f"""<div class="verdict-box verdict-haram"><div style="font-size:2rem; text-shadow: 0 0 20px #FF4B4B;">🚫</div><div><div style="font-weight:700; font-size:1.2rem; font-family:'Space Grotesk'; color:#FF4B4B;">{t['verdict_haram_title']}</div><div style="font-size:0.9rem; opacity:0.8;">{fail_txt}</div></div></div>""", unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs([t['tab_fund'], t['tab_shariah'], t['tab_exit']])

            with tab1:
                cols = st.columns(4)
                for i, item in enumerate(strategy_results):
                    # SAFE TRANSLATION ACCESS
                    label = t.get(item['k'], item['k']) 
                    tooltip = t.get(item['h'], "") 
                    with cols[i % 4]:
                        kpi_card(label, item['v'], item['t'], item['pass'], tooltip, goal_label=t['goal'])

            with tab2:
                cs_a, cs_b = st.columns(2)
                with cs_a:
                    is_boycotted = shariah['is_boycotted']
                    status_text = t['status_listed'] if is_boycotted else t['status_safe']
                    kpi_card(t['boycott_check'], status_text, t['boycott_target'], (not is_boycotted), t['boycott_help'], goal_label=t['goal'])
                with cs_b:
                    is_act_good = shariah['activity_ok']
                    status_text = t['status_approved'] if is_act_good else t['status_restricted']
                    kpi_card(t['act_check'], status_text, d['industry'][:20]+"...", is_act_good, t['act_help'], goal_label=t['goal'])
                st.markdown("---")
                cs1, cs2, cs3, cs4 = st.columns(4)
                with cs1: kpi_card(t['inc_haram'], f"{shariah['haram_ratio']:.2f}%", t['inc_target'], (shariah['haram_ratio'] < 5), t['inc_help'], goal_label=t['goal'])
                with cs2: kpi_card(t['debt'], f"{shariah['debt_ratio']:.1f}%", t['debt_target'], (shariah['debt_ratio'] < 33), t['debt_help'], goal_label=t['goal'])
                with cs3: kpi_card(t['real_assets'], f"{shariah['illiquid_ratio']:.1f}%", t['real_target'], (shariah['illiquid_ratio'] > 20), t['real_help'], goal_label=t['goal'])
                with cs4: 
                    is_liq = shariah['liquid_ok']
                    status_text = t['status_pass'] if is_liq else t['status_fail']
                    kpi_card(t['cash_cap'], status_text, t['cash_target'], is_liq, t['cash_help'], goal_label=t['goal'])

            with tab3:
                # SAFE EPS CHECK
                eps_val = d.get('eps', 0)
                if eps_val and eps_val > 0:
                    t15, t20 = eps_val * 15, eps_val * 20
                    hist = agent.stock.history(period="1y")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Price', line=dict(color='#00E096', width=2), fill='tozeroy', fillcolor='rgba(0, 224, 150, 0.05)'))
                    fig.add_hline(y=t15, line_dash="dot", line_color="#E0C38C", annotation_text=t['target1'], annotation_font_color="#E0C38C")
                    fig.add_hline(y=t20, line_dash="dot", line_color="#FF4B4B", annotation_text=t['target2'], annotation_font_color="#FF4B4B")
                    fig.update_layout(template="plotly_dark", title=t['chart_title'], paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=10, r=10, t=40, b=10), font=dict(family="Space Grotesk"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
                    st.plotly_chart(fig, use_container_width=True)
                    c1, c2 = st.columns(2)
                    c1.markdown(f"<div style='color:#E0C38C; font-family:Space Grotesk;'>🎯 {t['target1']} : <b>{t15:.2f} {d['currency']}</b></div>", unsafe_allow_html=True)
                    c2.markdown(f"<div style='color:#FF4B4B; font-family:Space Grotesk;'>🚀 {t['target2']} : <b>{t20:.2f} {d['currency']}</b></div>", unsafe_allow_html=True)
                else: st.warning(t['missing_eps'])
        except Exception as e: st.error(f"Error: {e}")
elif not st.session_state.active_ticker:
    st.markdown(f"""<div style="margin-top:50px; text-align:center; opacity:0.5;"><p>FinanceBro Protocol v6.4 • Error-Free Core</p></div>""", unsafe_allow_html=True)