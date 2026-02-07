"use client";

import { useState, useEffect, useRef } from "react";
import { Search, Loader2 } from "lucide-react";
import type { SearchResult } from "@/lib/types";

interface SearchBarProps {
  onSelect: (symbol: string) => void;
}

export default function SearchBar({ onSelect }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<SearchResult | null>(null);
  const wrapperRef = useRef<HTMLDivElement>(null);

  // Debounced search
  useEffect(() => {
    if (query.length < 1) {
      setResults([]);
      setOpen(false);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        setResults(data);
        setOpen(true);
      } catch {
        setResults([]);
      }
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  // Click outside to close
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleSelect = (r: SearchResult) => {
    setSelected(r);
    setQuery(r.name);
    setOpen(false);
  };

  const handleScan = () => {
    if (selected) {
      onSelect(selected.symbol);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto" ref={wrapperRef}>
      {/* Search input row */}
      <div className="flex gap-3">
        <div className="relative flex-1">
          <Search
            size={18}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-mizan-muted"
          />
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelected(null);
            }}
            onFocus={() => results.length > 0 && setOpen(true)}
            placeholder="Search ticker or company name..."
            className="
              w-full bg-[#0F1218] text-white pl-11 pr-4 py-4 rounded-xl
              border border-white/[0.08] outline-none font-body text-sm
              placeholder:text-mizan-muted/50
              focus:border-mizan-green/30 focus:shadow-[0_0_20px_rgba(0,224,150,0.06)]
              transition-all duration-300
            "
          />
          {loading && (
            <Loader2
              size={16}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-mizan-green animate-spin"
            />
          )}
        </div>

        <button
          onClick={handleScan}
          disabled={!selected}
          className="
            px-8 py-4 rounded-xl font-display font-bold text-sm uppercase tracking-wider
            bg-gradient-to-r from-mizan-green to-[#00B075] text-mizan-bg
            disabled:opacity-30 disabled:cursor-not-allowed
            hover:shadow-[0_0_28px_rgba(0,224,150,0.3)]
            active:scale-[0.98]
            transition-all duration-300
          "
        >
          Initiate Scan
        </button>
      </div>

      {/* Dropdown */}
      {open && results.length > 0 && (
        <div
          className="
            mt-2 bg-[#12151C] border border-white/[0.06] rounded-xl
            overflow-hidden shadow-[0_16px_48px_rgba(0,0,0,0.5)]
            animate-fade-in
          "
        >
          {results.map((r, i) => (
            <button
              key={`${r.symbol}-${i}`}
              onClick={() => handleSelect(r)}
              className="
                w-full flex items-center justify-between px-5 py-3.5
                hover:bg-white/[0.04] transition-colors duration-150
                border-b border-white/[0.03] last:border-0
              "
            >
              <div className="flex items-center gap-3">
                <span className="font-mono text-mizan-green text-sm font-bold">
                  {r.symbol}
                </span>
                <span className="text-mizan-silver text-sm font-body truncate max-w-[280px]">
                  {r.name}
                </span>
              </div>
              <span className="text-[10px] text-mizan-muted/60 font-mono uppercase">
                {r.exchange}
              </span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
