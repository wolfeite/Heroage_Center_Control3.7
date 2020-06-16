from libs.request import Params
def add_route(bp, **f):
    @bp.route("/data")
    def dataTable():
        print(">>>>>>>>/table/data")
        with Params(f["request"], ["branches", "leaves"]) as res:
            pass
        return f["render_template"]("templates/dataTable.html")

    @bp.route("/js")
    def jsTable():
        with Params(f["request"], ["branches", "leaves"]) as res:
            pass
        return f["render_template"]("templates/jsTable.html")
