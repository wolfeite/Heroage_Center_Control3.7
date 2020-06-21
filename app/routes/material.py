import json
from libs.IO import Movie
def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]

    @bp.route("/video", methods=["POST", "GET"])
    def video():
        return render("web/material/video.html", type="", dev={})

    @bp.route("/video/list", methods=["POST", "GET"])
    def videoList():
        video = db.models["video"]
        label = request.params["label"]
        label = None if int(label) == 0 else label
        orderBy = "order by number ASC,id DESC"
        clause = "where label is null {0}".format(orderBy) if label == None else "where label={0} {1}".format(label,
                                                                                                              orderBy)
        res = video.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/video/add", methods=["POST", "GET"])
    def videoAdd():
        video = db.models["video"]
        label = request.params["label"]
        label = None if int(label) == 0 else label
        number = request.params["number"]
        name = request.params["name"]
        # size = request.params["size"]
        # time = request.params["time"]
        file = Movie("data")
        path = file.up(request, "path", "video")
        size = file.size(("video", path))
        time = file.time(("video", path))
        row = {"label": label, "number": number, "name": name, "size": size, "time": time, "path": path}
        print("row>>>", row)
        optRes = video.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where label is null {0}".format(orderBy) if label == None else "where label={0} {1}".format(label,
                                                                                                              orderBy)
        res = video.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/video/update", methods=["POST", "GET"])
    def videoUpdate():
        video = db.models["video"]
        id = request.params["id"]
        label = request.params["label"]
        number = request.params["number"]
        name = request.params["name"]
        size = request.params["size"]
        time = request.params["time"]

        row = {"label": label, "number": number, "name": name, "size": size, "time": time}
        print("row>>>id", row, id)

        optRes = video.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = orderBy if label == None or label == 0 else "where label={0} {1}".format(label, orderBy)
        res = video.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/video/del", methods=["POST", "GET"])
    def videoDelete():
        video = db.models["video"]
        id = request.params["id"]
        label = request.params["label"]
        label = None if int(label) == 0 else label
        print("row>>>id", id)
        optRes = video.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where label is null {0}".format(orderBy) if label == None else "where label={0} {1}".format(label,
                                                                                                              orderBy)
        res = video.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/host", methods=["POST", "GET"])
    def setHost():
        return render("web/dev/host.html", type="", dev={})

    @bp.route("/infrared", methods=["POST", "GET"])
    def setInfrared():
        return render("web/dev.html", type="", dev={})

    @bp.route("/gorge", methods=["POST", "GET"])
    def setGorge():
        return render("web/dev.html", type="", dev={})
