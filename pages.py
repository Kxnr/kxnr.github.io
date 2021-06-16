from models import Content, Category
from flask import render_template, current_app

##########
# Special Pages
##########
def home_page(header: Content, feature: Content, previews: Category, extras: list = []):
    '''
    :param feature: name of article to feature
    :param previews: name of category for tiles
    :param collection:
    :param additional_links: additional
    :return:
    '''

#     header = render_component(header)
    feature = render_component(feature)
#     previews = render_component(previews)

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
    feature = render_component(feature)
    return render_template("layouts/feature.html", feature=feature)


##########
# Helper Functions
##########
def render_component(component: Content):
    return current_app.config["render_format"][component.display_type](component)


