import json
from app.models.Dev import Lamp, Host, Groups, Infrared, Serial_port

def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]

    @bp.route("/", methods=["POST", "GET"])
    def dev():
        return render("web/dev.html", type="", dev={})

    @bp.route("/lamp", methods=["POST", "GET"])
    def lamp():
        return render("web/dev/lamp.html")

    @bp.route("/lamp/list", methods=["POST", "GET"])
    def lampList():
        params = Lamp(db, request, pops="id")
        return json.dumps(params.findBy("exhibit"))

    @bp.route("/lamp/add", methods=["POST", "GET"])
    def lampAdd():
        params = Lamp(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.insert())

    @bp.route("/lamp/update", methods=["POST", "GET"])
    def lampUpdate():
        params = Lamp(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.updateById())

    @bp.route("/lamp/del", methods=["POST", "GET"])
    def lampDelete():
        params = Lamp(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.deleteById())

    @bp.route("/host", methods=["POST", "GET"])
    def host():
        return render("web/dev/host.html")

    @bp.route("/host/list", methods=["POST", "GET"])
    def hostList():
        params = Host(db, request, pops="id")
        return json.dumps(params.findBy("exhibit"))

    @bp.route("/host/add", methods=["POST", "GET"])
    def hostAdd():
        params = Host(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.insert())

    @bp.route("/host/update", methods=["POST", "GET"])
    def hostUpdate():
        params = Host(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.updateById())

    @bp.route("/host/del", methods=["POST", "GET"])
    def hostDelete():
        params = Host(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.deleteById())

    @bp.route("/groups", methods=["POST", "GET"])
    def groups():
        return render("web/dev/groups.html")

    @bp.route("/groups/list", methods=["POST", "GET"])
    def groupsList():
        params = Groups(db, request, pops="id")
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(params.findBy("exhibit"))

    @bp.route("/groups/add", methods=["POST", "GET"])
    def groupsAdd():
        params = Groups(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.insert())

    @bp.route("/groups/update", methods=["POST", "GET"])
    def groupsUpdate():
        params = Groups(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.updateById())

    @bp.route("/groups/del", methods=["POST", "GET"])
    def groupsDelete():
        params = Groups(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.deleteById())

    @bp.route("/infrared", methods=["POST", "GET"])
    def infrared():
        return render("web/dev/infrared.html")

    @bp.route("/infrared/list", methods=["POST", "GET"])
    def infraredList():
        params = Infrared(db, request, pops="id")
        return json.dumps(params.findBy("exhibit"))

    @bp.route("/infrared/add", methods=["POST", "GET"])
    def infraredAdd():
        params = Infrared(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.insert())

    @bp.route("/infrared/update", methods=["POST", "GET"])
    def infraredUpdate():
        params = Infrared(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.updateById())

    @bp.route("/infrared/del", methods=["POST", "GET"])
    def infraredDelete():
        params = Infrared(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.deleteById())

    @bp.route("/serial_port", methods=["POST", "GET"])
    def serial_port():
        return render("web/dev/serial_port.html")

    @bp.route("/serial_port/list", methods=["POST", "GET"])
    def serial_portList():
        params = Serial_port(db, request, pops="id")
        return json.dumps(params.findBy("exhibit"))

    @bp.route("/serial_port/add", methods=["POST", "GET"])
    def serial_portAdd():
        params = Serial_port(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.insert())

    @bp.route("/serial_port/update", methods=["POST", "GET"])
    def serial_portUpdate():
        params = Serial_port(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.updateById())

    @bp.route("/serial_port/del", methods=["POST", "GET"])
    def serial_portDelete():
        params = Serial_port(db, request, pops="id", byNames="exhibit")
        return json.dumps(params.deleteById())
