FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt первым для оптимизации кэширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем python-dotenv для работы с .env файлом
RUN pip install python-dotenv

# Копируем остальные файлы проекта
COPY . .

# Создаем директорию для статических файлов
RUN mkdir -p /app/static

# Устанавливаем права доступа
RUN chmod -R 755 /app/static

# Настраиваем переменные окружения
ENV DOTENV_LOAD=true
ENV DOCKER_ENV=true

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
