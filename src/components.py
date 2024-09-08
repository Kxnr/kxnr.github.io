'''
This file describes the relationship between data and it's html representation.
In essentially every case, there is a corresponding jinja2 template for each type
of component that describes how to render that piece. The result is an html fragment
that can composited into a full page.

As components are how data is rendered, the options for what display_type and format
are given in the Content database are handled here. Examples of this are at the bottom
of the page. As currently written, display type maps to the component class, while
format instructs the component class how to load the data--e.g. whether to link a
resource or parse the contents of a file.

Though not hugely different from Content objects, Components have the key property
that calling str(component) will return an html rendering of the content of the
component.
'''
from markdown import markdown
from markdown.extensions import Extension as MarkdownExtension
from models import Category, Content, db
from datastore import create_content_datastore
from jinja2.utils import markupsafe
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
            obj.content = Error(e)

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
            obj.content = Error(e)

        return obj

    def __str__(self):
        return render_template('components/panels.html', component=self)


class FullHeader(Component):
    # FIXME: this continues to be a puzzle and seems to point to an issue with
    # how/when components are constructed. Handling on page links requires some
    # knowledge of the page layout, which ideally the component shouldn't know,
    # but there are also decisions about whether to have an on page/separate page
    # link that need to be made before we reach the template layer. Making header
    # a macro in the template is a potential special case solution, but runs into
    # issues with controlling the order where the current list doesn't to the same
    # extent. This may be an argument for a builder based solution?

    @classmethod
    def from_content(cls, components: list[Union[Content, Component]], on_page: list[Union[Content, Component]] = []):
        obj = cls('full-header', 'Full Header', None, None, None)

        on_page = [item.id for item in on_page]
        obj.content = [(f'#{link.id}', link.short_name) if link.id in on_page else (link.ref, link.short_name) for link in components]
        return obj

    def __str__(self):
        return render_template('components/full_header.html', links=self.content)


class MiniHeader(Component):
    pass


class Pdf(Component):
    def __str__(self):
        return render_template('components/pdf.html', component=self)

    @classmethod
    def from_content(cls, component: Content):
        obj = super().from_content(component)
        try:
            obj.content = _load_pdf(obj.content, format=component.format)
        except Exception as e:
            # FIXME
            obj.content = Error(e)

        return obj


class Footer(Component):
    pass


class Error(Component):
    def __init__(self, error):
        self.error = error

    @classmethod
    def from_content(cls, component: Content):
        raise NotImplementedError()

    def __str__(self):
        error = self.error if current_app.config.get("DEBUG", False) else None
        return render_template('components/error.html', error=error)


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
        return markupsafe.Markup(markdown(article, output_format="html5", extensions=["smarty", "attr_list", MyExtension()]))

    if format == "html":
        return markupsafe.Markup(article)

    if format == "raw":
        return article

    raise NotImplementedError(f"format {format} not supported")


def _load_pdf(pdf, format='file'):
    if format == "link":
        return pdf
    elif format == "file":
        return encrypt_resource(pdf)


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
