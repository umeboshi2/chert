import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from ..alchemy import TimeStampMixin
from .base import BaseIdMixin, BaseNameIdMixin
# from .base import UserOwnedMixin


class PersonMixin(BaseNameIdMixin):
    @declared_attr
    def __tablename__(self):
        return 'people'

    @declared_attr
    def blogs(self):
        return relationship('Blog', backref='owner')

    @declared_attr
    def posts(self):
        return relationship('Post', backref='author')

    @declared_attr
    def comments(self):
        return relationship('Comment', backref='author')


class BlogMixin(BaseIdMixin):
    @declared_attr
    def __tablename__(self):
        return 'blogs'

    @declared_attr
    def title(self):
        return sa.Column(sa.UnicodeText)

    @declared_attr
    def owner_id(self):
        return sa.Column(sa.Integer, sa.ForeignKey('people.id'))

    @declared_attr
    def posts(self):
        return relationship('Post', backref='blog')


class PostMixin(BaseIdMixin):
    @declared_attr
    def __tablename__(self):
        return 'posts'

    @declared_attr
    def title(self):
        return sa.Column(sa.UnicodeText)

    @declared_attr
    def content(self):
        return sa.Column(sa.UnicodeText)

    @declared_attr
    def published_at(self):
        return sa.Column(sa.DateTime,
                         nullable=False, default=sa.func.now())

    @declared_attr
    def blog_id(self):
        return sa.Column(sa.Integer, sa.ForeignKey('blogs.id'))

    @declared_attr
    def author_id(self):
        return sa.Column(sa.Integer,
                         sa.ForeignKey('people.id'), nullable=False)

    @declared_attr
    def comments(self):
        return relationship('Comment', backref='post')


class CommentMixin(TimeStampMixin):
    @declared_attr
    def __tablename__(self):
        return 'comments'

    @declared_attr
    def comments_id(self):
        return sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def content(self):
        return sa.Column(sa.UnicodeText)

    @declared_attr
    def author_id(self):
        return sa.Column(sa.Integer,
                         sa.ForeignKey('people.id'), nullable=False)

    @declared_attr
    def post_id(self):
        return sa.Column(sa.Integer, sa.ForeignKey('posts.id'))

    @declared_attr
    def type(self):
        return sa.Column(sa.UnicodeText)
