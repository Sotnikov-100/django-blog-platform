from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from blog.models import Article, ArticleImage
from blog.forms import ArticleForm
from blog.utils import generate_ai_content


@login_required
@require_POST
def generate_content(request):
    prompt = request.POST.get("prompt", "")
    if not prompt:
        return JsonResponse({"error": "Prompt is required"}, status=400)

    content = generate_ai_content(prompt)
    return JsonResponse({"content": content})


class HomeView(TemplateView):
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_articles"] = Article.objects.all().order_by("-created_at")[:3]
        return context


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("article-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        files = self.request.FILES.getlist("images")
        for f in files:
            ArticleImage.objects.create(article=self.object, image=f)

        messages.success(self.request, "Article created successfully!")
        return response


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("article-list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Article deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        # Handle new images
        files = self.request.FILES.getlist("images")
        for f in files:
            ArticleImage.objects.create(article=self.object, image=f)

        messages.success(self.request, "Article updated successfully!")
        return response


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"
    success_url = reverse_lazy("article-list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
