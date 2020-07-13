import json
from libs.IO import Movie, File
import time
from app.models.Content import Content, Content_video, Content_image, Content_web, Content_welcome, Content_cover
from app.models.Content import Content_saver, Content_caption
from app.models.Material import Video, Image
from app.models.Set import Exhibit, Theme
from libs.Viewer import Request
import os

def add_route(bp, **f):
    render, db, request, url_for = f["render_template"], f["db"], f["request"], f["url_for"]
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
        return json.dumps(params.findBy())

    @bp.route("/theme", methods=["POST", "GET"])
    def contentTheme():
        params = Theme(db, request, pops="id")
        # res = params.model.find("*", clause="order by number ASC,id DESC")
        return json.dumps(params.findBy())

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
        links = params.model.find("id,name,exhibit")
        res["links"] = links["data"]
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/add", methods=["POST", "GET"])
    def contentAdd():
        params = Content(db, request, pops=("id", "links", "time"), byNames="exhibit")
        res = params.insert()
        links = params.model.find("id,name,exhibit")
        res["links"] = links["data"]
        return json.dumps(res)

    @bp.route("/update", methods=["POST", "GET"])
    def contentUpdate():
        params = Content(db, request, pops=("id", "links"), byNames="exhibit")
        params.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return json.dumps(params.updateById())

    @bp.route("/del", methods=["POST", "GET"])
    def contentDelete():
        params = Content(db, request, pops="id", byNames="exhibit")
        res = params.deleteById(foreign_keys=True)
        links = params.model.find("id,name,exhibit")
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
        if path:
            video = Video(db, request, pops="id")
            size = file.size(("video", path))
            video.model.insert(
                {"number": 1, "name": params.name, "path": params.path, "label": 0, "time": video.param("time"),
                 "size": size})

        cover = file.up(request, "cover", "image")
        params.cover = "image/{0}".format(cover)
        if cover:
            image = Image(db, request, pops="id")
            size = file.size(("image", cover))
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
            video.model.insert(
                {"number": 1, "name": params.name, "path": params.path, "label": 0, "time": video.param("time"),
                 "size": size})
        else:
            params.pops("path")

        cover = file.up(request, "cover", "image")
        if cover:
            image = Image(db, request, pops="id")
            params.cover = "image/{0}".format(cover)
            size = file.size(("image", cover))
            image.model.insert({"number": 1, "name": params.name, "path": params.cover, "label": 0, "size": size})
        else:
            params.pops("cover")

        return json.dumps(params.updateById())

    @bp.route("/video/del", methods=["POST", "GET"])
    def videoDelete():
        params = Content_video(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())

    # >>>图片
    @bp.route("/image/list", methods=["POST", "GET"])
    def imageList():
        params = Content_image(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content")))

    @bp.route("/image/add", methods=["POST", "GET"])
    def imageAdd():
        params = Content_image(db, request, pops="id", byNames=("theme", "content"))
        material = params.param("material")
        pages = []
        if material:
            m = material.split("_")
            m_path = m[0]
            name_png = m_path.split("/")[1]
            m_page = int(m[1])
            for i in range(m_page):
                params.path = "{0}/{1}_{2}.png".format(m_path, name_png, i)
                pages.append(dict(params))

        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            pages.append(dict(params))
            size = file.size(("image", path))
            image.model.insert({"number": 1, "name": params.name, "path": params.path, "label": 0, "size": size})
        # optRes = params.model.insert(dict(params))
        if len(pages) == 0:
            params.path = "image/"
            pages.append(dict(params))
        return json.dumps(params.insert(pages))

    @bp.route("/image/update", methods=["POST", "GET"])
    def imageUpdate():
        params = Content_image(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            size = file.size(("image", path))
            image.model.insert({"number": 1, "name": params.name, "path": params.path, "label": 0, "size": size})
        else:
            params.pops("path")
        return json.dumps(params.updateById())

    @bp.route("/image/del", methods=["POST", "GET"])
    def imageDelete():
        params = Content_image(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())

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
        if path:
            image = Image(db, request, pops="id")
            size = file.size(("image", path))
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
            name = params.get("name", "")
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})
        else:
            params.pops("path")
        return json.dumps(params.updateById())

    @bp.route("/welcome/del", methods=["POST", "GET"])
    def welcomeDelete():
        params = Content_welcome(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())

    # >>>封面
    @bp.route("/cover/list", methods=["POST", "GET"])
    def coverList():
        params = Content_cover(db, request, pops="id")
        return json.dumps(params.findBy(("theme", "content")))

    @bp.route("/cover/add", methods=["POST", "GET"])
    def coverAdd():
        params = Content_cover(db, request, pops="id", byNames=("theme", "content"))
        material = params.param("material")
        pages = []
        if material:
            m = material.split("_")
            m_path = m[0]
            name_png = m_path.split("/")[1]
            m_page = int(m[1])
            for i in range(m_page):
                params.path = "{0}/{1}_{2}.png".format(m_path, name_png, i)
                pages.append(dict(params))

        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            pages.append(dict(params))
            size = file.size(("image", path))
            name = params.get("name", "")
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})

        if len(pages) == 0:
            params.path = "image/"
            pages.append(dict(params))
        return json.dumps(params.insert(pages))

    @bp.route("/cover/update", methods=["POST", "GET"])
    def coverUpdate():
        params = Content_cover(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            size = file.size(("image", path))
            name = params.get("name", "")
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})
        else:
            params.pops("path")
        return json.dumps(params.updateById())

    @bp.route("/cover/del", methods=["POST", "GET"])
    def coverDelete():
        params = Content_cover(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())

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
        if path:
            model = Image if type == "image" else Video
            model_db = model(db, request, pops="id")
            size = file.size((type, path))
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
            name = params.get("name", "")
            data = {"number": 1, "name": name, "path": params.path, "label": 0, "size": size}
            if type == "video":
                data["time"] = model_db.param("time")
            model_db.model.insert(data)
        else:
            params.pops("path")
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
        path = file.up(request, "path", "image")
        params.path = "image/{0}".format(path)
        if path:
            image = Image(db, request, pops="id")
            size = file.size(("image", path))
            name = params.get("name", "")
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})
        return json.dumps(params.insert())

    @bp.route("/caption/update", methods=["POST", "GET"])
    def captionUpdate():
        params = Content_caption(db, request, pops="id", byNames=("theme", "content"))
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            image = Image(db, request, pops="id")
            params.path = "image/{0}".format(path)
            size = file.size(("image", path))
            name = params.get("name", "")
            image.model.insert({"number": 1, "name": name, "path": params.path, "label": 0, "size": size})
        else:
            params.pops("path")
        return json.dumps(params.updateById())

    @bp.route("/caption/del", methods=["POST", "GET"])
    def captionDelete():
        params = Content_caption(db, request, pops="id", byNames=("theme", "content"))
        return json.dumps(params.deleteById())
