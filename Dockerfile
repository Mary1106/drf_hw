FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt первым для оптимизации кэширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем python-dotenv для работы с .env файлом
RUN pip install python-dotenv

# Копируем .env файл в контейнер
COPY .env .

# Копируем остальные файлы проекта
COPY . .

# Создаем директорию для статических файлов
RUN mkdir -p /app/static

# Устанавливаем права доступа
RUN chmod -R 755 /app/static

# Настраиваем переменные окружения
ENV DOTENV_LOAD=true

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
