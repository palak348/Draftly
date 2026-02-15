"""
LLM client using OpenRouter with retry and fallback support.
"""

import logging
import requests
import json
from typing import List, Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from config import APIConfig, ModelConfig

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified OpenRouter client."""

    def __init__(self, model: Optional[str] = None):
        self.model = model or ModelConfig.WRITER_MODEL
        self.backup_model = ModelConfig.BACKUP_MODEL
        self.temperature = ModelConfig.TEMPERATURE
        self.max_tokens = ModelConfig.MAX_TOKENS

        if not APIConfig.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY missing.")

        self.api_key = APIConfig.OPENROUTER_API_KEY
        self.base_url = APIConfig.OPENROUTER_BASE_URL

        self.total_calls = 0
        self.total_tokens = 0

    @retry(stop=stop_after_attempt(3),
           wait=wait_exponential(multiplier=1, min=2, max=8),
           reraise=True)
    def generate(self,
                 messages: List[Dict[str, str]],
                 json_mode: bool = False) -> str:

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        self.total_calls += 1
        self.total_tokens += data.get("usage", {}).get("total_tokens", 0)

        return data["choices"][0]["message"]["content"]


def generate_structured(client: LLMClient,
                        messages: List[Dict[str, str]],
                        output_schema: str) -> Dict[str, Any]:
    """Force structured JSON response."""

    system_instruction = {
        "role": "system",
        "content": f"Respond ONLY with valid JSON.\nSchema:\n{output_schema}"
    }

    messages = [system_instruction] + messages
    raw = client.generate(messages, json_mode=True)

    cleaned = raw.strip().replace("```json", "").replace("```", "")
    return json.loads(cleaned)


def create_client_for_task(task: str) -> LLMClient:
    """Create LLM client for specific task with optimized model.
    
    Args:
        task: Task name (router, research, planner, writer, image_plan)
        
    Returns:
        LLMClient configured with task-appropriate model
    """
    model_map = {
        "router": ModelConfig.ROUTER_MODEL,
        "research": ModelConfig.RESEARCH_MODEL,
        "planner": ModelConfig.PLANNER_MODEL,
        "writer": ModelConfig.WRITER_MODEL,
        "writer": ModelConfig.WRITER_MODEL,
    }
    
    model = model_map.get(task, ModelConfig.BACKUP_MODEL)
    logger.debug(f"Creating client for task '{task}' with model '{model}'")
    
    return LLMClient(model=model)
