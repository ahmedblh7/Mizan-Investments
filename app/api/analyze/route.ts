import { NextRequest, NextResponse } from "next/server";
import { fetchStockData } from "@/lib/fmp";
import { analyzeShareah, evaluateStrategy } from "@/lib/analysis";
import type { StrategyName, AnalysisResult } from "@/lib/types";

export async function GET(req: NextRequest) {
  const ticker = req.nextUrl.searchParams.get("ticker");
  const strategy = (req.nextUrl.searchParams.get("strategy") ?? "Mizan") as StrategyName;

  if (!ticker) {
    return NextResponse.json({ error: "Missing ticker" }, { status: 400 });
  }

  try {
    const stockData = await fetchStockData(ticker);
    const shariahResult = await analyzeShareah(stockData);
    const strategyResult = evaluateStrategy(stockData, strategy);

    const result: AnalysisResult = {
      stockData,
      shariahResult,
      strategyResult,
    };

    return NextResponse.json(result);
  } catch (e) {
    return NextResponse.json(
      { error: (e as Error).message },
      { status: 500 }
    );
  }
}
