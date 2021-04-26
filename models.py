from flask_security import Security, UserMixin, RoleMixin, login_required, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, orm
import flask_login

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
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(80))
    format = db.Column(db.String(), default="file")  # file, raw, html, or md
    thumbnail = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(256), nullable=True)

    # metadata
    display_type = db.Column(db.String(16))
    required_roles = db.relationship('Role', secondary='content_roles',
                                 backref=db.backref('Content', lazy='dynamic'))
    categories = db.relationship('Category', secondary='content_categories',
                                 backref=db.backref('Content', lazy='dynamic'))


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
