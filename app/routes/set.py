import json
def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]
    @bp.route("/exhibit", methods=["POST", "GET"])
    def exhibit():
        return render("web/set/exhibit.html", type="")

    @bp.route("/exhibit/list", methods=["POST", "GET"])
    def exhibitList():
        exhibit = db.models["exhibit"]
        res = exhibit.find("*", clause="order by number ASC,id DESC")
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/exhibit/add", methods=["POST", "GET"])
    def exhibitAdd():
        # res = [{"index": 1, "name": "展览001"}, {"index": 2, "name": "展览002"}, {"index": 3, "name": "展览003"},
        #        {"index": 4, "name": "展览004"}, {"index": 5, "name": "展览005"}]
        exhibit = db.models["exhibit"]
        number = request.params["number"]
        name = request.params["name"]
        optRes = exhibit.insert({"number": number, "name": name})
        # print("optRes:>>", optRes)
        res = exhibit.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/exhibit/update", methods=["POST", "GET"])
    def exhibitUpdate():
        exhibit = db.models["exhibit"]
        number = request.params["number"]
        name = request.params["name"]
        id = request.params["id"]
        print("idddd:>>", id)
        optRes = exhibit.update({"number": number, "name": name}, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        res = exhibit.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/exhibit/del", methods=["POST", "GET"])
    def exhibitDelete():
        exhibit = db.models["exhibit"]
        id = request.params["id"]
        print("idddd:>>", id)
        # pragma foreign_keys=on;
        delSql = exhibit.delete(clause="where id={0}".format(id), isSql=True)
        optRes = db.executor(["pragma foreign_keys=on;", delSql])
        # print("optRes:>>", optRes)
        res = exhibit.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/theme", methods=["POST", "GET"])
    def theme():
        return render("web/set/theme.html", type="")

    @bp.route("/theme/list", methods=["POST", "GET"])
    def themeList():
        theme = db.models["theme"]
        res = theme.find("*", clause="order by number ASC,id DESC")
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/theme/add", methods=["POST", "GET"])
    def themeAdd():
        # res = [{"index": 1, "name": "展览001"}, {"index": 2, "name": "展览002"}, {"index": 3, "name": "展览003"},
        #        {"index": 4, "name": "展览004"}, {"index": 5, "name": "展览005"}]
        theme = db.models["theme"]
        number = request.params["number"]
        name = request.params["name"]
        optRes = theme.insert({"number": number, "name": name})
        # print("optRes:>>", optRes)
        res = theme.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/theme/update", methods=["POST", "GET"])
    def themeUpdate():
        theme = db.models["theme"]
        number = request.params["number"]
        name = request.params["name"]
        id = request.params["id"]
        print("idddd:>>", id)
        optRes = theme.update({"number": number, "name": name}, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        res = theme.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/theme/del", methods=["POST", "GET"])
    def themeDelete():
        theme = db.models["theme"]
        id = request.params["id"]
        print("idddd:>>", id)
        # pragma foreign_keys=on;
        delSql = theme.delete(clause="where id={0}".format(id), isSql=True)
        optRes = db.executor(["pragma foreign_keys=on;", delSql])
        # print("optRes:>>", optRes)
        res = theme.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/label", methods=["POST", "GET"])
    def label():
        return render("web/set/label.html", type="")

    @bp.route("/label/list", methods=["POST", "GET"])
    def labelList():
        label = db.models["label"]
        res = label.find("*", clause="order by number ASC,id DESC")
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/label/add", methods=["POST", "GET"])
    def labelAdd():
        # res = [{"index": 1, "name": "展览001"}, {"index": 2, "name": "展览002"}, {"index": 3, "name": "展览003"},
        #        {"index": 4, "name": "展览004"}, {"index": 5, "name": "展览005"}]
        label = db.models["label"]
        number = request.params["number"]
        name = request.params["name"]
        optRes = label.insert({"number": number, "name": name})
        # print("optRes:>>", optRes)
        res = label.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/label/update", methods=["POST", "GET"])
    def labelUpdate():
        label = db.models["label"]
        number = request.params["number"]
        name = request.params["name"]
        id = request.params["id"]
        print("idddd:>>", id)
        optRes = label.update({"number": number, "name": name}, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        res = label.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/label/del", methods=["POST", "GET"])
    def labelDelete():
        label = db.models["label"]
        id = request.params["id"]
        print("idddd:>>", id)
        # pragma foreign_keys=on;
        delSql = label.delete(clause="where id={0}".format(id), isSql=True)
        optRes = db.executor(["pragma foreign_keys=on;", delSql])
        # print("optRes:>>", optRes)
        res = label.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    # @bp.route("/theme", methods=["POST", "GET"])
    # def setLamp():
    #     return render("web/content_theme.html", type="", dev={})
    #
    # @bp.route("/host", methods=["POST", "GET"])
    # def setHost():
    #     return render("web/dev.html", type="", dev={})
    #
    # @bp.route("/infrared", methods=["POST", "GET"])
    # def setInfrared():
    #     return render("web/dev.html", type="", dev={})
    #
    # @bp.route("/gorge", methods=["POST", "GET"])
    # def setGorge():
    #     return render("web/dev.html", type="", dev={})
