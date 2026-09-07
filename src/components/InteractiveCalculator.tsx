import { useState } from 'preact/hooks';

export default function InteractiveCalculator() {
  const [teamSize, setTeamSize] = useState<number>(5);
  const [monthlyAssets, setMonthlyAssets] = useState<number>(40);
  const [primaryGoal, setPrimaryGoal] = useState<string>('brand-scale');

  // Interactive calculations
  const hoursPerAsset = 6;
  const avgHourlyRate = 450; // ZAR rate or relative units
  const totalHours = monthlyAssets * hoursPerAsset;
  const automationEfficiency = primaryGoal === 'ai-automation' ? 0.70 : primaryGoal === 'brand-scale' ? 0.55 : 0.40;
  
  const savedHoursMonth = Math.round(totalHours * automationEfficiency);
  const costSavingsMonth = savedHoursMonth * avgHourlyRate;
  const annualSavings = costSavingsMonth * 12;

  return (
    <div class="bg-paper border-2 border-ink p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(27,23,18,1)]">
      <div class="mb-6">
        <span class="text-xs font-mono tracking-widest text-ember font-bold uppercase block mb-1">
          Interactive Operations Tool
        </span>
        <h3 class="font-display text-2xl font-bold text-ink">
          Creative Automation ROI Calculator
        </h3>
        <p class="text-xs sm:text-sm text-slate mt-1">
          Estimate time recovered and operational savings by integrating Evans Mathibe custom AI workflow systems.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
        {/* Controls */}
        <div class="space-y-6">
          <div>
            <div class="flex justify-between text-sm font-semibold mb-2 text-ink">
              <label htmlFor="teamSize">Team Size / Collaborators:</label>
              <span class="font-mono text-ember font-bold">{teamSize} members</span>
            </div>
            <input 
              id="teamSize"
              type="range" 
              min="1" 
              max="50" 
              value={teamSize} 
              onInput={(e) => setTeamSize(parseInt((e.target as HTMLInputElement).value))}
              class="w-full h-2 bg-ink/20 rounded-lg appearance-none cursor-pointer accent-ember"
            />
          </div>

          <div>
            <div class="flex justify-between text-sm font-semibold mb-2 text-ink">
              <label htmlFor="monthlyAssets">Monthly Creative Deliverables:</label>
              <span class="font-mono text-ember font-bold">{monthlyAssets} assets</span>
            </div>
            <input 
              id="monthlyAssets"
              type="range" 
              min="10" 
              max="200" 
              step="5"
              value={monthlyAssets} 
              onInput={(e) => setMonthlyAssets(parseInt((e.target as HTMLInputElement).value))}
              class="w-full h-2 bg-ink/20 rounded-lg appearance-none cursor-pointer accent-ember"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold mb-2 text-ink">Primary Operational Objective:</label>
            <div class="grid grid-cols-3 gap-2">
              {[
                { id: 'brand-scale', label: 'Brand Scale' },
                { id: 'ai-automation', label: 'AI Pipeline' },
                { id: 'speed-to-market', label: 'Speed' },
              ].map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setPrimaryGoal(item.id)}
                  class={`py-2 px-3 text-xs font-semibold uppercase tracking-wider border transition-all ${
                    primaryGoal === item.id 
                      ? 'bg-ink text-paper border-ink' 
                      : 'bg-paper text-ink border-ink/30 hover:border-ink'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Output Card */}
        <div class="bg-ink text-paper p-6 border-l-4 border-ember space-y-4">
          <div>
            <span class="text-[11px] font-mono tracking-widest text-brass uppercase block">
              Estimated Recovered Capacity
            </span>
            <div class="text-3xl sm:text-4xl font-display font-bold text-paper mt-1">
              {savedHoursMonth} <span class="text-sm font-sans font-normal text-paper/70">hrs / month</span>
            </div>
          </div>

          <div class="pt-4 border-t border-paper/15">
            <span class="text-[11px] font-mono tracking-widest text-brass uppercase block">
              Projected Annual Operational Value
            </span>
            <div class="text-2xl sm:text-3xl font-display font-bold text-ember mt-1">
              R {annualSavings.toLocaleString()} <span class="text-xs font-sans font-normal text-paper/70">ZAR / yr</span>
            </div>
          </div>

          <p class="text-[11px] text-paper/60 font-sans italic pt-2">
            *Based on standard enterprise creative turnarounds and automated generative brand asset deployment.
          </p>
        </div>
      </div>
    </div>
  );
}
