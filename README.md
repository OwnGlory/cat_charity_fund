# QR KOT
## Описание
Проект для помощи котикам. Пожертвуй денежку на благо котиков.
Пожертвования могут производить только зарегистрированные пользователи.
## Запуск
Создание виртуального окружения
python -m venv venv
Активация виртуального окружения
source venv/Scripts/activate
Установка зависимостей
pip install -r requirements.txt
Применение миграций
alembic upgrade head
Запуск на локальном сервере
uvicorn app.main:app --reload (c автоперезагрузкой)
## Инструменты
Python
FastAPI
Pydantic
Alembic
SQLAlchemy
## Разработчик
Слепов В.А.