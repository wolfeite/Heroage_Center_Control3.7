# from . import web
# from flask import render_template, request
from libs.request import Params
def open():
    print("ok")
def add_route(bp, **f):
    @bp.route("/test")
    def test():
        print("method:", f["request"].method)
        # return render_template("templates/layout.html")
        # return render_template("templates/dataTable.html")
        # print(app.config["PORT"])
        return f["render_template"]("templates/dataTable.html")

    @bp.route("/width", methods=["get", "post"])
    def width():
        with Params(f["request"], ["name", "age", "sex"]) as res:
            print(">>>>>isGet:", res.isGet)
            # 1 / 0

        return f["render_template"]("templates/error.html", error=res.result) if res.result["error"] else f["render_template"](
            "templates/index.html")
