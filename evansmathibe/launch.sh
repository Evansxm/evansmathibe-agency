#!/bin/bash
# Launch Google Sites Creation for Evans Mathibe

echo "Opening resources for Google Sites creation..."

# Open Google Sites
google-chrome "https://sites.google.com" &

# Wait a bit
sleep 2

# Open the guide
google-chrome "/home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md" &

sleep 1

# Open the landing page for reference
google-chrome "/home/ev/evansmathibe/index.html" &

echo ""
echo "All resources opened!"
echo ""
echo "NEXT STEPS:"
echo "1. Go to Google Sites and create a new site"
echo "2. Use the content from GOOGLE_SITES_GUIDE.md"
echo "3. Upload images from evansmathibe/assets/"
echo "4. Publish when ready"
echo ""
