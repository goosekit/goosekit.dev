#!/bin/bash
DEPLOY_DIR="/tmp/goosekit-deploy"
BANNER_HTML='<div style="background:linear-gradient(90deg,#ff4800,#ff4800);padding:10px 16px;text-align:center;font-family:system-ui,sans-serif;font-size:0.85rem;color:#fff;font-weight:600;"><span>🚨 Ship It Kit Launch — €49 ends April 30</span> <a href="/ship-it-kit/" style="color:#fff;text-decoration:underline;margin-left:8px;">See the offer →</a></div>'
PAGES=("/json/" "/regex/" "/hash/" "/base64/" "/jwt/" "/screenshot/" "/index.html" "/blog/"/index.html "/tools/"/index.html)
for page in "${PAGES[@]}"; do
  f="$DEPLOY_DIR${page}"
  if [ -f "$f" ] && [ ! -d "$f" ]; then
    if ! grep -q "Ship It Kit Launch" "$f"; then
      sed -i.bak "s/<body>/<body>\n${BANNER_HTML}/" "$f"
      echo "Added banner to $f"
    else
      echo "Banner already in $f"
    fi
  fi
done
echo "Done."
