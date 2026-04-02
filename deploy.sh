#!/bin/bash
# Evans Mathibe Agency - Deployment Sequence
echo "[1/4] Staging V2 Redesign..."
git add .
echo "[2/4] Committing Premium Brand Identity..."
git commit -m "V2 Redesign: Premium Creative & AI Automation Aesthetic"
echo "[3/4] Purging CDN Cache & Forcing Push..."
git push origin main --force
echo "[4/4] Sequence Complete. Live at https://evansxm.github.io/evansmathibe-agency/"
