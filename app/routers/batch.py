from fastapi import APIRouter
from typing import List
from app.services.gemini_service import call_gemini
from app.services.cache_service import get_cache, set_cache
from app.services.context_manager import ContextManager
from app.data import context_doc_loader

router = APIRouter(prefix="/batch", tags=["batch"])

ctx = ContextManager(max_messages=4)

@router.post("/multi")
async def batch_multi(payload: dict):
    """
    payload: { "messages": ["status of A3", "sop for shutdown", "order 101 status"] }
    returns: { "replies": [ "...", "...", "..." ] }
    """
    msgs: List[str] = payload.get("messages", [])
    replies = []
    to_call = []
    indexes_to_call = []

    for i, m in enumerate(msgs):
        c = get_cache(m)
        if c:
            replies.append(c)
        else:
            replies.append(None)
            to_call.append(m)
            indexes_to_call.append(i)

    if to_call:
        system_text = f"You are a manufacturing assistant. Use this doc:\n\n{context_doc_loader.CONTEXT_DOC_BRIEF}"
        combined = "Answer the following requests. Return JSON array string with one element per request in same order.\n\nRequests:\n"
        for idx, r in enumerate(to_call):
            combined += f"{idx+1}. {r}\n"

        messages = [
            {"role": "user", "parts": [{"text": system_text}]},
            {"role": "user", "parts": [{"text": combined}]}
        ]

        raw = await call_gemini(messages)
        import json, re
        try:
            arr = json.loads(raw)
        except Exception:
            m = re.search(r'(\[.*\])', raw, re.S)
            if m:
                arr = json.loads(m.group(1))
            else:
                arr = [s.strip() for s in raw.splitlines() if s.strip()]

        for j, ans in enumerate(arr):
            orig_index = indexes_to_call[j]
            replies[orig_index] = ans
            set_cache(to_call[j], ans)

    return {"replies": replies}