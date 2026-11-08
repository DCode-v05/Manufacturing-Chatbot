from fastapi import APIRouter
from app.services.gemini_service import call_gemini
from app.services.context_manager import ContextManager
from app.services.cache_service import get_cache, set_cache, get_conversation_cache, add_to_conversation_cache
from app.services.safety_filter import check_safety
from app.services.workflow_service import get_machine_status, get_order_status
from app.services.user_profile_service import (
    extract_user_info, save_user_profile, get_user_profile, 
    format_user_context, format_all_profiles
)
import json

CONTEXT_DOC = open("app/data/context_doc.md", "r", encoding="utf-8").read()

router = APIRouter(prefix="/chat", tags=["chat"])
context = ContextManager()

@router.post("/")
async def chat_api(payload: dict):
    user_msg = payload["message"].strip()
    user_msg_normalized = user_msg.lower()
    user_id = payload.get("user_id", "default")

    user_profile_info = extract_user_info(user_msg)
    if user_profile_info:
        save_user_profile(user_id, user_profile_info)
        name = user_profile_info.get("name", "")
        role = user_profile_info.get("role", "")
        response = f"Profile saved: {name}" + (f", {role}" if role else "") + ". How can I help?"
        add_to_conversation_cache(user_id, "user", user_msg)
        add_to_conversation_cache(user_id, "assistant", response)
        return {"reply": response, "cached": False, "profile_updated": True}

    ok, reason = check_safety(user_msg_normalized)
    if not ok:
        return {
            "error": "unsafe_query",
            "reason": reason,
            "message": "Your query contains restricted or harmful content."
        }

    cached = get_cache(user_msg_normalized)
    if cached:
        conversation_history = get_conversation_cache(user_id)
        return {
            "reply": cached, 
            "cached": True,
            "conversation_history": conversation_history
        }

    real_time_data = ""
    
    machine_ids = ["a1", "a2", "a3", "b5", "b7", "c2"]
    for machine_id in machine_ids:
        if machine_id in user_msg_normalized:
            machine_data = get_machine_status(machine_id.upper())
            if "error" not in machine_data:
                real_time_data += f"\n\nCURRENT MACHINE STATUS - {machine_id.upper()}: {json.dumps(machine_data)}"
    
    order_ids = ["101", "102", "103", "104", "105"]
    for order_id in order_ids:
        if order_id in user_msg_normalized:
            order_data = get_order_status(order_id)
            if "error" not in order_data:
                real_time_data += f"\n\nCURRENT ORDER STATUS - {order_id}: {json.dumps(order_data)}"
    
    personnel_keywords = ["who", "working", "factory", "personnel", "employees", "staff", "people"]
    if any(keyword in user_msg_normalized for keyword in personnel_keywords):
        all_profiles = format_all_profiles()
        if "No user profiles" not in all_profiles:
            real_time_data += f"\n\n{all_profiles}"

    user_profile = get_user_profile(user_id)
    user_context = format_user_context(user_profile) if user_profile else ""
    
    conversation_history = get_conversation_cache(user_id)
    conversation_context = ""
    if conversation_history:
        conversation_context = "\n\nRECENT CONVERSATION:\n"
        for msg in conversation_history[-5:]:
            role = msg.get("role", "user").upper()
            text = msg.get("message", "")[:150]
            conversation_context += f"{role}: {text}\n"

    system_prompt = {
        "role": "user",
        "parts": [{
            "text": f"""You are a manufacturing assistant. Be CONCISE and DIRECT.

RULES:
- Keep responses SHORT (2-4 sentences max)
- Use bullet points for lists
- No unnecessary explanations
- Prioritize recent conversation context

{user_context}

{conversation_context}

KNOWLEDGE BASE:
{CONTEXT_DOC}{real_time_data}

IMPORTANT: Use real-time data when available. Reference user's role and previous context."""
        }]
    }

    context.add("user", user_msg)
    messages = [system_prompt] + context.get()

    reply = await call_gemini(messages)

    context.add("assistant", reply)
    set_cache(user_msg_normalized, reply)
    
    add_to_conversation_cache(user_id, "user", user_msg)
    add_to_conversation_cache(user_id, "assistant", reply)

    conversation_history = get_conversation_cache(user_id)
    return {
        "reply": reply, 
        "cached": False,
        "conversation_history": conversation_history
    }
