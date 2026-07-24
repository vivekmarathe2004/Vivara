"""
Fallback LLM & Intelligent Template Script Generator
---------------------------------------------------
Provides intelligent procedural script generation when no local LLM (Ollama/OmniRoute)
or remote API key is active. Guarantees script generation NEVER fails!
"""
from __future__ import annotations

import json
import logging
from backend.services.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class FallbackLLMProvider(LLMProvider):
    """Fallback provider that generates structured script JSON procedurally."""

    def __init__(self, primary_provider: LLMProvider | None = None):
        self.primary = primary_provider

    async def generate(self, messages: list[dict], **kwargs) -> str:
        if self.primary:
            try:
                return await self.primary.generate(messages, **kwargs)
            except Exception as exc:
                logger.warning(f"Primary LLM provider ({self.primary.name}) unreachable: {exc}. Falling back to Vivara Intelligent Script Engine.")

        user_content = ""
        for m in messages:
            if m.get("role") == "user":
                user_content = m.get("content", "")

        topic = "Top Trending Concepts"
        if "about '" in user_content:
            topic = user_content.split("about '")[1].split("'")[0]
        elif "about " in user_content:
            topic = user_content.split("about ")[1].split(".")[0].strip()

        video_type = "explainer"
        if "ranking" in user_content.lower() or "countdown" in user_content.lower():
            video_type = "ranking"
        elif "review" in user_content.lower():
            video_type = "review"
        elif "short" in user_content.lower():
            video_type = "shorts"
        elif "documentary" in user_content.lower():
            video_type = "documentary"

        return self._generate_procedural_json(topic, video_type)

    def _generate_procedural_json(self, topic: str, video_type: str) -> str:
        clean_topic = topic.capitalize()

        if video_type == "ranking":
            data = {
                "title": f"Top 5 Unbelievable Facts About {clean_topic} Revealed!",
                "description": f"Here are the top 5 mind-blowing rankings and secrets about {clean_topic}. Subscribe for more viral breakdowns!",
                "tags": [clean_topic.lower(), "top5", "ranking", "viral", "facts"],
                "script": (
                    f"[SCENE: Dramatic opening scene | {clean_topic} mystery]\n"
                    f"Welcome back! Today we are counting down the top 5 unbelievable entries about {clean_topic} that will completely change how you see the world.\n\n"
                    f"[SCENE: High technology interface | futuristic technology]\n"
                    f"Number 5: The Origin. Most people don't realize where {clean_topic} actually started. Early breakthroughs laid the foundation for everything we know today.\n\n"
                    f"[SCENE: Cinematic landscape shots | deep nature]\n"
                    f"Number 4: The hidden mechanism. When you look closely at {clean_topic}, the internal dynamics reveal unprecedented complexity.\n\n"
                    f"[SCENE: Modern sleek studio | futuristic laboratory]\n"
                    f"Number 3: The game changer. Recent innovations in {clean_topic} have pushed boundary performance by over 300 percent.\n\n"
                    f"[SCENE: Fast moving particle cloud | abstract cyber]\n"
                    f"Number 2: The controversy. Experts have debated this single aspect of {clean_topic} for years, sparking fierce discussions worldwide.\n\n"
                    f"[SCENE: Golden trophy spotlight | victory atmosphere]\n"
                    f"And Number 1: The ultimate secret. The top discovery surrounding {clean_topic} proves that the future is already here! Drop a comment with your thoughts and hit subscribe for more!"
                ),
                "scenes": [
                    {"description": "Dramatic mystery scene", "search_query": f"{clean_topic} mystery"},
                    {"description": "High tech interface", "search_query": "futuristic technology"},
                    {"description": "Cinematic landscape", "search_query": "cinematic nature"},
                    {"description": "Futuristic laboratory", "search_query": "laboratory science"},
                    {"description": "Abstract cyber particle", "search_query": "cyber technology"},
                    {"description": "Golden victory atmosphere", "search_query": "trophy victory"}
                ]
            }
        elif video_type == "shorts":
            data = {
                "title": f"Did You Know This About {clean_topic}? 😱",
                "description": f"The #1 viral secret about {clean_topic} explained in 30 seconds!",
                "tags": [clean_topic.lower(), "shorts", "viral", "quickfacts"],
                "script": (
                    f"[SCENE: Intense shock pattern disruptor | shocking reveal]\n"
                    f"Stop scrolling! Did you know this mind-blowing truth about {clean_topic}?\n\n"
                    f"[SCENE: Fast moving futuristic cyber background | fast cyber]\n"
                    f"Most people think {clean_topic} is simple, but scientists just uncovered a secret that changes everything.\n\n"
                    f"[SCENE: Sleek glowing neon abstract | neon energy]\n"
                    f"In less than 60 seconds, this single breakthrough is transforming how we live. Double tap if this blew your mind!"
                ),
                "scenes": [
                    {"description": "Shocking pattern disruptor", "search_query": "shocking reveal"},
                    {"description": "Fast cyber background", "search_query": "cyber motion"},
                    {"description": "Neon energy glow", "search_query": "neon lights"}
                ]
            }
        else:
            data = {
                "title": f"Everything You Need To Know About {clean_topic} Explained",
                "description": f"An in-depth breakdown of {clean_topic}, how it works, and why it matters in 2026.",
                "tags": [clean_topic.lower(), "explained", "guide", "education"],
                "script": (
                    f"[SCENE: Modern sleek introduction | {clean_topic} overview]\n"
                    f"What is {clean_topic}, and why is everyone talking about it? In this complete breakdown, we explore the history, mechanics, and future of {clean_topic}.\n\n"
                    f"[SCENE: Futuristic digital network | global network]\n"
                    f"To understand {clean_topic}, we first have to look at the fundamental principles driving its development.\n\n"
                    f"[SCENE: High resolution laboratory experiment | innovation research]\n"
                    f"Key innovations have accelerated progress, making {clean_topic} more accessible and powerful than ever before.\n\n"
                    f"[SCENE: Inspiring bright horizon | bright future]\n"
                    f"As we look ahead, {clean_topic} will continue shaping the future. Make sure to subscribe for more deep dives!"
                ),
                "scenes": [
                    {"description": "Modern sleek introduction", "search_query": f"{clean_topic} concept"},
                    {"description": "Futuristic digital network", "search_query": "digital network"},
                    {"description": "Innovation research lab", "search_query": "innovation research"},
                    {"description": "Inspiring horizon", "search_query": "bright future"}
                ]
            }

        return json.dumps(data, indent=2)

    async def is_available(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return "Vivara Intelligent Script Engine"
