export default {
  async fetch(request, env, ctx) {
    // Handle Preflight CORS requests from the web frontend
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        }
      });
    }

    if (request.method === "POST") {
      try {
        const data = await request.json();
        const email = data.email;

        if (!email) {
          return new Response(JSON.stringify({ error: "Email is required" }), {
            status: 400,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
          });
        }

        // Write lead record securely to storage
        await env.LEADS_KV.put(`lead:${email}`, JSON.stringify({
          email: email,
          timestamp: new Date().toISOString(),
          source: "sales_tunnel_sa"
        }));

        return new Response(JSON.stringify({ success: true, message: "Lead captured safely" }), {
          status: 200,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: "Invalid request payload" }), {
          status: 400,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }
    }

    return new Response("Method not allowed", { status: 405 });
  }
};
