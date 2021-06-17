from models import Content, Category
from flask import render_template, current_app
from components import error as render_error
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

    add_or_move(header, feature, 0)
    add_or_move(header, previews, 1)
    # header.extend(extras)
    header = filter(lambda x: x is not None, header)

    header = render_component(header, "full_header", on_page=(feature, previews, *extras))
    feature = render_component(feature, feature.display_type)
    previews = render_component(previews, previews.display_type)

    extras = [render_component(extra) for extra in extras]

    return render_template("layouts/home.html",
                           header=header,
                           feature=feature,
                           previews=previews,
                           extras=extras)

##########
# Cookie Cutter Pages
##########
def feature_page(feature: Content):
    feature = render_component(feature, feature.display_type)
    return render_template("layouts/feature.html", feature=feature)

def error_page(error):
    error = render_error(error)
    return render_template("layouts/feature.html", feature=error)

##########
# Helper Functions
##########
def render_component(component, display_type: str, **kwargs):
    return current_app.config["render_format"][display_type](component, **kwargs)


