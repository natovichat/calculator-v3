#!/bin/bash
set -e

echo "🚀 Deploying Calculator v3 to GitHub Pages..."

cd /Users/aviad.natovich/personal/agents-system/projects/calculator-v3

# Add only the calculator files
git add index.html style.css script.js
git commit -m "Calculator v3 web app" || echo "No changes to commit"

# Delete existing repo if it exists
gh repo delete natovichat/calculator-v3 --yes 2>/dev/null || true

# Create new GitHub repo and push
gh repo create natovichat/calculator-v3 --public --source=. --remote=origin --push

# Enable GitHub Pages
gh api repos/natovichat/calculator-v3/pages --method POST \
  --field 'source[branch]=main' --field 'source[path]=/'

echo "⏳ Waiting 60 seconds for GitHub Pages to deploy..."
sleep 60

# Verify deployment
echo "🔍 Verifying deployment..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://natovichat.github.io/calculator-v3/)
echo "HTTP status: $STATUS"

if [ "$STATUS" = "200" ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Live URL: https://natovichat.github.io/calculator-v3/"
else
    echo "⚠️  Deployment may still be in progress. Status: $STATUS"
    echo "🌐 URL: https://natovichat.github.io/calculator-v3/"
fi
