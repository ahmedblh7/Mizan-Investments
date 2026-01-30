"""
Styles CSS pour l'application Mizan.
"""
import streamlit as st


# Palette de couleurs
COLORS = {
    "bg_dark": "#0B0E13",
    "bg_card": "rgba(28, 32, 43, 0.6)",
    "accent_green": "#00E096",
    "accent_gold": "#E0C38C",
    "accent_red": "#FF4B4B",
    "text_white": "#FFFFFF",
    "text_silver": "#C8CDD5",
    "text_muted": "#6E7687",
    "border_subtle": "rgba(255, 255, 255, 0.08)",
}


CSS_STYLES = """
<style>
    /* Imports */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Variables CSS */
    :root {
        --bg-dark: #0B0E13;
        --bg-card: rgba(28, 32, 43, 0.6);
        --accent-green: #00E096;
        --accent-gold: #E0C38C;
        --accent-red: #FF4B4B;
        --text-white: #FFFFFF;
        --text-silver: #C8CDD5;
        --text-muted: #6E7687;
        --border-subtle: rgba(255, 255, 255, 0.08);
    }
    
    /* App Background */
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 50% 0%, #151922 0%, #0B0E13 80%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231C202B' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        font-family: 'Inter', sans-serif;
        color: var(--text-silver);
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.02em;
    }
    
    /* Glass Card */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        margin-bottom: 20px;
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
    
    /* KPI Cards */
    .kpi-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-muted);
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
    
    /* Value Colors */
    .val-green {
        color: var(--accent-green);
        text-shadow: 0 0 15px rgba(0, 224, 150, 0.4);
    }
    
    .val-gold {
        color: var(--accent-gold);
        text-shadow: 0 0 15px rgba(224, 195, 140, 0.3);
    }
    
    .val-red {
        color: var(--accent-red);
        text-shadow: 0 0 15px rgba(255, 75, 75, 0.3);
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input {
        background-color: #0F1218;
        color: white;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 12px;
        font-family: 'Space Grotesk';
    }
    
    /* Buttons */
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
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: var(--text-muted);
        font-family: 'Space Grotesk';
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1C202B;
        color: var(--accent-gold);
        border: 1px solid rgba(224, 195, 140, 0.2);
    }
    
    /* Verdict Boxes */
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
    
    /* Metrics */
    [data-testid="stMetricLabel"] {
        font-family: 'Inter';
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk';
        color: white;
        font-size: 1.8rem;
        font-weight: 600;
    }
</style>
"""


def apply_custom_styles() -> None:
    """Applique les styles CSS personnalisés à l'application."""
    st.markdown(CSS_STYLES, unsafe_allow_html=True)