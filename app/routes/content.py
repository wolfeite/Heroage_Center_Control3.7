import json
from libs.IO import Movie
import time
from app.models.Content import Content, Content_video, Content_image, Content_web, Content_welcome, Content_cover
from app.models.Content import Content_saver, Content_caption
from libs.Viewer import Request

def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]
    @bp.route("/", methods=["POST", "GET"])
    def content():
        return render("web/content/index.html")

    @bp.route("/detail", methods=["POST", "GET"])
    def detail():
        params = Request(request)
        return render("web/content/detail.html", detail="屏幕{0}详情".format(params.value("name")),
                      content_id=params.value("id"))

    @bp.route("/list", methods=["POST", "GET"])
    def contentList():
        params = Content(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/add", methods=["POST", "GET"])
    def contentAdd():
        params = Content(db, request, pops="id")
        params.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # row = {"exhibit": exhibit, "number": number, "tag": tag, "name": name, "ip": ip, "width": width,
        #        "height": height, "play": play, "volume": volume, "loop": loop, "cover_play": cover_play,
        #        "display": display, "style": style, "offset_x": offset_x, "offset_y": offset_y, "scale": scale,
        #        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/update", methods=["POST", "GET"])
    def contentUpdate():
        params = Content(db, request, pops="id")
        params.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/del", methods=["POST", "GET"])
    def contentDelete():
        params = Content(db, request, pops="id")
        delSql = params.model.delete(clause="where id={0}".format(params.id), isSql=True)
        optRes = db.executor(["pragma foreign_keys=on;", delSql])
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/vary", methods=["POST", "GET"])
    def contentVary():
        params = Content(db, request, pops="id")
        row = {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        optRes = params.model.update(row, clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>视频
    @bp.route("/video/list", methods=["POST", "GET"])
    def videoList():
        params = Content_video(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/video/add", methods=["POST", "GET"])
    def videoAdd():
        params = Content_video(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        params.cover = file.up(request, "cover", "video")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/video/update", methods=["POST", "GET"])
    def videoUpdate():
        params = Content_video(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        params.cover = file.up(request, "cover", "video")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/video/del", methods=["POST", "GET"])
    def videoDelete():
        params = Content_video(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>图片
    @bp.route("/image/list", methods=["POST", "GET"])
    def imageList():
        params = Content_image(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/image/add", methods=["POST", "GET"])
    def imageAdd():
        params = Content_image(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/image/update", methods=["POST", "GET"])
    def imageUpdate():
        params = Content_image(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.update((dict(params)), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/image/del", methods=["POST", "GET"])
    def imageDelete():
        params = Content_image(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>网页
    @bp.route("/web/list", methods=["POST", "GET"])
    def webList():
        params = Content_web(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/web/add", methods=["POST", "GET"])
    def webAdd():
        params = Content_web(db, request, pops="id")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/web/update", methods=["POST", "GET"])
    def webUpdate():
        params = Content_web(db, request, pops="id")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/web/del", methods=["POST", "GET"])
    def webDelete():
        params = Content_web(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>欢迎词
    @bp.route("/welcome/list", methods=["POST", "GET"])
    def welcomeList():
        params = Content_welcome(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/welcome/add", methods=["POST", "GET"])
    def welcomeAdd():
        params = Content_welcome(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/welcome/update", methods=["POST", "GET"])
    def welcomeUpdate():
        params = Content_welcome(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")

        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/welcome/del", methods=["POST", "GET"])
    def welcomeDelete():
        params = Content_welcome(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>封面
    @bp.route("/cover/list", methods=["POST", "GET"])
    def coverList():
        params = Content_cover(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/cover/add", methods=["POST", "GET"])
    def coverAdd():
        params = Content_cover(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/cover/update", methods=["POST", "GET"])
    def coverUpdate():
        params = Content_cover(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/cover/del", methods=["POST", "GET"])
    def coverDelete():
        params = Content_cover(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>屏保
    @bp.route("/saver/list", methods=["POST", "GET"])
    def saverList():
        params = Content_saver(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/saver/add", methods=["POST", "GET"])
    def saverAdd():
        params = Content_saver(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/saver/update", methods=["POST", "GET"])
    def saverUpdate():
        params = Content_saver(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/saver/del", methods=["POST", "GET"])
    def saverDelete():
        params = Content_saver(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>解说词
    @bp.route("/caption/list", methods=["POST", "GET"])
    def captionList():
        params = Content_caption(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/caption/add", methods=["POST", "GET"])
    def captionAdd():
        params = Content_caption(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/caption/update", methods=["POST", "GET"])
    def captionUpdate():
        params = Content_caption(db, request, pops="id")
        file = Movie("data")
        params.path = file.up(request, "path", "video")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/caption/del", methods=["POST", "GET"])
    def captionDelete():
        params = Content_caption(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(params.theme, params.content, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)
