from openai import OpenAI
from src.config.settings import settings
from src.utils.logger import get_logger
from src.utils.exceptions import ExtractionError

log = get_logger(__name__)

client = OpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.x.ai/v1",
)


def chat(prompt: str, system: str = "You are a helpful assistant.") -> str:
    try:
        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        raise ExtractionError(f"LLM call failed: {e}")