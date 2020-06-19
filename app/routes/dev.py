import json
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
        lamp = db.models["lamp"]
        exhibit = request.params["exhibit"]
        orderBy = "order by number ASC,id DESC"
        clause = orderBy if exhibit == None else "where exhibit={0} {1}".format(exhibit, orderBy)
        res = lamp.find("*", clause=clause)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/lamp/add", methods=["POST", "GET"])
    def exhibitAdd():
        # ["id", "exhibit", "number", "port", "name", "type", "display", "delay", "style", "offset_x",
        #  "offset_y", "scale", "grouped"]
        lamp = db.models["lamp"]
        exhibit = request.params["exhibit"]
        number = request.params["number"]
        port = request.params["port"]
        name = request.params["name"]
        type = request.params["type"]
        display = request.params["display"]
        delay = request.params["delay"]
        style = request.params["style"]
        offset_x = request.params["offset_x"]
        offset_y = request.params["offset_y"]
        scale = request.params["scale"]
        grouped = request.params["grouped"]

        row = {"exhibit": exhibit, "number": number, "port": port, "name": name, "type": type, "display": display,
               "delay": delay, "style": style, "offset_x": offset_x, "offset_y": offset_y, "scale": scale,
               "grouped": grouped}
        print("row>>>", row)
        optRes = lamp.insert(row)
        print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = orderBy if exhibit == None else "where exhibit={0} {1}".format(exhibit, orderBy)
        res = lamp.find("*", clause=clause)
        print("res:>>", res)
        optRes["data"] = res["data"]

        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/lamp/update", methods=["POST", "GET"])
    def lampUpdate():
        lamp = db.models["lamp"]
        id = request.params["id"]
        exhibit = request.params["exhibit"]
        number = request.params["number"]
        port = request.params["port"]
        name = request.params["name"]
        type = request.params["type"]
        display = request.params["display"]
        delay = request.params["delay"]
        style = request.params["style"]
        offset_x = request.params["offset_x"]
        offset_y = request.params["offset_y"]
        scale = request.params["scale"]
        grouped = request.params["grouped"]

        row = {"exhibit": exhibit, "number": number, "port": port, "name": name, "type": type,
               "display": display, "delay": delay, "style": style, "offset_x": offset_x, "offset_y": offset_y,
               "scale": scale, "grouped": grouped}
        print("row>>>id", row, id)

        optRes = lamp.update(row, clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = orderBy if exhibit == None else "where exhibit={0} {1}".format(exhibit, orderBy)
        res = lamp.find("*", clause=clause)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/lamp/del", methods=["POST", "GET"])
    def lampDelete():
        lamp = db.models["lamp"]
        id = request.params["id"]
        exhibit = request.params["exhibit"]
        print("row>>>id", id)
        optRes = lamp.delete(clause="where id={0}".format(id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        clause = orderBy if exhibit == None else "where exhibit={0} {1}".format(exhibit, orderBy)
        res = lamp.find("*", clause=clause)
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
