from libs.request import Params
# def add_route(bp, request=None, make_response=None, render_template=None, redirect=None, current_app=None, flash=None):
def add_route(bp, **f):
    @bp.route("/index")
    def index():
        with Params(f["request"], ["branches", "leaves"]) as res:
            pass
        print(">>>", f["current_app"].config["ASIDE"])
        headers = {
            # 默认为 text/html
            # 'content-type':'text/plain utf-8',
            'content-type': 'application/json',  # 以接口JSON数据方式响应浏览器
            'location': 'http://www.bing.com'
        }
        return f["render_template"]("templates/index.html")
