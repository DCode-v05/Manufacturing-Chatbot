# Manufacturing-Chatbot

**A shop-floor chatbot that answers questions about machine status, orders, SOPs and safety, using a factory knowledge base and live status data.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![Google Gemini](https://img.shields.io/badge/Google%20Gemini%202.5%20Flash-8E75B2?style=flat&logo=googlegemini&logoColor=white) ![React](https://img.shields.io/badge/React%2018-20232A?style=flat&logo=react&logoColor=61DAFB) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) ![Uvicorn](https://img.shields.io/badge/Uvicorn-2C3E50?style=flat&logo=gunicorn&logoColor=white)

## Overview

Manufacturing-Chatbot is a full-stack chatbot for people working a factory floor: operators, maintenance engineers, QC and plant managers. Instead of digging through binders of SOPs or asking a supervisor for the status of a machine, you ask a question in plain English and get a short answer back.

A manufacturing assistant has to deal with two kinds of information. The static kind is shift schedules, emergency shutdown procedures, QC tolerances and the escalation matrix. The live kind is whether machine A3 is down right now or where order 101 is in the pipeline. This project handles both. Answers are grounded in a factory knowledge document, and when a question mentions a specific machine or order, the backend looks up that record's status and adds it to the prompt before the model replies.

I built this during my AI Engineering internship at September Platforms (September AI). The backend is FastAPI, handling prompt building, profiling, caching and the safety check, and it calls Google Gemini 2.5 Flash. The chat UI is React 18. The repo used to be called Inventory-Assistance, which was a misleading name: it is a manufacturing assistant, not an inventory system.

## Key Features

- **Knowledge-grounded answers**: responses are limited to a factory knowledge base (`context_doc.md`) covering the machine directory, status codes, shift schedules, start/end-of-shift procedures, safety SOPs (emergency shutdown, fire response), maintenance flows, QC acceptance criteria and the escalation matrix. The system prompt tells the model to say the information is not in the knowledge base rather than guess.
- **Live status injection**: the chat endpoint scans each message for known machine IDs (A1, A2, A3, B5, B7, C2) and order IDs (101 to 105). If it finds one, it looks up the current record and adds it to the prompt, so the model answers from that status and not only from the static doc.
- **Direct lookup endpoints**: `GET /workflow/machine/{id}`, `GET /workflow/order/{id}` and `GET /workflow/safety` return machine status, order status and active safety alerts without calling the LLM.
- **User profiling**: when someone introduces themselves ("I'm Ravi, a maintenance engineer on Shift B, I handle A3"), the backend extracts name, role, shift, shift time, machines and orders from the text and stores a profile. The profile is added to later prompts so answers can reference the user's role and machines. Asking "who's working in the factory?" returns the stored profiles.
- **Conversation memory**: a per-user conversation cache keeps the last 5 messages for follow-up questions, alongside a rolling context window that feeds recent turns to the model.
- **Response caching**: normalised queries are cached for 5 minutes. Repeated questions return instantly and are flagged as cached in the UI.
- **Batch queries**: a `/batch/multi` endpoint takes a list of questions and answers them in one compact model call, checking the cache per question so already-answered items are skipped.
- **Safety filter**: a keyword check rejects clearly harmful or off-topic requests before they reach the model.
- **Token logging**: middleware estimates input tokens per request, records latency, writes a `token_logs.csv` log, and returns `X-Token-Estimate-In` / `X-Process-Time` response headers.
- **React chat UI**: markdown-rendered replies (GitHub-flavored), suggested quick questions, a typing indicator, a cached-response badge and auto-scroll.

## How It Works

A FastAPI backend does the processing and a React frontend handles the chat. Gemini is accessed with a Google Cloud service account rather than a bare API key.

### Request flow (the `/chat` endpoint)

Every message goes through the same pipeline:

1. **Profile detection**: the message is checked for introduction phrases ("my name is", "i'm", "i am", "remember:"). If it is an intro, name/role/shift/machines/orders are extracted with string and regex parsing, saved to an in-memory profile store, and the request returns a short acknowledgment without calling the model.
2. **Safety check**: the normalised text is run against a keyword blocklist. Disallowed content returns an `unsafe_query` error and never reaches the model.
3. **Cache check**: the normalised query is looked up in a response cache (5-minute TTL). A hit returns immediately with `cached: true`.
4. **Live-data enrichment**: the message is scanned for machine IDs and order IDs, and matching records from `machines.json` / `orders.json` are added to the prompt. Questions about "who's working" or "personnel" pull in the stored user profiles.
5. **Context assembly**: the user's saved profile, the last 5 conversation turns, the full knowledge base and any live data are combined into one system prompt that tells the model to stay concise (2-4 sentences, bullets for lists).
6. **Generation**: the assembled messages plus a rolling history window are sent to Gemini 2.5 Flash.
7. **Persistence**: the reply is added to the context window, written to the response cache, and appended to the conversation cache before it is returned.

### Retrieval and grounding

There is no vector store. The knowledge base is small enough that the whole document (`context_doc.md`) is loaded once at startup and put into the prompt, so retrieval is just "always include the doc". The live part works differently: the backend matches machine and order IDs and injects the matched records as `CURRENT MACHINE STATUS` / `CURRENT ORDER STATUS` blocks. That keeps the static and live data separate in the prompt and lets the model prefer the live data when it exists. Batch prompts use a trimmed 3,000-character version of the knowledge base to keep token counts down.

### Gemini integration

`gemini_service.py` wraps `google-generativeai`. It flattens the role/parts message array into a single text prompt and calls `gemini-2.5-flash`. Authentication is in `google_auth.py`, which loads a Google Cloud service-account credential scoped to `generative-language` and configures the SDK at import time. Model errors are caught and returned as a readable string instead of crashing the request.

### Memory: profiles, conversation cache, context window

There are three layers of state, all in memory and lost on restart:

- **User profiles**: keyed by `user_id` and merged on update (lists like machines are de-duplicated, non-empty fields overwrite). They are formatted into a `USER:/ROLE:/SHIFT:/SUPERVISES:` block for the prompt.
- **Conversation cache**: a `deque(maxlen=5)` per user with a 30-minute TTL, so only recent turns are kept and stale sessions expire.
- **Context window**: a `ContextManager` holding the last 6 messages (4 for batch) in Gemini's role/parts shape, dropping the oldest when full.

### Token logging middleware

A Starlette `BaseHTTPMiddleware` wraps every request. It reads the body, estimates input tokens with a words-to-tokens heuristic (about 1 token per 0.75 words), measures processing time, appends a row to `token_logs.csv`, and adds `X-Token-Estimate-In` and `X-Process-Time` headers to the response.

### Frontend

A single-page React 18 app (Create React App). `ChatPage` holds the message list, posts to `POST /chat/` through an axios service layer, and renders replies with `react-markdown` + `remark-gfm`. It shows a typing indicator while waiting, a "Cached Response" badge when the backend served from cache, and a set of suggested questions ("What's the status of machine A3?", "Show me order 101 status"). The dev server proxies API calls to `http://localhost:8000`, and the backend only allows CORS from `http://localhost:3000`.

### Limitations

- Machine and order data is a static JSON sample, so "live" status is only as live as those files.
- The safety filter is a keyword list.
- There are no tests.

## Tech Stack

- **Languages:** Python, JavaScript (plus HTML/CSS)
- **Backend:** FastAPI, Uvicorn, Starlette middleware
- **AI / model:** Google Gemini 2.5 Flash via `google-generativeai`
- **Auth:** Google Cloud service account (`google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`), `python-dotenv`
- **Frontend:** React 18, React Router DOM, axios, react-markdown, remark-gfm, react-scripts
- **Data:** JSON status stores and a markdown knowledge base (no external database)

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+ and npm
- A Google Cloud project with the Gemini / Generative Language API enabled, and a service-account JSON key

### Installation

```bash
git clone https://github.com/DCode-v05/Manufacturing-Chatbot.git
cd Manufacturing-Chatbot

# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

### Credentials

`service_account.json` is gitignored. Create a Google Cloud service account, download its JSON key, rename it to `service_account.json`, and put it in the project root (next to `requirements.txt`). The backend loads it on startup.

### Running

Start the backend from the project root:

```bash
uvicorn app.main:app --reload
# API on http://localhost:8000  (interactive docs at /docs)
```

Start the frontend in a second terminal:

```bash
cd frontend
npm start
# UI on http://localhost:3000
```

## Usage

1. **Introduce yourself** (optional but useful): "I'm Ravi, a maintenance engineer on Shift B." The bot saves your profile and uses it in later answers.
2. **Ask questions** about anything in the knowledge base or the live data:
   - Machine status: *"What's the status of machine A3?"*
   - Order tracking: *"Show me order 101 status"*
   - Procedures: *"What is the emergency shutdown procedure?"*
   - Shifts / safety: *"When does Shift B start?"*, *"What are the safety procedures?"*
3. **Read the reply**: answers are short and bulleted, based on the knowledge base and, when relevant, live machine/order data.

You can also call the API directly:

```bash
# Chat
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "status of machine A3", "user_id": "ravi"}'

# Direct status lookups (no LLM)
curl http://localhost:8000/workflow/machine/A3
curl http://localhost:8000/workflow/order/101
curl http://localhost:8000/workflow/safety

# Batch
curl -X POST http://localhost:8000/batch/multi \
  -H "Content-Type: application/json" \
  -d '{"messages": ["status of A3", "sop for shutdown", "order 101 status"]}'
```

## Project Structure

```
Manufacturing-Chatbot/
├── app/
│   ├── main.py                       # FastAPI app: CORS, middleware, routers
│   ├── data/
│   │   ├── context_doc.md            # Factory knowledge base (SOPs, safety, QC, shifts)
│   │   ├── context_doc_loader.py     # Loads full + trimmed knowledge base
│   │   ├── machines.json             # Machine status store (A1, A2, A3, B5, B7, C2)
│   │   └── orders.json               # Order status store (101-105)
│   ├── routers/
│   │   ├── chat.py                   # Main pipeline: profile, safety, cache, enrich, generate
│   │   ├── workflow.py               # Machine / order / safety-alert endpoints
│   │   └── batch.py                  # Multi-question batched generation
│   ├── services/
│   │   ├── gemini_service.py         # Gemini 2.5 Flash call wrapper
│   │   ├── google_auth.py            # Service-account auth for the model
│   │   ├── user_profile_service.py   # Extract / store / format user profiles
│   │   ├── cache_service.py          # Response + conversation caches with TTLs
│   │   ├── context_manager.py        # Rolling message-history window
│   │   ├── workflow_service.py       # Machine / order lookups from JSON
│   │   └── safety_filter.py          # Keyword blocklist
│   ├── middleware/
│   │   └── token_logger.py           # Token estimate + latency logging
│   └── utils/
│       └── tokenizer.py              # Word-based token estimator
├── frontend/
│   ├── public/index.html
│   └── src/
│       ├── App.js                    # Layout shell
│       ├── pages/ChatPage.js         # Chat UI, quick questions, markdown render
│       └── services/api.js           # axios calls to chat / workflow / batch
├── requirements.txt                  # Python deps
└── README.md
```

`token_logs.csv` is generated at runtime and is not tracked in the repo.

---

## Contact

<table>
  <tr><td><b>Portfolio:</b> <a href="https://www.denistan.me">Denistan</a></td><td><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/denistanb">denistanb</a></td></tr>
  <tr><td><b>GitHub:</b> <a href="https://github.com/DCode-v05">DCode-v05</a></td><td><b>LeetCode:</b> <a href="https://leetcode.com/u/Denistan_B">Denistan_B</a></td></tr>
  <tr><td colspan="2" align="center"><b>Email:</b> <a href="mailto:denistanb05@gmail.com">denistanb05@gmail.com</a></td></tr>
</table>

Made with ❤️ by **Denistan B**
