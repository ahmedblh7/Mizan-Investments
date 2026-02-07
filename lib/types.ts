export interface StockData {
  ticker: string; name: string; industry: string; sector: string;
  description: string; currency: string;
  currentPrice: number; marketCap: number;
  peRatio: number | null; pbRatio: number | null;
  pegRatio: number | null; eps: number | null;
  roe: number; operatingMargin: number; fcfYield: number;
  currentRatio: number; debtToEquity: number;
  netDebtEbitda: number; interestCoverage: number;
  revenueGrowth: number; revenuePerShare: number; momentum3m: number;
  totalDebt: number; totalAssets: number; interestIncome: number;
  illiquidAssets: number; currentAssets: number; totalRevenue: number;
}
export interface StrategyCheck {
  name: string; value: string; target: string; passed: boolean;
}
export interface StrategyResult {
  strategyName: string; checks: StrategyCheck[];
  score: number; passedCount: number; totalCount: number;
}
export interface ShariahResult {
  interestIncomeRatio: number; debtRatio: number;
  illiquidAssetsRatio: number; isLiquidOk: boolean;
  isActivityCompliant: boolean; activityIssue: string;
  isBoycotted: boolean; failures: string[]; isCompliant: boolean;
}
export interface PricePoint { date: string; close: number; ma50?: number; }
export interface AnalysisResult {
  stock: StockData; shariah: ShariahResult;
  strategy: StrategyResult; priceHistory: PricePoint[];
  exitPlan: { tp1: number; tp2: number };
}
export interface SearchResult {
  symbol: string; name: string; exchange: string; currency: string;
}
export type StrategyName = "Mizan" | "Graham" | "Lynch";
