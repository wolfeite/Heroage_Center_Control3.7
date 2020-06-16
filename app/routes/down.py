import os
def add_route(bp, **f):
    @bp.route("/db/<path:filename>")
    def common(filename):
        # 普通下载
        dirpath = os.path.join(f["request"].app["root"], 'data', "db")
        print(">>>", f["request"].app["root"], dirpath, filename)
        # send_from_directory其他配置项：mimetype=mimetype,cache_timeout=30*60
        response = f["make_response"](f["send_from_directory"](dirpath, filename, as_attachment=True))
        # 处理中文路径问题，不过尽量避免中文路径
        response.headers["Content-Disposition"] = "attachment; filename={}".format(dirpath.encode().decode('latin-1'))
        return response
        # return f["render_template"]("templates/form.html")

    @bp.route("/other")
    def other():
        print("other 参数》》", f["request"].role.params)
        return f["render_template"]("templates/jsTable.html")
