from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
from app.utils.tokenizer import estimate_tokens

class TokenLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        body = await request.body()
        try:
            import json
            j = json.loads(body) if body else {}
        except:
            j = {}
        user_text = j.get("message") or "" 
        if not user_text:
            msgs = j.get("messages", [])
            user_text = " ".join(msgs) if isinstance(msgs, list) else ""
        tokens_in = estimate_tokens(user_text)
        response = await call_next(request)
        process_time = time.time() - start
        response.headers["X-Token-Estimate-In"] = str(tokens_in)
        response.headers["X-Process-Time"] = str(process_time)
        with open("token_logs.csv", "a") as f:
            f.write(f"{time.time()},{request.url.path},{tokens_in},{process_time}\n")
        return response
