import os
import json
import time
import requests
from libs.IO import File
import ast
from app.models.Account import Account
from app.models.Set import Theme

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
    # app 用户验证
    @bp.route("/sign", methods=["POST", "GET"])
    def sign():
        account = Account(db, request, pops="id")
        # account = db.models["account"]
        clause = "where name='{0}' and password='{1}'".format(account.name, account.password)
        res = account.model.find("*", clause=clause)
        resData = res["data"]
        if len(resData) > 0:
            user = resData[0]
            user.pop("password")
            resTheme = "all" if user["theme"] == "all" else json.loads(user["theme"])
            params = Theme(db, request, pops="id")
            orderBy = "order by number ASC,id DESC"
            clauseT = orderBy
            # res["data"][0]["theme"] = json.loads(theme)

            if int(user["rank"]) < 800 and not resTheme == "all":
                ids = []
                for idKey in resTheme:
                    ids.append("id={0}".format(int(idKey)))
                idsStr = "id is NULL" if len(ids) == 0 else " or ".join(ids)
                clauseT = "where {0} {1}".format(idsStr, orderBy)
            optRes = params.model.find("*", clause=clauseT)["data"]
            res["data"][0]["theme"] = optRes
        else:
            res["msg"] = "账号或密码错误"
            res["success"] = False
        return json.dumps(res)

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
        context = content_id
        clause = "where id={0}".format(content_id)
        if context.startswith("tag_"):
            context = context.split("_")[1]
            clause = "where tag='{0}'".format(context)
            print(">>>>", context, clause)
        res = version.find("*", clause=clause)
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

    # 下载素材
    @bp.route("/down/<path:type>/<path:filename>", methods=["POST", "GET"])
    def downMaterial(type, filename, outName=None):
        print(">>>>开始普通下载！", type, filename)
        paths = ["data"]
        if type == "db":
            paths.append(type)
        elif type in ["video", "image", "voice"]:
            paths.extend(["statics", type])
        elif type in ["ppt", "pdf"]:
            names = filename.split("/")
            dirName = names[0]
            filename = names[1]
            paths.extend(["statics", type, dirName])
        dirpath = os.path.join(f["request"].app["root"], *paths)
        print(">>>下载路径为：", dirpath, filename, f["request"].app["root"])
        # send_from_directory其他配置项：mimetype=mimetype,cache_timeout=30*60
        response = f["make_response"](f["send_from_directory"](dirpath, filename, as_attachment=True))
        # 处理中文路径问题，不过尽量避免中文路径
        outName = outName if outName else filename
        response.headers["Content-Disposition"] = "attachment; filename={}".format(outName.encode().decode('latin-1'))
        # response.headers["Content-Disposition"] = "attachment; filename={}".format(dirpath.encode().decode('latin-1'))
        return response

    # 下载站点资源
    @bp.route("/app", methods=["POST", "GET"])
    def app():
        # dirpath = os.path.join(f["request"].app["root"], "website", "app.html")
        # print(">>>加载：", dirpath)
        # send_from_directory其他配置项：mimetype=mimetype,cache_timeout=30*60
        # return render(dirpath)
        return render("web/app.html")

    @bp.route("/website/<path:filename>", methods=["POST", "GET"])
    def downWebSite(filename, outName=None):
        print(">>>>开始站点资源下载！", type, filename)
        paths = ["website", "soft"]
        dirpath = os.path.join(f["request"].app["root"], *paths)
        print(">>>下载路径为：", dirpath, filename, f["request"].app["root"])
        # send_from_directory其他配置项：mimetype=mimetype,cache_timeout=30*60
        response = f["make_response"](f["send_from_directory"](dirpath, filename, as_attachment=True))
        # 处理中文路径问题，不过尽量避免中文路径
        outName = outName if outName else filename
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            outName.encode().decode('latin-1'))
        # response.headers["Content-Disposition"] = "attachment; filename={}".format(dirpath.encode().decode('latin-1'))
        return response

    # 设备信息获取
    @bp.route("/dev", methods=["POST", "GET"])
    def dev():
        res = {
            "success": True,
            "msg": "查询设备成功",
            "data": {"lamp": {}, "host": {}, "groups": {}, "infrared": {}, "serial_port": {}, "exhibit": {}}
        }
        orderBy = "order by number ASC,id DESC"
        for key in res["data"]:
            table = db.models[key]
            res["data"][key] = table.find("*", clause=orderBy)["data"]

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
        optRes = content.find("*", clause=orderBy)["data"]
        for i in range(len(optRes)):
            optRes[i]["links"] = json.loads(optRes[i]["links"])
        res["data"]["content"] = optRes
        print("获取到的内容》》", res)
        return json.dumps(res)

    # 内容详情获取
    @bp.route("/content/<path:content_id>", methods=["POST", "GET"])
    def contentDetail(content_id):
        res = {
            "success": True,
            "msg": "查询内容成功",
            "data": {"theme": {}, "content_video": {}, "content_image": {}, "content_web": {}, "content_welcome": {},
                     "content_cover": {}, "content_saver": {}, "content_caption": {}}
        }
        orderBy = "order by number ASC,id DESC"
        caluse = "where content={0} {1}".format(content_id, orderBy)
        for key in res["data"]:
            table = db.models[key]
            useBy = orderBy if key == "theme" else caluse
            res["data"][key] = table.find("*", clause=useBy)["data"]

        return json.dumps(res)

    # 内容详情调试
    @bp.route("/adjust/<path:type>/<path:id>", methods=["POST", "GET"])
    def contentDetail_adjust(type, id):
        tableName = "content_{0}".format(type)
        table = db.models[tableName]
        res = table.find("*", clause="where id={0}".format(id))["data"]
        return json.dumps(res[0] if len(res) > 0 else {})

    @bp.route("/other", methods=["POST", "GET"])
    def other():
        print("other 参数》》", f["request"].role.params)
        return f["render_template"]("templates/jsTable.html")

    # 屏幕节目单
    @bp.route("/detail", methods=["POST", "GET"])
    def detail():
        res = {}
        orderBy = "order by number ASC,id DESC"
        content = db.models["content"]
        cData = content.find("id,name,tag", clause=orderBy)["data"]
        tables = ["content_video", "content_image", "content_web", "content_welcome"]
        for val in cData:
            id = val["id"]
            res[id] = {"name": val["name"], "tag": val["tag"], "data": {}}
            caluse = "where content={0} {1}".format(id, orderBy)
            for key in tables:
                item = ["id", "name", "path"]
                if key == "content_video":
                    item.append("time")
                elif key == "content_welcome":
                    item.remove("name")
                    item.extend(["title", "sub_title"])
                elif key == "content_web":
                    item.remove("path")
                    item.append("url")
                table = db.models[key]
                res[id]["data"][key] = table.find(",".join(item), clause=caluse)["data"]
        print("所有屏幕节目单为{0}".format(res))
        return json.dumps(res)

    # 日志信息
    @bp.route("/log/<path:date>", methods=["POST", "GET"])
    def log(date):
        file = File(os.path.join("log"))
        res = list(filter(lambda val: "【 WS发送 】" in val, file.readLines(date)))
        open, close, video, image, web, welcome, = [], [], [], [], [], []

        for val in res:
            logStr = val.split(" ( ")
            time = logStr[0].split("####")[0].rstrip(":")
            jsonInfo = ast.literal_eval(logStr[1].split(" ) ")[0])
            jsonInfo["time"] = time
            if jsonInfo.get("act") == "ehcc_open":
                open.append(jsonInfo)
            elif jsonInfo.get("act") == "ehcc_close":
                close.append(jsonInfo)
            else:
                key = jsonInfo.get("key")
                data = {
                    "tag": jsonInfo.get("to"), "number": jsonInfo.get("number", 0), "time": jsonInfo.get("time")
                }
                if key == "play":
                    video.append(data)
                elif key in ["image_show", "image_next", "image_pre"]:
                    image.append(data)
                elif key in ["web_show", "web_next", "web_pre"]:
                    web.append(data)
                elif key == "word_open":
                    welcome.append(data)
        openInfo = open[0]["time"] if len(open) > 0 else ""
        closeInfo = close[len(close) - 1]["time"] if len(close) > 0 else ""
        info = {
            "open": openInfo, "close": closeInfo, "video": video, "image": image, "web": web, "welcome": welcome
        }
        print("读取{0}的结果为{1}".format(date, info))
        return json.dumps(info)
