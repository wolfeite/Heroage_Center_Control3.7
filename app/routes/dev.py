import json
from app.models.Dev import Lamp, Groups, Infrared, Serial_port

def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]

    @bp.route("/", methods=["POST", "GET"])
    def dev():
        return render("web/dev.html", type="", dev={})

    @bp.route("/lamp", methods=["POST", "GET"])
    def lamp():
        return render("web/dev/lamp.html", type="", dev={})

    @bp.route("/lamp/list", methods=["POST", "GET"])
    def lampList():
        params = Lamp(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/lamp/add", methods=["POST", "GET"])
    def lampAdd():
        params = Lamp(db, request, pops="id")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/lamp/update", methods=["POST", "GET"])
    def lampUpdate():
        params = Lamp(db, request, pops="id")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/lamp/del", methods=["POST", "GET"])
    def lampDelete():
        params = Lamp(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/groups", methods=["POST", "GET"])
    def groups():
        return render("web/dev/groups.html")

    @bp.route("/groups/list", methods=["POST", "GET"])
    def groupsList():
        params = Groups(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/groups/add", methods=["POST", "GET"])
    def groupsAdd():
        params = Groups(db, request, pops="id")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/groups/update", methods=["POST", "GET"])
    def groupsUpdate():
        params = Groups(db, request, pops="id")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/groups/del", methods=["POST", "GET"])
    def groupsDelete():
        params = Groups(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/infrared", methods=["POST", "GET"])
    def infrared():
        return render("web/dev/infrared.html")

    @bp.route("/infrared/list", methods=["POST", "GET"])
    def infraredList():
        params = Infrared(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/infrared/add", methods=["POST", "GET"])
    def infraredAdd():
        params = Infrared(db, request, pops="id")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/infrared/update", methods=["POST", "GET"])
    def infraredUpdate():
        params = Infrared(db, request, pops="id")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/infrared/del", methods=["POST", "GET"])
    def infraredDelete():
        params = Infrared(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/serial_port", methods=["POST", "GET"])
    def serial_port():
        return render("web/dev/serial_port.html")

    @bp.route("/serial_port/list", methods=["POST", "GET"])
    def serial_portList():
        params = Serial_port(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/serial_port/add", methods=["POST", "GET"])
    def serial_portAdd():
        params = Serial_port(db, request, pops="id")
        optRes = params.model.insert(dict(params))
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/serial_port/update", methods=["POST", "GET"])
    def serial_portUpdate():
        params = Serial_port(db, request, pops="id")
        optRes = params.model.update(dict(params), clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/serial_port/del", methods=["POST", "GET"])
    def serial_portDelete():
        params = Serial_port(db, request, pops="id")
        optRes = params.model.delete(clause="where id={0}".format(params.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = "where exhibit={0} {1}".format(params.exhibit, orderBy)
        res = params.model.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)
