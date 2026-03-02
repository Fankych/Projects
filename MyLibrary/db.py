from flask_sqlalchemy import SQLAlchemy
# db — это "движок" SQLAlchemy, привязанный к Flask.
# Через него мы создаём модели (таблицы) и работаем с сессией (запросы/commit).

db = SQLAlchemy()