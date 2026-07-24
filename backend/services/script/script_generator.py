from backend.services.llm.base import LLMProvider
import json
import re

class ScriptGenerator:
    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def generate(self, video_type: str, topic: str, settings: dict) -> dict:
        prompt = self._get_prompt(video_type, topic, settings)
        messages = [
            {"role": "system", "content": "You are a professional YouTube scriptwriter. Return ONLY valid JSON format, without markdown code blocks, containing the requested fields."},
            {"role": "user", "content": prompt}
        ]
        
        response_text = await self.llm.generate(messages)
        # Attempt to parse json
        try:
            # strip markdown blocks if they exist
            if response_text.startswith("```"):
                response_text = re.sub(r"```[a-zA-Z]*\n?", "", response_text)
                response_text = response_text.replace("```", "")
            data = json.loads(response_text)
            return data
        except json.JSONDecodeError:
            # Fallback extraction or error handling
            return {
                "title": f"Video about {topic}",
                "description": "",
                "tags": [],
                "script": response_text,
                "scenes": []
            }

    def _get_prompt(self, video_type: str, topic: str, settings: dict) -> str:
        base = f"Create a script for a {video_type} video about {topic}. "
        format_instructions = """
Return your response as a JSON object with this structure:
{
    "title": "A catchy YouTube title",
    "description": "Video description",
    "tags": ["tag1", "tag2"],
    "script": "The full spoken text of the script. Include [SCENE: description of visual] tags to indicate what should be shown on screen.",
    "scenes": [{"description": "description of visual", "search_query": "short query for stock video"}]
}
"""
        if video_type == "ranking":
            return base + "Structure: Hook (15s) -> Rankings 10 to 1 with 20-30s per entry -> Conclusion (15s). " + format_instructions
        elif video_type == "review":
            return base + "Structure: Hook -> Background/Context -> Detailed Analysis -> Pros -> Cons -> Verdict -> CTA. " + format_instructions
        elif video_type == "explainer":
            return base + "Structure: Hook with surprising fact -> Problem statement -> Deep explanation -> Key takeaways -> CTA. " + format_instructions
        elif video_type == "shorts":
            return base + "Structure: Ultra-punchy hook (3s) -> Core value (30s) -> CTA (3s) - max 60s total. " + format_instructions
        elif video_type == "documentary":
            return base + "Structure: Opening atmosphere -> Historical context -> Main narrative -> Expert perspective -> Conclusion. " + format_instructions
        elif video_type == "educational":
            return base + "Structure: Learning objective -> Core concept -> Examples -> Common mistakes -> Summary. " + format_instructions
        else:
            return base + format_instructions
