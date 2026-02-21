import React, { useState } from 'react';
import { Shield, MessageSquare, ChevronDown, Save, Wand2, ShieldCheck } from 'lucide-react';

const DropdownField = ({ label, options, value, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const selectedOption = options.find(opt => opt.value === value) || options[0];

  return (
    <div className="space-y-1.5 relative w-full">
      <label className="text-[13px] font-medium text-zinc-400 ml-0.5">
        {label}
      </label>
      <div 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-zinc-950 border border-zinc-800 text-white rounded-lg px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all cursor-pointer flex justify-between items-center hover:bg-zinc-900/50"
      >
        <span>{selectedOption.label}</span>
        <ChevronDown size={14} className={`text-zinc-500 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </div>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setIsOpen(false)} />
          <div className="absolute z-20 w-full mt-2 py-2 bg-zinc-900 border border-zinc-800 rounded-xl shadow-2xl max-h-60 overflow-auto">
            {options.map((opt) => (
              <div
                key={opt.value}
                onClick={() => {
                  onChange(opt.value);
                  setIsOpen(false);
                }}
                className={`px-4 py-2.5 text-sm cursor-pointer hover:bg-blue-600 hover:text-white transition-colors
                  ${value === opt.value ? 'bg-blue-600/10 text-blue-400' : 'text-zinc-400'}`}
              >
                {opt.label}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default function RulesConfig() {
  const [prompt, setPrompt] = useState('');
  const [selectedRule, setSelectedRule] = useState('ssh-bruteforce');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedXml, setGeneratedXml] = useState('');
  
  const wazuhRules = [
    { label: 'SSH Brute Force Protection', value: 'ssh-bruteforce', template: '<rule id="100001" level="5">\n  <if_sid>5716</if_sid>\n  <match>FAILED LOGIN</match>\n  <description>Custom SSH brute force detection</description>\n</rule>' },
    { label: 'Web Server SQLi Detection', value: 'web-sqli', template: '<rule id="100002" level="7">\n  <if_sid>31108</if_sid>\n  <url_match>UNION SELECT</url_match>\n  <description>SQL Injection attempt detected</description>\n</rule>' },
    { label: 'Invalid Login Attempts', value: 'invalid-login', template: '<rule id="100003" level="3">\n  <match>authentication failure</match>\n  <description>Invalid login attempt detected</description>\n</rule>' },
    { label: 'Unauthorized File Access', value: 'file-access', template: '<rule id="100004" level="8">\n  <directory>/etc/passwd</directory>\n  <description>Sensitive file access attempt</description>\n</rule>' },
    { label: 'System Service Failure', value: 'service-fail', template: '<rule id="100005" level="4">\n  <match>service failed</match>\n  <description>Critical service failure detected</description>\n</rule>' }
  ];

  const currentTemplate = wazuhRules.find(r => r.value === selectedRule)?.template || '';

  const handleGenerate = async () => {
    if (!prompt) return;
    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/rules/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          template: currentTemplate
        })
      });
      const data = await response.json();
      if (data.xml) {
        setGeneratedXml(data.xml);
      }
    } catch (err) {
      console.error("Failed to generate rule:", err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleTemplateChange = (val) => {
    setSelectedRule(val);
    setGeneratedXml(''); // Reset generated XML to show the new template
  };

  const [isDeploying, setIsDeploying] = useState(false);
  const [deployStatus, setDeployStatus] = useState(null);

  const handleSave = async () => {
    setIsDeploying(true);
    setDeployStatus(null);
    try {
      const response = await fetch('http://localhost:8000/api/v1/rules/deploy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          xml_content: generatedXml || currentTemplate,
          rule_name: selectedRule
        })
      });
      const data = await response.json();
      if (data.status === 'success') {
        setDeployStatus('success');
        setTimeout(() => setDeployStatus(null), 3000);
      }
    } catch (err) {
      console.error("Failed to deploy rules:", err);
      setDeployStatus('error');
    } finally {
      setIsDeploying(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8 mb-12 animate-in fade-in duration-500">
      <div className="bg-zinc-950/40 border border-zinc-900 rounded-2xl p-8 shadow-2xl backdrop-blur-sm">
        <div className="flex items-center gap-5 mb-10">
          <div className="p-4 bg-purple-600/10 rounded-xl border border-purple-600/20">
            <Shield className="text-purple-500" size={28} />
          </div>
          <div>
            <h2 className="text-2xl font-black text-white tracking-tight">Configure Rules</h2>
            <p className="text-zinc-500 text-sm mt-1">Generate and manage sophisticated security rules for your environment.</p>
          </div>
        </div>
        
        <div className="space-y-10">
          {/* Natural Language Query Section */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <MessageSquare size={18} className="text-purple-500" />
              <h3 className="text-md font-bold text-white uppercase tracking-wider text-xs opacity-70">Natural Language Rule Generator</h3>
            </div>
            
            <div className="relative group">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g. 'Alert me if any IP from Russia tries to access port 22 more than 5 times in a minute'"
                className="w-full bg-zinc-900/50 border border-zinc-800 text-white rounded-xl px-4 py-4 text-sm focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 transition-all min-h-[120px] outline-none placeholder:text-zinc-700 resize-none"
              />
              <div className="absolute bottom-3 right-3">
                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || !prompt}
                  className={`flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-[11px] font-bold rounded-lg transition-all shadow-lg shadow-purple-900/20 disabled:bg-zinc-800 disabled:text-zinc-600 disabled:cursor-not-allowed`}
                >
                  {isGenerating ? (
                    <div className="w-3 h-3 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                  ) : (
                    <Wand2 size={12} />
                  )}
                  {isGenerating ? 'GENERATING...' : 'GENERATE XML'}
                </button>
              </div>
            </div>
          </div>

          <div className="h-px bg-zinc-900 w-full" />

          {/* Wazuh XML Rules Dropdown */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Shield size={18} className="text-purple-500" />
              <h3 className="text-md font-bold text-white uppercase tracking-wider text-xs opacity-70">Wazuh XML Rules Templates</h3>
            </div>
            
            <DropdownField 
              label="Select Base Rule Template" 
              options={wazuhRules}
              value={selectedRule}
              onChange={handleTemplateChange}
            />
            
            <div className="mt-4 p-4 bg-zinc-950/80 border border-zinc-800/50 rounded-xl relative">
              <div className="absolute top-3 right-3 text-[10px] text-zinc-600 font-bold uppercase tracking-widest">
                {generatedXml ? 'AI Generated' : 'Template Baseline'}
              </div>
              <pre className="text-[12px] text-zinc-500 font-mono leading-relaxed overflow-x-auto">
                {generatedXml || currentTemplate}
              </pre>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-6 border-t border-zinc-900">
            <button
              onClick={handleSave}
              disabled={isDeploying}
              className={`w-full flex items-center justify-center gap-2 py-4 px-6 rounded-xl font-bold text-md transition-all duration-200 shadow-xl
                ${deployStatus === 'success' 
                  ? 'bg-emerald-600 text-white shadow-emerald-500/10' 
                  : deployStatus === 'error'
                  ? 'bg-red-600 text-white shadow-red-500/10'
                  : 'bg-purple-600 hover:bg-purple-700 text-white shadow-purple-500/10'}
                disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {isDeploying ? (
                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
              ) : deployStatus === 'success' ? (
                <ShieldCheck size={18} />
              ) : (
                <Save size={18} />
              )}
              {isDeploying ? 'DEPLOYING...' : deployStatus === 'success' ? 'DEPLOYED SUCCESSFULLY' : deployStatus === 'error' ? 'DEPLOYMENT FAILED' : 'Deploy Rule Set'}
            </button>
            {deployStatus === 'success' && (
              <p className="text-center text-xs text-emerald-500 mt-3 animate-in fade-in slide-in-from-top-1">
                Rules have been written to wazuh-rules/local_rules.xml
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
