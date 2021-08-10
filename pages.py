from flask import render_template, current_app
from models import Content, Category
from components import error as render_error
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

    feature = render_content(feature, feature.display_type)
    previews = render_content(previews, previews.display_type)

    # add on page links to header
    add_or_move(header, feature, 0)
    add_or_move(header, previews, 1)
    # header.extend(extras)

    header = filter(lambda x: x is not None, header)
    header = render_content(header, "full_header", on_page=(feature, previews, *extras))

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
    error = render_error(error) if current_app.config["DEBUG"] else None
    return render_template("layouts/feature.html", feature=error)



