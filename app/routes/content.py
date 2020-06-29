import json
from libs.IO import Movie
import time
def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]
    @bp.route("/", methods=["POST", "GET"])
    def content():
        return render("web/content/index.html")

    @bp.route("/detail", methods=["POST", "GET"])
    def detail():
        name = request.params["name"]
        id = request.params["id"]
        return render("web/content/detail.html", detail="屏幕{0}详情".format(name), content_id=id)

    @bp.route("/list", methods=["POST", "GET"])
    def contentList():
        content = db.models["content"]
        exhibit = request.params["exhibit"]
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(exhibit, orderBy)
        res = content.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/add", methods=["POST", "GET"])
    def contentAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]
        content = db.models["content"]
        exhibit = request.params["exhibit"]
        number = request.params["number"]
        tag = request.params["tag"]
        name = request.params["name"]
        ip = request.params["ip"]
        width = request.params["width"]
        height = request.params["height"]
        play = request.params["play"]
        volume = request.params["volume"]
        loop = request.params["loop"]
        cover_play = request.params["cover_play"]
        display = request.params["display"]
        style = request.params["style"]
        offset_x = request.params["offset_x"]
        offset_y = request.params["offset_y"]
        scale = request.params["scale"]

        row = {"exhibit": exhibit, "number": number, "tag": tag, "name": name, "ip": ip, "width": width,
               "height": height, "play": play, "volume": volume, "loop": loop, "cover_play": cover_play,
               "display": display, "style": style, "offset_x": offset_x, "offset_y": offset_y, "scale": scale,
               "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        print("row>>>", row)
        optRes = content.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(exhibit, orderBy)
        res = content.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/update", methods=["POST", "GET"])
    def contentUpdate():
        content = db.models["content"]
        id = request.params["id"]
        exhibit = request.params["exhibit"]
        number = request.params["number"]
        tag = request.params["tag"]
        name = request.params["name"]
        ip = request.params["ip"]
        width = request.params["width"]
        height = request.params["height"]
        play = request.params["play"]
        volume = request.params["volume"]
        loop = request.params["loop"]
        cover_play = request.params["cover_play"]
        display = request.params["display"]
        style = request.params["style"]
        offset_x = request.params["offset_x"]
        offset_y = request.params["offset_y"]
        scale = request.params["scale"]

        row = {"exhibit": exhibit, "number": number, "tag": tag, "name": name, "ip": ip, "width": width,
               "height": height, "play": play, "volume": volume, "loop": loop, "cover_play": cover_play,
               "display": display, "style": style, "offset_x": offset_x, "offset_y": offset_y, "scale": scale,
               "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        print("row>>>id", row, id)

        optRes = content.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(exhibit, orderBy)
        res = content.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/del", methods=["POST", "GET"])
    def contentDelete():
        content = db.models["content"]
        id = request.params["id"]
        exhibit = request.params["exhibit"]
        print("row>>>id", id)
        optRes = content.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(exhibit, orderBy)
        res = content.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/vary", methods=["POST", "GET"])
    def contentVary():
        content = db.models["content"]
        id = request.params["id"]
        exhibit = request.params["exhibit"]
        print("row>>>id", id)
        row = {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        optRes = content.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(exhibit, orderBy)
        res = content.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>视频
    @bp.route("/video/list", methods=["POST", "GET"])
    def videoList():
        video = db.models["content_video"]
        content = request.params["content"]
        theme = request.params["theme"]
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = video.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/video/add", methods=["POST", "GET"])
    def videoAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]
        video = db.models["content_video"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        name = request.params["name"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        cover = file.up(request, "cover", "video")
        # path = request.params["path"]
        # cover = request.params["cover"]
        display_modal = request.params["display_modal"]
        offset_x = request.params["offset_x"]
        offset_y = request.params["offset_y"]
        zoom_x = request.params["zoom_x"]
        zoom_y = request.params["zoom_y"]
        width = request.params["width"]
        height = request.params["height"]
        action_start = request.params["action_start"]
        action_end = request.params["action_end"]

        row = {"content": content, "theme": theme, "number": number, "name": name, "path": path, "cover": cover,
               "display_modal": display_modal, "offset_x": offset_x, "offset_y": offset_y, "zoom_x": zoom_x,
               "zoom_y": zoom_y, "width": width, "height": height, "action_start": action_start,
               "action_end": action_end}
        print("row>>>", row)
        optRes = video.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = video.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/video/update", methods=["POST", "GET"])
    def videoUpdate():
        video = db.models["content_video"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        name = request.params["name"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        cover = file.up(request, "cover", "video")
        # path = request.params["path"]
        # cover = request.params["cover"]
        display_modal = request.params["display_modal"]
        offset_x = request.params["offset_x"]
        offset_y = request.params["offset_y"]
        zoom_x = request.params["zoom_x"]
        zoom_y = request.params["zoom_y"]
        width = request.params["width"]
        height = request.params["height"]
        action_start = request.params["action_start"]
        action_end = request.params["action_end"]

        row = {"content": content, "theme": theme, "number": number, "name": name, "path": path, "cover": cover,
               "display_modal": display_modal, "offset_x": offset_x, "offset_y": offset_y, "zoom_x": zoom_x,
               "zoom_y": zoom_y, "width": width, "height": height, "action_start": action_start,
               "action_end": action_end}
        print("row>>>id", row, id)

        optRes = video.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = video.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/video/del", methods=["POST", "GET"])
    def videoDelete():
        video = db.models["content_video"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        print("row>>>id", id)
        optRes = video.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = video.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>图片
    @bp.route("/image/list", methods=["POST", "GET"])
    def imageList():
        image = db.models["content_image"]
        content = request.params["content"]
        theme = request.params["theme"]
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = image.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/image/add", methods=["POST", "GET"])
    def imageAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]
        image = db.models["content_image"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        name = request.params["name"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]
        style = request.params["style"]

        row = {"content": content, "theme": theme, "number": number, "name": name, "path": path, "style": style}
        print("row>>>", row)
        optRes = image.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = image.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/image/update", methods=["POST", "GET"])
    def imageUpdate():
        image = db.models["content_image"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        name = request.params["name"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]
        style = request.params["style"]

        row = {"content": content, "theme": theme, "number": number, "name": name, "path": path, "style": style}
        print("row>>>id", row, id)

        optRes = image.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = image.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/image/del", methods=["POST", "GET"])
    def imageDelete():
        image = db.models["content_image"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        print("row>>>id", id)
        optRes = image.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = image.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>网页
    @bp.route("/web/list", methods=["POST", "GET"])
    def webList():
        web = db.models["content_web"]
        content = request.params["content"]
        theme = request.params["theme"]
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = web.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/web/add", methods=["POST", "GET"])
    def webAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]
        web = db.models["content_web"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        name = request.params["name"]
        url = request.params["url"]

        row = {"content": content, "theme": theme, "number": number, "name": name, "url": url}
        print("row>>>", row)
        optRes = web.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = web.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/web/update", methods=["POST", "GET"])
    def webUpdate():
        web = db.models["content_web"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        name = request.params["name"]
        url = request.params["url"]

        row = {"content": content, "theme": theme, "number": number, "name": name, "url": url}
        print("row>>>id", row, id)

        optRes = web.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = web.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/web/del", methods=["POST", "GET"])
    def webDelete():
        web = db.models["content_web"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        print("row>>>id", id)
        optRes = web.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = web.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>欢迎词
    @bp.route("/welcome/list", methods=["POST", "GET"])
    def welcomeList():
        welcome = db.models["content_welcome"]
        content = request.params["content"]
        theme = request.params["theme"]
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = welcome.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/welcome/add", methods=["POST", "GET"])
    def welcomeAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]

        welcome = db.models["content_welcome"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]
        title = request.params["title"]
        color = request.params["color"]
        font = request.params["font"]
        offset_x = request.params["offset_x"]
        offset_y = request.params["offset_y"]
        align = request.params["align"]
        sub_title = request.params["sub_title"]
        sub_color = request.params["sub_color"]
        sub_font = request.params["sub_font"]
        sub_offset_x = request.params["sub_offset_x"]
        sub_offset_y = request.params["sub_offset_y"]
        sub_align = request.params["sub_align"]

        row = {"content": content, "theme": theme, "number": number, "path": path, "title": title, "color": color,
               "font": font, "offset_x": offset_x, "offset_y": offset_y, "align": align, "sub_title": sub_title,
               "sub_color": sub_color, "sub_font": sub_font, "sub_offset_x": sub_offset_x, "sub_offset_y": sub_offset_y,
               "sub_align": sub_align}
        print("row>>>", row)
        optRes = welcome.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = welcome.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/welcome/update", methods=["POST", "GET"])
    def welcomeUpdate():
        welcome = db.models["content_welcome"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]
        title = request.params["title"]
        color = request.params["color"]
        font = request.params["font"]
        offset_x = request.params["offset_x"]
        offset_y = request.params["offset_y"]
        align = request.params["align"]
        sub_title = request.params["sub_title"]
        sub_color = request.params["sub_color"]
        sub_font = request.params["sub_font"]
        sub_offset_x = request.params["sub_offset_x"]
        sub_offset_y = request.params["sub_offset_y"]
        sub_align = request.params["sub_align"]

        row = {"content": content, "theme": theme, "number": number, "path": path, "title": title, "color": color,
               "font": font, "offset_x": offset_x, "offset_y": offset_y, "align": align, "sub_title": sub_title,
               "sub_color": sub_color, "sub_font": sub_font, "sub_offset_x": sub_offset_x, "sub_offset_y": sub_offset_y,
               "sub_align": sub_align}
        print("row>>>id", row, id)

        optRes = welcome.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = welcome.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/welcome/del", methods=["POST", "GET"])
    def welcomeDelete():
        welcome = db.models["content_welcome"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        print("row>>>id", id)
        optRes = welcome.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = welcome.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>封面
    @bp.route("/cover/list", methods=["POST", "GET"])
    def coverList():
        cover = db.models["content_cover"]
        content = request.params["content"]
        theme = request.params["theme"]
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = cover.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/cover/add", methods=["POST", "GET"])
    def coverAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]
        cover = db.models["content_cover"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        name = request.params["name"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]

        row = {"content": content, "theme": theme, "number": number, "name": name, "path": path}
        print("row>>>", row)
        optRes = cover.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = cover.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/cover/update", methods=["POST", "GET"])
    def coverUpdate():
        cover = db.models["content_cover"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        name = request.params["name"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]

        row = {"content": content, "theme": theme, "number": number, "name": name, "path": path}
        print("row>>>id", row, id)

        optRes = cover.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = cover.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/cover/del", methods=["POST", "GET"])
    def coverDelete():
        cover = db.models["content_cover"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        print("row>>>id", id)
        optRes = cover.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = cover.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>屏保
    @bp.route("/saver/list", methods=["POST", "GET"])
    def saverList():
        saver = db.models["content_saver"]
        content = request.params["content"]
        theme = request.params["theme"]
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = saver.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/saver/add", methods=["POST", "GET"])
    def saverAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]
        saver = db.models["content_saver"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        type = request.params["type"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]

        row = {"content": content, "theme": theme, "number": number, "type": type, "path": path}
        print("row>>>", row)
        optRes = saver.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = saver.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/saver/update", methods=["POST", "GET"])
    def saverUpdate():
        saver = db.models["content_saver"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        type = request.params["type"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]

        row = {"content": content, "theme": theme, "number": number, "type": type, "path": path}
        print("row>>>id", row, id)

        optRes = saver.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = saver.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/saver/del", methods=["POST", "GET"])
    def saverDelete():
        saver = db.models["content_saver"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        print("row>>>id", id)
        optRes = saver.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = saver.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # >>>解说词
    @bp.route("/caption/list", methods=["POST", "GET"])
    def captionList():
        caption = db.models["content_caption"]
        content = request.params["content"]
        theme = request.params["theme"]
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = caption.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/caption/add", methods=["POST", "GET"])
    def captionAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]
        caption = db.models["content_caption"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        text = request.params["text"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]

        row = {"content": content, "theme": theme, "number": number, "text": text, "path": path}
        print("row>>>", row)
        optRes = caption.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = caption.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/caption/update", methods=["POST", "GET"])
    def captionUpdate():
        caption = db.models["content_caption"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        number = request.params["number"]
        text = request.params["text"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        # path = request.params["path"]

        row = {"content": content, "theme": theme, "number": number, "text": text, "path": path}
        print("row>>>id", row, id)

        optRes = caption.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = caption.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/caption/del", methods=["POST", "GET"])
    def captionDelete():
        caption = db.models["content_caption"]
        id = request.params["id"]
        content = request.params["content"]
        theme = request.params["theme"]
        print("row>>>id", id)
        optRes = caption.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where theme={0} and content={1} {2}".format(theme, content, orderBy)
        res = caption.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)
