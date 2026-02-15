# ⚙️ Draftly — Backend

FastAPI + LangGraph multi-agent blog generation engine.

---

## 🚀 Setup

```bash
pip install -r requirements.txt
cp .env.example .env          # Add API keys
```

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | LLM access via OpenRouter |
| `TAVILY_API_KEY` | Web research via Tavily |

## ▶️ Run

```bash
# API Server
uvicorn src.app:app --reload --port 8000

# CLI (standalone)
python -m src.main --topic "Your Topic" --platform medium
```

---

## 📡 API

### `POST /generate-blog`

```json
{
  "topic": "Microservices Design Patterns",
  "platform": "medium",
  "enable_research": true
}
```

**Response:** `{ title, content, word_count, sections, platform, topic }`

### `GET /health` → `{ "status": "ok" }`

---

## 🧠 Agent Flow

```
Router (Llama 3.3) → Research (Tavily) → Planner (Gemini 2.0) → Workers (parallel) → Merger
```

## 🎯 Platforms

| Platform | Words | Tone |
|----------|-------|------|
| `generic` | 1500–2500 | Balanced |
| `medium` | 1500–3000 | Conversational |
| `devto` | 1000–2000 | Technical |
| `linkedin` | 800–1500 | Professional |

---

## 📁 Structure

```
src/
├── app.py            # FastAPI endpoints
├── main.py           # CLI interface
├── config.py         # Models, keys, platform settings
├── core/
│   ├── blog_agent.py # LangGraph workflow
│   └── llm_client.py # OpenRouter client (retry + fallback)
├── prompts/
│   └── system_prompts.py
└── utils/
    └── helpers.py    # Logging, cache, file I/O
```
