from flask import Flask, render_template, request, abort, g
from libs.request import Params

def requester(request):
    with Params(request, ["name", "age", "sex"]) as res:
        request.role = res
        print(">>>>>requester:", request.path, request.role.params["name"], res)

def filterPath(request, other=None):
    path = request.path
    other = str(other) if other else "None"
    return path.startswith("/favicon.ico") or path.startswith("/statics") or path.startswith(other)

def filter(flaskApp, **f):
    print("app>>>>>>>httpServer", flaskApp)
    # g.root_path = flaskApp.root_path
    @flaskApp.before_request
    def auther():
        request.app = {}
        request.app["aside"] = flaskApp.config["ASIDE"]
        request.app["root"] = flaskApp.root_path
        if filterPath(request, "/sign"):
            return None

        # if request.path == "/favicon.ico":
        #     # abort(200)
        if request.path == "/login":
            return None
            print("登入页")
        print("app请求前置处理器auther:》》》》", request.path)
        return None

    @flaskApp.before_request
    def params():
        if filterPath(request, "/sign"):
            return None
        requester(request)
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
