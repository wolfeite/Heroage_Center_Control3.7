def add_route(bp, **f):
    render = f["render_template"]
    @bp.route("/", methods=["POST", "GET"])
    def rights():
        return render("templates/tab.html", type="", dev={})

    # @bp.route("/lamp", methods=["POST", "GET"])
    # def setLamp():
    #     return render("web/dev.html", type="", dev={})
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
