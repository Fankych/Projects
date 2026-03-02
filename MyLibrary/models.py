from datetime import datetime
from db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # relationship: у пользователя много записей в библиотеке (Entry)
    entries = db.relationship(
        "Entry",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

class Title(db.Model):
    __tablename__ = "titles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # relationship: один Title может встречаться во многих Entry (у разных юзеров)
    entries = db.relationship(
        "Entry",
        back_populates="title",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Title id={self.id} kind={self.kind} name={self.name!r}"

class Entry(db.Model):
    """
       Entry = "Запись в библиотеке пользователя"
       Это связь User <-> Title + данные пользователя: статус/оценка/заметка.
       """
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title_id = db.Column(db.Integer, db.ForeignKey("titles.id"), nullable=False)
    # planned / in_progress / completed / dropped
    status = db.Column(db.String(20), nullable=False, default="planned")
    # 0..10 (пока без жёстких ограничений — добавим позже)
    rating = db.Column(db.Integer, nullable=True)
    note = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # ORM-связи
    user = db.relationship("User", back_populates="entries")
    title = db.relationship("Titles", back_populates="entries")

    def __repr__(self):
        return f"<Entry id={self.id} user_id={self.user_id} title_id={self.title_id} status={self.status}>"