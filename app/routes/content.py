def add_route(bp, **f):
    render = f["render_template"]
    @bp.route("/", methods=["POST", "GET"])
    def dev():
        return render("web/content.html", type="", dev={})

    @bp.route("/theme", methods=["POST", "GET"])
    def setLamp():
        return render("web/content_theme.html", type="", dev={})
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
