import React, { useState, useEffect, useRef } from 'react';
import { 
  Activity, 
  Zap, 
  Layers, 
  ChevronRight,
  Wifi,
  Radio,
  Search,
  Database,
  Cpu
} from 'lucide-react';

const Panel = ({ title, icon: Icon, children, color, glowColor }) => (
  <div className={`bg-zinc-950 border border-zinc-900 rounded-xl flex flex-col h-full shadow-lg overflow-hidden group/panel`}>
    <div className="px-5 py-4 border-b border-zinc-900 flex justify-between items-center bg-zinc-900/20">
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg ${color} bg-opacity-20 relative`}>
          <div className={`absolute inset-0 rounded-lg ${glowColor} opacity-0 group-hover/panel:opacity-40 blur-md transition-opacity duration-500`} />
          <Icon className={`${color.replace('bg-', 'text-').replace('-600', '-400').replace('-500', '-400')} relative z-10`} size={18} />
        </div>
        <h3 className="font-bold text-white tracking-tight group-hover/panel:text-blue-400 transition-colors duration-300">{title}</h3>
      </div>
      <div className="flex gap-1.5">
        <div className="w-1.5 h-1.5 rounded-full bg-zinc-800 group-hover/panel:bg-zinc-600 transition-colors" />
        <div className="w-1.5 h-1.5 rounded-full bg-zinc-800 group-hover/panel:bg-zinc-600 transition-colors" />
      </div>
    </div>
    <div className="flex-grow overflow-auto p-4 custom-scrollbar bg-black/20">
      {children}
    </div>
  </div>
);

const LogItem = ({ data }) => (
  <div className="mb-2 p-3 font-mono text-[11px] bg-black/40 rounded border border-zinc-800/50 hover:border-zinc-700 hover:bg-zinc-900/40 transition-all duration-200 group/item">
    <div className="flex justify-between mb-1">
      <span className="text-blue-400/80 group-hover/item:text-blue-400">[{data?.timestamp}]</span>
      <span className="text-zinc-600 group-hover/item:text-zinc-500 flex items-center gap-1">
        <Radio size={10} className="animate-pulse" />
        {data?.eventid}
      </span>
    </div>
    <div className="text-zinc-400 group-hover/item:text-zinc-200 break-all">{data?.message}</div>
    {data?.src_ip && (
      <div className="text-zinc-500 mt-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="px-1.5 py-0.5 bg-zinc-900 rounded text-[9px] uppercase tracking-wider font-bold text-zinc-400">IP</span>
          <span className="group-hover/item:text-zinc-300">{data?.src_ip}</span>
        </div>
        <ChevronRight size={12} className="opacity-0 group-hover/item:opacity-100 transition-opacity text-blue-500" />
      </div>
    )}
  </div>
);

const RiskItem = ({ data }) => (
  <div className="mb-3 p-3 bg-zinc-900/20 rounded-lg flex items-center gap-4 border border-zinc-900 group hover:border-zinc-700 hover:bg-zinc-800/30 transition-all duration-300">
    <div className="relative w-12 h-12 flex-shrink-0">
      <svg className="w-12 h-12 -rotate-90">
        <circle
          cx="24"
          cy="24"
          r="18"
          stroke="currentColor"
          strokeWidth="3.5"
          fill="transparent"
          className="text-zinc-900"
        />
        <circle
          cx="24"
          cy="24"
          r="18"
          stroke="currentColor"
          strokeWidth="3.5"
          fill="transparent"
          strokeDasharray={2 * Math.PI * 18}
          strokeDashoffset={2 * Math.PI * 18 * (1 - (data?.score || 0) / 100)}
          style={{ color: data?.colour }}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <span className="absolute inset-0 flex items-center justify-center text-[10px] font-black text-white group-hover:scale-110 transition-transform">
        {data?.score}
      </span>
      <div className="absolute -top-1 -right-1">
        <div className={`p-1 rounded-full shadow-lg`} style={{ backgroundColor: data?.colour }}>
          <Zap size={8} className="text-white" />
        </div>
      </div>
    </div>
    <div className="flex-grow min-w-0">
      <div className="flex items-center justify-between gap-2 mb-1">
        <div className="flex items-center gap-1.5">
          <Activity size={10} style={{ color: data?.colour }} className="animate-pulse" />
          <span className="text-[10px] font-black uppercase tracking-tighter" style={{ color: data?.colour }}>
            {data?.severity}
          </span>
        </div>
        <span className="text-[9px] text-zinc-600 font-mono italic truncate">{data?.session}</span>
      </div>
      <h4 className="text-xs font-bold text-zinc-300 truncate group-hover:text-white transition-colors uppercase tracking-tight">{data?.eventid}</h4>
      <div className="text-[9px] text-zinc-600 mt-1 flex items-center gap-1">
        <Wifi size={8} />
        {data?.src_ip}
      </div>
    </div>
  </div>
);

const AttackChainItem = ({ data }) => (
  <div className="mb-4 bg-zinc-950/40 border border-zinc-900 rounded-xl overflow-hidden shadow-xl group/chain hover:border-zinc-700 transition-all duration-500">
    <div className="p-4 border-b border-zinc-900 flex justify-between items-start bg-zinc-900/20 group-hover/chain:bg-zinc-900/40 transition-colors">
      <div>
        <div className="flex items-center gap-2 mb-1.5">
          <div className="relative">
            <span className={`absolute inset-0 rounded-full ${data?.severity === 'critical' ? 'bg-red-500/50' : 'bg-orange-500/50'} animate-ping opacity-20`} />
            <span className={`relative block w-2 h-2 rounded-full ${data?.severity === 'critical' ? 'bg-red-500' : 'bg-orange-500'}`} />
          </div>
          <h4 className="text-[11px] font-black text-white uppercase tracking-tighter group-hover/chain:text-blue-400 transition-colors">{data?.chain_id}</h4>
        </div>
        <p className="text-[10px] text-zinc-500 font-mono flex items-center gap-1.5">
          <Search size={10} />
          <span>Attacker:</span>
          <span className="text-zinc-200">{data?.attacker_ip}</span>
        </p>
      </div>
      <div className="text-right">
        <span className="text-[9px] text-zinc-600 block mb-1 font-mono uppercase tracking-widest">{data?.detected_at}</span>
        <div className={`text-[9px] font-bold uppercase px-2 py-0.5 rounded-full border ${data?.severity === 'critical' ? 'bg-red-500/5 border-red-500/30 text-red-400' : 'bg-orange-500/5 border-orange-500/30 text-orange-400'}`}>
          {data?.severity}
        </div>
      </div>
    </div>
    <div className="p-4 bg-black/10">
      <div className="space-y-4 relative before:absolute before:left-[7px] before:top-2 before:bottom-2 before:w-[1px] before:bg-zinc-800 before:bg-gradient-to-b before:from-zinc-800 before:via-zinc-700 before:to-zinc-800">
        {data?.steps?.map((step) => (
          <div key={step.step} className="flex gap-4 relative group/step">
             <div className={`w-3.5 h-3.5 rounded-full border-2 bg-zinc-950 border-zinc-800 flex-shrink-0 z-10 transition-all duration-300 group-hover/step:border-blue-500 group-hover/step:scale-110 ${step.step === data?.steps?.length ? 'border-orange-500' : ''}`} />
             <div className="min-w-0 flex-grow">
               <div className="text-[10px] font-bold text-zinc-300 leading-none mb-1 group-hover/step:text-white transition-colors">{step.desc}</div>
               <div className="text-[9px] text-zinc-500 font-mono truncate italic">{step.event}</div>
             </div>
          </div>
        ))}
      </div>
      <div className="mt-5 pt-4 border-t border-zinc-900 flex items-center justify-between">
        <div className="flex flex-col">
          <div className="text-[8px] font-black text-zinc-600 uppercase tracking-[0.2em] mb-1">MITRE ATT&CK</div>
          <div className="text-[10px] text-blue-400/80 font-medium leading-relaxed italic group-hover/chain:text-blue-400 transition-colors uppercase tracking-tight">{data?.technique}</div>
        </div>
        <Layers size={14} className="text-zinc-800 group-hover/chain:text-emerald-500/50 transition-colors" />
      </div>
    </div>
  </div>
);

export default function ClassificationDashboard() {
  const [liveLogs, setLiveLogs] = useState([]);
  const [riskScores, setRiskScores] = useState([]);
  const [attackChains, setAttackChains] = useState([]);

  const eventSourcesRef = useRef([]);

  useEffect(() => {
    const endpoints = [
      { url: '/api/v1/dashboard/live-logs', setter: setLiveLogs, limit: 20 },
      { url: '/api/v1/dashboard/risk-scores', setter: setRiskScores, limit: 15 },
      { url: '/api/v1/dashboard/attack-chains', setter: setAttackChains, limit: 5 }
    ];

    endpoints.forEach(({ url, setter, limit }) => {
      try {
          const source = new EventSource(`http://localhost:8000${url}`);
          source.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              setter(prev => [data, ...prev].slice(0, limit));
            } catch (err) {
              console.error("Error parsing SSE data:", err);
            }
          };
          source.onerror = (err) => {
              console.error(`SSE Error for ${url}:`, err);
              source.close();
          };
          eventSourcesRef.current.push(source);
      } catch (e) {
          console.error(`Failed to create EventSource for ${url}:`, e);
      }
    });

    return () => {
      eventSourcesRef.current.forEach(source => {
          if (source && typeof source.close === 'function') {
              source.close();
          }
      });
      eventSourcesRef.current = [];
    };
  }, []);

  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 grid-rows-2 gap-6 h-full p-6 animate-in fade-in duration-1000 slide-in-from-bottom-2">
      <Panel title="Real-time Feed" icon={Cpu} color="bg-blue-600" glowColor="bg-blue-500">
        {liveLogs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-zinc-500 italic text-[10px] gap-4 tracking-widest uppercase font-black">
            <Radio className="animate-pulse text-blue-500" size={32} />
            Establishing Uplink...
          </div>
        ) : (
          liveLogs.map((log, i) => <LogItem key={i} data={log} />)
        )}
      </Panel>

      <Panel title="Live Diagnostics" icon={Activity} color="bg-orange-600" glowColor="bg-orange-500">
        {riskScores.length === 0 ? (
           <div className="flex flex-col items-center justify-center h-full text-zinc-500 italic text-[10px] gap-4 tracking-widest uppercase font-black">
             <Zap className="animate-pulse text-orange-500" size={32} />
             Calculating Risk...
           </div>
        ) : (
          riskScores.map((score, i) => <RiskItem key={i} data={score} />)
        )}
      </Panel>

      <div className="xl:col-span-2">
        <Panel title="Attack Correlation" icon={Database} color="bg-emerald-600" glowColor="bg-emerald-500">
          {attackChains.length === 0 ? (
             <div className="flex flex-col items-center justify-center h-full text-zinc-500 italic text-[10px] gap-4 tracking-widest uppercase font-black">
               <Layers className="text-emerald-500" size={32} />
               Connecting Nodes...
             </div>
          ) : (
            attackChains.map((chain, i) => <AttackChainItem key={i} data={chain} />)
          )}
        </Panel>
      </div>
    </div>
  );
}
