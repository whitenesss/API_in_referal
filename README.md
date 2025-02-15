# IMEI Checker Bot

## Общее описание

**IMEI Checker Bot** — это бэкенд-система для проверки IMEI устройств, интегрированная с Telegram-ботом и предоставляющая API для внешних запросов. Проект реализует базовый функционал для:
- **Белого списка пользователей** для доступа к функционалу Telegram-бота.
- **Авторизации через API** по JWT-токену.
- **Проверки IMEI**: валидность номера, получение информации о устройстве с использованием сервиса [imeicheck.net](https://imeicheck.net/).

## Функционал

### 1. Доступ
- **Белый список Telegram-пользователей:** Только пользователи, внесённые в белый список, могут пользоваться ботом.
- **Авторизация по API:** Доступ к API осуществляется посредством JWT-токена, который выдаётся при авторизации.

### 2. Telegram-бот
- Пользователь отправляет боту IMEI.
- Бот проверяет валидность IMEI:
  - Если IMEI не соответствует формату (15 цифр), возвращается сообщение об ошибке.
  - Если формат корректный, бот отправляет запрос к внешнему сервису imeicheck.net и возвращает информацию об устройстве.

### 3. API для проверки IMEI
- **Метод:** `POST /api/check-imei`
- **Параметры запроса:**
  - `imei` (строка, обязательный) — IMEI устройства.
  - `token` (строка, не обязательный) — JWT-токен передается в куки.
- **Ответ:** JSON с информацией о IMEI.

### 4. Интеграция с внешним сервисом
- Используется тестовый API сервис [imeicheck.net](https://imeicheck.net/) для проверки IMEI.
- Для работы с сервисом используется **API Sandbox Token**:

## Для старта проекта потребуется

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://gitlab.com/your_username/vps_manager.git
cd vps_manager
```
### 2. Создание виртуального окружения
Убедитесь, что у вас установлен Python версии 3.10 или выше. 
Затем создайте виртуальное окружение и активируйте его:
```bash
python -m venv env
source env/bin/activate  # Для macOS/Linux
env\Scripts\activate     # Для Windows
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Создать файл .env в корне проекта, рядом с docker-compose.yml
### Перенисите данные в файл и добавьте токен телеграмм 
```
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/imei_checker
TELEGRAM_TOKEN=Добавьте ваши данные 
IMEI_API_SANDBOX_TOKEN=e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b
SECRET_KEY=mysecretkey
ALGORITHM=HS256
API_BASE_URL=http://localhost:8000
IMEI_CHECK_API_URL=https://api.imeicheck.net/v1/checks
API_TOKEN=e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b
API_BASE_URL_BOT=http://api:8000/api/v1/check-imei
```
### 4. Сделайте файл исполняемым.
```Выполните команду в терминале из директории, где находится скрипт:
chmod +x start2.sh
```
### 5. Для запуска потребуется запустить скрипт 
```
 ./scripts/start2.sh
```

**Теперь API доступно по адресу: http://127.0.0.1:8000/**