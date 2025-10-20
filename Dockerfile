# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем системные зависимости (для SQLite и других)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем папку для alembic версий (если используется)
RUN mkdir -p alembic/versions

# 1. Генерируем миграцию
RUN alembic revision --autogenerate -m "Initial migration"

# 2. Применяем миграции
RUN alembic upgrade head

# 3. Заполняем тестовыми данными
RUN python seed_data.py

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]