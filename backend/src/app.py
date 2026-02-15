"""
FastAPI entry point for Blog Agent.
Exposes blog generation endpoint.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from config import load_config, validate_config, PLATFORM_CONFIGS
from core.blog_agent import create_blog_agent
from utils.helpers import setup_logging

# Initialize logging
setup_logging()

# Validate config on startup
api_config, _, _, _ = load_config()
valid, message = validate_config(api_config)
if not valid:
    raise RuntimeError(f"Configuration error: {message}")

# Initialize agent once (singleton)
agent = create_blog_agent()

app = FastAPI(
    title="Blog Writing Agent API",
    description="AI-powered multi-agent blog generation system",
    version="1.0.0"
)

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Request Schema ----------------

class BlogRequest(BaseModel):
    topic: str
    platform: Optional[str] = "generic"
    enable_research: bool = True


class BlogResponse(BaseModel):
    title: str
    content: str
    word_count: int
    sections: int
    platform: str
    topic: str


# ---------------- Health Check ----------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------- Generate Blog ----------------

@app.post("/generate-blog", response_model=BlogResponse)
def generate_blog(request: BlogRequest):

    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    platform = request.platform.lower()
    if platform not in PLATFORM_CONFIGS:
        platform = "generic"

    try:
        result = agent.invoke({
            "topic": request.topic,
            "platform": platform,
            "needs_research": request.enable_research,
            "mode": "",
            "queries": [],
            "evidence": [],
            "plan": None,
            "sections": [],
            "final_blog": "",
            "metadata": {}
        })

        metadata = result["metadata"]

        return BlogResponse(
            title=metadata["title"],
            content=result["final_blog"],
            word_count=metadata["word_count"],
            sections=metadata["sections"],
            platform=metadata["platform"],
            topic=metadata["topic"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
