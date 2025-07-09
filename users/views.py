from django.contrib.auth import login, logout
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from users.forms import RegistrationForm, LoginForm


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
    redirect_authenticated_user = True


@require_http_methods(["GET", "POST"])
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("home")


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            f"Welcome, {user.first_name}! Your account has been created successfully.",
        )
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"
    login_url = reverse_lazy("login")
