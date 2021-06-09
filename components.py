from markdown import markdown
from models import Category, Content, db
from jinja2 import Markup
from flask import render_template, url_for
from utils import encrypt_resource
import os

# TODO: enhancement: make navbar support popovers for subsection

##########
# functions to accompany each page template and
# build all required data
##########


def home_page(feature: Content, previews: Category = None,
              collection: Content = None, links: list = []):
    '''
    :param feature: name of article to feature
    :param previews: name of category for tiles
    :param collection:
    :param additional_links: additional
    :return:
    '''

    if feature:
        feature.content = _load_article(feature.content, format=feature.format)

    return render_template("pages/home.html",
                           feature=feature,
                           previews=previews,
                           collection=collection,
                           links=links)


def gallery_page(category: str):
    # TODO
    return render_template("pages/gallery.html")


def article_page(article: Content):
    article.content = _load_article(article.content, format=article.format)
    return render_template("pages/feature.html", feature=article)

def full_header():
    # TODO: read header links out of a file
    pass


##########
# Functions to support subcomponents of page views
##########

def _load_header(header_content):
    # TODO: links as content:, category:, and external:
    pass

def _load_article(article, format="md"):
    '''
    Load data from article file into html formatted text

    :param article:
    :param format: article format to load
    :return:
    '''
    # TODO: rectify embedded images and links

    if format == "file":
        # TODO split ext
        _, format = os.path.splitext(article)
        format = format[1:] # split decimal

        with open(article, 'r') as f:
            article = f.read()

    if format == "md":
        return Markup(markdown(article, output_format="html5", extensions=["smarty"]))

    if format == "html":
        return Markup(article)

    if format == "raw":
        return article

    if format == "pdf":
        return f'<embed src="{encrypt_resource(article)}" type="application/pdf">'

    raise NotImplementedError(f"format {format} not supported")
