// ============================================================
// FMP Client — Server-side only (API key never exposed)
// Miroir de services/market_data.py
// ============================================================

import { FMP_BASE_URL } from "./constants";
import type { StockData, PricePoint } from "./types";

const API_KEY = process.env.FMP_API_KEY ?? "";

async function fmpGet<T>(endpoint: string, params: Record<string, string> = {}): Promise<T> {
  const url = new URL(`${FMP_BASE_URL}${endpoint}`);
  url.searchParams.set("apikey", API_KEY);
  for (const [k, v] of Object.entries(params)) {
    url.searchParams.set(k, v);
  }

  const res = await fetch(url.toString(), { next: { revalidate: 300 } });

  if (!res.ok) {
    throw new Error(`FMP ${res.status}: ${res.statusText} — ${endpoint}`);
  }

  const data = await res.json();

  if (data && typeof data === "object" && "Error Message" in data) {
    throw new Error(data["Error Message"]);
  }

  return data as T;
}

function safe(value: unknown, fallback = 0): number {
  if (value === null || value === undefined) return fallback;
  const n = Number(value);
  return isNaN(n) ? fallback : n;
}

// ------------------------------------------------------------------
//  Récupérer les données complètes d'une action
// ------------------------------------------------------------------
export async function fetchStockData(ticker: string): Promise<StockData> {
  const symbol = ticker.toUpperCase();

  // 5 requêtes parallèles (endpoints gratuits)
  const [profileArr, incomeArr, balanceArr, cashflowArr] = await Promise.all([
    fmpGet<Record<string, unknown>[]>("/stable/profile", { symbol }),
    fmpGet<Record<string, unknown>[]>("/stable/income-statement", {
      symbol,
      period: "annual",
      limit: "2",
    }),
    fmpGet<Record<string, unknown>[]>("/stable/balance-sheet-statement", {
      symbol,
      period: "annual",
      limit: "1",
    }),
    fmpGet<Record<string, unknown>[]>("/stable/cash-flow-statement", {
      symbol,
      period: "annual",
      limit: "1",
    }),
  ]);

  const p = Array.isArray(profileArr) && profileArr.length > 0 ? profileArr[0] : {};
  const income = Array.isArray(incomeArr) && incomeArr.length > 0 ? incomeArr[0] : {};
  const balance = Array.isArray(balanceArr) && balanceArr.length > 0 ? balanceArr[0] : {};
  const cashflow = Array.isArray(cashflowArr) && cashflowArr.length > 0 ? cashflowArr[0] : {};

  const name = (p.companyName as string) || symbol;
  if (!name) throw new Error(`No data for ${symbol}`);

  let marketCap = safe(p.marketCap ?? p.mktCap, 1);
  if (marketCap <= 0) marketCap = 1;

  const price = safe(p.price);
  const sharesOut = price > 0 ? marketCap / price : 0;

  // Income statement
  const totalRevenue = safe(income.revenue);
  const netIncome = safe(income.netIncome);
  const operatingIncomeVal = safe(income.operatingIncome);
  const ebitda = safe(income.ebitda);
  const interestExpense = Math.abs(safe(income.interestExpense));
  const interestIncome = safe(income.interestIncome);
  const epsFromIncome = safe(income.eps ?? income.epsdiluted ?? income.epsDiluted);

  // Balance sheet
  let totalAssets = safe(balance.totalAssets, 1);
  if (totalAssets <= 0) totalAssets = 1;
  const totalDebt = safe(balance.totalDebt);
  const cash = safe(balance.cashAndCashEquivalents);
  const totalEquity = safe(balance.totalStockholdersEquity);
  const totalCurrentAssets = safe(balance.totalCurrentAssets);
  const totalCurrentLiabilities = safe(balance.totalCurrentLiabilities);

  // Illiquid assets
  const ppe = safe(balance.propertyPlantEquipmentNet);
  const goodwill = safe(balance.goodwill);
  const intangibles = safe(balance.intangibleAssets);
  const inventory = safe(balance.inventory);
  let illiquidAssets = ppe + goodwill + intangibles + inventory;
  if (illiquidAssets === 0 && totalCurrentAssets > 0) {
    illiquidAssets = totalAssets - totalCurrentAssets;
  }

  // Cash flow
  const fcf = safe(cashflow.freeCashFlow);

  // ============================================================
  //  RATIOS (calculés manuellement — pas d'endpoints payants)
  // ============================================================
  const peRatio = epsFromIncome > 0 ? price / epsFromIncome : null;

  const bvps = sharesOut > 0 ? totalEquity / sharesOut : 0;
  const pbRatio = bvps > 0 ? price / bvps : null;

  // EPS: profil d'abord, puis income statement
  const epsFromProfile = safe(p.eps);
  let eps = epsFromProfile !== 0 ? epsFromProfile : epsFromIncome;
  if (!eps && sharesOut > 0) eps = netIncome / sharesOut;

  const roe = totalEquity > 0 ? (netIncome / totalEquity) * 100 : 0;
  const operatingMargin = totalRevenue > 0 ? (operatingIncomeVal / totalRevenue) * 100 : 0;
  const fcfYield = marketCap > 0 ? (fcf / marketCap) * 100 : 0;
  const currentRatio = totalCurrentLiabilities > 0 ? totalCurrentAssets / totalCurrentLiabilities : 0;
  const debtToEquity = totalEquity > 0 ? (totalDebt / totalEquity) * 100 : 0;
  const netDebtEbitda = ebitda > 0 ? (totalDebt - cash) / ebitda : 0;
  const interestCoverage = interestExpense > 0 ? operatingIncomeVal / interestExpense : 100;

  // Revenue growth YoY
  let revenueGrowth = 0;
  if (Array.isArray(incomeArr) && incomeArr.length >= 2) {
    const revCurr = safe(incomeArr[0].revenue);
    const revPrev = safe(incomeArr[1].revenue);
    if (revPrev > 0) revenueGrowth = ((revCurr - revPrev) / revPrev) * 100;
  }

  const revenuePerShare = sharesOut > 0 ? totalRevenue / sharesOut : 0;
  const pegRatio = peRatio && revenueGrowth > 0 ? peRatio / revenueGrowth : null;

  // Momentum 3 mois
  const momentum3m = await calculateMomentum(symbol);

  return {
    ticker: symbol,
    name,
    industry: (p.industry as string) || "Unknown",
    sector: (p.sector as string) || "Unknown",
    description: (p.description as string) || "",
    currency: (p.currency as string) || "USD",
    currentPrice: price,
    marketCap,
    peRatio,
    pbRatio,
    pegRatio,
    eps,
    roe,
    operatingMargin,
    fcfYield,
    currentRatio,
    debtToEquity,
    netDebtEbitda,
    interestCoverage,
    revenueGrowth,
    revenuePerShare,
    momentum3m,
    totalDebt,
    totalAssets,
    interestIncome,
    illiquidAssets,
    currentAssets: totalCurrentAssets,
    totalRevenue,
  };
}

// ------------------------------------------------------------------
//  Momentum
// ------------------------------------------------------------------
async function calculateMomentum(symbol: string, days = 90): Promise<number> {
  try {
    const dateTo = new Date().toISOString().split("T")[0];
    const dateFrom = new Date(Date.now() - days * 86400000).toISOString().split("T")[0];

    const data = await fmpGet<unknown>("/stable/historical-price-eod/full", {
      symbol,
      from: dateFrom,
      to: dateTo,
    });

    const historical = Array.isArray(data)
      ? data
      : (data as { historical?: unknown[] })?.historical ?? [];

    if (historical.length < 2) return 0;

    const first = historical[0] as Record<string, number>;
    const last = historical[historical.length - 1] as Record<string, number>;
    const endPrice = first.close ?? first.adjClose ?? 0;
    const startPrice = last.close ?? last.adjClose ?? 0;

    return startPrice > 0 ? ((endPrice - startPrice) / startPrice) * 100 : 0;
  } catch {
    return 0;
  }
}

// ------------------------------------------------------------------
//  Historique des prix
// ------------------------------------------------------------------
export async function fetchPriceHistory(
  ticker: string,
  period = "1y"
): Promise<PricePoint[]> {
  const periodDays: Record<string, number> = {
    "3mo": 90,
    "6mo": 180,
    "1y": 365,
    "2y": 730,
    "5y": 1825,
  };
  const days = periodDays[period] ?? 365;
  const symbol = ticker.toUpperCase();

  try {
    const dateTo = new Date().toISOString().split("T")[0];
    const dateFrom = new Date(Date.now() - days * 86400000).toISOString().split("T")[0];

    const data = await fmpGet<unknown>("/stable/historical-price-eod/full", {
      symbol,
      from: dateFrom,
      to: dateTo,
    });

    const historical = Array.isArray(data)
      ? data
      : (data as { historical?: unknown[] })?.historical ?? [];

    if (!historical.length) return [];

    // Trier par date croissante
    const sorted = [...(historical as Record<string, unknown>[])].sort(
      (a, b) => new Date(a.date as string).getTime() - new Date(b.date as string).getTime()
    );

    // Calculer MA50
    const closes = sorted.map((d) => safe(d.close));
    const points: PricePoint[] = sorted.map((d, i) => {
      let ma50: number | null = null;
      if (i >= 49) {
        const slice = closes.slice(i - 49, i + 1);
        ma50 = slice.reduce((a, b) => a + b, 0) / 50;
      }
      return {
        date: d.date as string,
        close: safe(d.close),
        ma50,
      };
    });

    return points;
  } catch {
    return [];
  }
}

// ------------------------------------------------------------------
//  Recherche de symboles
// ------------------------------------------------------------------
export async function searchSymbols(query: string, maxResults = 10) {
  if (!query || query.length < 1) return [];

  const data = await fmpGet<Record<string, unknown>[]>("/stable/search-name", {
    query,
    limit: "30",
  });

  if (!Array.isArray(data)) return [];

  const FREE = new Set(["NASDAQ", "NYSE", "AMEX"]);
  const results: { symbol: string; name: string; exchange: string; currency: string }[] = [];

  for (const item of data) {
    const symbol = (item.symbol as string) || "";
    const name = (item.name as string) || symbol;
    const exchange = (item.exchange as string) || "";

    if (!symbol) continue;

    // Filtrer : uniquement les exchanges US gratuits
    if (!FREE.has(exchange)) continue;

    results.push({ symbol, name, exchange, currency: (item.currency as string) || "USD" });
    if (results.length >= maxResults) break;
  }

  return results;
}