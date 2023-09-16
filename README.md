## API Менеджера задач.

Менеджер задач, написан на FastAPI.

### Установка и запуск проекта:

- Клонировать репозиторий;
````angular2html
git clone https://github.com/akorsunov23/task_manager.git
````
- Перейти в рабочую директорию;
````angular2html
cd task_manager/
````
- Переименовать .env.template в .env и заполнить по примеру, а также и в /docker;
- Запустить сборку и запуск контейнера;
```angular2html
docker compose -f docker/docker-compose.yml up --build
```
- суперпользователя можно добавить командой;
```angular2html
docker compose -f docker/docker-compose.yml exec backend python createsuperuser.py
```

--# ДЛЯ ЗАПУСКА ТЕСТОВ #--
- Создать виртуальное окружение;
```angular2html
python3 -m venv venv
```
- Установить зависимости:
```angular2html  
pip install -r req.txt
```
- Активировать виртуальное окружение;
```angular2html
source venv/bin/activate
```
- Изменить данные в .env проекта на локальные хосты
- Выполнить миграции в БД (не забываем добавить в .env данные для тестовой базы данных);
```angular2html
alembic --config alembic_test.ini upgrade head
```
- Запустить Redis;
```angular2html
redis-server
```
- Запустить Celery;
```angular2html
celery --app src.celery_tasks.tasks worker -l INFO
```
- Выполнить тесты;
```angular2html
pytest -v tests/
```


### Обзор проекта:

После запуска контейнера документация проекта будет доступна на 127.0.0.1:8000/docs, а также утилита для Celery на 127.0.0.1:5555.

Возможности проекта:
- CRUD над пользователями. После аутентификации, токен пользователя хранится на 1 час в cookies клиента. Суперпользователю доступны возможности редактирования, чтения и удаления данных других пользователей;  
- CRUD над своими задачами.
- Назначение задач другим пользователям;
- Уведомление пользователю на почту о назначенной задачи;
- Уведомление пользователя на почту о просроченной задаче;
- Отметка о выполнении задачи.
