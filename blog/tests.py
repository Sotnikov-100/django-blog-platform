from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Article, ArticleImage
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os

User = get_user_model()


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
        )
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            author=self.user,
        )

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.author, self.user)
        self.assertIsNotNone(self.article.created_at)

    def test_article_str(self):
        self.assertEqual(str(self.article), "Test Article")


class ArticleViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
        )
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            author=self.user,
        )

    def test_article_list_view(self):
        response = self.client.get(reverse("article-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")

    def test_article_detail_view(self):
        response = self.client.get(
            reverse("article-detail", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")

    def test_article_create_view_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("article-create"))
        self.assertEqual(response.status_code, 200)

    def test_article_create_view_unauthenticated(self):
        response = self.client.get(reverse("article-create"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_article_update_view_owner(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("article-update", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_article_update_view_not_owner(self):
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(
            reverse("article-update", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_article_delete_view_owner(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("article-delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_article_delete_view_not_owner(self):
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(
            reverse("article-delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 403)


class ArticleFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
        )

    def test_article_form_valid(self):
        from blog.forms import ArticleForm

        form_data = {
            "title": "Test Article",
            "content": "This is test content.",
        }
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_article_form_invalid(self):
        from blog.forms import ArticleForm

        form_data = {
            "title": "",  # Empty title
            "content": "This is test content.",
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
