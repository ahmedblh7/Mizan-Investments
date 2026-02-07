import { NextRequest, NextResponse } from "next/server";
import { fetchPriceHistory } from "@/lib/fmp";

export async function GET(req: NextRequest) {
  const ticker = req.nextUrl.searchParams.get("ticker");
  const period = req.nextUrl.searchParams.get("period") ?? "1y";

  if (!ticker) {
    return NextResponse.json({ error: "Missing ticker" }, { status: 400 });
  }

  try {
    const data = await fetchPriceHistory(ticker, period);
    return NextResponse.json(data);
  } catch (e) {
    return NextResponse.json(
      { error: (e as Error).message },
      { status: 500 }
    );
  }
}
