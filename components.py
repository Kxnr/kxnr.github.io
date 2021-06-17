from markdown import markdown
from markdown.extensions import Extension as MarkdownExtension
from models import Category, Content, db
from jinja2 import Markup
from flask import render_template, url_for
from utils import encrypt_resource
import xml.etree.ElementTree as ElementTree
import os
from urllib.parse import urlparse
from utils import encrypt_resource
from datastore import create_content_datastore

_datastore = create_content_datastore()

##########
# functions to accompany each page template and
# build all required data
##########
# TODO: enhancement: make navbar support popovers for subsection

def article(component: Content):
    component.content = _load_article(component.content, format=component.format)
    return render_template('components/article.html', component=component)

def panels(component: Content):
    panels = _load_panels(component.content, format=component.format)
    panels.id = component.id # update id for on page links
    return render_template('components/panels.html', component=panels)

def mini_header(component: Content):
    pass

def full_header(components: list[Content], on_page=[]):
    # TODO: always contains login
    # TODO: popover, deal with overflow, group pages
    links = [(f'#{link.id}', link.name) if link in on_page else (link.ref, link.name) for link in components]

    return render_template('components/full_header.html', links=links)

def pdf(component: Content):
    # TODO: support pdf links as well as files
    component.content = encrypt_resource(component.content)
    return render_template('components/pdf.html', component=component)

def footer():
    pass

def error(error):
    # TODO
    return render_template('components/error.html', error=error)

##########
# Functions to support subcomponents of page views
##########

def _load_panels(panels, format='category'):
    if format == 'category':
        return _datastore.find_category(name=panels)

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
        return Markup(markdown(article, output_format="html5", extensions=["smarty", "attr_list", MyExtension()]))

    if format == "html":
        return Markup(article)

    if format == "raw":
        return article

    raise NotImplementedError(f"format {format} not supported")


##########
# Extensions to markdown
##########
class MyExtension(MarkdownExtension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(LinkFixer(md), "link_fixer", 1)
        md.treeprocessors.register(ImageFormatter(md), "image_formatter", 1)

class ImageFormatter:
    def __init__(self, md):
        self.md = md

    def run(self, doc_tree: ElementTree):
        images = doc_tree.findall(f".//*img")
        for img in images:
            # this uses cascading to determine what is applied--md-image should
            # be described later in the stylesheet than other relevant image styles
            # this will only be applied to images derived from ![]() tags, not raw html
            img.set('class', " ".join((img.get('class') or '', "md-image")))

class LinkFixer:
    def __init__(self, md):
        self.md = md

    def run(self, doc_tree: ElementTree):
        def _attribute(attr):
            # get all elements and descendents with attr
            links = doc_tree.findall(f".//*[@{attr}]")

            for element in links:
                link = element.get(attr)

                if urlparse(link).scheme in ('http', 'https'):
                    pass
                elif os.path.exists(link):
                    link = encrypt_resource(link)
                else:
                    # TODO
                    raise Exception()

                element.set(attr, link)

        _attribute('src')
        _attribute('href')
