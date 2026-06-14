/**
 * Evans Mathibe AI - Funnel API Worker
 * Cloudflare Worker for lead capture, email triggers, and analytics
 * Deploy: npx wrangler deploy funnel/api/worker.js --name evans-funnel-api
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

const KV_KEYS = {
  LEADS: 'funnel:leads',
  CONFIG: 'funnel:config',
  STATS: 'funnel:stats',
};

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: CORS_HEADERS });
  }

  const url = new URL(request.url);
  const path = url.pathname.replace('/api/', '');

  try {
    switch (path) {
      case 'lead':
        return handleLead(request);
      case 'leads':
        return handleGetLeads(request);
      case 'stats':
        return handleStats(request);
      case 'email/trigger':
        return handleEmailTrigger(request);
      case 'export':
        return handleExport(request);
      default:
        return jsonResponse({ error: 'Not found' }, 404);
    }
  } catch (err) {
    return jsonResponse({ error: err.message }, 500);
  }
}

async function handleLead(request) {
  if (request.method !== 'POST') {
    return jsonResponse({ error: 'Method not allowed' }, 405);
  }

  const data = await request.json();
  const lead = {
    id: 'ld_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 6),
    ...data,
    score: calculateScore(data),
    stage: 'captured',
    timestamp: new Date().toISOString(),
    source: request.headers.get('Referer') || 'direct',
    userAgent: request.headers.get('User-Agent') || '',
  };

  // Store in KV
  const leads = await getLeads();
  leads.push(lead);
  await FUNNEL_KV.put(KV_KEYS.LEADS, JSON.stringify(leads));

  // Update stats
  await updateStats();

  // Trigger welcome sequence
  await triggerWelcomeSequence(lead);

  return jsonResponse({ success: true, lead });
}

async function handleGetLeads(request) {
  const leads = await getLeads();
  const url = new URL(request.url);
  const location = url.searchParams.get('location');
  const vertical = url.searchParams.get('vertical');
  const stage = url.searchParams.get('stage');

  let filtered = leads;
  if (location) filtered = filtered.filter(l => l.location === location);
  if (vertical) filtered = filtered.filter(l => l.vertical === vertical);
  if (stage) filtered = filtered.filter(l => l.stage === stage);

  return jsonResponse({ leads: filtered, total: filtered.length });
}

async function handleStats(request) {
  const leads = await getLeads();
  const stats = {
    total: leads.length,
    goal: 1000,
    percent: Math.min(100, Math.round((leads.length / 1000) * 100)),
    byLocation: countBy(leads, 'location'),
    byVertical: countBy(leads, 'vertical'),
    byStage: countBy(leads, 'stage'),
    hotLeads: leads.filter(l => calculateScore(l) >= 50).length,
    warmLeads: leads.filter(l => calculateScore(l) >= 20 && calculateScore(l) < 50).length,
  };
  return jsonResponse(stats);
}

async function handleEmailTrigger(request) {
  if (request.method !== 'POST') {
    return jsonResponse({ error: 'Method not allowed' }, 405);
  }

  const { leadId, template } = await request.json();
  const leads = await getLeads();
  const lead = leads.find(l => l.id === leadId);

  if (!lead) {
    return jsonResponse({ error: 'Lead not found' }, 404);
  }

  // In production: integrate with SendGrid / Mailchimp / Resend
  console.log(`[EMAIL TRIGGER] Lead: ${leadId} | Template: ${template} | To: ${lead.email}`);

  return jsonResponse({
    success: true,
    message: `Email ${template} queued for ${lead.email}`,
    lead: { id: lead.id, email: lead.email, template }
  });
}

async function handleExport(request) {
  const leads = await getLeads();
  const headers = ['Name', 'Company', 'Email', 'WhatsApp', 'Location', 'Vertical', 'Challenge', 'Score', 'Stage', 'Date', 'Source'];
  const rows = leads.map(l => [
    l.first_name || '', l.company || '', l.email || '', l.phone || '',
    l.location || '', l.vertical || '', (l.challenge || '').replace(/,/g, ';'),
    calculateScore(l), l.stage || 'captured', l.timestamp || '', l.source || ''
  ]);
  const csv = [headers.join(','), ...rows.map(r => r.map(c => `"${c}"`).join(','))].join('\n');
  return new Response(csv, {
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': `attachment; filename="evans-funnel-${new Date().toISOString().slice(0,10)}.csv"`,
      ...CORS_HEADERS,
    }
  });
}

async function getLeads() {
  try {
    const data = await FUNNEL_KV.get(KV_KEYS.LEADS, 'json');
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

function calculateScore(lead) {
  let score = 0;
  if (lead.location) score += 10;
  if (lead.vertical) {
    const v = lead.vertical.toLowerCase();
    if (v.includes('media house') || v.includes('ad agenc')) score += 20;
  }
  if (lead.calendar_viewed === 'true') score += 15;
  if (lead.whatsapp_replied === 'true') score += 30;
  if (lead.email_opened === 'true') score += 5;
  if (lead.calendar_booked === 'true') score += 25;
  return score;
}

function countBy(arr, key) {
  const result = {};
  arr.forEach(item => {
    const val = item[key] || 'Unknown';
    result[val] = (result[val] || 0) + 1;
  });
  return result;
}

async function updateStats() {
  const leads = await getLeads();
  await FUNNEL_KV.put(KV_KEYS.STATS, JSON.stringify({
    total: leads.length,
    updated: new Date().toISOString(),
  }));
}

async function triggerWelcomeSequence(lead) {
  const group = getGroup(lead.vertical);
  const province = getProvince(lead.location);

  console.log(`[SEQUENCE] Lead: ${lead.id} | Group: ${group} | Province: ${province}`);
  console.log(`[SEQUENCE] Email 1 (welcome) → To: ${lead.email} | Subject: "${lead.first_name}, your Evans Mathibe audit (${lead.location})"`);
  console.log(`[SEQUENCE] WhatsApp T1 → In 5 min: "Hey ${lead.first_name}, it's Evans. Saw your request from ${lead.company}..."`);

  // In production: Queue these via email API + WhatsApp Business API
}

function getGroup(vertical) {
  if (!vertical) return 'corporate';
  const v = vertical.toLowerCase();
  if (v.includes('media house') || v.includes('ad agenc')) return 'media-agency';
  if (v.includes('universit') || v.includes('creative school')) return 'university';
  return 'corporate';
}

function getProvince(location) {
  if (!location) return 'gauteng';
  const loc = location.toLowerCase();
  if (loc.includes('sandton') || loc.includes('rosebank') || loc.includes('midrand') ||
      loc.includes('menlyn') || loc.includes('auckland') || loc.includes('braamfontein')) return 'gauteng';
  if (loc.includes('ct') || loc.includes('cape') || loc.includes('century') ||
      loc.includes('woodstock') || loc.includes('waterfront') || loc.includes('green')) return 'western_cape';
  if (loc.includes('umhlanga') || loc.includes('durban') || loc.includes('morningside')) return 'kwazulu_natal';
  return 'gauteng';
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS }
  });
}
