from markdown import markdown
from markdown.extensions import Extension as MarkdownExtension
from models import Category, Content, db
from datastore import create_content_datastore
from jinja2 import Markup
from flask import render_template, url_for, current_app
from utils import encrypt_resource
import xml.etree.ElementTree as ElementTree
import os
from urllib.parse import urlparse
from typing import Union

_datastore = create_content_datastore()

##########
# Helper Functions
##########
def render_content(component: Union[Content, list[Content]], display_type: str, **kwargs):
    return current_app.config["render_format"][display_type].from_content(component, **kwargs)

# WIP
class Component:
    def __init__(self, id, title, content, ref, short_name=None, thumbnail=None):
        self._id = id
        self.title = title
        self.short_name = short_name
        self.content = content
        self.thumbnail = thumbnail
        self._ref = ref

    def __str__(self):
        '''Render this page component into an html string'''
        return self.content

    @classmethod
    def from_content(cls, component: Content):
        return cls(id=component.id, title=component.name,
                   short_name=component.short_name,
                   content=component.content, ref=component.ref,
                   thumbnail=component.thumbnail)

    @property
    def id(self):
        return self._id

    @property
    def ref(self):
        return self._ref

class Article(Component):
    @classmethod
    def from_content(cls, component: Content):
        obj = super().from_content(component)
        try:
            obj.content = _load_article(obj.content, format=component.format)
        except Exception as e:
            # FIXME
            obj.content = error(e)

        return obj

    def __str__(self):
        return render_template('components/article.html', component=self)

class Panels(Component):
    @classmethod
    def from_content(cls, component: Content):
        obj = super().from_content(component)

        try:
            obj.content = _load_panels(obj.content, format=component.format)
            # FIXME
        except Exception as e:
            obj.content = error(e)

        return obj

    def __str__(self):
        return render_template('components/panels.html', component=self)

class FullHeader(Component):

    @classmethod
    def from_content(cls, components: list[Content], on_page=[]):
        obj = cls('full-header', 'Full Header', None, None, None)
        obj.content = [(f'#{link.id}', link.name) if link in on_page else (link.ref, link.name) for link in components]
        return obj

    def __str__(self):
        return render_template('components/full_header.html', links=self.content)

class MiniHeader(Component):
    pass

class Pdf(Component):
    def __str__(self):
        return render_template('components/panels.html', component=self)

class Footer(Component):
    pass

class Error(Component):
    def __init__(self, error):
        self.error = error

    @classmethod
    def from_content(cls, component: Content):
        raise NotImplementedError()

    def __str__(self):
        return render_template('components/error.html', error=self.error)

def error(error):
    return Error(error)

##########
# Functions to support subcomponents of page views
##########

def _load_panels(panels, format='category'):
    if format == 'category':
        return [render_content(c, c.display_type) for c in _datastore.find_category(name=panels).content]

    raise NotImplementedError(f"format {format} not supported")

def _load_article(article, format="md"):
    '''
    Load data from article file into html formatted text

    :param article:
    :param format: article format to load
    :return:
    '''
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
                    # FIXME
                    raise Exception()

                element.set(attr, link)

        _attribute('src')
        _attribute('href')
