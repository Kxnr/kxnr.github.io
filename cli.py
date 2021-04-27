import click
from functools import wraps
from flask import current_app
from flask_security import login_user, logout_user
import flask_security
import flask.cli
from datastore import create_user_datastore, create_content_datastore

with_appcontext = flask.cli.with_appcontext
_datastore = create_content_datastore()
_security_datastore = create_user_datastore()


def commit(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
        _datastore.commit()
    return wrapper


@click.group()
def content():
    """Content commands."""


@click.group()
def category():
    """Category commands."""

##########
# Content Commands
##########


@content.command("create")
@click.argument("name")
@click.argument("content")
@click.argument("description")
@click.option("--format", default="file")
@click.option("--thumbnail", default=None)
@click.option("--display", default="article")
@click.option("--role", default=[], multiple=True)
@click.option("--category", default=[], multiple=True)
@with_appcontext
@commit
def content_creator(name, content, description, **kwargs):
    kwargs["display_type"] = kwargs.pop("display")
    kwargs["required_roles"] = [_security_datastore.find_role(r) for r in kwargs.pop("role")]
    kwargs["categories"] = [_datastore.find_category(c) for c in kwargs.pop("category")]

    """Add content to content database"""
    if _datastore.create_content(name, content, description, **kwargs):
        click.secho(
            f'Content added successfully.',
            fg="green",
        )
    else:
        raise click.UsageError("Cannot to add content")


@content.command("edit")
@click.argument("name")
@click.option("--new-name", default="")
@click.option("--content", default="")
@click.option("--description", default="")
@click.option("--format", default="")
@click.option("--thumbnail", default="")
@click.option("--display", default="")
@click.option("--role", default=[], multiple=True)
@click.option("--category", default=[], multiple=True)
@with_appcontext
@commit
def content_editor(name, **kwargs):
    """Change properties on content object"""
    content_obj = _datastore.find_content(name=name, one=True)

    if content_obj is None:
        raise click.UsageError("Content not found")

    values = {k: v for k, v in kwargs.items() if v != ""}
    if "new_name" in values:
        values["name"] = values["new_name"]
        del values["new_name"]
    
    if _datastore.update_content(content_obj, **values):
        click.secho(
            f'Updated content "{content_obj.name}"',
            fg="green",
        )
    else:
        raise click.UsageError("Cannot update content")

# TODO: add Role separately from edit

##########
# Category Commands
##########


@category.command("create")
@click.argument("category")
@click.option("--description", default=None)
@with_appcontext
@commit
def category_creator(category, **kwargs):
    """Create new category entry with optional description"""
    if _datastore.create_category(category, kwargs["description"]):
        click.secho(
            f'Category "{category}" created successfully',
            fg="green",
        )
    else:
        raise click.UsageError("Cannot create category")


@category.command("add")
@click.argument("category")
@click.argument("article")
@with_appcontext
@commit
def category_adder(category, content):
    content_obj = _datastore.find_content(name=content)
    if content_obj is not None:
        raise click.UsageError("Cannot find content")

    category_obj = _datastore.find_category(name=category)
    if category_obj is None:
        raise click.UsageError("Cannot find category")

    if _datastore.add_content_to_category(content_obj, category_obj):
        click.secho(
            f'Content "{content}" added to "{category}" successfully',
            fg="green",
        )
    else:
        click.UsageError("Cannot add content to category")


@category.command("remove")
@click.argument("category")
@click.argument("article")
@with_appcontext
@commit
def category_remover(category, content):
    content_obj = _datastore.find_content(name=content)
    if content_obj is None:
        raise click.UsageError("Cannot find content")

    category_obj = _datastore.find_category(name=category)
    if category_obj is None:
        raise click.UsageError("Cannot find category")

    if _datastore.remove_content_from_category(content_obj, category_obj):
        click.secho(
            f'Content "{content}" removed from "{category}" successfully',
            fg="green",
        )
    else:
        click.UsageError("Cannot remove content from category")
