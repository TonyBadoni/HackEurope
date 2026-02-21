import React from 'react';
import { Shield, Zap, Lock, Globe, Terminal } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="bg-zinc-950 border border-zinc-900 p-6 rounded-xl hover:border-zinc-800 transition-colors group">
    <div className="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-blue-500/20 transition-colors">
      <Icon className="text-blue-500" size={24} />
    </div>
    <h3 className="text-white font-semibold mb-2">{title}</h3>
    <p className="text-zinc-500 text-sm leading-relaxed">{description}</p>
  </div>
);

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-64px)] p-8 text-center bg-zinc-950/20">
      <div className="max-w-4xl w-full">
        {/* Hero Section */}
        <div className="mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-500 text-xs font-bold uppercase tracking-wider mb-6 animate-pulse">
            <Lock size={12} />
            Secure by Design
          </div>
          <h1 className="text-6xl font-black text-white mb-6 tracking-tight">
            Pen Test <span className="text-blue-600">Agent</span>
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto leading-relaxed">
            A suite of agents for affordable security. Automate your vulnerability discovery and remediation with AI-powered workflows.
          </p>
          <div className="mt-10 flex items-center justify-center gap-4">
            <button className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold transition-all shadow-lg shadow-blue-500/20">
              Get Started
            </button>
            <button className="px-8 py-3 bg-zinc-900 hover:bg-zinc-800 text-white border border-zinc-800 rounded-lg font-bold transition-all">
              Documentation
            </button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
          <FeatureCard 
            icon={Shield} 
            title="Automated Pentesting" 
            description="Our agents perform continuous scanning and penetration testing on your linked codebases." 
          />
          <FeatureCard 
            icon={Zap} 
            title="Real-time Detection" 
            description="SSE-powered visualization allows you to see every step of the agent's logic as it happens." 
          />
          <FeatureCard 
            icon={Terminal} 
            title="AI Fixer" 
            description="Don't just find bugs - fix them. Our Fixer agent generates PRs to remediate vulnerabilities instantly." 
          />
        </div>

        {/* Footer info */}
        <div className="mt-20 flex items-center justify-center gap-12 border-t border-zinc-900 pt-12">
            <div className="text-center">
                <p className="text-white font-bold text-2xl">99.9%</p>
                <p className="text-zinc-500 text-xs uppercase tracking-widest mt-1">Accuracy</p>
            </div>
            <div className="text-center">
                <p className="text-white font-bold text-2xl">24/7</p>
                <p className="text-zinc-500 text-xs uppercase tracking-widest mt-1">Monitoring</p>
            </div>
            <div className="text-center">
                <p className="text-white font-bold text-2xl">&lt;1 min</p>
                <p className="text-zinc-500 text-xs uppercase tracking-widest mt-1">Response</p>
            </div>
        </div>
      </div>
    </div>
  );
}
