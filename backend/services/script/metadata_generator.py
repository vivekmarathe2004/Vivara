from backend.services.llm.base import LLMProvider
import json

class MetadataGenerator:
    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def generate(self, script: str) -> dict:
        messages = [
            {"role": "system", "content": "You are a YouTube SEO expert. Generate title, description and tags for a video based on its script. Return ONLY JSON: {\"title\": \"...\", \"description\": \"...\", \"tags\": [\"...\"]}"},
            {"role": "user", "content": script}
        ]
        
        response_text = await self.llm.generate(messages)
        try:
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            return json.loads(response_text)
        except:
            return {"title": "Generated Video", "description": "", "tags": []}
