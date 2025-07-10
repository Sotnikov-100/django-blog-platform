from django.db import models
from django.conf import settings
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(blank=True, verbose_name="Content")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name="Author",
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Article",
    )
    image = models.ImageField(
        upload_to="article_images/%Y/%m/%d/", verbose_name="Image"
    )
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Article Image"
        verbose_name_plural = "Article Images"

    def __str__(self):
        return f"Image for {self.article.title}"
