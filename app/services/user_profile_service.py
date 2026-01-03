import json
import time
from typing import Optional, Dict

USER_PROFILES = {}  # In-memory storage: {user_id: {profile_data}}

def extract_user_info(message: str) -> Optional[Dict]:
    """Extract user profile information from introduction messages"""
    msg_lower = message.lower()
    
    # Check if it's an introduction message
    intro_keywords = ["my name is", "i'm", "i am", "store this about me", "remember:", "my details:"]
    if not any(keyword in msg_lower for keyword in intro_keywords):
        return None
    
    profile = {
        "name": None,
        "role": None,
        "shift": None,
        "machines": [],
        "responsibilities": [],
        "preferences": [],
        "timestamp": time.time()
    }
    
    # Extract name
    try:
        if "my name is" in msg_lower:
            parts = message.split("my name is", 1)
            if len(parts) > 1:
                name_part = parts[1].split(".", 1)[0].strip()
                profile["name"] = name_part.split(",")[0].strip()
        elif "i'm" in msg_lower or "i am" in msg_lower:
            for split_text in ["i'm", "i am"]:
                if split_text in msg_lower:
                    parts = message.lower().split(split_text, 1)
                    if len(parts) > 1:
                        # Get the original case version
                        idx = message.lower().index(split_text) + len(split_text)
                        rest = message[idx:].strip()
                        first_part = rest.split(",")[0].split(".")[0].strip()
                        # Check if it's a name (has uppercase letters)
                        if any(char.isupper() for char in first_part):
                            profile["name"] = first_part
                            break
    except (IndexError, ValueError):
        pass  # Skip name extraction if parsing fails
    
    # Extract role/position
    try:
        roles = ["supervisor", "manager", "technician", "engineer", "officer", "coordinator", "operator"]
        for role in roles:
            if role in msg_lower:
                # Find the phrase containing the role
                idx = msg_lower.find(role)
                if idx != -1:
                    # Get surrounding context (20 chars before, 30 after)
                    start = max(0, idx - 20)
                    end = min(len(message), idx + len(role) + 30)
                    role_context = message[start:end].strip()
                    # Clean up the role context
                    for sep in [",", ".", "\n"]:
                        if sep in role_context:
                            role_context = role_context.split(sep)[0].strip()
                    profile["role"] = role_context
                    break
    except (IndexError, ValueError):
        pass  # Skip role extraction if parsing fails
    
    # Extract shift
    try:
        shifts = ["shift a", "shift b", "shift c", "morning shift", "evening shift", "night shift"]
        for shift in shifts:
            if shift in msg_lower:
                profile["shift"] = shift.title()
                break
    except (IndexError, ValueError):
        pass
    
    # Extract time ranges
    try:
        import re
        time_pattern = r'\d{1,2}:\d{2}\s*[AP]M\s*[-–]\s*\d{1,2}:\d{2}\s*[AP]M'
        time_matches = re.findall(time_pattern, message, re.IGNORECASE)
        if time_matches:
            profile["shift_time"] = time_matches[0]
    except (IndexError, ValueError, AttributeError):
        pass
    
    # Extract machines
    try:
        machine_ids = ["a1", "a2", "a3", "b5", "b7", "c2"]
        for machine in machine_ids:
            if machine in msg_lower:
                profile["machines"].append(machine.upper())
    except (IndexError, ValueError):
        pass
    
    # Extract orders
    try:
        import re
        order_pattern = r'\b(?:orders?|order)\s*(\d{3}(?:\s*[-,]\s*\d{3})*)'
        order_matches = re.findall(order_pattern, msg_lower)
        if order_matches:
            profile["orders"] = order_matches
    except (IndexError, ValueError, AttributeError):
        pass
    
    return profile if profile["name"] or profile["role"] else None


def save_user_profile(user_id: str, profile_data: Dict):
    """Save or update user profile"""
    if user_id in USER_PROFILES:
        # Merge with existing profile
        existing = USER_PROFILES[user_id]
        for key, value in profile_data.items():
            if value:  # Only update non-empty values
                if isinstance(value, list) and key in existing:
                    # Merge lists
                    existing[key] = list(set(existing[key] + value))
                else:
                    existing[key] = value
        existing["timestamp"] = time.time()
    else:
        USER_PROFILES[user_id] = profile_data


def get_user_profile(user_id: str) -> Optional[Dict]:
    """Retrieve user profile"""
    return USER_PROFILES.get(user_id)


def get_all_user_profiles() -> Dict:
    """Get all stored user profiles"""
    return USER_PROFILES


def format_all_profiles() -> str:
    """Format all user profiles for display"""
    if not USER_PROFILES:
        return "No user profiles stored yet."
    
    profiles_text = "STORED USER PROFILES:\n"
    for user_id, profile in USER_PROFILES.items():
        name = profile.get("name", "Unknown")
        role = profile.get("role", "No role specified")
        shift = profile.get("shift", "") or profile.get("shift_time", "")
        machines = ", ".join(profile.get("machines", []))
        
        profiles_text += f"\n• {name}"
        if role:
            profiles_text += f" - {role}"
        if shift:
            profiles_text += f" ({shift})"
        if machines:
            profiles_text += f" | Machines: {machines}"
    
    return profiles_text


def format_user_context(profile: Dict) -> str:
    """Format user profile into context string for AI"""
    if not profile:
        return ""
    
    context_parts = []
    
    if profile.get("name"):
        context_parts.append(f"USER: {profile['name']}")
    if profile.get("role"):
        context_parts.append(f"ROLE: {profile['role']}")
    if profile.get("shift") or profile.get("shift_time"):
        shift_info = profile.get("shift", "") + (" " + profile.get("shift_time", "")).strip()
        context_parts.append(f"SHIFT: {shift_info}")
    if profile.get("machines"):
        context_parts.append(f"SUPERVISES: Machines {', '.join(profile['machines'])}")
    if profile.get("orders"):
        context_parts.append(f"ORDERS: {', '.join(profile['orders'])}")
    if profile.get("preferences"):
        context_parts.append(f"PREFERENCES: {', '.join(profile['preferences'])}")
    
    return "\n".join(context_parts) if context_parts else ""


def clear_user_profile(user_id: str):
    """Clear user profile"""
    if user_id in USER_PROFILES:
        del USER_PROFILES[user_id]
