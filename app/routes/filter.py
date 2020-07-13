from flask import Flask, render_template, request, abort, g, redirect, url_for, session
import copy

def filterPath(request, other=None):
    path = request.path
    other = str(other) if other else "None"
    return path.startswith("/favicon.ico") or path.startswith("/statics") or path.startswith(other)

def filter(flaskApp, **f):
    print("app>>>>>>>httpServer", flaskApp)
    # g.root_path = flaskApp.root_path
    @flaskApp.before_request
    def auther():
        path = request.path
        # if request.path == "/favicon.ico":
        #     # abort(200)

        if filterPath(request, "/sign"):
            return None

        user = session.get("user")
        if not user:
            print(">>>进入登入页")
            return redirect(url_for("sign.login"))

        return None

    @flaskApp.before_request
    def parserAside():
        if filterPath(request, "/sign"):
            return None
        # rootAside = copy.deepcopy(flaskApp.config["ASIDE"])
        aside = flaskApp.config["ASIDE"]
        rootAside = []
        user = session.get("user")
        if user:
            rootAside = [aside[1], aside[4]] if user["rank"] < 800 else aside
        request.app = {}
        request.app["aside"] = rootAside
        request.app["root"] = flaskApp.root_path
        request.app["pathsName"] = []

        for val in rootAside:
            request.path.startswith(val["url"]) and request.app["pathsName"].append(val["title"])
            if val.get("item") and len(val["item"]) > 0:
                for cval in val["item"]:
                    request.path.startswith(cval["url"]) and request.app["pathsName"].append(cval["title"])

    @flaskApp.before_request
    def pathsFilter():
        if filterPath(request, "/sign"):
            return None
        path = request.path
        startWith = path.split("/", 3)[1]
        filters = []
        user = session.get("user")
        index = flaskApp.config["INDEX"]
        if user and user["rank"] < 800:
            index = "/content"
            filters = ["dev", "rights", "set"]

        if path == "/" or path == "/index" or startWith in filters:
            # 首页/默认页
            return redirect(index)

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
