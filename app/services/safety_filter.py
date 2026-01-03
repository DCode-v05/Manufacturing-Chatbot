BAD_KEYWORDS = ["bomb", "attack", "kill", "weapon", "hack", "exploit"]

def check_safety(text: str):
    t = text.lower()
    for k in BAD_KEYWORDS:
        if k in t:
            return False, f"Request contains disallowed content: {k}"
    return True, ""
