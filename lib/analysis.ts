// ============================================================
// Analyse Engine — Shariah screening + Strategy evaluation
// Miroir exact de domain/shariah.py + domain/strategies.py
// ============================================================

import type {
  StockData,
  ShariahResult,
  StrategyResult,
  StrategyCheckResult,
  StrategyName,
} from "./types";
import {
  SHARIAH,
  STRATEGIES,
  SECTOR_BLACKLIST,
  KEYWORD_BLACKLIST,
  BOYCOTT_API_URL,
} from "./constants";

// ------------------------------------------------------------------
//  Shariah Analysis (AAOIFI standards)
// ------------------------------------------------------------------

async function checkBoycott(companyName: string): Promise<boolean> {
  try {
    const res = await fetch(`${BOYCOTT_API_URL}?q=${encodeURIComponent(companyName)}`, {
      signal: AbortSignal.timeout(3000),
    });
    if (!res.ok) return false;
    const data = await res.json();
    return Array.isArray(data) && data.length > 0;
  } catch {
    return false;
  }
}

function checkBusinessActivity(stock: StockData): { ok: boolean; issue: string } {
  const industry = stock.industry.toLowerCase();
  const sector = stock.sector.toLowerCase();
  const desc = stock.description.toLowerCase();

  for (const blacklisted of SECTOR_BLACKLIST) {
    if (industry.includes(blacklisted) || sector.includes(blacklisted)) {
      return { ok: false, issue: `Sector: ${blacklisted}` };
    }
  }

  for (const keyword of KEYWORD_BLACKLIST) {
    if (` ${desc} `.includes(` ${keyword} `)) {
      return { ok: false, issue: `Keyword: ${keyword}` };
    }
  }

  return { ok: true, issue: "OK" };
}

export async function analyzeShareah(stock: StockData): Promise<ShariahResult> {
  const failures: string[] = [];

  // 1. Business activity
  const activity = checkBusinessActivity(stock);
  if (!activity.ok) failures.push("Activity");

  // 2. Boycott
  const isBoycotted = await checkBoycott(stock.name);
  if (isBoycotted) failures.push("Boycott Listed");

  // 3. Interest income ratio
  const interestIncomeRatio =
    stock.totalRevenue > 0 ? (stock.interestIncome / stock.totalRevenue) * 100 : 0;
  if (interestIncomeRatio >= SHARIAH.maxInterestIncomeRatio) {
    failures.push(`Interest > ${SHARIAH.maxInterestIncomeRatio}%`);
  }

  // 4. Debt ratio
  const debtRatio =
    stock.totalAssets > 0 ? (stock.totalDebt / stock.totalAssets) * 100 : 0;
  if (debtRatio >= SHARIAH.maxDebtRatio) {
    failures.push(`Debt > ${SHARIAH.maxDebtRatio}%`);
  }

  // 5. Real assets ratio
  const illiquidAssetsRatio =
    stock.totalAssets > 0 ? (stock.illiquidAssets / stock.totalAssets) * 100 : 0;
  if (illiquidAssetsRatio <= SHARIAH.minRealAssetsRatio) {
    failures.push(`Real Assets < ${SHARIAH.minRealAssetsRatio}%`);
  }

  // 6. Liquidity check
  const isLiquidOk = stock.currentAssets < stock.marketCap;
  if (!isLiquidOk) failures.push("Cash > Cap");

  return {
    interestIncomeRatio,
    debtRatio,
    illiquidAssetsRatio,
    isLiquidOk,
    isActivityCompliant: activity.ok,
    activityIssue: activity.issue,
    isBoycotted,
    failures,
    isCompliant: failures.length === 0,
  };
}

// ------------------------------------------------------------------
//  Strategy evaluation
// ------------------------------------------------------------------

function fmt(v: number | null, suffix = ""): string {
  if (v === null || v === undefined) return "N/A";
  return `${v.toFixed(2)}${suffix}`;
}

function fmtPct(v: number): string {
  return `${v.toFixed(1)}%`;
}

function evaluateMizan(stock: StockData): StrategyResult {
  const cfg = STRATEGIES.Mizan;
  const checks: StrategyCheckResult[] = [];

  const isGrowth = stock.revenueGrowth > 10;
  const targetFcf = isGrowth ? cfg.fcfYieldGrowth : cfg.fcfYieldMature;
  checks.push({
    name: "FCF Yield",
    value: fmtPct(stock.fcfYield),
    target: `> ${targetFcf}% (${isGrowth ? "Growth" : "Mature"})`,
    passed: stock.fcfYield > targetFcf,
  });

  const pe = stock.peRatio && stock.peRatio > 0 ? stock.peRatio : 999;
  checks.push({
    name: "P/E",
    value: stock.peRatio && stock.peRatio > 0 ? fmt(stock.peRatio) : "N/A",
    target: `< ${cfg.maxPE}`,
    passed: pe < cfg.maxPE,
  });

  checks.push({
    name: "Op. Margin",
    value: fmtPct(stock.operatingMargin),
    target: `> ${cfg.minMargin}%`,
    passed: stock.operatingMargin > cfg.minMargin,
  });

  checks.push({
    name: "Net Debt/EBITDA",
    value: `${stock.netDebtEbitda.toFixed(2)}x`,
    target: `< ${cfg.maxNetDebtEbitda}x`,
    passed: stock.netDebtEbitda < cfg.maxNetDebtEbitda,
  });

  const passed = checks.filter((c) => c.passed).length;
  return {
    strategyName: "Mizan",
    checks,
    score: Math.round((passed / checks.length) * 100),
    passedCount: passed,
    totalCount: checks.length,
  };
}

function evaluateGraham(stock: StockData): StrategyResult {
  const cfg = STRATEGIES.Graham;
  const checks: StrategyCheckResult[] = [];

  const pe = stock.peRatio && stock.peRatio > 0 ? stock.peRatio : 999;
  checks.push({
    name: "P/E",
    value: stock.peRatio && stock.peRatio > 0 ? fmt(stock.peRatio) : "N/A",
    target: `< ${cfg.maxPE}`,
    passed: pe < cfg.maxPE,
  });

  checks.push({
    name: "Current Ratio",
    value: fmt(stock.currentRatio),
    target: `> ${cfg.minCurrentRatio}`,
    passed: stock.currentRatio > cfg.minCurrentRatio,
  });

  const de = stock.debtToEquity || 999;
  checks.push({
    name: "Debt/Equity",
    value: `${de.toFixed(0)}%`,
    target: `< ${cfg.maxDebtEquity}%`,
    passed: de < cfg.maxDebtEquity,
  });

  checks.push({
    name: "Interest Coverage",
    value: `${stock.interestCoverage.toFixed(1)}x`,
    target: `> ${cfg.minInterestCoverage}x`,
    passed: stock.interestCoverage > cfg.minInterestCoverage,
  });

  checks.push({
    name: "ROE",
    value: fmtPct(stock.roe),
    target: `> ${cfg.minROE}%`,
    passed: stock.roe > cfg.minROE,
  });

  const passed = checks.filter((c) => c.passed).length;
  return {
    strategyName: "Graham",
    checks,
    score: Math.round((passed / checks.length) * 100),
    passedCount: passed,
    totalCount: checks.length,
  };
}

function evaluateLynch(stock: StockData): StrategyResult {
  const cfg = STRATEGIES.Lynch;
  const checks: StrategyCheckResult[] = [];

  const peg = stock.pegRatio ?? 999;
  checks.push({
    name: "PEG",
    value: stock.pegRatio !== null ? fmt(stock.pegRatio) : "N/A",
    target: `< ${cfg.maxPEG}`,
    passed: peg < cfg.maxPEG,
  });

  checks.push({
    name: "Revenue Growth",
    value: fmtPct(stock.revenueGrowth),
    target: `> ${cfg.minGrowth}%`,
    passed: stock.revenueGrowth > cfg.minGrowth,
  });

  const de = stock.debtToEquity || 999;
  checks.push({
    name: "Debt/Equity",
    value: `${de.toFixed(0)}%`,
    target: `< ${cfg.maxDebtEquity}%`,
    passed: de < cfg.maxDebtEquity,
  });

  const pe = stock.peRatio && stock.peRatio > 0 ? stock.peRatio : 999;
  checks.push({
    name: "P/E",
    value: stock.peRatio && stock.peRatio > 0 ? fmt(stock.peRatio) : "N/A",
    target: `< ${cfg.maxPE}`,
    passed: pe < cfg.maxPE,
  });

  const passed = checks.filter((c) => c.passed).length;
  return {
    strategyName: "Lynch",
    checks,
    score: Math.round((passed / checks.length) * 100),
    passedCount: passed,
    totalCount: checks.length,
  };
}

export function evaluateStrategy(stock: StockData, strategy: StrategyName): StrategyResult {
  switch (strategy) {
    case "Graham":
      return evaluateGraham(stock);
    case "Lynch":
      return evaluateLynch(stock);
    default:
      return evaluateMizan(stock);
  }
}
