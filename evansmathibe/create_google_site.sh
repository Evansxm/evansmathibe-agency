#!/bin/bash
# Complete Google Sites Creation - Non-Interactive
# Run this to open everything needed

echo "=========================================="
echo "🚀 EVANS MATHIBE - GOOGLE SITES CREATOR"
echo "=========================================="

echo ""
echo "📂 Opening all resources..."

# Open Google Sites
echo "   🌐 Opening Google Sites..."
google-chrome "https://sites.google.com" 2>/dev/null &
sleep 1

# Open the content guide
echo "   📄 Opening content guide..."
google-chrome "/home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md" 2>/dev/null &
sleep 1

# Open the HTML landing page
echo "   🎨 Opening landing page preview..."
google-chrome "/home/ev/evansmathibe/index.html" 2>/dev/null &
sleep 1

# Open the assets folder
echo "   🖼️ Opening assets folder..."
xdg-open "/home/ev/evansmathibe/assets" 2>/dev/null &

echo ""
echo "✅ All resources opened!"
echo ""
echo "=========================================="
echo "📋 STEP-BY-STEP INSTRUCTIONS"
echo "=========================================="
echo ""
echo "1. In Google Sites (first tab):"
echo "   → Click 'Create new site'"
echo "   → Choose 'Blank' template"
echo "   → Name: 'Evans Mathibe'"
echo ""
echo "2. Add Pages (left sidebar):"
echo "   → Home (already there)"
echo "   → About"
echo "   → Services"
echo "   → Experience"
echo "   → Testimonials"
echo "   → Contact"
echo ""
echo "3. Add Content (from guide):"
echo "   → Copy text from GOOGLE_SITES_GUIDE.md"
echo "   → Paste into each page"
echo ""
echo "4. Add Images:"
echo "   → Use files from assets/ folder"
echo ""
echo "5. Customize Theme:"
echo "   → Click paintbrush icon"
echo "   → Choose dark theme"
echo ""
echo "6. Publish:"
echo "   → Click 'Publish' (top right)"
echo "   → Choose URL: evansmathibe.site"
echo ""
echo "=========================================="
echo ""
echo "📁 Resources:"
echo "   Content: /home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md"
echo "   Images:  /home/ev/evansmathibe/assets/"
echo "   Preview: /home/ev/evansmathibe/index.html"
echo ""
echo "Press any key when done to save your URL..."
read -r

echo ""
echo "Enter your published site URL:"
read -r SITE_URL

if [ -n "$SITE_URL" ]; then
    echo "$SITE_URL" > /home/ev/evansmathibe/SITE_URL.txt
    echo "✅ URL saved to: /home/ev/evansmathibe/SITE_URL.txt"
    echo ""
    echo "🎉 Your site is live: $SITE_URL"
else
    echo "No URL entered. You can add it later."
fi

echo ""
echo "=========================================="
echo "Done! 🎉"
echo "=========================================="
