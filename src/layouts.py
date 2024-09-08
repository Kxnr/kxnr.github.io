'''
This file describes the organization of full pages. Most pages are categorical,
such as the feature, and can be built from what amounts to a generic template.
For special cases, such as the home page, a dedicated function ensures that items
are ordered as expected and things like on page links are handled correctly.

NOTE: As noted in components, dealing with headers and the fact that all pages
to this point are linear, it may be worthwhile considering a builder
based solution more, and moving away from the full page templates
'''
from flask import render_template
from models import Content, Category
from components import render_content
from utils import add_or_move


##########
# Special Pages
##########
def home_page(header: list[Content], feature: Content, previews: Category, extras: list = []):
    '''
    :param feature: name of article to feature
    :param previews: name of category for tiles
    :param collection:
    :param additional_links: additional
    :return:
    '''

    # move feature and previews links to the front of the header
    add_or_move(header, feature, 0)
    add_or_move(header, previews, 1)
    # header.extend(extras)

    header = filter(lambda x: x is not None, header)
    header = render_content(header, "full_header", on_page=(feature, previews, *extras))

    feature = render_content(feature, feature.display_type)
    previews = render_content(previews, previews.display_type)

    extras = [render_content(extra) for extra in extras]

    return render_template("layouts/home.html",
                           header=header,
                           feature=feature,
                           previews=previews,
                           extras=extras)


##########
# Cookie Cutter Pages
##########
def feature_page(feature: Content):
    feature = render_content(feature, feature.display_type)
    return render_template("layouts/feature.html", feature=feature)


def error_page(error):
    return render_template("layouts/feature.html", feature=error)
