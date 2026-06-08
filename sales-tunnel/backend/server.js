const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Path to CRM "database"
const LEADS_FILE = path.join(__dirname, 'leads.json');

// Initialize leads file if it doesn't exist
if (!fs.existsSync(LEADS_FILE)) {
    fs.writeFileSync(LEADS_FILE, JSON.stringify([]));
}

// Mock Email Transporter (Update with real SMTP for production)
const transporter = nodemailer.createTransport({
    jsonTransport: true // Logs emails as JSON to console
});

app.post('/api/capture-lead', async (req, res) => {
    const { email, industry, source } = req.body;

    if (!email) {
        return res.status(400).json({ error: 'Email is required' });
    }

    try {
        // 1. Save Lead to CRM
        const leads = JSON.parse(fs.readFileSync(LEADS_FILE));
        leads.push({
            email,
            industry: industry || 'Unknown',
            source: source || 'Direct',
            timestamp: new Date().toISOString()
        });
        fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2));

        // 2. Trigger Automated Delivery
        const blueprintPath = path.join(__dirname, '../assets/blueprint.md');
        const blueprintContent = fs.readFileSync(blueprintPath, 'utf8');

        const mailOptions = {
            from: '"Evans Mathibe Agency" <automation@evansmathibe.com>',
            to: email,
            subject: 'Your South African Business Automation Blueprint',
            text: `Hello,\n\nThank you for requesting the blueprint. You can find the content below:\n\n${blueprintContent}\n\nRegards,\nEvans Mathibe Agency`,
            html: `
                <div style="font-family: serif; color: #111; max-width: 600px; margin: auto;">
                    <h1 style="color: #D4AF37;">Your Automation Blueprint is Here</h1>
                    <p>Thank you for requesting <strong>The South African Business Automation Blueprint</strong>.</p>
                    <p>This guide is designed to help you scale your operations efficiently.</p>
                    <hr/>
                    <div style="background: #f9f9f9; padding: 20px; border-left: 4px solid #D4AF37;">
                        ${blueprintContent.replace(/\n/g, '<br>')}
                    </div>
                    <p style="margin-top: 20px; font-size: 12px; color: #666;">
                        Evans Mathibe Agency | Sandton | Rosebank | Menlyn | Century City | Umhlanga Ridge
                    </p>
                </div>
            `
        };

        const info = await transporter.sendMail(mailOptions);
        console.log(`Lead captured: ${email}. Email sent (Mock):`, info.message);

        res.status(200).json({ message: 'Lead captured and email sent' });

    } catch (error) {
        console.error('Error processing lead:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`Sales Tunnel Backend running on http://localhost:${PORT}`);
});
