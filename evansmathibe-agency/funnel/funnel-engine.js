/* Evans Mathibe AI - Adaptive Sales Funnel Engine v1.0 */
(function () {
  'use strict';

  const CONFIG = {
    brand: { name: 'Evans Mathibe AI', whatsapp: '27724165061', email: 'evans.mathibe@mail.com' },
    goal: 1000,
    scoreThresholds: { hot: 50, warm: 20 },
    storageKey: 'evans_funnel_leads'
  };

  const LOCATIONS = {
    gauteng: [
      'Sandton CBD (Rivonia)', 'Sandton CBD (West)', 'Sandton CBD (Maude)',
      'Rosebank (Oxford)', 'Rosebank (Jellicoe)', 'Midrand Waterfall',
      'Menlyn Maine', 'Auckland Park', 'Braamfontein'
    ],
    western_cape: [
      'CT CBD (Heerengracht)', 'CT CBD (Bree)', 'CT CBD (Long)',
      'Century City', 'Woodstock', 'V&A Waterfront', 'Green Point'
    ],
    kwazulu_natal: [
      'Umhlanga Ridge', 'Durban Central', 'Morningside'
    ]
  };

  const VERTICALS = [
    'Media Houses (SABC, MultiChoice, eMedia, Primedia)',
    'Ad Agencies (Ogilvy, VML, TBWA, Joe Public, Odd Number, Avatar)',
    'Radio (947, 702, Jacaranda, Kaya, YFM, Kfm, Heart, Good Hope, ECR, Ukhozi)',
    'Universities & Creative Schools (Wits, UJ, UP, UCT, Stellenbosch, UKZN, AFDA, Vega, Open Window)',
    'Podcast / Content Studios',
    'Corporate HQs & Nightlife Groups'
  ];

  function getProvince(location) {
    for (const [prov, locs] of Object.entries(LOCATIONS)) {
      if (locs.some(l => location.includes(l.split('(')[0].trim()) || l === location)) return prov;
    }
    return 'gauteng';
  }

  function getTimeConfig(province) {
    const configs = {
      gauteng: { start: 9, end: 17, tz: 'SAST', label: '09:00-17:00' },
      western_cape: { start: 9.5, end: 17.5, tz: 'SAST', label: '09:30-17:30' },
      kwazulu_natal: { start: 9, end: 16.5, tz: 'SAST', label: '09:00-16:30' }
    };
    return configs[province] || configs.gauteng;
  }

  function getVerticalGroup(vertical) {
    if (!vertical) return 'corporate';
    const v = vertical.toLowerCase();
    if (v.includes('media house') || v.includes('ad agenc')) return 'media-agency';
    if (v.includes('universit') || v.includes('creative school')) return 'university';
    if (v.includes('corporate') || v.includes('radio') || v.includes('nightlife')) return 'corporate';
    if (v.includes('podcast') || v.includes('content studio')) return 'corporate';
    return 'corporate';
  }

  function calculateScore(lead) {
    let score = 0;
    if (lead.location) score += 10;
    const group = getVerticalGroup(lead.vertical);
    if (group === 'media-agency') score += 20;
    if (lead.calendar_viewed === 'true') score += 15;
    if (lead.whatsapp_replied === 'true') score += 30;
    if (lead.email_opened === 'true') score += 5;
    if (lead.calendar_booked === 'true') score += 25;
    return score;
  }

  function getLeadStatus(score) {
    if (score >= CONFIG.scoreThresholds.hot) return 'hot';
    if (score >= CONFIG.scoreThresholds.warm) return 'warm';
    return 'cold';
  }

  function generateId() {
    return 'ld_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 6);
  }

  const FunnelEngine = {
    CONFIG,
    LOCATIONS,
    VERTICALS,
    getProvince,
    getTimeConfig,
    getVerticalGroup,
    calculateScore,
    getLeadStatus,
    generateId,

    getURLParams() {
      const params = new URLSearchParams(window.location.search);
      return {
        location: params.get('location') || '',
        vertical: params.get('vertical') || '',
        source: params.get('source') || 'direct',
        ref: params.get('ref') || ''
      };
    },

    replaceDynamicText(text, data) {
      if (!text) return '';
      const d = data || {};
      return text
        .replace(/\{\{first_name\}\}/g, d.first_name || 'there')
        .replace(/\{\{company\}\}/g, d.company || 'your company')
        .replace(/\{\{location\}\}/g, d.location || 'South Africa')
        .replace(/\{\{vertical\}\}/g, d.vertical || 'business')
        .replace(/\{\{email\}\}/g, d.email || '')
        .replace(/\{\{phone\}\}/g, d.phone || '')
        .replace(/\{\{score\}\}/g, d.score || '0')
        .replace(/\{\{status\}\}/g, d.status || 'New');
    },

    getWhatsAppLink(message) {
      const text = encodeURIComponent(message || '');
      return `https://wa.me/${CONFIG.brand.whatsapp}?text=${text}`;
    },

    getWhatsAppMessage(lead) {
      const name = lead?.first_name || 'there';
      const company = lead?.company || 'your company';
      const location = lead?.location || 'your area';
      return `Hi Evans, I'm ${name} from ${company} in ${location}. I just signed up for the AI Brand Audit. Keen to chat!`;
    },

    getAllLocations() {
      return [...LOCATIONS.gauteng, ...LOCATIONS.western_cape, ...LOCATIONS.kwazulu_natal];
    },

    getLocationOptionsHtml() {
      const groups = [
        { label: 'Gauteng', locs: LOCATIONS.gauteng },
        { label: 'Western Cape', locs: LOCATIONS.western_cape },
        { label: 'KwaZulu-Natal', locs: LOCATIONS.kwazulu_natal }
      ];
      let html = '<option value="">Select your location</option>';
      groups.forEach(g => {
        html += `<optgroup label="${g.label}">`;
        g.locs.forEach(l => { html += `<option value="${l}">${l}</option>`; });
        html += '</optgroup>';
      });
      return html;
    },

    getVerticalOptionsHtml() {
      let html = '<option value="">Select your industry</option>';
      VERTICALS.forEach(v => { html += `<option value="${v}">${v}</option>`; });
      return html;
    },

    /* ---- LEAD STORAGE ---- */
    getLeads() {
      try {
        return JSON.parse(localStorage.getItem(CONFIG.storageKey)) || [];
      } catch { return []; }
    },

    saveLead(lead) {
      const leads = this.getLeads();
      lead.id = lead.id || this.generateId();
      lead.timestamp = lead.timestamp || new Date().toISOString();
      lead.score = lead.score || this.calculateScore(lead);
      lead.stage = lead.stage || 'captured';
      const idx = leads.findIndex(l => l.id === lead.id);
      if (idx >= 0) leads[idx] = lead; else leads.push(lead);
      localStorage.setItem(CONFIG.storageKey, JSON.stringify(leads));
      this.syncToServer(lead);
      return lead;
    },

    updateLead(id, updates) {
      const leads = this.getLeads();
      const idx = leads.findIndex(l => l.id === id);
      if (idx < 0) return null;
      leads[idx] = { ...leads[idx], ...updates, score: this.calculateScore({ ...leads[idx], ...updates }) };
      localStorage.setItem(CONFIG.storageKey, JSON.stringify(leads));
      this.syncToServer(leads[idx]);
      return leads[idx];
    },

    deleteLead(id) {
      const leads = this.getLeads().filter(l => l.id !== id);
      localStorage.setItem(CONFIG.storageKey, JSON.stringify(leads));
    },

    syncToServer(lead) {
      try {
        const payload = { event: 'lead_sync', lead, source: window.location.href, timestamp: new Date().toISOString() };
        fetch('https://formsubmit.co/ajax/evans.mathibe@mail.com', {
          method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(payload)
        }).catch(() => {});
      } catch {}
    },

    /* ---- DASHBOARD DATA ---- */
    getDashboardData() {
      const leads = this.getLeads();
      const total = leads.length;
      const goal = CONFIG.goal;
      const percent = Math.min(100, Math.round((total / goal) * 100));

      const byLocation = {};
      const byVertical = {};
      const byStage = { captured: 0, booked: 0, proposal: 0, won: 0, lost: 0 };
      let hotCount = 0;
      let warmCount = 0;

      leads.forEach(l => {
        const loc = l.location || 'Unknown';
        byLocation[loc] = (byLocation[loc] || 0) + 1;
        const vert = l.vertical || 'Unknown';
        const short = vert.split('(')[0].trim();
        byVertical[short] = (byVertical[short] || 0) + 1;
        if (byStage[l.stage] !== undefined) byStage[l.stage]++;
        const score = this.calculateScore(l);
        if (score >= CONFIG.scoreThresholds.hot) hotCount++;
        else if (score >= CONFIG.scoreThresholds.warm) warmCount++;
      });

      return { total, goal, percent, leads, byLocation, byVertical, byStage, hotCount, warmCount };
    },

    /* ---- FORM HANDLING ---- */
    initCaptureForm(formId) {
      const form = document.getElementById(formId);
      if (!form) return;

      const params = this.getURLParams();
      if (params.location) {
        const locSelect = form.querySelector('[name="location"]');
        if (locSelect) locSelect.value = params.location;
      }
      if (params.vertical) {
        const vertSelect = form.querySelector('[name="vertical"]');
        if (vertSelect) vertSelect.value = params.vertical;
      }

      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector('[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Sending...';

        const fd = new FormData(form);
        const data = { source: params.source || 'organic' };
        fd.forEach((v, k) => { data[k] = v; });
        data.score = this.calculateScore(data);
        data.stage = 'captured';

        const newLead = this.saveLead(data);

        const redirectUrl = new URL('thank-you.html', window.location.href);
        redirectUrl.searchParams.set('id', newLead.id);
        redirectUrl.searchParams.set('first_name', data.first_name || 'there');
        redirectUrl.searchParams.set('company', data.company || '');
        redirectUrl.searchParams.set('location', data.location || '');
        redirectUrl.searchParams.set('vertical', data.vertical || '');

        fetch(form.action || 'https://formsubmit.co/ajax/evans.mathibe@mail.com', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(data)
        }).finally(() => {
          window.location.href = redirectUrl.toString();
        });
      });
    },

    /* ---- THANK YOU PAGE ---- */
    initThankYou() {
      const params = this.getURLParams();
      const firstName = params.first_name || 'there';
      const company = params.company || '';
      const location = params.location || 'your area';
      const vertical = params.vertical || '';

      document.querySelectorAll('[data-dynamic]').forEach(el => {
        const key = el.dataset.dynamic;
        el.textContent = this.replaceDynamicText(el.textContent, params);
      });

      const headline = document.getElementById('ty-headline');
      if (headline) {
        headline.textContent = `Thanks ${firstName}, your ${location} audit is queued`;
      }

      const waLink = document.getElementById('ty-whatsapp-link');
      if (waLink) {
        const msg = `Hi Evans, I'm ${firstName} from ${company} in ${location}. I just signed up for the AI Brand Audit. Keen to chat!`;
        waLink.href = this.getWhatsAppLink(msg);
      }

      const waBtn = document.getElementById('ty-whatsapp-btn');
      if (waBtn) {
        const msg = `Hi Evans, I'm ${firstName} from ${company} in ${location}. I just signed up for the AI Brand Audit. Keen to chat!`;
        waBtn.href = this.getWhatsAppLink(msg);
      }

      const leadId = params.id;
      if (leadId) {
        this.updateLead(leadId, { stage: 'thank_you', calendar_viewed: 'true' });
        this.triggerAutomation(leadId, 'welcome');
      }
    },

    /* ---- AUTOMATION TRIGGERS ---- */
    triggerAutomation(leadId, trigger) {
      const leads = this.getLeads();
      const lead = leads.find(l => l.id === leadId);
      if (!lead) return;

      const group = this.getVerticalGroup(lead.vertical);
      const province = this.getProvince(lead.location);

      console.log(`[EvansFunnel] Trigger: ${trigger} | Lead: ${leadId} | Group: ${group} | Province: ${province}`);

      if (trigger === 'welcome') {
        this.scheduleEmail(lead, 'welcome', 0);
        this.scheduleWhatsApp(lead, 'template_1', 5);
      }
    },

    scheduleEmail(lead, template, delayMin) {
      const group = this.getVerticalGroup(lead.vertical);
      const province = this.getProvince(lead.location);
      const timeConfig = this.getTimeConfig(province);

      console.log(`[EvansFunnel] Email queued: ${template} | To: ${lead.email} | Group: ${group} | Delay: ${delayMin}min | Hours: ${timeConfig.label}`);
      this.logSequence(lead.id, 'email', template, delayMin);

      if (template === 'welcome') {
        const subject = `${lead.first_name}, your Evans Mathibe audit (${lead.location})`;
        console.log(`[EvansFunnel] WELCOME EMAIL → To: ${lead.email} | Subject: ${subject}`);
        console.log(`[EvansFunnel] Body: Hi ${lead.first_name},\n\nThank you for requesting your AI Brand Audit for ${lead.company} in ${lead.location}.\n\nWe've received your request and Evans will review it personally within 48 hours.\nIn the meantime, here's what to expect:\n1. We'll analyze your current brand presence\n2. Identify AI automation opportunities\n3. Deliver a custom strategy tailored to ${lead.location}\n\nBook a quick 15-min call to fast-track:\nhttps://calendly.com/evansmathibe/15min\n\nBest,\nEvans Mathibe\nEvans Mathibe AI`);
      }

      if (template === 'email_2') {
        if (group === 'media-agency') {
          console.log(`[EvansFunnel] EMAIL 2 (Media/Agency) → Subject: How we automated promos for a MultiChoice-style channel`);
          console.log(`[EvansFunnel] Body: Hi ${lead.first_name},\n\nCase Study: We helped a media client in ${lead.location} automate their promo scheduling with AI, reducing manual work by 80%...\n\n[Read Full Case Study →]\n\nBest,\nEvans`);
        } else if (group === 'university') {
          console.log(`[EvansFunnel] EMAIL 2 (University) → Subject: 3 AI campaigns that filled open days at Wits and UCT`);
          console.log(`[EvansFunnel] Body: Hi ${lead.first_name},\n\nDiscover how universities in SA are using AI to boost open day attendance...\n\n[Download Case Study →]\n\nBest,\nEvans`);
        } else {
          console.log(`[EvansFunnel] EMAIL 2 (Corporate) → Subject: Sandton brand cut agency costs 32% with AI`);
          console.log(`[EvansFunnel] Body: Hi ${lead.first_name},\n\nA Sandton-based corporate client of ours reduced agency costs by 32% using AI automation...\n\n[See How →]\n\nBest,\nEvans`);
        }
      }
    },

    scheduleWhatsApp(lead, template, delayMin) {
      console.log(`[EvansFunnel] WhatsApp queued: ${template} | To: ${lead.phone || lead.whatsapp || 'N/A'} | Delay: ${delayMin}min`);

      if (template === 'template_1') {
        const msg = `Hey ${lead.first_name}, it's Evans. Saw your request from ${lead.company}. Are you free for 15 mins tomorrow to discuss your AI Brand Audit?`;
        console.log(`[EvansFunnel] WHATSAPP T1 → ${msg}`);
        console.log(`[EvansFunnel] Send via: ${this.getWhatsAppLink(msg)}`);
      }
    },

    logSequence(leadId, channel, template, delayMin) {
      const key = `evans_seq_log_${leadId}`;
      try {
        const log = JSON.parse(localStorage.getItem(key)) || [];
        log.push({ channel, template, delayMin, timestamp: new Date().toISOString() });
        localStorage.setItem(key, JSON.stringify(log));
      } catch {}
    },

    /* ---- DASHBOARD INIT ---- */
    initDashboard() {
      const data = this.getDashboardData();
      const container = document.getElementById('dash-container');
      if (!container) return;

      const hotBadge = data.hotCount > 0
        ? `<span class="badge badge-hot" style="animation: pulse 1.5s ease-in-out infinite;">${data.hotCount} HOT</span>`
        : '';

      container.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;margin-bottom:2rem;">
          <div>
            <h1 style="font-size:1.5rem;font-weight:700;">Lead Dashboard</h1>
            <p style="color:rgba(255,255,255,0.3);font-size:0.8rem;">Evans Mathibe AI Sales Funnel</p>
          </div>
          <div style="display:flex;gap:0.75rem;align-items:center;">
            ${hotBadge}
            <button onclick="FunnelEngine.exportCSV()" class="btn-outline" style="padding:0.5rem 1rem;font-size:0.7rem;">Export CSV</button>
            <button onclick="FunnelEngine.resetTestData()" class="btn-outline" style="padding:0.5rem 1rem;font-size:0.7rem;border-color:rgba(212,92,92,0.3);">Reset Test Data</button>
          </div>
        </div>

        <!-- Goal Tracker -->
        <div class="glass-card" style="margin-bottom:1.5rem;">
          <div class="goal-tracker">
            <div class="goal-number">${data.total}</div>
            <div class="goal-subtitle">of ${data.goal.toLocaleString()} leads · ${data.percent}% to goal</div>
            <div class="progress-bar" style="margin-top:1rem;max-width:400px;margin-left:auto;margin-right:auto;">
              <div class="progress-fill" style="width:${data.percent}%"></div>
            </div>
          </div>
        </div>

        <!-- Stats -->
        <div class="stats-grid" style="margin-bottom:1.5rem;">
          <div class="stat-card"><div class="stat-number">${data.total}</div><div class="stat-label">Total Leads</div></div>
          <div class="stat-card"><div class="stat-number">${data.hotCount}</div><div class="stat-label">Hot Leads</div></div>
          <div class="stat-card"><div class="stat-number">${data.warmCount}</div><div class="stat-label">Warm Leads</div></div>
          <div class="stat-card"><div class="stat-number">${data.byStage.booked || 0}</div><div class="stat-label">Calls Booked</div></div>
          <div class="stat-card"><div class="stat-number">${data.byStage.won || 0}</div><div class="stat-label">Deals Won</div></div>
        </div>

        <!-- Charts Row -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
          <div class="chart-container">
            <h3 style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:1rem;">Leads by Location</h3>
            <div id="chart-location" style="height:220px;">${this.renderBarChart(data.byLocation)}</div>
          </div>
          <div class="chart-container">
            <h3 style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:1rem;">Leads by Vertical</h3>
            <div id="chart-vertical" style="height:220px;">${this.renderBarChart(data.byVertical)}</div>
          </div>
        </div>

        <!-- Stage Funnel -->
        <div class="glass-card" style="margin-bottom:1.5rem;">
          <h3 style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:1rem;">Funnel Stages</h3>
          <div style="display:flex;gap:0.5rem;align-items:center;">
            ${this.renderFunnelStages(data.byStage)}
          </div>
        </div>

        <!-- Filters -->
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.75rem;margin-bottom:1rem;">
          <h3 style="font-size:0.85rem;font-weight:600;">All Leads <span style="color:rgba(255,255,255,0.3);font-weight:400;">(${data.total})</span></h3>
          <div class="filter-bar" style="margin-bottom:0;">
            <select id="filter-location" onchange="FunnelEngine.filterDashboard()" class="form-select" style="padding:0.5rem 0.75rem;font-size:0.75rem;">
              <option value="">All Locations</option>
              ${this.getAllLocations().map(l => `<option value="${l}">${l}</option>`).join('')}
            </select>
            <select id="filter-vertical" onchange="FunnelEngine.filterDashboard()" class="form-select" style="padding:0.5rem 0.75rem;font-size:0.75rem;">
              <option value="">All Verticals</option>
              ${VERTICALS.map(v => `<option value="${v}">${v.split('(')[0].trim()}</option>`).join('')}
            </select>
            <select id="filter-stage" onchange="FunnelEngine.filterDashboard()" class="form-select" style="padding:0.5rem 0.75rem;font-size:0.75rem;">
              <option value="">All Stages</option>
              <option value="captured">Captured</option>
              <option value="thank_you">Thank You</option>
              <option value="booked">Booked</option>
              <option value="proposal">Proposal</option>
              <option value="won">Won</option>
            </select>
          </div>
        </div>

        <!-- Table -->
        <div class="glass-card" style="padding:0;overflow:hidden;">
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Company</th>
                  <th>Location</th>
                  <th>Vertical</th>
                  <th>Score</th>
                  <th>Stage</th>
                  <th>Date</th>
                  <th></th>
                </tr>
              </thead>
              <tbody id="leads-table-body">
                ${this.renderLeadsTable(data.leads)}
              </tbody>
            </table>
          </div>
        </div>
      `;
    },

    renderBarChart(data) {
      const entries = Object.entries(data).sort((a, b) => b[1] - a[1]).slice(0, 10);
      if (entries.length === 0) return '<p style="color:rgba(255,255,255,0.2);text-align:center;padding:3rem;">No data yet</p>';
      const maxVal = Math.max(...entries.map(e => e[1]));
      const bars = entries.map(([key, val]) => {
        const pct = Math.max(4, (val / maxVal) * 100);
        const label = key.length > 15 ? key.slice(0, 14) + '…' : key;
        return `<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;">
          <span style="font-size:0.6rem;color:rgba(255,255,255,0.3);margin-bottom:0.25rem;">${val}</span>
          <div class="chart-bar" style="height:${pct}%;width:100%;max-width:40px;background:linear-gradient(180deg,var(--brand-coral),var(--brand-gold));"></div>
          <span style="font-size:0.55rem;color:rgba(255,255,255,0.2);margin-top:0.5rem;text-align:center;line-height:1.2;">${label}</span>
        </div>`;
      }).join('');
      return `<div style="display:flex;align-items:flex-end;height:100%;gap:0.25rem;">${bars}</div>`;
    },

    renderFunnelStages(stages) {
      const labels = { captured: 'Captured', booked: 'Booked', proposal: 'Proposal', won: 'Won' };
      const maxVal = Math.max(...Object.values(stages), 1);
      return Object.entries(labels).map(([key, label]) => {
        const val = stages[key] || 0;
        const pct = Math.max(4, (val / maxVal) * 100);
        return `<div style="flex:1;text-align:center;">
          <div style="font-size:1.5rem;font-weight:700;color:var(--brand-coral);">${val}</div>
          <div style="height:60px;display:flex;align-items:flex-end;justify-content:center;margin:0.5rem 0;">
            <div style="width:100%;max-width:60px;height:${pct}%;background:linear-gradient(180deg,var(--brand-coral),var(--brand-gold));border-radius:4px 4px 0 0;transition:height 0.5s ease;"></div>
          </div>
          <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:rgba(255,255,255,0.3);">${label}</div>
        </div>`;
      }).join('');
    },

    renderLeadsTable(leads) {
      if (leads.length === 0) {
        return '<tr><td colspan="8" style="text-align:center;padding:3rem;color:rgba(255,255,255,0.2);">No leads captured yet. Share your funnel link to start generating leads.</td></tr>';
      }
      return leads.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).map(l => {
        const score = this.calculateScore(l);
        const status = this.getLeadStatus(score);
        const date = new Date(l.timestamp).toLocaleDateString('en-ZA', { day: '2-digit', month: 'short' });
        const stageLabel = l.stage ? l.stage.replace('_', ' ') : 'new';
        return `<tr>
          <td style="font-weight:600;">${l.first_name || 'N/A'}</td>
          <td>${l.company || '-'}</td>
          <td>${l.location || '-'}</td>
          <td>${l.vertical ? l.vertical.split('(')[0].trim() : '-'}</td>
          <td><span class="badge badge-${status}">${score}</span></td>
          <td><span style="font-size:0.7rem;text-transform:capitalize;color:rgba(255,255,255,0.4);">${stageLabel}</span></td>
          <td style="font-size:0.75rem;color:rgba(255,255,255,0.3);">${date}</td>
          <td><button onclick="FunnelEngine.deleteLead('${l.id}');FunnelEngine.initDashboard();" style="background:none;border:none;color:rgba(212,92,92,0.4);cursor:pointer;font-size:0.75rem;">✕</button></td>
        </tr>`;
      }).join('');
    },

    filterDashboard() {
      const locFilter = document.getElementById('filter-location')?.value || '';
      const vertFilter = document.getElementById('filter-vertical')?.value || '';
      const stageFilter = document.getElementById('filter-stage')?.value || '';
      const allLeads = this.getLeads();
      const filtered = allLeads.filter(l => {
        if (locFilter && l.location !== locFilter) return false;
        if (vertFilter && l.vertical !== vertFilter) return false;
        if (stageFilter && l.stage !== stageFilter) return false;
        return true;
      });
      const tbody = document.getElementById('leads-table-body');
      if (tbody) tbody.innerHTML = this.renderLeadsTable(filtered);
    },

    exportCSV() {
      const leads = this.getLeads();
      if (leads.length === 0) { alert('No leads to export'); return; }
      const headers = ['Name', 'Company', 'Email', 'WhatsApp', 'Location', 'Vertical', 'Challenge', 'Score', 'Stage', 'Date'];
      const rows = leads.map(l => [
        l.first_name || '',
        l.company || '',
        l.email || '',
        l.whatsapp || l.phone || '',
        l.location || '',
        l.vertical || '',
        (l.challenge || '').replace(/,/g, ';'),
        this.calculateScore(l),
        l.stage || 'captured',
        l.timestamp || ''
      ]);
      const csv = [headers.join(','), ...rows.map(r => r.map(c => `"${c}"`).join(','))].join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = `evans-funnel-leads-${new Date().toISOString().slice(0,10)}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    },

    resetTestData() {
      if (confirm('Remove all test leads? This cannot be undone.')) {
        localStorage.removeItem(CONFIG.storageKey);
        this.initDashboard();
        this.showToast('Test data cleared');
      }
    },

    seedTestData() {
      if (this.getLeads().length > 0) return;
      const testLeads = [
        { first_name: 'Thabo', company: 'MultiChoice Group', email: 'thabo@multichoice.co.za', location: 'Sandton CBD (Rivonia)', vertical: VERTICALS[0], challenge: 'Needs automated promo scheduling', stage: 'captured' },
        { first_name: 'Lerato', company: 'Ogilvy SA', email: 'lerato@ogilvy.co.za', location: 'Rosebank (Oxford)', vertical: VERTICALS[1], challenge: 'Looking for AI creative tools', stage: 'captured' },
        { first_name: 'Sipho', company: 'Wits University', email: 'sipho@wits.ac.za', location: 'Braamfontein', vertical: VERTICALS[3], challenge: 'Student recruitment campaigns', stage: 'thank_you' },
        { first_name: 'Priya', company: 'V&A Waterfront', email: 'priya@waterfront.co.za', location: 'V&A Waterfront', vertical: VERTICALS[5], challenge: 'Brand refresh needed', stage: 'booked' },
        { first_name: 'Nomsa', company: '947 Radio', email: 'nomsa@947.co.za', location: 'Auckland Park', vertical: VERTICALS[2], challenge: 'Radio promo automation', stage: 'captured' },
        { first_name: 'Daniel', company: 'AFDA Cape Town', email: 'daniel@afda.co.za', location: 'CT CBD (Bree)', vertical: VERTICALS[3], challenge: 'Open day campaigns', stage: 'captured' },
        { first_name: 'Zanele', company: 'Ukhozi FM', email: 'zanele@ukhozi.co.za', location: 'Durban Central', vertical: VERTICALS[2], challenge: 'Digital transformation', stage: 'proposal' },
        { first_name: 'James', company: 'TBWA Durban', email: 'james@tbwa.co.za', location: 'Umhlanga Ridge', vertical: VERTICALS[1], challenge: 'AI integration', stage: 'won' },
        { first_name: 'Amara', company: 'Stellenbosch University', email: 'amara@sun.ac.za', location: 'Menlyn Maine', vertical: VERTICALS[3], challenge: 'Brand awareness', stage: 'captured' },
        { first_name: 'Kabelo', company: 'Primedia', email: 'kabelo@primedia.co.za', location: 'Century City', vertical: VERTICALS[0], challenge: 'Content automation', stage: 'captured' }
      ];
      testLeads.forEach(l => {
        l.id = this.generateId();
        l.timestamp = new Date(Date.now() - Math.random() * 14 * 86400000).toISOString();
        l.score = this.calculateScore(l);
        this.saveLead(l);
      });
    },

    showToast(msg) {
      let toast = document.getElementById('funnel-toast');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'funnel-toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
      }
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3000);
    },

    /* ---- DYNAMIC PAGE CONTENT ---- */
    injectDynamicContent() {
      const params = this.getURLParams();
      document.querySelectorAll('[data-replace]').forEach(el => {
        const key = el.dataset.replace;
        el.textContent = this.replaceDynamicText(el.textContent, params);
      });

      const locationDisplay = document.getElementById('dynamic-location');
      if (locationDisplay) {
        locationDisplay.textContent = params.location || 'South Africa';
      }

      const headline = document.getElementById('dynamic-headline');
      if (headline) {
        const vertical = params.vertical || '';
        const location = params.location || 'South Africa';
        const group = this.getVerticalGroup(vertical);

        const headlines = {
          'media-agency': `AI-Powered Media Solutions for ${location}`,
          'university': `Future-Ready Creative Talent for ${location}`,
          'corporate': `Brand Growth Accelerator for ${location}`
        };
        headline.textContent = headlines[group] || `AI Brand Growth for ${location}`;
      }

      const subheadline = document.getElementById('dynamic-subheadline');
      if (subheadline) {
        const location = params.location || 'your city';
        subheadline.textContent = `Serving ${location} brands from Sandton to Sea Point`;
      } else {
        const els = document.querySelectorAll('[data-serving]');
        els.forEach(el => {
          el.textContent = `Serving ${params.location || 'SA'} brands from Sandton to Sea Point`;
        });
      }
    },

    /* ---- DISABLE STOP LOGIC ---- */
    checkStopped() {
      const stopped = localStorage.getItem('evans_stopped_leads') || '';
      if (!stopped) return '';
      return stopped.split(',');
    },

    markStopped(leadId) {
      const stopped = this.checkStopped().split(',').filter(Boolean);
      stopped.push(leadId);
      localStorage.setItem('evans_stopped_leads', stopped.join(','));
    }
  };

  window.FunnelEngine = FunnelEngine;

  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('funnel-capture-form')) {
      FunnelEngine.injectDynamicContent();
      FunnelEngine.initCaptureForm('funnel-capture-form');
    }
    if (document.getElementById('ty-container')) {
      FunnelEngine.injectDynamicContent();
      FunnelEngine.initThankYou();
    }
    if (document.getElementById('dash-container')) {
      FunnelEngine.seedTestData();
      FunnelEngine.initDashboard();
    }
    if (document.getElementById('dynamic-headline') || document.getElementById('dynamic-location')) {
      FunnelEngine.injectDynamicContent();
    }
  });
})();
