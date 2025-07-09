from django.apps import AppConfig
import openai
from django.conf import settings


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        openai.api_key = settings.OPENAI_API_KEY
