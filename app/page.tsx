"use client";

import { useState } from "react";
import { Search, ArrowRight, ChevronRight, Shield, BarChart3, Target, Twitter, Youtube, Linkedin } from "lucide-react";
import AnalysisPanel from "@/components/AnalysisPanel";
import type { StrategyName, SearchResult } from "@/lib/types";

export default function HomePage() {
  const [ticker, setTicker] = useState<string | null>(null);
  const [strategy, setStrategy] = useState<StrategyName>("Mizan");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedResult, setSelectedResult] = useState<SearchResult | null>(null);

  // Search handler with debounce
  const handleSearch = async (value: string) => {
    setQuery(value);
    setSelectedResult(null);
    
    if (value.length < 1) {
      setResults([]);
      setShowDropdown(false);
      return;
    }

    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(value)}`);
      const data = await res.json();
      setResults(data);
      setShowDropdown(true);
    } catch {
      setResults([]);
    }
  };

  const handleSelect = (result: SearchResult) => {
    setSelectedResult(result);
    setQuery(`${result.symbol} - ${result.name}`);
    setShowDropdown(false);
  };

  const handleAnalyze = () => {
    if (selectedResult) {
      setTicker(selectedResult.symbol);
    }
  };

  // Si une analyse est en cours, afficher le panel
  if (ticker) {
    return (
      <div className="min-h-screen bg-[#0a0d10]">
        <Nav strategy={strategy} setStrategy={setStrategy} />
        <main className="max-w-7xl mx-auto px-6 py-8">
          <button 
            onClick={() => setTicker(null)}
            className="mb-6 text-mizan-green hover:text-mizan-green/80 flex items-center gap-2 text-sm font-medium transition-colors"
          >
            ← Retour à l'accueil
          </button>
          <AnalysisPanel ticker={ticker} strategy={strategy} />
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0d10]">
      <Nav strategy={strategy} setStrategy={setStrategy} />
      
      {/* Hero Section */}
      <section className="pt-20 pb-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight mb-6">
            Votre patrimoine, géré
            <br />
            <span className="text-mizan-green">avec excellence.</span>
          </h1>
          <p className="text-mizan-silver/70 text-lg mb-10">
            Gérez. Analysez. Dominez.
          </p>

          {/* Search Bar */}
          <div className="relative max-w-2xl mx-auto">
            <div className="flex gap-3">
              <div className="relative flex-1">
                <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-mizan-muted" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => handleSearch(e.target.value)}
                  placeholder="Rechercher un actif (ex: AAPL, TotalEnergies...)"
                  className="w-full bg-[#111518] text-white pl-11 pr-4 py-4 rounded-xl border border-white/10 outline-none text-sm placeholder:text-mizan-muted/50 focus:border-mizan-green/40 transition-all"
                />
                
                {/* Dropdown */}
                {showDropdown && results.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-2 bg-[#111518] border border-white/10 rounded-xl overflow-hidden z-50 shadow-2xl">
                    {results.map((r, i) => (
                      <button
                        key={`${r.symbol}-${i}`}
                        onClick={() => handleSelect(r)}
                        className="w-full flex items-center justify-between px-4 py-3 hover:bg-white/5 transition-colors border-b border-white/5 last:border-0"
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-mizan-green font-mono font-bold text-sm">{r.symbol}</span>
                          <span className="text-mizan-silver text-sm truncate">{r.name}</span>
                        </div>
                        <span className="text-[10px] text-mizan-muted font-mono">{r.exchange}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
              
              <button
                onClick={handleAnalyze}
                disabled={!selectedResult}
                className="px-6 py-4 bg-mizan-green text-[#0a0d10] font-bold text-sm rounded-xl hover:bg-mizan-green/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center gap-2"
              >
                LANCER L'ANALYSE
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-4">
            L'Analyse Financière, <span className="text-mizan-green">Réinventée.</span>
          </h2>
          <p className="text-mizan-silver/60 text-center mb-12 max-w-2xl mx-auto">
            Une approche rigoureuse combinant analyse fondamentale et conformité éthique Sharia pour des investissements responsables.
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            <FeatureCard
              icon={<BarChart3 className="text-mizan-green" size={24} />}
              title="Analyse Fondamentale"
              description="Analyse financière approfondie utilisant les méthodologies éprouvées de Graham, Lynch et notre stratégie Mizan propriétaire."
            />
            <FeatureCard
              icon={<Shield className="text-mizan-green" size={24} />}
              title="Conformité Éthique & Sharia"
              description="Screening conforme aux standards AAOIFI : ratio de dette, revenus d'intérêts, activités illicites et actifs réels."
              highlighted
            />
            <FeatureCard
              icon={<Target className="text-mizan-green" size={24} />}
              title="Stratégies d'Excellence"
              description="Trois stratégies d'investissement éprouvées pour identifier les meilleures opportunités selon votre profil."
            />
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-6 bg-[#080a0d]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-bold text-white text-center mb-12">
            Validé par des Investisseurs Exigeants.
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <TestimonialCard
              quote="Être éthique tout en prenant une marge, préférer votre foi aux rendements suspects. Obtenir cette suite ici des investissements."
              author="Rahul Maouit"
              role="Analyste"
            />
            <TestimonialCard
              quote="L'outil examine rigoureusement dans mes critères excellence. Elle m'offre clairement une vue privée. Je considère maintenant mes investissements Exigeants."
              author="Sarah Alaoui"
              role="Portfolio Manager"
            />
            <TestimonialCard
              quote="Mais mon but ne doit tant que l'étroitement par vrai business les bases."
              author="Youssef Benali"
              role="Investisseur Privé"
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-white/5">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-mizan-green/20 rounded-lg flex items-center justify-center">
                  <span className="text-mizan-green font-bold">⚖</span>
                </div>
                <span className="font-bold text-white">MIZAN INVESTMENTS</span>
              </div>
              <p className="text-sm text-mizan-muted">
                Analyse financière éthique et conforme Sharia.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">STRATÉGIES</h4>
              <ul className="space-y-2 text-sm text-mizan-muted">
                <li className="hover:text-mizan-green cursor-pointer transition-colors">Mizan Strategy</li>
                <li className="hover:text-mizan-green cursor-pointer transition-colors">Graham Value</li>
                <li className="hover:text-mizan-green cursor-pointer transition-colors">Lynch Growth</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">À PROPOS</h4>
              <ul className="space-y-2 text-sm text-mizan-muted">
                <li className="hover:text-mizan-green cursor-pointer transition-colors">Notre Mission</li>
                <li className="hover:text-mizan-green cursor-pointer transition-colors">Méthodologie</li>
                <li className="hover:text-mizan-green cursor-pointer transition-colors">Contact</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">PARTENAIRES</h4>
              <div className="flex gap-4 text-mizan-muted">
                <span className="text-sm font-semibold">Bloomberg</span>
                <span className="text-sm font-semibold">Reuters</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center justify-between pt-8 border-t border-white/5">
            <p className="text-sm text-mizan-muted">© MIZAN INVESTMENTS 2024</p>
            <div className="flex gap-4">
              <Twitter size={18} className="text-mizan-muted hover:text-mizan-green cursor-pointer transition-colors" />
              <Youtube size={18} className="text-mizan-muted hover:text-mizan-green cursor-pointer transition-colors" />
              <Linkedin size={18} className="text-mizan-muted hover:text-mizan-green cursor-pointer transition-colors" />
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Navigation Component
function Nav({ strategy, setStrategy }: { strategy: StrategyName; setStrategy: (s: StrategyName) => void }) {
  return (
    <nav className="border-b border-white/5 bg-[#0a0d10]/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-mizan-green/20 rounded-lg flex items-center justify-center">
            <span className="text-mizan-green font-bold">⚖</span>
          </div>
          <span className="font-bold text-white tracking-tight">MIZAN INVESTMENTS</span>
        </div>

        <div className="hidden md:flex items-center gap-8 text-sm">
          <button 
            onClick={() => setStrategy("Mizan")}
            className={`transition-colors ${strategy === "Mizan" ? "text-mizan-green" : "text-mizan-muted hover:text-white"}`}
          >
            STRATÉGIES
          </button>
          <span className="text-mizan-muted hover:text-white cursor-pointer transition-colors">À PROPOS</span>
          <span className="text-mizan-muted hover:text-white cursor-pointer transition-colors">SERVICES</span>
          <span className="text-mizan-muted hover:text-white cursor-pointer transition-colors">CONTACT</span>
        </div>
      </div>
    </nav>
  );
}

// Feature Card Component
function FeatureCard({ icon, title, description, highlighted = false }: { 
  icon: React.ReactNode; 
  title: string; 
  description: string;
  highlighted?: boolean;
}) {
  return (
    <div className={`p-6 rounded-2xl border transition-all hover:-translate-y-1 ${
      highlighted 
        ? "bg-mizan-green/10 border-mizan-green/30" 
        : "bg-[#111518] border-white/5 hover:border-white/10"
    }`}>
      <div className="w-12 h-12 bg-mizan-green/10 rounded-xl flex items-center justify-center mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-bold text-white mb-2">{title}</h3>
      <p className="text-sm text-mizan-silver/70 leading-relaxed mb-4">{description}</p>
      <button className="text-mizan-green text-sm font-medium flex items-center gap-1 hover:gap-2 transition-all">
        En savoir plus <ChevronRight size={14} />
      </button>
    </div>
  );
}

// Testimonial Card Component
function TestimonialCard({ quote, author, role }: { quote: string; author: string; role: string }) {
  return (
    <div className="p-6 bg-[#111518] rounded-2xl border border-white/5">
      <p className="text-mizan-silver/80 text-sm leading-relaxed mb-6">"{quote}"</p>
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-mizan-green/20 rounded-full flex items-center justify-center">
          <span className="text-mizan-green font-bold text-sm">{author[0]}</span>
        </div>
        <div>
          <p className="text-white font-medium text-sm">{author}</p>
          <p className="text-mizan-muted text-xs">{role}</p>
        </div>
      </div>
    </div>
  );
}
