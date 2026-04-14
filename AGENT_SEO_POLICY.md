# Autonomous Agent System Instructions: SEO Monitoring

The agent is tasked with maintaining search dominance for Evans Mathibe Agency through autonomous monitoring and indexing.

1. Monitoring Protocol:
   - Monitor the local repository for any changes to index.html, sitemap.xml, or metadata.
   - Periodically check for Google Search Console logs or crawl status updates.
   - Compare the current site state with the last known indexed state.

2. Trigger Mechanism:
   - If a discrepancy is detected (e.g., content updated but not yet recrawled), the agent must trigger the 'index-now.js' script.
   - The agent should execute 'node index-now.js' locally or verify the GitHub Action has completed.

3. Autonomous Execution:
   - No manual prompts are required for these checks.
   - The agent operates as a background observer and takes corrective action automatically to ensure the Google Index remains synchronized with the live repository.
