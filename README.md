## Руководство по развертыванию приложения

### Предварительные требования
- Docker (версия 19.03 или выше)
- Docker Compose (версия 1.25 или выше)

### Подготовка окружения
#### Для Linux/MacOS:

- Клонируйте репозиторий:

```
git clone https://github.com/<репозиторий>.git
cd <репозиторий>
```

- Создайте файл конфигурации:

```
cp .env.example .env
```

#### Для Windows:

- Клонируйте репозиторий:

```
git clone https://github.com/<репозиторий>.git
cd <репозиторий>
```

- Создайте файл конфигурации:

Через PowerShell:

```
Copy-Item .env.example -Destination .env
```

Или через командную строку:

```
copy .env.example .env
```

## Настройка параметров

Отредактируйте файл .env, указав необходимые значения:

- SECRET_KEY=ваш_секретный_ключ
- STRIPE_API_KEY=ваш_api_ключ_stripe
- DEBUG=True/False
- DATABASE_NAME=имя_базы_данных
- DATABASE_USER=пользователь_бд
- DATABASE_PASSWORD=пароль_бд
- EMAIL_HOST=ваш_smtp_хост
- EMAIL_PORT=порт
- EMAIL_HOST_USER=email_логин
- EMAIL_HOST_PASSWORD=email_пароль
- DEFAULT_FROM_EMAIL=email@домен.com


### Запуск приложения
#### Сборка и запуск:

```
docker-compose up -d
```

#### Проверка работоспособности

- Веб-интерфейс: откройте http://localhost:8000 в браузере
- Логи: проверьте через команду ` docker-compose logs -f `
- PostgreSQL: подключитесь к базе данных через pgAdmin или другой клиент
- Redis: используйте `redis-cli` для проверки подключения
- Celery и Celery Beat: проверьте логи в терминале, чтобы убедиться, что задачи выполняются без ошибок

### Управление приложением
#### Перезапуск:

```
docker-compose restart
```

#### Остановка:

```
docker-compose down
```
