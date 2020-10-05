import json
from libs.IO import Movie, File
import time
from app.models.Content import Content, Content_video, Content_image, Content_web, Content_welcome, Content_cover
from app.models.Content import Content_saver, Content_caption
from app.models.Material import Video, Image, Voice
from app.models.Set import Exhibit, Theme
from app.models.Account import Account
from libs.Viewer import Request
import os

def add_route(bp, **f):
    render, db, request, url_for, session = f["render_template"], f["db"], f["request"], f["url_for"], f["session"]
    @bp.route("/", methods=["POST", "GET"])
    def content():
        return render("web/content/index.html")

    @bp.route("/detail", methods=["POST", "GET"])
    def detail():
        params = Request(request)
        return render("web/content/detail.html", detail="{0}-详情：".format(params.value("name")),
                      content_id=params.value("id"))

    @bp.route("/exhibit", methods=["POST", "GET"])
    def contentExhibit():
        params = Exhibit(db, request, pops="id")
        # res = params.model.find("*", clause="order by number ASC,id DESC")
        pat = request.app["pattern"]
        strOrder = "where {0} order by number ASC,id DESC".format("id>0" if pat == 0 else "id=0")
        return json.dumps(params.findBy(orderBy=strOrder))

    @bp.route("/theme", methods=["POST", "GET"])
    def contentTheme():
        params = Theme(db, request, pops="id")
        pat = request.app["pattern"]

        if pat == 1:
            return json.dumps(params.findBy(orderBy="where id=0 order by number ASC,id DESC"))
        elif pat == 0:
            user = session["user"]
            account = Account(db, request)
            res = account.model.find("*", clause="where id={0}".format(user["id"]))["data"]
            themeVal = res[0]["theme"]
            hasTheme = "all" if themeVal == "all" else json.loads(themeVal)

            content = Content(db, request)
            res = content.findBy("id")["data"]
            print("屏幕为：", res, "该用户有权限的主题：", hasTheme)
            resTheme = res[0]["themes"]
            resTheme = [] if resTheme == "" or resTheme == None else resTheme.split(",")
            ids = []
            for idKey in resTheme:
                (hasTheme == "all" or str(idKey) in hasTheme) and ids.append("id={0}".format(int(idKey)))
            idsStr = " or ".join(ids)
            optRes = {"data": [], "success": True} if not idsStr else params.model.find("*", clause="where {0}".format(
                idsStr))
            return json.dumps(optRes)
        else:
            return json.dumps({"data": [], "success": True})

    @bp.route("/themeList", methods=["POST", "GET"])
    def themeList():
        params = Theme(db, request, pops="id")
        pat = request.app["pattern"]
        user = session["user"]
        account = Account(db, request)
        res = account.model.find("*", clause="where id={0}".format(user["id"]))["data"]

        if not pat == 0:
            return json.dumps(params.findBy(orderBy="where id=0 order by number ASC,id DESC"))

        if int(res[0]["rank"]) >= 800 or res[0]["theme"] == "all":
            return json.dumps(params.findBy(orderBy="where id>0 order by number ASC,id DESC"))
        else:
            resTheme = json.loads(res[0]["theme"])
            ids = []
            for idKey in resTheme:
                ids.append("id={0}".format(int(idKey)))
            idsStr = " or ".join(ids)
            optRes = {"data": [], "success": True} if not idsStr else params.model.find("*", clause="where {0}".format(
                idsStr))
            return json.dumps(optRes)
        # res = params.model.find("*", clause="order by number ASC,id DESC")
        # return json.dumps(params.findBy())

    @bp.route("/setThemes", methods=["POST", "GET"])
    def setThemes():
        params = Content(db, request, pops="id")
        updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("params.themes:", params.themes)
        themes = params.themes
        optRes = params.model.update({"time": updateTime, "themes": themes}, clause="where id={0}".format(params.id))
        optRes["data"] = themes
        return json.dumps(optRes)

    @bp.route("/links", methods=["POST", "GET"])
    def contentLinks():
        params = Content(db, request, pops="id")
        updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("params.links", params.links)
        links = json.dumps(params.links.split(","))
        optRes = params.model.update({"time": updateTime, "links": links}, clause="where id={0}".format(params.id))
        optRes["data"] = links
        return json.dumps(optRes)

    @bp.route("/list", methods=["POST", "GET"])
    def contentList():
        params = Content(db, request, pops="id")
        res = params.findBy("exhibit")
        pat = request.app["pattern"]
        strOrder = "where {0} order by number ASC,id DESC".format("exhibit>0" if pat == 0 else "exhibit=0")
        links = params.model.find("id,name,exhibit", clause=strOrder)
        res["links"] = links["data"]
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/add", methods=["POST", "GET"])
    def contentAdd():
        params = Content(db, request, pops=("id", "links", "time"), byNames="exhibit")
        pat = request.app["pattern"]
        strOrder = "where {0} order by number ASC,id DESC".format("exhibit>0" if pat == 0 else "exhibit=0")
        res = params.insert()
        links = params.model.find("id,name,exhibit", clause=strOrder)
        res["links"] = links["data"]
        return json.dumps(res)

    @bp.route("/update", methods=["POST", "GET"])
    def contentUpdate():
        params = Content(db, request, pops=("id", "links"), byNames="exhibit")
        pat = request.app["pattern"]
        strOrder = "where {0} order by number ASC,id DESC".format("exhibit>0" if pat == 0 else "exhibit=0")
        params.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return json.dumps(params.updateById(orderBy=strOrder))

    @bp.route("/del", methods=["POST", "GET"])
    def contentDelete():
        params = Content(db, request, pops="id", byNames="exhibit")
        res = params.deleteById(foreign_keys=True)
        pat = request.app["pattern"]
        strOrder = "where {0} order by number ASC,id DESC".format("exhibit>0" if pat == 0 else "exhibit=0")
        links = params.model.find("id,name,exhibit", clause=strOrder)
        res["links"] = links["data"]
        if res["success"]:
            # 删除与其相关联的links内容
            others = params.model.find("id,name,exhibit,links", clause="where links like '%{0}%'".format(params.id))
            updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for other in others["data"]:
                link = json.loads(other["links"])
                link.remove(params.id)
                link = json.dumps(link)
                print(">>>>>修改后link：", link)
                params.model.update({"time": updateTime, "links": link}, clause="where id={0}".format(other["id"]))

        # return json.dumps(optRes if not optRes["success"] else res)
        return json.dumps(res)

    @bp.route("/vary", methods=["POST", "GET"])
    def contentVary():
        params = Content(db, request, pops="id", byNames="exhibit")
        row = {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        res = params.updateById(row)
        return json.dumps(res)

    # >>>视频
    @bp.route("/video/list", methods=["POST", "GET"])
    def videoList():
        params = Content_video(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content")))
        # return json.dumps(res, default=lambda o: o.__dict__)

    @bp.route("/video/add", methods=["POST", "GET"])
    def videoAdd():
        params = Content_video(db, request, pops="id", byNames=("theme", "content"))
        file = Movie(os.path.join("data", "statics"))
        path = file.up(request, "path", "video")
        params.path = "video/{0}".format(path)
        params.size = 0
        params.cover_size = 0
        if path:
            video = Video(db, request, pops="id")
            size = file.size(("video", path))
            params.size = size
            video.model.insert(
                {"number": 1, "name": params.name, "path": params.path, "label": 0, "time": video.param("time"),
                 "size": size})

        cover = file.up(request, "cover", "image")
        params.cover = "image/{0}".format(cover)
        if cover:
            image = Image(db, request, pops="id")
            size = file.size(("image", cover))
            params.cover_size = size
            image.model.insert({"number": 1, "name": params.name, "path": params.cover, "label": 0, "size": size})

        return json.dumps(params.insert())

    @bp.route("/video/update", methods=["POST", "GET"])
    def videoUpdate():
        params = Content_video(db, request, pops="id", byNames=("theme", "content"))
        file = Movie(os.path.join("data", "statics"))
        path = file.up(request, "path", "video")
        if path:
            video = Video(db, request, pops="id")
            params.path = "video/{0}".format(path)
            size = file.size(("video", path))
            params.size = size
            video.model.insert(
                {"number": 1, "name": params.name, "path": params.path, "label": 0, "time": video.param("time"),
                 "size": size})
        else:
            params.pops("path", "size")

        cover = file.up(request, "cover", "image")
        if cover:
            image = Image(db, request, pops="id")
            params.cover = "image/{0}".format(cover)
            size = file.size(("image", cover))
            params.cover_size = size
            image.model.insert({"number": 1, "name": params.name, "path": params.cover, "label": 0, "size": size})
        else:
            params.pops("cover", "cover_size")

        return json.dumps(params.updateById())

    @bp.route("/video/del", methods=["POST", "GET"])
    def videoDelete():
        params = Content_video(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())

    # >>>图片
    @bp.route("/image/list", methods=["POST", "GET"])
    def imageList():
        params = Content_image(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content"), orderBy="order by number ASC,id ASC"))

    @bp.route("/image/add", methods=["POST", "GET"])
    def imageAdd():
        params = Content_image(db, request, pops="id", byNames=("theme", "content"))
        material = params.param("material")
        name = params.get("name", "")
        pages = []
        file = File(os.path.join("data", "statics"))

        if material:
            m = material.split("_")
            m_path = m[0]
            name_png = m_path.split("/")[1]
            m_page = int(m[1])
            for i in range(m_page):
                params.path = "{0}/{1}_{2}.png".format(m_path, name_png, i)
                print("<>>>>>素材路径》》》", params.path)
                params.size = file.size(params.path)
                params.name = "{0}_{1}".format(name, i)
                pages.append(dict(params))

        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            params.name = name
            size = file.size(("image", path))
            params.size = size
            pages.append(dict(params))
            image.model.insert({"number": 1, "name": params.name, "path": params.path, "label": 0, "size": size})
        # optRes = params.model.insert(dict(params))
        if len(pages) == 0:
            params.path = "image/"
            params.size = 0
            pages.append(dict(params))
        return json.dumps(params.insert(pages, orderBy="order by number ASC,id ASC"))

    @bp.route("/image/update", methods=["POST", "GET"])
    def imageUpdate():
        params = Content_image(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            size = file.size(("image", path))
            params.size = size
            image.model.insert({"number": 1, "name": params.name, "path": params.path, "label": 0, "size": size})
        else:
            params.pops("path", "size")
        return json.dumps(params.updateById(orderBy="order by number ASC,id ASC"))

    @bp.route("/image/del", methods=["POST", "GET"])
    def imageDelete():
        params = Content_image(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById(orderBy="order by number ASC,id ASC"))

    # >>>网页
    @bp.route("/web/list", methods=["POST", "GET"])
    def webList():
        params = Content_web(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content")))

    @bp.route("/web/add", methods=["POST", "GET"])
    def webAdd():
        params = Content_web(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.insert())

    @bp.route("/web/update", methods=["POST", "GET"])
    def webUpdate():
        params = Content_web(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.updateById())

    @bp.route("/web/del", methods=["POST", "GET"])
    def webDelete():
        params = Content_web(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())

    # >>>欢迎词
    @bp.route("/welcome/list", methods=["POST", "GET"])
    def welcomeList():
        params = Content_welcome(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content")))

    @bp.route("/welcome/add", methods=["POST", "GET"])
    def welcomeAdd():
        params = Content_welcome(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        params.path = "image/{0}".format(path)
        params.size = 0
        if path:
            image = Image(db, request, pops="id")
            size = file.size(("image", path))
            params.size = size
            name = params.get("name", "")
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})
        return json.dumps(params.insert())

    @bp.route("/welcome/update", methods=["POST", "GET"])
    def welcomeUpdate():
        params = Content_welcome(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            size = file.size(("image", path))
            params.size = size
            name = params.get("name", "")
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})
        else:
            params.pops("path", "size")
        return json.dumps(params.updateById())

    @bp.route("/welcome/del", methods=["POST", "GET"])
    def welcomeDelete():
        params = Content_welcome(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())

    # >>>封面
    @bp.route("/cover/list", methods=["POST", "GET"])
    def coverList():
        params = Content_cover(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content"), orderBy="order by number ASC,id ASC"))

    @bp.route("/cover/add", methods=["POST", "GET"])
    def coverAdd():
        params = Content_cover(db, request, pops="id", byNames=("theme", "content"))
        material = params.param("material")
        name = params.get("name", "")
        pages = []
        file = File(os.path.join("data", "statics"))

        if material:
            m = material.split("_")
            m_path = m[0]
            name_png = m_path.split("/")[1]
            m_page = int(m[1])
            for i in range(m_page):
                params.path = "{0}/{1}_{2}.png".format(m_path, name_png, i)
                params.size = file.size(params.path)
                params.name = "{0}_{1}".format(name, i)
                pages.append(dict(params))

        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            params.name = name
            size = file.size(("image", path))
            params.size = size
            pages.append(dict(params))
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})

        if len(pages) == 0:
            params.path = "image/"
            params.size = 0
            pages.append(dict(params))
        return json.dumps(params.insert(pages, orderBy="order by number ASC,id ASC"))

    @bp.route("/cover/update", methods=["POST", "GET"])
    def coverUpdate():
        params = Content_cover(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            size = file.size(("image", path))
            params.size = size
            name = params.get("name", "")
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})
        else:
            params.pops("path", "size")
        return json.dumps(params.updateById(orderBy="order by number ASC,id ASC"))

    @bp.route("/cover/del", methods=["POST", "GET"])
    def coverDelete():
        params = Content_cover(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById(orderBy="order by number ASC,id ASC"))

    # >>>屏保
    @bp.route("/saver/list", methods=["POST", "GET"])
    def saverList():
        params = Content_saver(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content")))

    @bp.route("/saver/add", methods=["POST", "GET"])
    def saverAdd():
        params = Content_saver(db, request, pops="id", byNames=("theme", "content"))
        type = "image" if int(params.type) == 0 else "video"
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", type)
        params.path = "{0}/{1}".format(type, path)
        params.size = 0
        if path:
            model = Image if type == "image" else Video
            model_db = model(db, request, pops="id")
            size = file.size((type, path))
            params.size = size
            name = params.get("name", "")
            data = {"number": 1, "name": name, "path": params.path, "label": 0, "size": size}
            if type == "video":
                data["time"] = model_db.param("time")
            model_db.model.insert(data)
        return json.dumps(params.insert())

    @bp.route("/saver/update", methods=["POST", "GET"])
    def saverUpdate():
        params = Content_saver(db, request, pops="id", byNames=("theme", "content"))
        type = "image" if int(params.type) == 0 else "video"
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", type)
        if path:
            model = Image if type == "image" else Video
            model_db = model(db, request, pops="id")
            params.path = "{0}/{1}".format(type, path)
            size = file.size((type, path))
            params.size = size
            name = params.get("name", "")
            data = {"number": 1, "name": name, "path": params.path, "label": 0, "size": size}
            if type == "video":
                data["time"] = model_db.param("time")
            model_db.model.insert(data)
        else:
            params.pops("path", "size")
        return json.dumps(params.updateById())

    @bp.route("/saver/del", methods=["POST", "GET"])
    def saverDelete():
        params = Content_saver(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())

    # >>>解说词
    @bp.route("/caption/list", methods=["POST", "GET"])
    def captionList():
        params = Content_caption(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content")))

    @bp.route("/caption/add", methods=["POST", "GET"])
    def captionAdd():
        params = Content_caption(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "voice")
        params.path = "voice/{0}".format(path)
        params.size = 0
        if path:
            voice = Voice(db, request, pops="id")
            size = file.size(("voice", path))
            params.size = size
            name = params.get("name", "")
            voice.model.insert(
                {"number": 1, "name": name, "path": params.path, "label": 0, "time": voice.param("time"), "size": size})
        return json.dumps(params.insert())

    @bp.route("/caption/update", methods=["POST", "GET"])
    def captionUpdate():
        params = Content_caption(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "voice")
        if path:
            voice = Voice(db, request, pops="id")
            params.path = "voice/{0}".format(path)
            size = file.size(("voice", path))
            params.size = size
            name = params.get("name", "")
            voice.model.insert(
                {"number": 1, "name": name, "path": params.path, "label": 0, "time": voice.param("time"), "size": size})
        else:
            params.pops("path", "size")
        return json.dumps(params.updateById())

    @bp.route("/caption/del", methods=["POST", "GET"])
    def captionDelete():
        params = Content_caption(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())
