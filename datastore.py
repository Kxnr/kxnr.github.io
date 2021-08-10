import flask
from flask_security.datastore import Datastore, SQLAlchemyDatastore, SQLAlchemyUserDatastore
from sqlalchemy.orm import joinedload, lazyload
import flask_security
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, true
from models import User, Role, Content, Category, db
from werkzeug.local import LocalProxy

def create_user_datastore():
    if flask.current_app:
        if "user_datastore" not in flask.g:
            flask.g["user_datastore"] = SQLAlchemyUserDatastore(db, User, Role)
        return flask.g
    else:
        return LocalProxy(lambda: SQLAlchemyUserDatastore(db, User, Role))


def create_content_datastore():
    if flask.current_app:
        if "user_datastore" not in flask.g:
            flask.g["user_datastore"] = SQLAlchemyContentDatastore(db, Content, Category)
        return flask.g
    else:
        return LocalProxy(lambda: SQLAlchemyContentDatastore(db, Content, Category))


class SQLAlchemyContentDatastore(SQLAlchemyDatastore, Datastore):

    def __init__(self, db, content_model, category_model):
        self.content_model = content_model
        self.category_model = category_model
        SQLAlchemyDatastore.__init__(self, db)

    def find_content(self, one=False, **kwargs):
        '''
        :param user:
        :param kwargs:
        :return:
        '''

        query = self.content_model.query
        query = query.options(joinedload("categories")).options(joinedload("allowed_roles"))


        if "categories" in kwargs:
            # allow different kwargs for find_categories
            kwargs["categories"] = [self.find_category(name=c) if isinstance(c, str) else c for c in kwargs["categories"]]
            query = query.filter(and_(self.content_model.categories.contains(c) for c in kwargs.pop("categories")))

        query = query.filter_by(**kwargs)

        if one:
            return query.first()
        else:
            return query.all()

    def find_category(self, **kwargs):
        return self.category_model.query.filter_by(**kwargs).first()

    def create_content(self, name, content, description, **kwargs):
        content_obj = self.find_content(name=name)
        if len(content_obj):
            return False

        kwargs["name"] = name
        kwargs["content"] = content
        kwargs["description"] = description

        thumbnail = None
        if "thumbnail" in kwargs:
            # TODO: this is pretty inelegant, and suggests a need for clarification
            # of model vs datastore
            thumbnail = kwargs.pop("thumbnail")

        row = self.content_model(**kwargs)
        row.thumbnail = thumbnail
        self.put(row)
        return True

    def update_content(self, entry, **kwargs):
        for k, v in kwargs.items():
            setattr(entry, k, v)
        self.put(entry)
        return True

    def create_category(self, category, description):
        cat_obj = self.find_category(name=category)
        if cat_obj is not None:
            return False

        self.put(self.category_model(name=category,
                                     description=description))
        return True

    def update_category(self, entry, **kwargs):
        for k, v in kwargs.items():
            setattr(entry, k, v)
        self.put(entry)
        return True

    def add_content_to_category(self, content, category):
        if category not in content.categories:
            content.categories.append(category)
            self.put(content)
            return True
        return False

    def remove_content_from_category(self, content, category):
        if category in content.categories:
            content.categories.remove(category)
            self.put(content)
            return True
        return False
