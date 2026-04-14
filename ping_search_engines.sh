#!/bin/bash
SITEMAP_URL="https://evansxm.github.io/evansmathibe-agency/sitemap.xml"
echo "Starting sitemap submission for Evans Mathibe Agency"
curl -s "https://www.google.com/ping?sitemap=$SITEMAP_URL" > /dev/null
echo "Google has been notified"
curl -s "https://www.bing.com/ping?sitemap=$SITEMAP_URL" > /dev/null
echo "Bing has been notified"
echo "Search engines successfully pinged"
