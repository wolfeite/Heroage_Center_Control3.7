from libs.request import Params
def add_route(bp, **f):
    @bp.route("/input")
    def input():
        print("input 参数》》",f["request"].role.params)
        return f["render_template"]("templates/form.html")

    @bp.route("/other")
    def other():
        print("other 参数》》",f["request"].role.params)
        return f["render_template"]("templates/jsTable.html")