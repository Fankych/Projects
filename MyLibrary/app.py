from flask import Flask
from db import db

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-change-me"
    # SQLite база будет файлом mylibrary.db рядом с проектом
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///MyLibrary.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # "прикручиваем" db к Flask-приложению
    db.init_app(app)
    # Важно: импорт моделей после init_app,
    # чтобы SQLAlchemy "увидел" классы таблиц.
    from models import User, Title, Entry  # noqa: F401
    # Создаём таблицы (для старта так можно; миграции добавим позже)
    with app.app_context():
        db.create_all()

    @app.get("/")
    def index():
        return "MyLibrary is alive ✅"

    return app

# Flask CLI (shell/run) ищет переменную app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)