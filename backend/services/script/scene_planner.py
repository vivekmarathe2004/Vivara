import re

class ScenePlanner:
    def plan_scenes(self, script: str) -> list[dict]:
        # Extract [SCENE: ...] tags
        scenes = []
        pattern = r"\[SCENE:\s*(.*?)\]"
        matches = re.finditer(pattern, script)
        for match in matches:
            description = match.group(1)
            # Create a simple search query from description
            search_query = " ".join(description.split()[:4])
            scenes.append({
                "description": description,
                "search_query": search_query
            })
        return scenes
