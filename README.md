# 💸 FinanceBro Terminal

**FinanceBro** is an "All-in-One" stock analysis dashboard powered by **Streamlit**. It combines the mathematical rigor of Value Investing with the ethical strictness of Islamic Finance.

Designed for investors who refuse to choose between **Performance** and **Principles**.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Strategy](https://img.shields.io/badge/Strategy-Value%20%2B%20Shariah-green)

## 🎯 The Dual Strategy

The agent performs two parallel audits on every stock ticker:

### 1. 📊 The Financial Audit ("The Bro Strategy")
Based on Deep Value and Quality Investing principles:
- **Valuation**: P/E Ratio < 12 (Ideally < 8).
- **Quality (Moat)**: ROE > 10% and Operating Margin > 14%.
- **Health**: Working Capital Requirement (WCR) controlled (< 25% of Revenue).
- **Momentum**: Positive price trend over the last 3 months.

### 2. ☪️ The Shariah Audit ("IFG Standards")
Strict application of the criteria defined by *Islamic Finance Guru* and *Mufti Taqi Usmani*:
- **Business Activity**: Manual verification of the sector (via integrated Musaffa link).
- **Non-Compliant Income**: Interest income must be **< 5%** of Total Revenue.
- **Interest-Bearing Debt**: Total debt must be **< 33%** of **Total Assets** (not Market Cap).
- **Real Assets**: Illiquid assets (PPE, Inventory, Intangibles) must represent **> 20%** of Total Assets.
- **Liquidity**: Net liquid assets (Cash) should not exceed Market Capitalization.

## 🛠 Quick Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/FinanceBro.git](https://github.com/YOUR_USERNAME/FinanceBro.git)
   cd FinanceBro

python -m venv venv
venv\Scripts\activate
streamlit run app.py