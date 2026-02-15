"""
Configuration - Blog Writing Agent

Centralized configuration for:
- API keys
- Model selection
- Blog generation settings
- Platform rules
- System behavior
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------
# API CONFIGURATION
# ---------------------------------------------------------------------

class APIConfig:
    """API keys and endpoints."""

    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        if not cls.OPENROUTER_API_KEY:
            return False, "OPENROUTER_API_KEY is missing."
        return True, "API configuration valid."


# ---------------------------------------------------------------------
# MODEL CONFIGURATION
# ---------------------------------------------------------------------

class ModelConfig:
    """LLM model selection with task-specific optimization."""

    # Fast tasks (Router, Research, Image Planning) - Llama for speed
    ROUTER_MODEL: str = "meta-llama/llama-3.3-70b-instruct"
    RESEARCH_MODEL: str = "meta-llama/llama-3.3-70b-instruct"

    
    # Quality tasks (Planning, Writing) - Gemini for better output
    PLANNER_MODEL: str = "google/gemini-2.0-flash-001"
    WRITER_MODEL: str = "google/gemini-2.0-flash-001"
    
    # Fallback model for all tasks
    BACKUP_MODEL: str = "google/gemini-2.0-flash-001"

    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 4096

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        if not (0 <= cls.TEMPERATURE <= 2):
            return False, "TEMPERATURE must be between 0 and 2."
        if cls.MAX_TOKENS <= 0:
            return False, "MAX_TOKENS must be positive."
        return True, "Model configuration valid."



# ---------------------------------------------------------------------
# BLOG SETTINGS
# ---------------------------------------------------------------------

class BlogConfig:
    """Blog generation parameters."""

    DEFAULT_WORD_COUNT: int = 2000
    MIN_SECTIONS: int = 5
    MAX_SECTIONS: int = 9
    MIN_QUALITY_SCORE: int = 7
    MAX_RETRIES: int = 2

    # Research limits
    RESULTS_PER_QUERY: int = 5
    MAX_RESEARCH_QUERIES: int = 5

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        if cls.MIN_SECTIONS > cls.MAX_SECTIONS:
            return False, "MIN_SECTIONS cannot exceed MAX_SECTIONS."
        if cls.MAX_RETRIES < 0:
            return False, "MAX_RETRIES cannot be negative."
        return True, "Blog configuration valid."


# ---------------------------------------------------------------------
# PLATFORM CONFIGS
# ---------------------------------------------------------------------

PLATFORM_CONFIGS = {
    "medium": {
        "word_count": (1500, 3000),
        "tone": "conversational, storytelling",
        "max_images": 0
    },
    "devto": {
        "word_count": (1000, 2000),
        "tone": "technical, tutorial",
        "max_images": 0
    },
    "linkedin": {
        "word_count": (800, 1500),
        "tone": "professional",
        "max_images": 0
    },
    "generic": {
        "word_count": (1500, 2500),
        "tone": "balanced",
        "max_images": 0
    }
}


# ---------------------------------------------------------------------
# SYSTEM SETTINGS
# ---------------------------------------------------------------------

class SystemConfig:
    """System-level behavior."""

    ENABLE_CACHE: bool = True
    CACHE_DIR: str = ".cache"
    CACHE_TTL_HOURS: int = 24

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "blog_agent.log"

    MAX_PARALLEL_WORKERS: int = 5
    OUTPUT_DIR: str = "generated_blogs"

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        if cls.MAX_PARALLEL_WORKERS <= 0:
            return False, "MAX_PARALLEL_WORKERS must be positive."
        return True, "System configuration valid."


# ---------------------------------------------------------------------
# GLOBAL VALIDATION & LOADING
# ---------------------------------------------------------------------

def load_config() -> tuple[type[APIConfig], type[ModelConfig], type[BlogConfig], type[SystemConfig]]:
    return APIConfig, ModelConfig, BlogConfig, SystemConfig


def validate_config(api_config: type[APIConfig] = APIConfig) -> tuple[bool, str]:
    is_valid, message = api_config.validate()
    if not is_valid:
        return False, message

    for config_class in (ModelConfig, BlogConfig, SystemConfig):
        is_valid, message = config_class.validate()
        if not is_valid:
            return False, message

    return True, "Configuration valid."
