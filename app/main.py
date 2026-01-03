from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, workflow, batch
from app.middleware.token_logger import TokenLoggerMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TokenLoggerMiddleware)
app.include_router(chat.router)
app.include_router(workflow.router)
app.include_router(batch.router)
