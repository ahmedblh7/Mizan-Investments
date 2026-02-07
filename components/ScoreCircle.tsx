"use client";

import { useEffect, useRef, useState } from "react";

interface ScoreCircleProps {
  score: number;
  isCompliant: boolean;
  title?: string;
}

export default function ScoreCircle({
  score,
  isCompliant,
  title = "Mizan Quality Score",
}: ScoreCircleProps) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const ref = useRef<SVGCircleElement>(null);

  // Couleur selon score + conformité
  let color: string;
  let glow: string;

  if (!isCompliant) {
    color = "#FF4B4B";
    glow = "rgba(255,75,75,0.5)";
  } else if (score >= 70) {
    color = "#00E096";
    glow = "rgba(0,224,150,0.5)";
  } else if (score >= 50) {
    color = "#E0C38C";
    glow = "rgba(224,195,140,0.5)";
  } else {
    color = "#FF8C42";
    glow = "rgba(255,140,66,0.5)";
  }

  const circumference = 2 * Math.PI * 54; // r = 54
  const offset = circumference - (circumference * score) / 100;

  // Animation compteur
  useEffect(() => {
    let start = 0;
    const duration = 1500;
    const step = (ts: number) => {
      if (!start) start = ts;
      const progress = Math.min((ts - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      setAnimatedScore(Math.round(eased * score));
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [score]);

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative w-[160px] h-[160px] group cursor-pointer">
        <svg viewBox="0 0 120 120" className="-rotate-90 w-full h-full">
          {/* Track */}
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke="rgba(255,255,255,0.06)"
            strokeWidth="7"
          />
          {/* Progress */}
          <circle
            ref={ref}
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke={color}
            strokeWidth="7"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference}
            style={{
              filter: `drop-shadow(0 0 10px ${glow})`,
              transition: "filter 0.3s ease",
              animation: `score-arc 1.5s ease-out forwards`,
              // @ts-expect-error CSS custom property
              "--target-offset": `${offset}`,
            }}
          />
        </svg>

        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className="font-display text-5xl font-bold leading-none transition-all duration-300 group-hover:scale-110"
            style={{ color, textShadow: `0 0 24px ${glow}` }}
          >
            {animatedScore}
          </span>
          <span className="text-mizan-muted text-xs font-mono mt-1">/ 100</span>
        </div>
      </div>

      <span className="text-[11px] uppercase tracking-[2px] text-mizan-muted font-body">
        {title}
      </span>

      <style jsx>{`
        @keyframes score-arc {
          0% {
            stroke-dashoffset: ${circumference};
          }
          100% {
            stroke-dashoffset: ${offset};
          }
        }
        circle[ref] {
          animation: score-arc 1.5s ease-out forwards;
        }
      `}</style>
    </div>
  );
}
