from markdown import markdown
from models import Category, Content, db
from jinja2 import Markup
from flask import render_template, url_for
from utils import encrypt_resource
import os

# TODO: enhancement: make navbar support popovers for subsection
render_format = {"article": article,
                 "gallery": panels,
                 "pdf": pdf,
                 "full_header": full_header}

def render_component(component: Content, format=render_format):
    return formats[component.display_type](component)

##########
# functions to accompany each page template and
# build all required data
##########

def article(component: Content):
    component.content = _load_article(component)
    return render_template('components/article.html', component)

def panels(component: Content):
    return render_template('components/panels.html', component)

def mini_header(component: Content):
    pass

def full_header(component: Content):
    component.content = _load_header(component.content, content.format)
    return render_template('components/full_header.html', component)
    pass

def pdf(component: Content):
    # TODO: support pdf links as well as files
    component.content = encrypt_resource(component.content)
    return render_template('components/pdf.html', component)

def footer():
    pass

##########
# Functions to support subcomponents of page views
##########

def _load_header(header, format='category'):
    if format == 'category':
        return = [(link.ref, link.name) for link in content_datastore.find_category(name=header.content).content]

    raise NotImplementedError(f"format {format} not supported")

def _load_gallery(gallery, format='category'):
    if format == 'category':
        return datastore.find_category(name=gallery.content)

    raise NotImplementedError(f"format {format} not supported")

def _load_article(article, format="md"):
    '''
    Load data from article file into html formatted text

    :param article:
    :param format: article format to load
    :return:
    '''
    # TODO: rectify embedded images and links

    if format == "file":
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

    raise NotImplementedError(f"format {format} not supported")
