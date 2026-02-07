import { NextRequest, NextResponse } from "next/server";
import { searchSymbols } from "@/lib/fmp";

export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get("q") ?? "";

  if (q.length < 1) {
    return NextResponse.json([]);
  }

  try {
    const results = await searchSymbols(q);
    return NextResponse.json(results);
  } catch (e) {
    return NextResponse.json(
      { error: (e as Error).message },
      { status: 500 }
    );
  }
}