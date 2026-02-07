"use client";

import { useState, useEffect } from "react";

import {
  TrendingUp,
  TrendingDown,
  Shield,
  BarChart3,
  Target,
  Loader2,
} from "lucide-react";
import type { AnalysisResult, StrategyName } from "@/lib/types";
import VerdictBox from "./VerdictBox";
import ScoreCircle from "./ScoreCircle";
import KPICard from "./KPICard";
import PriceChart from "./PriceChart";

type TabId = "strategy" | "compliance" | "exit";

interface AnalysisPanelProps {
  ticker: string;
  strategy: StrategyName;
}

export default function AnalysisPanel({ ticker, strategy }: AnalysisPanelProps) {
  const [data, setData] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabId>("strategy");

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(`/api/analyze?ticker=${ticker}&strategy=${strategy}`)
      .then((r) => {
        if (!r.ok) throw new Error(`Error ${r.status}`);
        return r.json();
      })
      .then((d) => {
        if (d.error) throw new Error(d.error);
        setData(d);
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, [ticker, strategy]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-32 gap-4">
        <Loader2 size={32} className="text-mizan-green animate-spin" />
        <p className="text-mizan-muted font-body text-sm animate-pulse">
          Analyzing {ticker}...
        </p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="text-center py-20">
        <p className="text-mizan-red font-body">{error || "Unknown error"}</p>
      </div>
    );
  }

  const { stockData: s, shariahResult: sh, strategyResult: st } = data;

  // Price targets
  let tp1 = 0;
  let tp2 = 0;
  if (s.eps && s.eps > 0) {
    tp1 = s.eps * 15;
    tp2 = s.eps * 25;
  } else if (s.revenuePerShare > 0) {
    tp1 = s.revenuePerShare * 6;
    tp2 = s.revenuePerShare * 10;
  }

  const tabs: { id: TabId; label: string; icon: React.ReactNode }[] = [
    { id: "strategy", label: "Strategy Audit", icon: <BarChart3 size={14} /> },
    { id: "compliance", label: "Compliance", icon: <Shield size={14} /> },
    { id: "exit", label: "Exit Plan", icon: <Target size={14} /> },
  ];

  return (
    <div className="space-y-8 animate-fade-up" style={{ animationFillMode: "forwards" }}>
      {/* ── Header metrics ── */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricBlock label="Issuer" value={s.name} />
        <MetricBlock label="Spot Price" value={`${s.currentPrice.toFixed(2)} ${s.currency}`} />
        <MetricBlock
          label="Market Cap"
          value={s.marketCap > 1 ? `${(s.marketCap / 1e9).toFixed(1)}B` : "N/A"}
        />
        <MetricBlock
          label="Momentum (3M)"
          value={`${s.momentum3m.toFixed(2)}%`}
          trend={s.momentum3m}
        />
      </div>

      {/* ── Verdict + Score ── */}
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-6 items-center">
        <VerdictBox result={sh} />
        <ScoreCircle
          score={st.score}
          isCompliant={sh.isCompliant}
          title="Mizan Quality Score"
        />
      </div>

      {/* ── Tabs ── */}
      <div className="border-b border-white/[0.06]">
        <div className="flex gap-1 bg-white/[0.02] rounded-t-xl p-1.5">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`
                flex items-center gap-2 px-5 py-2.5 rounded-lg text-xs uppercase tracking-wider
                font-display font-semibold transition-all duration-200
                ${
                  activeTab === t.id
                    ? "bg-mizan-card text-mizan-gold border border-mizan-gold/20"
                    : "text-mizan-muted hover:text-mizan-silver hover:bg-white/[0.03]"
                }
              `}
            >
              {t.icon}
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* ── Tab content ── */}
      <div className="min-h-[300px]">
        {activeTab === "strategy" && (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {st.checks.map((c, i) => (
              <KPICard
                key={c.name}
                label={c.name}
                value={c.value}
                target={c.target}
                passed={c.passed}
                delay={i * 80}
              />
            ))}
          </div>
        )}

        {activeTab === "compliance" && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <KPICard
                label="Boycott"
                value={sh.isBoycotted ? "LISTED" : "SAFE"}
                target="Not Listed"
                passed={!sh.isBoycotted}
                delay={0}
              />
              <KPICard
                label="Activity"
                value={sh.isActivityCompliant ? "APPROVED" : "RESTRICTED"}
                target={s.industry.length > 18 ? `${s.industry.slice(0, 18)}…` : s.industry}
                passed={sh.isActivityCompliant}
                delay={80}
              />
            </div>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <KPICard
                label="Interest Inc."
                value={`${sh.interestIncomeRatio.toFixed(2)}%`}
                target="< 5%"
                passed={sh.interestIncomeRatio < 5}
                delay={160}
              />
              <KPICard
                label="Leverage"
                value={`${sh.debtRatio.toFixed(1)}%`}
                target="< 33%"
                passed={sh.debtRatio < 33}
                delay={240}
              />
              <KPICard
                label="Real Assets"
                value={`${sh.illiquidAssetsRatio.toFixed(1)}%`}
                target="> 20%"
                passed={sh.illiquidAssetsRatio > 20}
                delay={320}
              />
              <KPICard
                label="Liquidity"
                value={sh.isLiquidOk ? "PASS" : "FAIL"}
                target="Cash < Cap"
                passed={sh.isLiquidOk}
                delay={400}
              />
            </div>
          </div>
        )}

        {activeTab === "exit" && (
          <div className="space-y-6">
            <PriceChart
              ticker={ticker}
              tp1={tp1}
              tp2={tp2}
              currency={s.currency}
            />
            {tp1 > 0 && (
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-mizan-card/40 rounded-xl p-4 border border-white/[0.04]">
                  <p className="text-[10px] uppercase tracking-wider text-mizan-muted mb-1 font-body">
                    TP1 (Safety)
                  </p>
                  <p className="font-display text-xl font-bold text-mizan-gold">
                    {tp1.toFixed(2)} {s.currency}
                  </p>
                </div>
                <div className="bg-mizan-card/40 rounded-xl p-4 border border-white/[0.04]">
                  <p className="text-[10px] uppercase tracking-wider text-mizan-muted mb-1 font-body">
                    TP2 (Euphoria)
                  </p>
                  <p className="font-display text-xl font-bold text-mizan-red">
                    {tp2.toFixed(2)} {s.currency}
                  </p>
                </div>
                <div className="bg-mizan-card/40 rounded-xl p-4 border border-white/[0.04]">
                  <p className="text-[10px] uppercase tracking-wider text-mizan-muted mb-1 font-body">
                    Current
                  </p>
                  <p className="font-display text-xl font-bold text-mizan-green">
                    {s.currentPrice.toFixed(2)} {s.currency}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ------------------------------------------------------------------
//  Petit composant métrique d'en-tête
// ------------------------------------------------------------------
function MetricBlock({
  label,
  value,
  trend,
}: {
  label: string;
  value: string;
  trend?: number;
}) {
  return (
    <div className="space-y-1">
      <p className="text-[10px] uppercase tracking-wider text-mizan-muted font-body">
        {label}
      </p>
      <div className="flex items-center gap-2">
        <p className="font-display text-xl font-semibold text-white truncate">
          {value}
        </p>
        {trend !== undefined && (
          trend >= 0 ? (
            <TrendingUp size={16} className="text-mizan-green" />
          ) : (
            <TrendingDown size={16} className="text-mizan-red" />
          )
        )}
      </div>
    </div>
  );
}
