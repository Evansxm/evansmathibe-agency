#!/bin/bash

# Evans Mathibe Agency - V2 Final Deployment Script
# Senior DevOps & Creative Engineer Protocol

echo "--- STARTING HIGH-END DEPLOYMENT SEQUENCE ---"

# Root directory check
PROJECT_DIR="/home/ev/evansmathibe-agency/"
cd "$PROJECT_DIR" || exit

# Status check
echo "[1/4] Checking repository status..."
git status

# Stage all files including sitemap.xml and robots.txt
echo "[2/4] Staging production assets and SEO tools..."
git add .

# Final commit with branding-specific message
echo "[3/4] Committing the Creative Director Aesthetic (84.Paris inspired)..."
git commit -m "V2 Production: Creative Director Aesthetic - Immersive UX/UI Complete"

# Push to Live Repository
echo "[4/4] Final Push to GitHub Pages..."
git push origin main

echo "--- SEQUENCE COMPLETE. EVANS MATHIBE BRAND IDENTITY IS LIVE. ---"