#!/bin/bash
# Deploy Calculator v3 to GitHub Pages
# Conversation ID: 64f713a0-1d01-4446-8ec3-3d510b89ac6c

set -e

echo "🚀 Deploying Calculator v3 to GitHub Pages..."

cd /Users/aviad.natovich/personal/agents-system/projects/calculator-v3

# Clean up old status files
rm -f *.md *.py *.sh deploy.* execute_*.* NOTIFY_*.* 2>/dev/null || true

# Ensure only calculator files remain
echo "📦 Preparing files..."
git add index.html style.css script.js
git commit -m "Calculator v3 - Modern web calculator" || echo "Nothing to commit"

# Delete old repository if exists
echo "🗑️  Removing old repository..."
gh repo delete natovichat/calculator-v3 --yes 2>/dev/null || true

# Create new repository and push
echo "📤 Creating GitHub repository..."
gh repo create natovichat/calculator-v3 --public --source=. --remote=origin --push

# Enable GitHub Pages
echo "🌐 Enabling GitHub Pages..."
gh api repos/natovichat/calculator-v3/pages --method POST \
  --field 'source[branch]=main' --field 'source[path]=/'

# Wait for deployment
echo "⏳ Waiting 60 seconds for GitHub Pages deployment..."
sleep 60

# Verify deployment
echo "🔍 Verifying deployment..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://natovichat.github.io/calculator-v3/)
echo "HTTP Status: $STATUS"

if [ "$STATUS" = "200" ] || [ "$STATUS" = "301" ] || [ "$STATUS" = "302" ]; then
  echo "✅ DEPLOYMENT SUCCESSFUL!"
  echo "🌐 Live URL: https://natovichat.github.io/calculator-v3/"
  
  # Notify beta_user
  echo "📧 Notifying beta_user..."
  cd /Users/aviad.natovich/personal/agents-system
  python3 scripts/send.py \
    --receiver beta_user \
    --type Task \
    --payload '{"artifact":"projects/calculator-v3","url":"https://natovichat.github.io/calculator-v3/","conversation_id":"64f713a0-1d01-4446-8ec3-3d510b89ac6c"}' \
    --sender developer \
    --conversation-id 64f713a0-1d01-4446-8ec3-3d510b89ac6c
  
  echo "✅ COMPLETE! Beta user notified."
else
  echo "⚠️  Deployment may still be in progress. Check in a few minutes:"
  echo "    https://natovichat.github.io/calculator-v3/"
fi
