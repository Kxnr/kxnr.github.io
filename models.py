from flask_security import UserMixin, RoleMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property
from utils import encrypt_resource

db = SQLAlchemy()

class RoleRequiredMixin():
    # TODO
    pass


class RoleUser(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    tf_totp_secret = db.Column(db.String(255), unique=True, nullable=True)
    tf_primary_method = db.Column(db.String(64), nullable=True)
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class ContentCategory(db.Model):
    __tablename__ = 'content_categories'
    id = db.Column(db.Integer(), primary_key=True)
    content_id = db.Column('content_id', db.Integer(), db.ForeignKey('content.id'))
    category_id = db.Column('category_id', db.Integer(), db.ForeignKey('category.id'))


class ContentRoles(db.Model):
    __tablename__ = 'content_roles'
    id = db.Column(db.Integer(), primary_key=True)
    content_id = db.Column('content_id', db.Integer(), db.ForeignKey('content.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class Content(db.Model):
    __tablename__ = 'content'

    # display data
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80))
    format = db.Column(db.String(), default="file")  # file, raw, html, or md
    description = db.Column(db.String(256), nullable=True)

    _thumbnail = db.Column('thumbnail', db.String(80), nullable=True)
    _short_name = db.Column('short_name', db.String(80), nullable=True)

    @hybrid_property
    def thumbnail(self):
        return encrypt_resource(self._thumbnail)

    @thumbnail.setter
    def thumbnail(self, thumbnail):
        self._thumbnail = thumbnail

    @hybrid_property
    def short_name(self):
        return self._short_name or self.name

    @short_name.setter
    def short_name(self, short_name):
        self._short_name = short_name

    # metadata
    display_type = db.Column(db.String(16))
    allowed_roles = db.relationship('Role', secondary='content_roles',
                                    backref=db.backref('content', lazy='dynamic'))
    categories = db.relationship('Category', secondary='content_categories',
                                 backref=db.backref('content', lazy='joined'))

    @property
    def ref(self):
        if self.display_type == "link":
            return self.content
        else:
            return url_for("content_page", display_type=self.display_type, content=self.name)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)