export default {
  async fetch(request, env, ctx) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method === "POST") {
      try {
        const data = await request.json();
        const email = data.email;

        if (!email) {
          return new Response(JSON.stringify({ error: "Email is required" }), {
            status: 400,
            headers: { ...corsHeaders, "Content-Type": "application/json" }
          });
        }

        // 1. Save Lead to Storage (KV)
        await env.LEADS_KV.put(`lead:${email}`, JSON.stringify({
          email: email,
          timestamp: new Date().toISOString(),
          source: data.source || "sales_tunnel_sa",
          industry: data.industry || "Unknown",
          region: data.region || "South Africa"
        }));

        // 2. Automated Asset Delivery (Email)
        // Note: Configure EMAIL_API_KEY via `wrangler secret put EMAIL_API_KEY`
        // This example uses the Resend API (resend.com)
        if (env.EMAIL_API_KEY) {
          await fetch("https://api.resend.com/emails", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${env.EMAIL_API_KEY}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              from: "Evans Mathibe Agency <automation@evansmathibe.com>",
              to: [email],
              subject: "Your South African Business Automation Blueprint",
              html: `
                <div style="font-family: serif; color: #111; max-width: 600px; margin: auto; border: 1px solid #D4AF37; padding: 40px;">
                  <h1 style="color: #D4AF37; text-align: center;">Success! Your Blueprint is Ready.</h1>
                  <p>Thank you for requesting <strong>The South African Business Automation Blueprint</strong>.</p>
                  <p>Our systems have logged your interest. You can download the full guide below, or read the key phases directly in this email.</p>
                  <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
                  <div style="background: #fdfdfd; padding: 20px; border-left: 4px solid #D4AF37;">
                    <h3 style="margin-top: 0;">Phase 1: ROI-Focused Lead Capture</h3>
                    <p>Stop wasting 80% of your marketing budget on impressions that don't convert. Localize your outreach for hubs like Sandton, Midrand, and Polokwane...</p>
                  </div>
                  <p style="text-align: center; margin-top: 40px;">
                    <a href="https://evansmathibe.com/blueprint-pdf" style="background: #D4AF37; color: #000; padding: 15px 30px; text-decoration: none; font-weight: bold; display: inline-block;">DOWNLOAD FULL BLUEPRINT</a>
                  </p>
                  <footer style="margin-top: 60px; font-size: 10px; color: #999; text-align: center; text-transform: uppercase; letter-spacing: 2px;">
                    Evans Mathibe Agency | Sandton | Midrand | Cape Town | Polokwane
                  </footer>
                </div>
              `
            }),
          });
        }

        return new Response(JSON.stringify({ success: true, message: "Lead captured and blueprint sent" }), {
          status: 200,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });

      } catch (err) {
        return new Response(JSON.stringify({ error: "Invalid request payload or server error" }), {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }
    }

    return new Response("Method not allowed", { status: 405 });
  }
};
