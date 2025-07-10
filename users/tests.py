from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.forms import RegistrationForm, LoginForm

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            bio="Test bio",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.bio, "Test bio")

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
        )

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_login_failure(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpass"},
        )
        self.assertEqual(response.status_code, 200)  # Stay on login page

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "New",
                "username": "newuser",
                "password1": "newpass123",
                "password2": "newpass123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_password_mismatch(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "New",
                "username": "newuser",
                "password1": "newpass123",
                "password2": "differentpass",
            },
        )
        self.assertEqual(response.status_code, 200)  # Stay on register page
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_profile_view_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect after logout


class UserFormTest(TestCase):
    def test_registration_form_valid(self):
        form_data = {
            "first_name": "Test",
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        form_data = {
            "first_name": "Test",
            "username": "testuser",
            "password1": "testpass123",
            "password2": "differentpass",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_login_form_valid(self):
        form_data = {
            "username": "testuser",
            "password": "testpass123",
        }
        form = LoginForm(data=form_data)
        # Login form validation requires a user to exist
        self.assertFalse(form.is_valid())  # Will fail because no user exists

    def test_login_form_invalid(self):
        form_data = {
            "username": "",
            "password": "",
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
