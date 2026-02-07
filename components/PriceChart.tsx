"use client";

import { useEffect, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import type { PricePoint } from "@/lib/types";

interface PriceChartProps {
  ticker: string;
  tp1: number;
  tp2: number;
  currency: string;
}

export default function PriceChart({ ticker, tp1, tp2, currency }: PriceChartProps) {
  const [data, setData] = useState<PricePoint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/price-history?ticker=${ticker}&period=1y`)
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [ticker]);

  if (loading) {
    return (
      <div className="h-[400px] flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-mizan-green/30 border-t-mizan-green rounded-full animate-spin" />
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="h-[400px] flex items-center justify-center text-mizan-muted font-body">
        Insufficient data for chart.
      </div>
    );
  }

  // Format date for axis
  const formatted = data.map((d) => ({
    ...d,
    label: new Date(d.date).toLocaleDateString("en", { month: "short", day: "numeric" }),
  }));

  return (
    <div className="w-full h-[400px] opacity-0 animate-fade-up" style={{ animationDelay: "300ms", animationFillMode: "forwards" }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={formatted} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#00E096" stopOpacity={0.2} />
              <stop offset="100%" stopColor="#00E096" stopOpacity={0} />
            </linearGradient>
          </defs>

          <XAxis
            dataKey="label"
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 10, fill: "#6E7687", fontFamily: "JetBrains Mono" }}
            interval="preserveStartEnd"
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 10, fill: "#6E7687", fontFamily: "JetBrains Mono" }}
            domain={["auto", "auto"]}
            width={60}
            tickFormatter={(v) => `${v.toFixed(0)}`}
          />

          <Tooltip
            contentStyle={{
              background: "#1C202B",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: 12,
              fontFamily: "DM Sans",
              fontSize: 13,
            }}
            formatter={(value: number, name: string) => [
              `${value.toFixed(2)} ${currency}`,
              name === "close" ? "Price" : "MA50",
            ]}
            labelFormatter={(label) => label}
          />

          {/* TP lines */}
          {tp1 > 0 && (
            <ReferenceLine
              y={tp1}
              stroke="#E0C38C"
              strokeDasharray="6 4"
              strokeOpacity={0.6}
              label={{
                value: "TP1",
                fill: "#E0C38C",
                fontSize: 11,
                fontFamily: "JetBrains Mono",
                position: "right",
              }}
            />
          )}
          {tp2 > 0 && (
            <ReferenceLine
              y={tp2}
              stroke="#FF4B4B"
              strokeDasharray="6 4"
              strokeOpacity={0.6}
              label={{
                value: "TP2",
                fill: "#FF4B4B",
                fontSize: 11,
                fontFamily: "JetBrains Mono",
                position: "right",
              }}
            />
          )}

          {/* MA50 */}
          <Area
            type="monotone"
            dataKey="ma50"
            stroke="#6E7687"
            strokeWidth={1}
            strokeOpacity={0.4}
            fill="none"
            dot={false}
            connectNulls={false}
          />

          {/* Price */}
          <Area
            type="monotone"
            dataKey="close"
            stroke="#00E096"
            strokeWidth={2}
            fill="url(#priceGradient)"
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
