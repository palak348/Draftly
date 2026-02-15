"""
Draftly - Blog Writing Agent CLI

Production-ready command-line interface for blog generation.

Responsibilities:
- Load and validate configuration
- Parse CLI arguments
- Invoke blog agent
- Persist generated output
- Handle runtime errors gracefully

Core agent logic and model configuration are NOT modified here.
"""

import logging
import time
import argparse
from typing import Dict, Any

from core.blog_agent import create_blog_agent
from utils.helpers import setup_logging, save_blog, ProgressTracker
from config import load_config, validate_config, PLATFORM_CONFIGS


# ---------------------------------------------------------------------
# State Factory
# ---------------------------------------------------------------------

def create_initial_state(topic: str, platform: str) -> Dict[str, Any]:
    """
    Creates initial state object for the blog agent.
    Encapsulated to avoid inline state dictionaries.
    """
    return {
        "topic": topic,
        "platform": platform,
        "needs_research": False,
        "mode": "",
        "queries": [],
        "evidence": [],
        "plan": None,
        "sections": [],
        "final_blog": "",
        "md_with_placeholders": "",
        "image_specs": [],
        "final_images": [],
        "metadata": {}
    }


# ---------------------------------------------------------------------
# Blog Generation Wrapper
# ---------------------------------------------------------------------

def generate_blog(topic: str, platform: str) -> Dict[str, Any]:
    """
    Executes blog generation using the configured agent.

    Args:
        topic: Blog topic
        platform: Target publishing platform

    Returns:
        Result dictionary containing final_blog and metadata
    """

    if platform not in PLATFORM_CONFIGS:
        logging.warning("Invalid platform '%s'. Falling back to 'generic'.", platform)
        platform = "generic"

    logging.info("Starting blog generation | Topic: %s | Platform: %s", topic, platform)

    agent = create_blog_agent()
    tracker = ProgressTracker(total_steps=3)

    state = create_initial_state(topic, platform)

    start_time = time.time()

    tracker.update("Processing", "Generating blog content...")
    result = agent.invoke(state)
    tracker.complete()

    duration = round(time.time() - start_time, 2)
    logging.info("Blog generation completed in %s seconds", duration)

    if isinstance(result, dict):
        result.setdefault("metadata", {})
        result["metadata"]["generation_time"] = duration

    return result


# ---------------------------------------------------------------------
# CLI Argument Parsing
# ---------------------------------------------------------------------

def parse_arguments():
    """
    Parses CLI arguments for interactive and automation usage.
    """
    parser = argparse.ArgumentParser(
        description="Draftly - AI Blog Generator"
    )

    parser.add_argument(
        "--topic",
        type=str,
        help="Blog topic"
    )

    parser.add_argument(
        "--platform",
        type=str,
        default="generic",
        help=f"Target platform ({', '.join(PLATFORM_CONFIGS.keys())})"
    )

    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Disable preview output"
    )

    return parser.parse_args()


# ---------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------

def main() -> int:
    """
    CLI entry point.
    Returns exit code.
    """

    setup_logging()

    # Load and validate configuration
    api_config, model_config, blog_config, system_config = load_config()
    is_valid, message = validate_config(api_config)

    if not is_valid:
        print("Configuration Error:")
        print(message)
        print("Verify environment variables and API keys.")
        return 2

    args = parse_arguments()

    topic = args.topic or input("Enter blog topic: ").strip()
    if not topic:
        print("Topic is required.")
        return 1

    platform = args.platform.lower()
    if platform not in PLATFORM_CONFIGS:
        logging.warning("Unsupported platform '%s'. Using generic.", platform)
        platform = "generic"

    print("Generating blog...\n")

    try:
        result = generate_blog(topic, platform)

        metadata = result.get("metadata", {})
        final_blog = result.get("final_blog", "")

        filepath = save_blog(
            content=final_blog,
            title=metadata.get("title", "untitled"),
            metadata=metadata
        )

        print("Blog generated successfully.")
        print("-" * 50)
        print(f"Title: {metadata.get('title', 'N/A')}")
        print(f"Word count: {metadata.get('word_count', 'N/A')}")
        print(f"Sections: {metadata.get('sections', 'N/A')}")
        print(f"Generation time: {metadata.get('generation_time', 'N/A')} seconds")
        print(f"Saved to: {filepath}")
        print()

        if not args.no_preview and final_blog:
            preview = final_blog[:500]
            print("Preview:")
            print("-" * 50)
            print(preview + "..." if len(final_blog) > 500 else preview)
            print()

        return 0

    except KeyboardInterrupt:
        print("Execution interrupted by user.")
        return 1

    except Exception as exc:
        logging.exception("Unexpected error during blog generation")
        print(f"Error: {exc}")
        print("Check application logs for details.")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
