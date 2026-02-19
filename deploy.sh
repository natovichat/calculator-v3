#!/bin/bash
# Deploy Calculator v3 to GitHub Pages

set -e

cd /Users/aviad.natovich/personal/agents-system/projects/calculator-v3

echo "🚀 Deploying Calculator v3 to GitHub Pages..."

# Initialize git if not already
if [ ! -d .git ]; then
    git init
fi

# Add and commit files
git add .
git commit -m "Calculator v3 web app with modern UI" || echo "No changes to commit"

# Delete existing repo if it exists (fresh start)
gh repo delete natovichat/calculator-v3 --yes 2>/dev/null || true

# Create new repo and push
echo "📦 Creating GitHub repository..."
gh repo create natovichat/calculator-v3 --public --source=. --remote=origin --push

# Enable GitHub Pages
echo "🌐 Enabling GitHub Pages..."
gh api repos/natovichat/calculator-v3/pages --method POST \
  --field 'source[branch]=main' --field 'source[path]=/'

# Wait for GitHub Pages to deploy
echo "⏳ Waiting for GitHub Pages deployment (60 seconds)..."
sleep 60

# Check deployment status
echo "✅ Checking deployment status..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://natovichat.github.io/calculator-v3/)
echo "   HTTP Status: $STATUS"

if [ "$STATUS" = "200" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 Live URL: https://natovichat.github.io/calculator-v3/"
    echo "📦 Repository: https://github.com/natovichat/calculator-v3"
    echo ""
else
    echo ""
    echo "⚠️  Deployment may still be in progress (Status: $STATUS)"
    echo "🌐 URL: https://natovichat.github.io/calculator-v3/"
    echo "   Please wait a few more minutes and check the URL"
    echo ""
fi

# Send completion message to beta_user
echo "📨 Sending task to beta_user for testing..."
python3 /Users/aviad.natovich/personal/agents-system/scripts/send.py \
  --receiver beta_user \
  --type Task \
  --payload '{"artifact":"projects/calculator-v3","url":"https://natovichat.github.io/calculator-v3/","conversation_id":"82fb7b48-9d5e-488c-9b5a-309bd1f154fc"}' \
  --sender architect \
  --conversation-id 82fb7b48-9d5e-488c-9b5a-309bd1f154fc

echo "✅ Deployment complete!"
