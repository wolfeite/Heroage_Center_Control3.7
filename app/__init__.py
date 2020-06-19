from .routes import filter, dev, content, rights, down, set

def config_jinja(app):
    app.flask.add_template_global(app.config["ASIDE"], 'aside')
    app.flask.add_template_global(app.config["ENV"], 'env')
    @app.flask.template_filter('parserPath')
    def parserPath(arr):
        res = []
        for val in arr:
            not val == "" and res.append(val)
        return res

def config_db(app):
    db = app.attr["db"]
    exhibit = db.model("exhibit", {
        "id": "integer not null primary key autoincrement unique",
        "number": "integer not null",
        "name": "text"
    })
    lamp = db.model("lamp", {
        "id": "integer not null primary key autoincrement unique",
        "exhibit": "int not null references exhibit(id) on delete cascade",
        "number": "integer not null",
        "port": "int not null unique",
        "name": "text not null",
        "type": "boolean not null",
        "display": "boolean not null",
        "delay": "int not null",
        "style": "text",
        "offset_x": "int",
        "offset_y": "int",
        "scale": "float",
        "grouped": "text",
    }, foreign="foreign key(exhibit) references exhibit(id)")

def config_app(app):
    app.config = ("app.config.secure", "app.config.setting")
    config_jinja(app)
    config_db(app)
    print(">>>>app.root_path:", app.flask.root_path)
    app.register_filter(filter.filter)
    app.register_router("dev", __name__, dev.add_route, url_prefix="/dev")
    app.register_router("content", __name__, content.add_route, url_prefix="/content")
    app.register_router("rights", __name__, rights.add_route, url_prefix="/rights")
    app.register_router("down", __name__, down.add_route, url_prefix="/down")
    app.register_router("set", __name__, set.add_route, url_prefix="/set")
