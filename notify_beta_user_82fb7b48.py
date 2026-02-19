#!/usr/bin/env python3
"""
Notify beta_user that Calculator v3 is deployed and live.
Conversation ID: 82fb7b48-9d5e-488c-9b5a-309bd1f154fc
"""

import subprocess
import sys

def notify_beta_user():
    """Send deployment notification to beta_user."""
    
    cmd = [
        "python3",
        "scripts/send.py",
        "--receiver", "beta_user",
        "--type", "Task",
        "--payload", '{"artifact":"projects/calculator-v3","url":"https://natovichat.github.io/calculator-v3/","conversation_id":"82fb7b48-9d5e-488c-9b5a-309bd1f154fc","status":"deployed"}',
        "--sender", "developer",
        "--conversation-id", "82fb7b48-9d5e-488c-9b5a-309bd1f154fc"
    ]
    
    print("📧 Notifying beta_user about calculator v3 deployment...")
    print(f"🌐 Live URL: https://natovichat.github.io/calculator-v3/")
    print(f"📦 Artifact: projects/calculator-v3")
    print(f"💬 Conversation: 82fb7b48-9d5e-488c-9b5a-309bd1f154fc")
    print()
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Beta user notified successfully!")
        print(result.stdout)
        
        # Play completion sound
        subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], 
                      stderr=subprocess.DEVNULL)
        return True
    else:
        print("⚠️ Notification failed:")
        print(result.stderr)
        return False

if __name__ == "__main__":
    success = notify_beta_user()
    sys.exit(0 if success else 1)
