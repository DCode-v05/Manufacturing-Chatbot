import time
from collections import deque

CACHE = {}  # global shared dictionary
# Store conversation history per session/user
CONVERSATION_CACHE = {}  # key: session_id, value: {"messages": deque, "time": timestamp}

def get_cache(key: str):
    if key in CACHE:
        entry = CACHE[key]
        if time.time() - entry["time"] < 300:  # 5 minutes TTL
            return entry["value"]
        else:
            del CACHE[key]  # expired → remove
    return None

def set_cache(key: str, value: str):
    CACHE[key] = {
        "value": value,
        "time": time.time()
    }

def get_conversation_cache(session_id: str = "default"):
    """Get last 5 messages from conversation cache"""
    if session_id in CONVERSATION_CACHE:
        entry = CONVERSATION_CACHE[session_id]
        if time.time() - entry["time"] < 1800:  # 30 minutes TTL for conversations
            return list(entry["messages"])
        else:
            del CONVERSATION_CACHE[session_id]
    return []

def add_to_conversation_cache(session_id: str = "default", role: str = "user", message: str = ""):
    """Add message to conversation cache, keeping last 5 messages"""
    if session_id not in CONVERSATION_CACHE:
        CONVERSATION_CACHE[session_id] = {
            "messages": deque(maxlen=5),  # Automatically keeps only last 5
            "time": time.time()
        }
    
    CONVERSATION_CACHE[session_id]["messages"].append({
        "role": role,
        "message": message
    })
    CONVERSATION_CACHE[session_id]["time"] = time.time()

def clear_conversation_cache(session_id: str = "default"):
    """Clear conversation cache for a session"""
    if session_id in CONVERSATION_CACHE:
        del CONVERSATION_CACHE[session_id]
