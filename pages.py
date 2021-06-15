
##########
# Special Pages
##########
def home_page(feature: Content, previews: Category = None, extras: list = []):
    '''
    :param feature: name of article to feature
    :param previews: name of category for tiles
    :param collection:
    :param additional_links: additional
    :return:
    '''

    if feature:
        feature = render_component(feature)

    if previews:
        previews = render_component(previews)

    extras = [render_component(extra) for extra in extras]

    return render_template("layouts/home.html",
                           feature=feature,
                           previews=previews,
                           collection=collection,
                           links=links)

##########
# Cookie Cutter Pages
##########
def feature_page(feature: Content):
    feature = render_component(feature)
    render_template("layouts/feature.html", feature=feature)
