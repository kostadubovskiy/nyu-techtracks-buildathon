from anthropic import Anthropic
from ..config import settings
import os

# Initialize the client with just the API key
anthropic = Anthropic()

async def generate_roadmap_content(topic: str, level: str) -> str:
    """
    Generate a learning roadmap using Claude
    """
    prompt = f"""Create a detailed learning roadmap for {topic} at {level} level.
    Include:
    1. Key concepts to master
    2. Recommended resources
    3. Project ideas
    4. Estimated timeline
    """
    
    message = await anthropic.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    return message.content 