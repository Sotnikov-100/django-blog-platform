from django.urls import path
from blog.views import (
    HomeView,
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    generate_content,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path("articles/new/", ArticleCreateView.as_view(), name="article-create"),
    path("articles/<int:pk>/edit/", ArticleUpdateView.as_view(), name="article-update"),
    path(
        "articles/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article-delete"
    ),
    path("generate-content/", generate_content, name="generate-content"),
]
