#!/usr/bin/env bash
# Скрипт для запуска Docker-контейнеров и подготовки проекта

set -e  # Прерываем выполнение при ошибках

export ENVIRONMENT=local
export PYTHONDONTWRITEBYTECODE=1

# Пути к шаблонам и основному .env файлу
MAIN_ENV=.env
TEMPLATE_ENV=.env.example

# Проверяем наличие docker/.env
if [[ ! -f ${TEMPLATE_ENV} ]]; then
    echo "❌ Файл ${TEMPLATE_ENV} не найден. Создайте его перед запуском."
    exit 1
fi

# Проверяем наличие src/.env, если его нет — создаем
if [[ ! -f ${MAIN_ENV} ]]; then
    cp "${TEMPLATE_ENV}" "${MAIN_ENV}"
    echo "✅ Создан файл ${MAIN_ENV} на основе ${TEMPLATE_ENV}"
fi

# Запуск Docker Compose
echo "🚀 Запуск контейнеров Docker..."
docker compose -f docker-compose.yml up --build -d  # Запуск в фоновом режиме

echo "✅ Контейнеры запущены. Для остановки выполните команду:"
echo "   docker-compose -f docker/docker-compose.yml down"

# Проверка состояния контейнеров
echo "⏳ Ожидание готовности базы данных..."
until docker exec -it $(docker ps -qf "name=db") pg_isready -U user > /dev/null 2>&1; do
    echo "⏳ Ждем готовности PostgreSQL..."
    sleep 2
done

echo "✅ База данных готова к работе."
