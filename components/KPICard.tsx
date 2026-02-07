"use client";

import { Check, X } from "lucide-react";

interface KPICardProps {
  label: string;
  value: string;
  target: string;
  passed: boolean;
  delay?: number;
}

export default function KPICard({ label, value, target, passed, delay = 0 }: KPICardProps) {
  return (
    <div
      className="
        group relative overflow-hidden
        bg-mizan-card/60 backdrop-blur-md border border-white/[0.06]
        rounded-2xl p-5 flex flex-col justify-between
        transition-all duration-300
        hover:-translate-y-1 hover:border-mizan-green/20
        hover:shadow-[0_8px_32px_rgba(0,224,150,0.08)]
        opacity-0 animate-fade-up
      "
      style={{ animationDelay: `${delay}ms`, animationFillMode: "forwards" }}
    >
      {/* Status indicator */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-[11px] uppercase tracking-[1.5px] text-mizan-muted font-body">
          {label}
        </span>
        <div
          className={`
            w-6 h-6 rounded-full flex items-center justify-center
            ${passed
              ? "bg-mizan-green/15 text-mizan-green"
              : "bg-mizan-red/15 text-mizan-red"
            }
          `}
        >
          {passed ? <Check size={13} strokeWidth={3} /> : <X size={13} strokeWidth={3} />}
        </div>
      </div>

      {/* Value */}
      <div
        className={`
          font-display text-3xl font-bold tracking-tight mb-2
          ${passed
            ? "text-mizan-green drop-shadow-[0_0_12px_rgba(0,224,150,0.3)]"
            : "text-mizan-red drop-shadow-[0_0_12px_rgba(255,75,75,0.3)]"
          }
        `}
      >
        {value}
      </div>

      {/* Target */}
      <div className="text-xs text-mizan-muted/60 font-mono">
        Target: <span className="text-mizan-muted">{target}</span>
      </div>
    </div>
  );
}
