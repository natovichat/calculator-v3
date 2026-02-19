#!/bin/bash
# Notify beta_user of completed calculator v3 deployment
# Conversation ID: 82fb7b48-9d5e-488c-9b5a-309bd1f154fc

python scripts/send.py --receiver beta_user --type Task \
  --payload '{"artifact":"projects/calculator-v3","url":"https://natovichat.github.io/calculator-v3/","conversation_id":"82fb7b48-9d5e-488c-9b5a-309bd1f154fc"}' \
  --sender developer \
  --conversation-id 82fb7b48-9d5e-488c-9b5a-309bd1f154fc

echo "✅ Notification sent to beta_user"
echo "🌐 Live URL: https://natovichat.github.io/calculator-v3/"
