# Inventory-Assistance

A chatbot for factory-floor staff (operators, maintenance, QC, managers). You ask in plain English about machine status, orders, shift schedules, SOPs or safety, and it answers from a factory knowledge document plus the live status of any machine or order you mention. The backend is FastAPI calling Gemini 2.5 Flash, the UI is React.

I built it during my AI engineering internship at September AI. The repo name is a leftover; it is a manufacturing assistant, not an inventory system.

## How it works

`POST /chat/` runs a fixed pipeline for each message (`app/routers/chat.py`):

1. **Profile detection.** Messages like "I'm Ravi, a maintenance engineer on Shift B" are parsed for name, role, shift, machines and orders, saved to an in-memory profile, and acknowledged without calling the model.
2. **Safety filter.** A keyword blocklist (`safety_filter.py`) rejects clearly unsafe or off-topic requests before they reach the model.
3. **Cache.** Normalised queries are cached for 5 minutes. A hit returns immediately with `cached: true`.
4. **Live data.** The message is scanned for machine IDs (A1, A2, A3, B5, B7, C2) and order IDs (101 to 105). Matching records from `app/data/machines.json` and `orders.json` are added to the prompt. Asking who is working pulls the stored profiles.
5. **Prompt assembly.** The user's profile, the last 5 turns, the whole knowledge base (`app/data/context_doc.md`) and any live data go into one system prompt. The prompt tells the model to answer briefly and to say when something is not in the knowledge base.
6. **Generation.** The prompt plus a rolling window of recent messages goes to `gemini-2.5-flash`.
7. **Persistence.** The reply goes into the context window, the response cache and the per-user conversation cache (30 minute TTL).

There is no vector store. The knowledge base is small enough to include in full on every call; batch requests use a trimmed 3,000 character version.

Other endpoints:

- `GET /workflow/machine/{id}`, `GET /workflow/order/{id}`, `GET /workflow/safety`: direct lookups, no LLM.
- `POST /batch/multi`: several questions in one model call, skipping ones already cached.

Token logging middleware (`app/middleware/token_logger.py`) estimates input tokens from word count, writes a row per request to `token_logs.csv` and sets `X-Token-Estimate-In` and `X-Process-Time` headers.

All state (profiles, caches, context window) is in memory and is lost on restart.

## Tech stack

- Backend: Python 3.10+, FastAPI, Uvicorn
- Model: Gemini 2.5 Flash through `google-generativeai`, authenticated with a Google Cloud service account
- Frontend: React 18 (Create React App), axios, react-markdown, remark-gfm
- Data: JSON files and one markdown file, no database

## Setup

You need a Google Cloud project with the Generative Language API enabled. Create a service account, download its JSON key and save it as `service_account.json` in the repo root (it is gitignored).

```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

Run the backend from the repo root, then the frontend in a second terminal:

```bash
uvicorn app.main:app --reload     # http://localhost:8000, docs at /docs
cd frontend && npm start          # http://localhost:3000
```

CORS only allows `http://localhost:3000`.

Try the API directly:

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "status of machine A3", "user_id": "ravi"}'

curl http://localhost:8000/workflow/machine/A3

curl -X POST http://localhost:8000/batch/multi \
  -H "Content-Type: application/json" \
  -d '{"messages": ["status of A3", "sop for shutdown", "order 101 status"]}'
```

## Project structure

```
app/
  main.py          app, CORS, middleware, routers
  routers/         chat, workflow, batch
  services/        gemini, auth, profiles, caches, context window, workflow lookups, safety filter
  middleware/      token logger
  utils/           token estimator
  data/            context_doc.md, machines.json, orders.json, loader
frontend/src/      ChatPage, App, api client
```

## Limitations

- Machine and order data is a static JSON sample, so "live" status is only as live as those files.
- The safety filter is a keyword list.
- There are no tests.
