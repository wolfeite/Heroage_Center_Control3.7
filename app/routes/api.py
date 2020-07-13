import os
import json
import time
import requests

class Dev:
    def __init__(self):
        self.data = {}

    def step(self, *value):
        print("数据：", value)
        if not self.data.get(value[0]):
            self.data[value[0]] = []
        self.data[value[0]].append(value)

    def finalize(self):
        return json.dumps(self.data)

def filterDev(data):
    res = {}
    print(">>??>>", data)
    for row in data:
        val = row["exhibit"]
        if (not res.get(val)):
            res[val] = []
        res[val].append(row)
    return res

def add_route(bp, **f):
    render, db, request, redirect = f["render_template"], f["db"], f["request"], f["redirect"]
    # 版本更新
    @bp.route("/update", methods=["POST", "GET"])
    def updated():
        version = db.models["version"]
        res = version.update({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}, clause="where number=3.7")
        print(">>>数据库更新结果：", res)
        # return render("web/dev.html", type={}, dev={})
        return json.dumps(res)

    # APP版本获取
    @bp.route("/check", methods=["POST", "GET"])
    def checkVersion():
        print("开始检测版本数据库》》")
        version = db.models["version"]
        res = version.find("*", clause="where number=3.7")
        print("APP版本》》", res)
        return json.dumps(res)

    # 内容版本获取
    @bp.route("/vary/<path:content_id>", methods=["POST", "GET"])
    def varyVersion(content_id):
        version = db.models["content"]
        res = version.find("*", clause="where id={0}".format(content_id))
        print(">>>内容版本：", res)
        return json.dumps(res)

    # 数据库下载本机测试
    @bp.route("/down/db/test", methods=["POST", "GET"])
    def test():
        print("downloading with requests")
        # url = 'http://127.0.0.1:3500/down/db/ccs.db'
        url = 'http://192.168.9.54:3500/api/down/db/ccs.db'
        r = requests.get(url)
        with open("copy_css.db", "wb") as code:
            code.write(r.content)

        return json.dumps({"success": True, "msg": "下载成功"})
        # return f["render_template"]("templates/form.html")

    # 下载数据库请求处理
    @bp.route("/down/db/<path:filename>", methods=["POST", "GET"])
    def common(filename):
        # 普通下载
        print(">>>>开始普通下载！")
        dirpath = os.path.join(f["request"].app["root"], 'data', "db")
        print(">>>", f["request"].app["root"], dirpath, filename)
        # send_from_directory其他配置项：mimetype=mimetype,cache_timeout=30*60
        response = f["make_response"](f["send_from_directory"](dirpath, filename, as_attachment=True))
        # 处理中文路径问题，不过尽量避免中文路径
        response.headers["Content-Disposition"] = "attachment; filename={}".format(dirpath.encode().decode('latin-1'))
        return response
        # return f["render_template"]("templates/form.html")

    # 下载视频文件
    @bp.route("/down/video/<path:filename>", methods=["POST", "GET"])
    def downVideo(filename):
        # 普通下载
        print(">>>>开始普通下载！")
        dirpath = os.path.join(f["request"].app["root"], 'data', "statics", "video")
        print(">>>", f["request"].app["root"], dirpath, filename)
        # send_from_directory其他配置项：mimetype=mimetype,cache_timeout=30*60
        response = f["make_response"](f["send_from_directory"](dirpath, filename, as_attachment=True))
        # 处理中文路径问题，不过尽量避免中文路径
        response.headers["Content-Disposition"] = "attachment; filename={}".format(dirpath.encode().decode('latin-1'))
        return response
        # return f["render_template"]("templates/form.html")

    # 设备信息获取
    @bp.route("/dev", methods=["POST", "GET"])
    def dev():
        res = {
            "success": True,
            "msg": "查询设备成功",
            "data": {"lamp": {}, "groups": {}, "infrared": {}, "serial_port": {}}
        }
        orderBy = "order by number ASC,id DESC"
        lamp = db.models["lamp"]
        res["data"]["lamp"] = filterDev(lamp.find("*", clause=orderBy)["data"])
        infrared = db.models["infrared"]
        res["data"]["infrared"] = filterDev(infrared.find("*", clause=orderBy)["data"])
        groups = db.models["groups"]
        res["data"]["groups"] = filterDev(groups.find("*", clause=orderBy)["data"])
        serial_port = db.models["serial_port"]
        res["data"]["serial_port"] = filterDev(serial_port.find("*", clause=orderBy)["data"])
        # orderBy = "group by exhibit order by number ASC,id DESC"

        # res = lamp.find("dev(exhibit,number,port)", clause=orderBy, create_aggregate=("dev", -1, Dev))
        # res = lamp.find("*", clause=orderBy)
        # res["data"] = filterDev(res["data"])
        print("获取到的DEV》》", res)
        return json.dumps(res)

    # 内容信息获取
    @bp.route("/content", methods=["POST", "GET"])
    def content():
        res = {
            "success": True,
            "msg": "查询内容成功",
            "data": {}
        }
        orderBy = "order by number ASC,id DESC"
        exhibit = db.models["exhibit"]
        res["data"]["exhibit"] = exhibit.find("*", clause=orderBy)["data"]
        content = db.models["content"]
        res["data"]["content"] = content.find("*", clause=orderBy)["data"]
        print("获取到的内容》》", res)
        return json.dumps(res)

    # 内容详情获取
    @bp.route("/content/<path:content_id>", methods=["POST", "GET"])
    def contentDetail(content_id):
        res = {
            "success": True,
            "msg": "查询内容成功",
            "data": {}
        }
        orderBy = "order by number ASC,id DESC".format(content_id)
        caluse = "where content={0} {1}".format(content_id, orderBy)
        theme = db.models["theme"]
        res["data"]["theme"] = theme.find("*", clause=orderBy)["data"]
        content_video = db.models["content_video"]
        res["data"]["content_video"] = content_video.find("*", clause=caluse)["data"]
        content_image = db.models["content_image"]
        res["data"]["content_image"] = content_image.find("*", clause=caluse)["data"]
        content_web = db.models["content_web"]
        res["data"]["content_web"] = content_web.find("*", clause=caluse)["data"]
        content_welcome = db.models["content_welcome"]
        res["data"]["content_welcome"] = content_welcome.find("*", clause=caluse)["data"]
        content_cover = db.models["content_cover"]
        res["data"]["content_cover"] = content_cover.find("*", clause=caluse)["data"]
        content_saver = db.models["content_saver"]
        res["data"]["content_saver"] = content_saver.find("*", clause=caluse)["data"]
        content_caption = db.models["content_caption"]
        res["data"]["content_caption"] = content_caption.find("*", clause=caluse)["data"]
        print("获取到的内容详情》》", res, content_id)
        return json.dumps(res)

    @bp.route("/other", methods=["POST", "GET"])
    def other():
        print("other 参数》》", f["request"].role.params)
        return f["render_template"]("templates/jsTable.html")
