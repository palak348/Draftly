
<p align="center">
  <h1 align="center">✍️ Draftly</h1>
  <p align="center"><strong>AI-powered blog writing agent — from idea to research-grade article in seconds.</strong></p>
</p>

---

## ⚡ Features

- 🧠 **Multi-Agent Pipeline** — Router → Research → Planner → Parallel Writers → Merger
- 🔍 **Auto Web Research** — Real-time Tavily search with source citation
- ⚡ **Parallel Writing** — LangGraph fan-out workers write sections simultaneously
- 🎯 **Platform-Aware** — Adapts tone and length for Medium, Dev.to, LinkedIn
- 📄 **Export** — Copy, download `.md`, or save as PDF
- 🔗 **Source Linking** — Research sources cited and linked in the blog
- 💾 **Smart Caching** — 24h file-based cache on research results to save API calls

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python · FastAPI · LangGraph · OpenRouter |
| **Frontend** | Next.js 16 · React 19 · Tailwind CSS v4 · Framer Motion |
| **LLMs** | Gemini 2.0 Flash · Llama 3.3 70B (via OpenRouter) |
| **Research** | Tavily Search API |

---

## 🏗️ Architecture

```
Topic → Router → Research (Tavily) → Planner → Workers (parallel) → Merger → Final Blog
```

---

## 📁 Project Structure

```
Draftly/
├── backend/
│   └── src/
│       ├── app.py            # FastAPI server
│       ├── main.py           # CLI interface
│       ├── config.py         # Configuration
│       ├── core/
│       │   ├── blog_agent.py # LangGraph agent workflow
│       │   └── llm_client.py # OpenRouter client
│       ├── prompts/          # LLM system prompts
│       └── utils/            # Logging, caching, helpers
├── frontend/
│   ├── app/                  # Pages & styles
│   ├── components/           # UI components
│   └── lib/                  # API client
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+ · Node.js 18+
- [OpenRouter](https://openrouter.ai/) API key
- [Tavily](https://tavily.com/) API key

### Installation

```bash
# Clone
git clone https://github.com/yourusername/Draftly.git
cd Draftly

# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env          # Add API keys
uvicorn src.app:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | LLM access via OpenRouter |
| `TAVILY_API_KEY` | Web research via Tavily |

---

## 🔮 What's Next

- [ ] Streaming response (SSE) for real-time writing
- [ ] User authentication and blog history
- [ ] Direct publish to Medium / Dev.to via API
- [ ] SEO score analysis
- [ ] Multi-language support

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
