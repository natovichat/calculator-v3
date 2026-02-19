#!/bin/bash

# Navigate to calculator-v3 directory
cd "$(dirname "$0")"

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
fi

# Add all files
git add .

# Commit
git commit -m "Calculator web app v3" || true

# Delete existing repo if it exists
gh repo delete natovichat/calculator-v3 --yes 2>/dev/null || true

# Create new repo and push
gh repo create natovichat/calculator-v3 --public --source=. --remote=origin --push

# Enable GitHub Pages
gh api repos/natovichat/calculator-v3/pages --method POST \
  --field 'source[branch]=main' --field 'source[path]=/' 2>/dev/null || \
gh api repos/natovichat/calculator-v3/pages --method POST \
  --field 'source[branch]=master' --field 'source[path]=/' || true

echo "Deployment initiated. Waiting 60 seconds for GitHub Pages..."
sleep 60

# Check deployment status
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://natovichat.github.io/calculator-v3/)
echo "HTTP status: $STATUS"

if [ "$STATUS" = "200" ]; then
    echo "✅ Calculator v3 is live at https://natovichat.github.io/calculator-v3/"
else
    echo "⚠️ Deployment may still be processing. URL: https://natovichat.github.io/calculator-v3/"
fi
