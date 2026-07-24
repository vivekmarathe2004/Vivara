"""
Script Generator & Prompt Engine
---------------------------------
Generates highly engaging YouTube & Short scripts with embedded [SCENE: visual | search query] tags.
"""
from __future__ import annotations

import json
import re
from backend.services.llm.base import LLMProvider


class ScriptGenerator:
    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def generate(self, video_type: str, topic: str, settings: dict) -> dict:
        prompt = self._get_prompt(video_type, topic, settings)
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are a master viral YouTube scriptwriter and content director. "
                    "You write punchy, high-retention scripts designed for maximum watch time. "
                    "Return ONLY valid JSON without markdown code blocks, containing 'title', 'description', 'tags', 'script', and 'scenes'."
                )
            },
            {"role": "user", "content": prompt}
        ]
        
        response_text = await self.llm.generate(messages)
        
        # Strip markdown syntax if present
        clean_text = response_text.strip()
        if clean_text.startswith("```"):
            clean_text = re.sub(r"^```[a-zA-Z]*\n?", "", clean_text)
            clean_text = re.sub(r"```$", "", clean_text).strip()

        try:
            data = json.loads(clean_text)
            if not data.get("script"):
                data["script"] = response_text
            return data
        except json.JSONDecodeError:
            # Robust fallback parser if JSON formatting was incomplete
            return {
                "title": f"The Ultimate Guide to {topic}",
                "description": f"Explore everything you need to know about {topic}.",
                "tags": [topic.lower(), "viral", "documentary", "explained"],
                "script": response_text,
                "scenes": []
            }

    def _get_prompt(self, video_type: str, topic: str, settings: dict) -> str:
        duration = settings.get("duration", "medium")
        format_instructions = """
Format Requirement: Return ONLY a valid JSON object matching this schema:
{
    "title": "High-CTR Viral YouTube Title",
    "description": "Engaging video description with timestamp highlights.",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "script": "Full spoken narrative. Embed [SCENE: visual description | search query] tags every 15-20 seconds to direct B-roll media matching.",
    "scenes": [
        {"description": "Visual scene concept", "search_query": "specific 2-word stock media query"}
    ]
}
"""
        if video_type == "ranking":
            return (
                f"Write a viral countdown script about '{topic}' ({duration} duration). "
                "Structure: Ultra-gripping hook (0-15s) -> Fast-paced Countdown -> Surprising #1 Entry -> Strong CTA. "
                + format_instructions
            )
        elif video_type == "review":
            return (
                f"Write an in-depth review video script for '{topic}' ({duration} duration). "
                "Structure: Punchy Hook -> Context & Expectations -> Detailed Pros & Cons -> Final Score & Verdict -> CTA. "
                + format_instructions
            )
        elif video_type == "explainer":
            return (
                f"Write a captivating explainer video script about '{topic}' ({duration} duration). "
                "Structure: Mind-bending Hook -> The Core Problem -> Step-by-Step Breakdown -> Key Takeaway -> CTA. "
                + format_instructions
            )
        elif video_type == "shorts":
            return (
                f"Write an explosive vertical 9:16 Short/Reel script about '{topic}' (under 60s). "
                "Structure: Immediate 3-second pattern disruptor hook -> Fast value delivery -> Loop payoff CTA. "
                + format_instructions
            )
        elif video_type == "documentary":
            return (
                f"Write an atmospheric cinematic documentary script about '{topic}' ({duration} duration). "
                "Structure: Atmospheric Opening -> Historical Arc -> Unseen Mystery -> Philosophical Conclusion. "
                + format_instructions
            )
        elif video_type == "educational":
            return (
                f"Write a masterclass educational video script about '{topic}' ({duration} duration). "
                "Structure: Learning Objective -> Core Concept -> Real-World Example -> Common Pitfalls -> Actionable Summary. "
                + format_instructions
            )
        else:
            return f"Write a high-engagement video script about '{topic}'. " + format_instructions
