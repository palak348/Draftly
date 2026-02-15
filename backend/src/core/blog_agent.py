import logging
from typing import TypedDict, List, Annotated, Optional, Any, cast
import operator
from datetime import date
from pathlib import Path
import os
import json

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage


from core.llm_client import LLMClient, generate_structured, create_client_for_task
from config import BlogConfig, PLATFORM_CONFIGS, APIConfig, ModelConfig
from utils.helpers import CacheManager, count_words

from prompts import system_prompts

logger = logging.getLogger(__name__)

llm_client = LLMClient()
cache = CacheManager()


# ---------------- STATE ----------------

class BlogState(TypedDict):
    topic: str
    platform: str

    needs_research: bool
    mode: str
    queries: List[str]

    evidence: List[dict]
    plan: Optional[dict]

    sections: Annotated[List[tuple[int, str]], operator.add]

    final_blog: str
    metadata: dict


# ---------------- ROUTER ----------------

def router_node(state: BlogState) -> dict:
    ctx = f"Topic: {state['topic']}\nPlatform: {state['platform']}\nDate: {date.today().isoformat()}\nResearch Requested: {state.get('needs_research')}"
    prompt = f"{system_prompts.ROUTER_PROMPT}\n\n{ctx}"

    decision = generate_structured(
        llm_client,
        [
            {"role": "system", "content": system_prompts.MASTER_BLOG_WRITER_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "{needs_research, mode, queries}"
    )

    # If user forced research, override the boolean but keep queries/mode
    if state.get("needs_research"):
        return {
            "needs_research": True,
            "mode": str(decision.get("mode", "research")), # default to research mode
            "queries": cast(List[str], decision.get("queries", []))
        }

    return {
        "needs_research": bool(decision.get("needs_research", False)),
        "mode": str(decision.get("mode", "closed_book")),
        "queries": cast(List[str], decision.get("queries", []))
    }


def route_next(state: BlogState) -> str:
    return "research" if state["needs_research"] else "planner"


# ---------------- RESEARCH ----------------

def research_node(state: BlogState) -> dict:
    if not APIConfig.TAVILY_API_KEY:
        logger.warning("Tavily API key missing. Skipping research.")
        return {"evidence": []}

    try:
        tool = TavilySearchResults(
            max_results=BlogConfig.RESULTS_PER_QUERY,
            tavily_api_key=APIConfig.TAVILY_API_KEY
        )

        results = []
        queries = cast(List[str], state.get("queries", []))
        for query in queries[:BlogConfig.MAX_RESEARCH_QUERIES]:
            cache_key = f"tavily_{query}"
            cached = cache.get(cache_key)
            if cached:
                results.extend(cached)
                continue

            response = tool.invoke({"query": query})
            normalized = [{
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", "")[:300]
            } for r in response or []]

            cache.set(cache_key, normalized)
            results.extend(normalized)

        return {"evidence": results}
    except Exception as e:
        logger.error(f"Research failed: {e}")
        return {"evidence": []}


# ---------------- PLANNER ----------------

def planner_node(state: BlogState) -> dict:
    platform_config = PLATFORM_CONFIGS.get(
        state["platform"],
        PLATFORM_CONFIGS["generic"]
    )

    evidence = cast(List[dict], state.get("evidence", []))
    evidence_text = "\n".join(
        f"- {e.get('title', 'N/A')}: {e.get('snippet', '')} ({e.get('url', '')})"
        for e in evidence[:5]
    )

    ctx = f"Topic: {state['topic']}\nTone: {platform_config['tone']}\nWord Target: {platform_config['word_count']}\nEvidence:\n{evidence_text}"
    prompt = f"{system_prompts.PLANNER_PROMPT}\n\n{ctx}"

    plan = generate_structured(
        llm_client,
        [
            {"role": "system", "content": system_prompts.MASTER_BLOG_WRITER_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "{blog_title, sections}"
    )

    return {"plan": plan}


# ---------------- FANOUT ----------------

def fanout_to_workers(state: BlogState) -> List[Send]:
    plan = cast(Optional[dict], state.get("plan"))
    if not plan:
        return []

    return [
        Send("worker", {
            "section": section,
            "topic": state["topic"],
            "platform": state["platform"],
            "blog_title": plan.get("blog_title", "Untitled"),
            "evidence": cast(List[dict], state.get("evidence", []))
        })
        for section in cast(List[dict], plan.get("sections", []))
    ]


# ---------------- WORKER ----------------

def worker_node(payload: dict) -> dict:
    section = cast(dict, payload.get("section", {}))
    evidence = cast(List[dict], payload.get("evidence", []))

    # Format relevant evidence for this section
    evidence_text = "\n".join(
        f"- {e.get('snippet', '')} (Source: {e.get('url', '')})"
        for e in evidence[:3]
    )

    prompt = system_prompts.WRITER_PROMPT.format(
        section_title=str(section.get("title", "No Title")),
        goal=str(section.get("goal", "")),
        bullets="\n".join(f"- {b}" for b in cast(List[str], section.get("bullets", []))),
        target_words=section.get("target_words", 300),
        platform=str(payload.get("platform", "generic"))
    )

    # Append evidence content strictly
    user_msg = f"{prompt}\n\nEvidence Content:\n{evidence_text}"

    content = llm_client.generate([
        {"role": "system", "content": system_prompts.MASTER_BLOG_WRITER_PROMPT},
        {"role": "user", "content": user_msg}
    ])

    return {"sections": [(int(section.get("id", 0)), content)]}


# ---------------- MERGER ----------------

def merger_node(state: BlogState) -> dict:
    sections = cast(List[tuple[int, str]], state.get("sections", []))
    sorted_sections = sorted(sections, key=lambda x: x[0])
    combined = "\n\n".join(content for _, content in sorted_sections)

    plan = cast(dict, state.get("plan") or {})
    title = plan.get("blog_title", "Untitled")

    final_blog = f"# {title}\n\n{combined}"
    word_count = count_words(final_blog)

    metadata = {
        "title": title,
        "word_count": word_count,
        "sections": len(sorted_sections),
        "platform": state["platform"],
        "topic": state["topic"],
        "models_used": {
            "router": ModelConfig.ROUTER_MODEL,
            "planner": ModelConfig.PLANNER_MODEL,
            "writer": ModelConfig.WRITER_MODEL,
        },
        "research_used": bool(state.get("needs_research", False)),
        "generated_at": date.today().isoformat()
    }

    return {"final_blog": final_blog, "metadata": metadata}


# ---------------- GRAPH ----------------

def create_blog_agent():
    graph = StateGraph(BlogState)

    graph.add_node("router", router_node)
    graph.add_node("research", research_node)
    graph.add_node("planner", planner_node)
    graph.add_node("worker", worker_node)
    graph.add_node("merger", merger_node)

    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", route_next,
                                {"research": "research", "planner": "planner"})
    graph.add_edge("research", "planner")
    graph.add_conditional_edges("planner", fanout_to_workers, ["worker"])
    graph.add_edge("worker", "merger")
    graph.add_edge("merger", END)

    return graph.compile()
