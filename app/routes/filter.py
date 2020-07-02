from flask import Flask, render_template, request, abort, g, redirect, url_for, session
from libs.request import Params

def requester(request, params=[]):
    with Params(request, params) as res:
        request.params = res.params
        print(">>>>>requester:", request.path, res)

def filterPath(request, other=None):
    path = request.path
    other = str(other) if other else "None"
    return path.startswith("/favicon.ico") or path.startswith("/statics") or path.startswith(other)

def filter(flaskApp, **f):
    print("app>>>>>>>httpServer", flaskApp)
    # g.root_path = flaskApp.root_path
    @flaskApp.before_request
    def parser():
        staticAside = flaskApp.config["ASIDE"]
        request.app = {}
        request.app["aside"] = staticAside
        request.app["root"] = flaskApp.root_path
        request.app["pathsName"] = []

        for val in staticAside:
            request.path.startswith(val["url"]) and request.app["pathsName"].append(val["title"])
            if val.get("item") and len(val["item"]) > 0:
                for cval in val["item"]:
                    request.path.startswith(cval["url"]) and request.app["pathsName"].append(cval["title"])

    @flaskApp.before_request
    def auther():
        path = request.path
        if filterPath(request, "/sign"):
            return None

        # if request.path == "/favicon.ico":
        #     # abort(200)

        if filterPath(request, "/sign"):
            return None

        user = session.get("user")
        if not user:
            print(">>>进入登入页")
            return redirect(url_for("sign.login"))

        if path == "/" or path == "/index":
            # 首页
            return redirect(flaskApp.config["INDEX"])
        return None

    @flaskApp.before_request
    def params():
        if filterPath(request):
            return None
        path = request.path
        routeRoot = path.split("/", 3)[1]

        list = {
            # "sign": ["id", "number", "name", "password", "nickname", "rank", "right"],
            # "rights": ["id", "number", "name", "password", "nickname", "rank", "right"],
            #  "set": ["id", "number", "name"],
            # "dev": ["id", "exhibit", "number", "port", "name", "type", "display", "delay_start", "delay_end",
            #         "num_start", "num_end" "style", "offset_x", "offset_y", "scale", "grouped", "host", "tag",
            #         "params"],
            "material": ["id", "number", "name", "label", "size", "time", "path"],
            # "content": [
            #     "id", "exhibit", "number", "name", "tag", "ip", "width", "height", "play", "volume", "loop",
            #     "cover_play", "display", "style", "scale", "offset_x", "offset_y", "theme", "content", "path", "cover",
            #     "display_modal", "zoom_x", "zoom_y", "action_start", "action_end", "url", "title", "color", "font",
            #     "align", "sub_title", "sub_color", "sub_font", "sub_offset_x", "sub_offset_y", "sub_align", "type",
            #     "text"
            # ]
        }
        paramsList = list.get(routeRoot)
        paramsList = paramsList if paramsList else []
        print(">>>>获取参数数组", paramsList, routeRoot)
        requester(request, paramsList)
        # 1 / 0
        print("app请求前置处理器》》》》params:", request.path)
        return None

    @flaskApp.after_request
    def excp(response):
        if not filterPath(request, "/sign"):
            print("《《《《app请求结果处理器", request.path, response)
        return response
    # register_route(app)

    # # 在请求之后,出现异常时执行
    # @app.teardown_request
    # def teardown_request(e):
    #     # 在请求之后,必须接受异常作为参数
    #     print("teardown_request" + "异常:" + str(e), request.path)

    if flaskApp.config["ENV"] == "production":
        @flaskApp.errorhandler(404)
        def error_404(error_info):
            # werkzeug.exceptions.InternalServerError
            # werkzeug.exceptions.NotFound
            if not filterPath(request, "/sign"):
                print("request:", type(error_info), request.path)
            return render_template("templates/error.html", error=error_info)

        @flaskApp.errorhandler(Exception)
        def error_other(error):
            """这个handler可以catch住所有的abort(500)和raise exeception."""
            response = dict(status=0, message="500 Error")
            if not filterPath(request, "/sign"):
                print("other_error:", type(error), ">>>>>", error, request.path)
            return render_template("templates/error.html", error=error)

    # 注意debug模式下只能在主线程中
    # app.run(host="0.0.0.0", debug=app.config["DEBUG"], port=app.config["PORT"])
