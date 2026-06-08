# Evans Mathibe Agency Sales Tunnel

This directory contains the automated sales tunnel for the agency, designed to convert cold South African business traffic into high-value leads.

## Structure
- `/assets`: Contains the lead magnet (`blueprint.md`).
- `/landing-page`: Contains the high-converting landing page (`index.html`).
- `/backend`: Contains the Node.js Express server for lead capture and delivery.

## Deployment Instructions

### 1. Backend Setup
Navigate to the `backend` directory and install dependencies:
```bash
cd backend
npm install
```

Start the server:
```bash
npm start
```
The server will run on `http://localhost:3000`.

### 2. Frontend Connection
The landing page is currently configured to send POST requests to `/api/capture-lead`. Ensure your web server (e.g., Nginx or Apache) routes these requests to the Node.js backend or update the `fetch` URL in `landing-page/index.html` to the full backend URL.

### 3. Lead Management
Leads are automatically stored in `backend/leads.json` in a structured format, acting as a lightweight CRM.

### 4. Email Delivery
The backend uses `nodemailer` with a mock transport. To enable real email delivery, update the `transporter` configuration in `backend/server.js` with your SMTP credentials (e.g., Gmail, SendGrid, or Postmark).

## Strategy
- **Targeting**: Focus on commercial and provincial hubs (Sandton, Midrand, Cape Town, Pietermaritzburg, Polokwane, Lebowakgomo, Tzaneen, Tshwane, Pretoria East, Menlyn, Centurion, Rustenburg, Brits, Mahikeng, Bloemfontein, Springs, Benoni, Hartbeespoort).
- **Hook**: Operational efficiency and cost reduction through AI.
- **CTA**: Immediate value delivery via the Blueprint.
