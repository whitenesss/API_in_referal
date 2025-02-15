# 🚀 Referral System API

RESTful API для реферальной системы с аутентификацией JWT, кешированием и интеграцией со сторонними сервисами.

## 🌟 Особенности

- JWT аутентификация (OAuth2 с Bearer токенами)
- Управление реферальными кодами (создание/удаление)
- Поиск реферальных кодов по email
- Регистрация по реферальным кодам
- Просмотр информации о рефералах
- Интеграция с EmailHunter (опционально)
- Кеширование с использованием Redis
- Автоматические миграции базы данных (Alembic)
- Документация API через Swagger UI и ReDoc
- Готовый Docker-образ с PostgreSQL и Redis

## 🛠️ Установка и запуск

**Предварительные требования:**
- Docker и Docker Compose
- Python 3.11+

1. Клонировать репозиторий:
```bash
cd API_in_referal
```
```bash
git clone https://github.com/whitenesss/API_in_referal.git
```

2. Создать файл окружения и заполните по примеру .env.example:
```bash
cp .env
```
3. Запустить проект:
```bash
chmod +x scripts/start2.sh
./scripts/start2.sh
```
## Сервис будет доступен по адресу: http://localhost:8000

### 🔧 Переменные окружения (.env)
```ini
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/dbname
SECRET_KEY=mysecretkey
ALGORITHM=HS256
EMAILHUNTER_API_KEY=your-secret-key #Добавить вашь API key
```

### 📚 Документация API
После запуска доступны:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
