from serpapi import GoogleSearch
import os
import logging

logger = logging.getLogger(__name__)

SERP_API_KEY = os.getenv("SERP_API_KEY")

async def get_celebrity_image_url(name: str) -> str:
    try:
        search = GoogleSearch({
            "q": name,
            "tbm": "isch",
            "api_key": SERP_API_KEY
        })

        results = search.get_dict()

        images = results.get("images_results", [])

        if images:
            return images[0]["original"]
    except Exception as e:
        logger.error(f"An error occurred while image search - {e}")
    return None