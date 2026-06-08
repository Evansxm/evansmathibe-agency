# Evans Mathibe Agency Sales Tunnel (Edge-Native)

This directory contains an automated, high-conversion sales tunnel architected to run on the **Cloudflare Edge**. It is designed to capture and nurture high-value business leads across South Africa's major commercial and provincial hubs.

## 📍 Target Regions
The tunnel is localized for maximum ROI in:
Sandton, Midrand, Cape Town, Pietermaritzburg, Polokwane, Lebowakgomo, Tzaneen, Tshwane, Pretoria East, Menlyn, Centurion, Rustenburg, Brits, Mahikeng, Bloemfontein, Springs, Benoni, and Hartbeespoort.

## 🏗️ Architecture
- **`/src`**: Edge-optimized Cloudflare Worker (`index.js`).
- **`/landing-page`**: High-converting, mobile-responsive frontend (`index.html`).
- **`/assets`**: The Lead Magnet: *The South African Business Automation Blueprint*.
- **`/backend`**: (Legacy/Classic) Node.js fallback server.

## 🚀 Deployment Instructions (Recommended: Edge)

### 1. Configure Cloudflare
Ensure you have the KV Namespace ID and Account ID ready in `wrangler.toml`.

### 2. Provision Secrets
```bash
# Set your transactional email API key
echo "YOUR_API_KEY" | npx wrangler secret put EMAIL_API_KEY
```

### 3. Deploy to Production
```bash
npx wrangler deploy
```
The tunnel will be live at `https://evansmathibe-agency.evansmathibe.workers.dev`.

---

## 🏛️ Deployment Instructions (Alternative: Classic Node.js)

If you prefer a traditional VPS deployment:
1. Navigate to `/backend`.
2. Run `npm install && npm start`.
3. Update the `fetch` URL in `landing-page/index.html` to your server's IP/Domain.

## 📈 Strategy
- **Hook**: Operational efficiency and 30% overhead reduction via AI.
- **CTA**: Instant download of the localized Automation Blueprint.
- **CRM**: Leads are automatically tagged by region and saved to Cloudflare KV (Edge) or `leads.json` (Classic).
