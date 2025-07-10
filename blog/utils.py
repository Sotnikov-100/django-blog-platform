import openai
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


def generate_ai_content(prompt, model=settings.OPENAI_DEFAULT_MODEL, user_id=None):
    """
    Генерує текст за допомогою OpenAI API з обмеженням частоти запитів
    """
    if not settings.OPENAI_API_KEY:
        logger.error("OpenAI API key is not configured!")
        return None

    if user_id and cache.get(f"openai_limit_{user_id}"):
        logger.warning(f"Rate limit exceeded for user {user_id}")
        return None

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful blog content assistant. Create quality, informative and interesting content in English. The text should be well-structured and easy to read.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        if user_id:
            cache.set(f"openai_limit_{user_id}", True, 60)

        return response.choices[0].message.content.strip()

    except openai.APIError as e:
        logger.error(f"OpenAI API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    return None
