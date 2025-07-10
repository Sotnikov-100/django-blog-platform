# Django Blog Platform

Простий сервіс для ведення та перегляду інтернет блогу з інтеграцією OpenAI для генерації контенту.

## Функціональність

- **Аутентифікація**: Реєстрація та логін користувачів
- **Перегляд статей**: Список всіх статей з пагінацією
- **Детальний перегляд**: Повний перегляд статті з зображеннями
- **CRUD операції**: Створення, редагування, видалення статей (для авторизованих користувачів)
- **AI генерація**: Інтеграція з OpenAI для генерації тексту статей
- **Завантаження зображень**: Підтримка множинних зображень для статей

## Технології

- Python 3.10+
- Django 5.0+
- PostgreSQL
- Bootstrap 5
- OpenAI API
- Docker & Docker Compose

## Швидкий запуск

### З Docker (рекомендовано)

1. Клонуйте репозиторій:
```bash
git clone <repository-url>
cd django-blog-platform
```

2. Створіть файл `.env` на основі `env.example`:
```bash
cp env.example .env
```

3. Відредагуйте `.env` файл, вказавши ваш OpenAI API ключ:
```env
OPENAI_API_KEY=sk-proj-your-actual-api-key
```

4. Запустіть проект:
```bash
docker-compose up --build
```

5. Відкрийте браузер: http://localhost:8000

### Локальний запуск

1. Створіть віртуальне середовище:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate  # Windows
```

2. Встановіть залежності:
```bash
pip install -r requirements.txt
```

3. Створіть `.env` файл та налаштуйте змінні середовища

4. Запустіть міграції:
```bash
python manage.py migrate
```

5. Створіть суперкористувача:
```bash
python manage.py createsuperuser
```

6. Запустіть сервер:
```bash
python manage.py runserver
```

## Структура проекту

```
django-blog-platform/
├── blog/                 # Додаток для статей
├── users/               # Додаток для користувачів
├── config/              # Налаштування Django
├── templates/           # HTML шаблони
├── static/              # Статичні файли
├── media/               # Завантажені файли
├── requirements.txt     # Python залежності
├── Dockerfile          # Docker конфігурація
├── docker-compose.yml  # Docker Compose конфігурація
└── README.md           # Цей файл
```

## API Endpoints

- `/` - Список статей
- `/login/` - Логін
- `/register/` - Реєстрація
- `/profile/` - Профіль користувача
- `/new/` - Створення нової статті
- `/<id>/` - Перегляд статті
- `/<id>/edit/` - Редагування статті
- `/<id>/delete/` - Видалення статті

## Розробка

### Запуск тестів
```bash
python manage.py test
```

### Перевірка коду
```bash
black .
flake8 .
```
