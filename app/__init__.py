from .routes import form, index, table, test_route, filter, dev, content, rights, down

def config_app(app):
    app.config = ("app.config.secure", "app.config.setting")
    app.flask.add_template_global(app.config["ASIDE"], 'aside')
    app.flask.add_template_global(app.config["ENV"], 'env')
    print(">>>>app.root_path:", app.flask.root_path)
    app.register_filter(filter.filter)
    app.register_router("web", __name__, index.add_route)
    app.register_router("web", __name__, test_route.add_route)
    app.register_router("table", __name__, table.add_route, url_prefix="/table")
    app.register_router("form", __name__, form.add_route, url_prefix="/form")
    app.register_router("dev", __name__, dev.add_route, url_prefix="/dev")
    app.register_router("content", __name__, content.add_route, url_prefix="/content")
    app.register_router("rights", __name__, rights.add_route, url_prefix="/rights")
    app.register_router("down", __name__, down.add_route, url_prefix="/down")
