import json
from app.models.Set import Exhibit, Theme, Label

def add_route(bp, **f):
    render, db, request, session = f["render_template"], f["db"], f["request"], f["session"]

    @bp.route("/exhibit", methods=["POST", "GET"])
    def exhibit():
        return render("web/set/exhibit.html", type="")

    @bp.route("/exhibit/list", methods=["POST", "GET"])
    def exhibitList():
        params = Exhibit(db, request, pops="id")
        res = params.model.find("*", clause="order by number ASC,id DESC")
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/exhibit/add", methods=["POST", "GET"])
    def exhibitAdd():
        params = Exhibit(db, request, pops="id")
        optRes = params.model.insert(dict(params))
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/exhibit/update", methods=["POST", "GET"])
    def exhibitUpdate():
        params = Exhibit(db, request, pops="id")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/exhibit/del", methods=["POST", "GET"])
    def exhibitDelete():
        params = Exhibit(db, request, pops="id")
        # pragma foreign_keys=on;
        delSql = params.model.delete(clause="where id={0}".format(params.id), isSql=True)
        optRes = db.executor(["pragma foreign_keys=on;", delSql])
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/theme", methods=["POST", "GET"])
    def theme():
        return render("web/set/theme.html", type="")

    @bp.route("/theme/list", methods=["POST", "GET"])
    def themeList():
        params = Theme(db, request, pops="id")
        res = params.model.find("*", clause="order by number ASC,id DESC")
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/theme/add", methods=["POST", "GET"])
    def themeAdd():
        params = Theme(db, request, pops="id")
        optRes = params.model.insert(dict(params))
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/theme/update", methods=["POST", "GET"])
    def themeUpdate():
        params = Theme(db, request, pops="id")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/theme/del", methods=["POST", "GET"])
    def themeDelete():
        params = Theme(db, request, pops="id")
        # pragma foreign_keys=on;
        delSql = params.model.delete(clause="where id={0}".format(params.id), isSql=True)
        optRes = db.executor(["pragma foreign_keys=on;", delSql])
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/label", methods=["POST", "GET"])
    def label():
        return render("web/set/label.html", type="")

    @bp.route("/label/list", methods=["POST", "GET"])
    def labelList():
        params = Label(db, request, pops="id")
        # label = db.models["label"]
        res = params.model.find("*", clause="order by number ASC,id DESC")
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/label/add", methods=["POST", "GET"])
    def labelAdd():
        params = Label(db, request, pops="id")
        optRes = params.model.insert(dict(params))
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/label/update", methods=["POST", "GET"])
    def labelUpdate():
        params = Label(db, request, pops="id")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/label/del", methods=["POST", "GET"])
    def labelDelete():
        params = Label(db, request, pops="id")
        delSql = params.model.delete(clause="where id={0}".format(params.id), isSql=True)
        # pragma foreign_keys=on;
        optRes = db.executor(["pragma foreign_keys=on;", delSql])
        # print("optRes:>>", optRes)
        res = params.model.find("*", clause="order by number ASC,id DESC")
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)
