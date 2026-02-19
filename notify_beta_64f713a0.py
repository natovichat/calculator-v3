#!/usr/bin/env python3
"""Notify beta_user about calculator-v3 completion."""

import sys
from pathlib import Path

# Add project root to path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

import redis
from src.models.message import Message, MessageType

def main():
    """Send completion notification to beta_user."""
    
    payload = {
        "artifact": "projects/calculator-v3",
        "url": "https://natovichat.github.io/calculator-v3/",
        "conversation_id": "64f713a0-1d01-4446-8ec3-3d510b89ac6c"
    }
    
    msg = Message(
        type=MessageType.Task,
        sender_id="developer",
        receiver_id="beta_user",
        conversation_id="64f713a0-1d01-4446-8ec3-3d510b89ac6c",
        payload=payload
    )
    
    try:
        r = redis.from_url("redis://localhost:6379/0")
        r.xadd("agent.bus", msg.to_redis_dict(), "*")
        print("✅ Notification sent to beta_user")
        print(f"🌐 URL: {payload['url']}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
