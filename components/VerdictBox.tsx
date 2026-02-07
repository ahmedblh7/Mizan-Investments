"use client";

import { ShieldCheck, ShieldX } from "lucide-react";
import type { ShariahResult } from "@/lib/types";

export default function VerdictBox({ result }: { result: ShariahResult }) {
  const compliant = result.isCompliant;

  return (
    <div
      className={`
        relative overflow-hidden rounded-2xl border p-6
        flex items-center gap-5 transition-all duration-500
        ${
          compliant
            ? "border-mizan-green/30 bg-gradient-to-r from-mizan-green/10 to-transparent"
            : "border-mizan-red/30 bg-gradient-to-r from-mizan-red/10 to-transparent"
        }
      `}
    >
      {/* Glow effect */}
      <div
        className={`
          absolute -left-10 top-1/2 -translate-y-1/2 w-32 h-32 rounded-full blur-3xl opacity-20
          ${compliant ? "bg-mizan-green" : "bg-mizan-red"}
        `}
      />

      <div className="relative z-10">
        {compliant ? (
          <ShieldCheck size={44} className="text-mizan-green drop-shadow-[0_0_16px_rgba(0,224,150,0.5)]" />
        ) : (
          <ShieldX size={44} className="text-mizan-red drop-shadow-[0_0_16px_rgba(255,75,75,0.5)]" />
        )}
      </div>

      <div className="relative z-10">
        <h3
          className={`font-display text-xl font-bold tracking-tight ${
            compliant ? "text-mizan-green" : "text-mizan-red"
          }`}
        >
          {compliant ? "COMPLIANT ASSET" : "NON-COMPLIANT"}
        </h3>
        <p className="text-mizan-silver/70 text-sm mt-1 font-body">
          {compliant
            ? "Meets quantitative Shariah standards."
            : `Failed checks: ${result.failures.join(", ")}`}
        </p>
      </div>
    </div>
  );
}
