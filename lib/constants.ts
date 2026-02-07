// ============================================================
// Configuration — miroir de config/settings.py
// ============================================================

export const APP = {
  name: "Mizan Investments",
  icon: "⚖️",
  version: "3.0.0",
} as const;

// Seuils Shariah (AAOIFI)
export const SHARIAH = {
  maxDebtRatio: 33.0,
  maxInterestIncomeRatio: 5.0,
  minRealAssetsRatio: 20.0,
} as const;

// Seuils stratégies
export const STRATEGIES = {
  Mizan: {
    label: "Mizan Strategy",
    subtitle: "Quality Growth",
    description: "Focus on sustainable quality at reasonable prices",
    maxPE: 25.0,
    minMargin: 15.0,
    maxNetDebtEbitda: 3.0,
    fcfYieldGrowth: 2.5,
    fcfYieldMature: 5.0,
  },
  Graham: {
    label: "Ben Graham",
    subtitle: "Modern Value",
    description: "Margin of safety with quality focus",
    maxPE: 15.0,
    minCurrentRatio: 1.5,
    maxDebtEquity: 50.0,
    minInterestCoverage: 3.0,
    minROE: 8.0,
  },
  Lynch: {
    label: "Peter Lynch",
    subtitle: "Growth",
    description: "GARP — Growth at Reasonable Price",
    maxPEG: 1.0,
    minGrowth: 15.0,
    maxDebtEquity: 80.0,
    maxPE: 25.0,
  },
} as const;

// Secteurs blacklistés
export const SECTOR_BLACKLIST = new Set([
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
]);

// Mots-clés blacklistés
export const KEYWORD_BLACKLIST = new Set([
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
]);

// Exchanges gratuits FMP
export const FREE_EXCHANGES = new Set(["NASDAQ", "NYSE", "AMEX"]);

// API
export const FMP_BASE_URL = "https://financialmodelingprep.com";
export const BOYCOTT_API_URL = "https://api.boycottisraeli.biz/v1/search";
