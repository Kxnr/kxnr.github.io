from flask import url_for, current_app
from flask_security import current_user
import itsdangerous


def encrypt_resource(string):
    user_id = current_user.get_id()
    key = user_id or current_app.config['RESOURCE_KEY']
    access = 'user' if user_id else 'public'

    return url_for("download_resource",
                   encrypted=itsdangerous.URLSafeSerializer(key, salt=access).dumps(string),
                   access=access)


def decrypt_resource(string, method):
    key = current_user.get_id() if method == 'user' else current_app.config['RESOURCE_KEY']
    return itsdangerous.URLSafeSerializer(key, salt=method).loads(string)


def add_or_move(lst, item, index):
    if lst.index(item) == index:
        return

    try:
        lst.remove(item)
    except ValueError:
        pass
    finally:
        lst.insert(index, item)



