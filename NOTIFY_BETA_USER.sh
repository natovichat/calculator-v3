#!/bin/bash
# Notification script for beta_user - Calculator v3 deployment
# Conversation ID: 64f713a0-1d01-4446-8ec3-3d510b89ac6c

cd /Users/aviad.natovich/personal/agents-system

python3 scripts/send.py \
  --receiver beta_user \
  --type Task \
  --payload '{"artifact":"projects/calculator-v3","url":"https://natovichat.github.io/calculator-v3/","status":"deployed","conversation_id":"64f713a0-1d01-4446-8ec3-3d510b89ac6c"}' \
  --sender developer \
  --conversation-id 64f713a0-1d01-4446-8ec3-3d510b89ac6c

echo ""
echo "✅ Notification sent to beta_user"
echo "📦 Artifact: projects/calculator-v3"
echo "🌐 URL: https://natovichat.github.io/calculator-v3/"
echo "🆔 Conversation: 64f713a0-1d01-4446-8ec3-3d510b89ac6c"
