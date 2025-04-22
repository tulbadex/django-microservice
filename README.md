# 🛠️ Django Background Task Microservice

A modular Django 5.1.8 microservice for background task processing using Celery and Redis. It features token-based authentication (JWT), a custom user model, async task execution, and browsable API documentation using Swagger (drf_yasg).

---

## 🔧 Features

- ✅ JWT Authentication with email & password
- ✅ Custom `CustomUser` model
- ✅ Background task execution via Celery & Redis
- ✅ Auto-generated Swagger and ReDoc API docs
- ✅ CORS support for frontend integration
- ✅ Token blacklist (logout)
- ✅ REST API with DRF
- ✅ Task status tracking
- ✅ Dockerized deployment
- ✅ AWS ECS deployment with Terraform
- ✅ CI/CD pipeline with GitHub Actions

---

## 📦 Tech Stack

- Django 5.1.8
- Django REST Framework
- Celery
- Redis
- drf-yasg (Swagger)
- SimpleJWT

---

## 🗂️ Project Structure

```
.
├── accounts/              # Auth & custom user logic
├── api/                   # Core app with task logic
├── config/                # Project settings
├── staticfiles/           # For WhiteNoise deployment
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🚀 Quickstart (Local Dev)

### 1. Clone and Setup

```bash
git clone https://github.com/your-username/django-task-microservice.git
cd django-task-microservice
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Variables

#### copy .env.example and rename it to .env
```bash
cp .env.example .env
```

```env
SECRET_KEY=your-django-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional)
DB_ENGINE=sqlite
DB_NAME=db.sqlite3

# Redis for Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Start Servers

In separate terminals:

```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Celery worker
celery -A config worker --loglevel=info
```

---

## 🧪 API Testing

- Visit: [`http://localhost:8000/swagger/`](http://localhost:8000/swagger/) for Swagger docs.
- Visit: [`http://localhost:8000/redoc/`](http://localhost:8000/redoc/) for Redoc docs.

### 🔐 Authentication Flow

- `POST /api/account/register/`: Register with email + password
- `POST /api/account/login/`: Login, receive `access` and `refresh` tokens
- `POST /api/account/logout/`: Blacklist refresh token
- Use `Authorization: Bearer <token>` header for protected endpoints

---

## ⚙️ Background Tasks with Celery

All long-running operations (like async processing) are offloaded to Celery workers.

Example structure:

```python
# tasks.py
@shared_task
def process_heavy_task(data):
    # long-running logic here
```

Triggered via:

```python
process_heavy_task.delay(payload)
```

## 🚀 Deployment Tips

- Use Gunicorn + Nginx + Supervisor for production
- Use `.env` file or secrets manager for config
- Use `whitenoise` for serving static files
- Setup Redis & Celery as system services or Docker containers
- Set `DEBUG=False` in production!

---

## 🤝 Contribution

Feel free to fork, raise issues, or submit PRs!

---

## 📜 License

MIT License.
```

---