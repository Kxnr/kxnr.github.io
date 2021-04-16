from markdown import markdown
from models import Category, Content, db
from jinja2 import Markup
from flask import render_template, url_for
import os

# TODO: is there a better way to build navbar?
# TODO: enhancement: make navbar support popovers for subsection

##########
# functions to accompany each page template and
# build all required data
##########

def home_page(feature: Content, previews: Category = None,
              collection: Content = None, additional_links = None):
    '''
    :param feature: name of article to feature
    :param previews: name of category for tiles
    :param collection:
    :param additional_links: additional
    :return:
    '''

    if feature:
        feature.content = _load_article(feature.content, feature.format)

    return render_template("pages/home.html",
                           feature=feature,
                           previews=previews,
                           collection=collection,
                           additional_links=additional_links)


def gallery_page(category: str):
    return render_template("pages/gallery.html")


def article_page(article: Content):
    return render_template("pages/article.html")


##########
# Functions to support subcomponents of page views
##########


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
        format = os.path.splitext(article)
        with open(article, 'r') as f:
            article = f.read()

    if format == "md":
        return Markup(markdown(article, output_format="html5"))

    if format == "html":
        return Markup(article)

    if format == "raw":
        return article

    raise NotImplementedError(f"format {format} not supported")