import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(30), unique=True)
    email = sa.Column(sa.String(30), unique=True)
    password_hash = sa.Column(sa.String())


class Blog(BaseModel):
    __tablename__ = "blogs"

    id = sa.Column(sa.Integer, primary_key=True)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    title = sa.Column(sa.Text, unique=True)
    content = sa.Column(sa.Text)
    publication_date = sa.Column(sa.DateTime)


class Comment(BaseModel):
    __tablename__ = "comments"

    id = sa.Column(sa.Integer, primary_key=True)
    is_on = sa.Column(sa.Integer, sa.ForeignKey("blogs.id"))
    is_by = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    content = sa.Column(sa.Text)