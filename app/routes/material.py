import json
from libs.IO import Movie, File, Office
from app.models.Material import Video, Image, Pdf, Ppt
from app.models.Set import Label
import os

def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]

    @bp.route("/list/<path:label_id>", methods=["POST", "GET"])
    def materialList(label_id):
        optRes = {"success": True, "msg": "查询成功", "data": []}
        orderBy = "order by number ASC,id DESC"
        pdf = Pdf(db, request, pops="id")
        clause = "where label={0} {1}".format(label_id, orderBy)
        resPdf = pdf.model.find("*", clause=clause)
        if not resPdf["success"]:
            optRes["data"]["success"] = resPdf["success"]
            optRes["data"]["msg"] = resPdf["msg"]
        optRes["data"].extend(resPdf["data"])

        ppt = Ppt(db, request, pops="id")
        clause = "where label={0} {1}".format(label_id, orderBy)
        resPpt = ppt.model.find("*", clause=clause)
        if not resPpt["success"]:
            optRes["data"]["success"] = resPpt["success"]
            optRes["data"]["msg"] = resPpt["msg"]
        optRes["data"].extend(resPpt["data"])

        return json.dumps(optRes)

    @bp.route("/label", methods=["POST", "GET"])
    def materialLabel():
        params = Label(db, request, pops="id")
        # res = params.model.find("*", clause="order by number ASC,id DESC")
        return json.dumps(params.findBy())

    @bp.route("/video", methods=["POST", "GET"])
    def video():
        return render("web/material/video.html", type="", dev={})

    @bp.route("/video/list", methods=["POST", "GET"])
    def videoList():
        params = Video(db, request, pops="id")
        return json.dumps(params.findBy("label"))

    @bp.route("/video/add", methods=["POST", "GET"])
    def videoAdd():
        params = Video(db, request, pops="id", byNames="label")
        file = Movie(os.path.join("data", "statics"))
        path = file.up(request, "path", "video")
        params.path = "video/{0}".format(path)
        params.size = file.size(("video", path)) if path else 0
        # time = file.time(("video", path))
        params.time = 0;

        return json.dumps(params.insert())

    @bp.route("/video/update", methods=["POST", "GET"])
    def videoUpdate():
        params = Video(db, request, pops="id", byNames="label")
        file = Movie(os.path.join("data", "statics"))
        path = file.up(request, "path", "video")
        if path:
            params.path = path
            params.size = file.size(("video", path))
        else:
            params.pops("path", "size")

        return json.dumps(params.updateById())

    @bp.route("/video/del", methods=["POST", "GET"])
    def videoDelete():
        params = Video(db, request, pops="id", byNames="label")
        return json.dumps(params.deleteById())

    @bp.route("/image", methods=["POST", "GET"])
    def image():
        return render("web/material/image.html", type="", dev={})

    @bp.route("/image/list", methods=["POST", "GET"])
    def imageList():
        params = Image(db, request, pops="id")
        return json.dumps(params.findBy("label"))

    @bp.route("/image/add", methods=["POST", "GET"])
    def imageAdd():
        print("添加图片》》》》》》")
        params = Image(db, request, pops="id", byNames="label")
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        params.path = "image/{0}".format(path)
        params.size = file.size(("image", path)) if path else 0
        return json.dumps(params.insert())

    @bp.route("/image/update", methods=["POST", "GET"])
    def imageUpdate():
        params = Image(db, request, pops="id", byNames="label")
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "image")
        if path:
            params.path = "image/{0}".format(path)
            params.size = file.size(("video", path))
        else:
            params.pops("path", "size")
        return json.dumps(params.updateById())

    @bp.route("/image/del", methods=["POST", "GET"])
    def imageDelete():
        params = Image(db, request, pops="id", byNames="label")
        return json.dumps(params.deleteById())

    @bp.route("/pdf", methods=["POST", "GET"])
    def pdf():
        return render("web/material/pdf.html", type="", dev={})

    @bp.route("/pdf/list", methods=["POST", "GET"])
    def pdfList():
        params = Pdf(db, request, pops="id")
        return json.dumps(params.findBy("label"))

    @bp.route("/pdf/add", methods=["POST", "GET"])
    def pdfAdd():
        params = Pdf(db, request, pops="id", byNames="label")
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "pdf")
        dirName = ""
        if path:
            dirName = path.split(".")[0]
            pages = file.pdf2img(path, "pdf", dirName)
            file.remove("pdf", path)
        params.path = "pdf/{0}".format(dirName)
        params.page = len(pages)
        return json.dumps(params.insert())

    @bp.route("/pdf/update", methods=["POST", "GET"])
    def pdfUpdate():
        params = Pdf(db, request, pops="id", byNames="label")
        file = File(os.path.join("data", "statics"))
        path = file.up(request, "path", "pdf")
        if path:
            dirName = path.split(".")[0]
            pages = file.pdf2img(path, "pdf", dirName)
            file.remove("pdf", path)
            params.path = "pdf/{0}".format(dirName)
            params.page = len(pages)
        else:
            params.pops("path", "page")

        return json.dumps(params.updateById())

    @bp.route("/pdf/del", methods=["POST", "GET"])
    def pdfDelete():
        params = Pdf(db, request, pops="id", byNames="label")
        return json.dumps(params.deleteById())

    @bp.route("/ppt", methods=["POST", "GET"])
    def ppt():
        return render("web/material/ppt.html", type="", dev={})

    @bp.route("/ppt/list", methods=["POST", "GET"])
    def pptList():
        params = Ppt(db, request, pops="id")
        return json.dumps(params.findBy("label"))

    @bp.route("/ppt/add", methods=["POST", "GET"])
    def pptAdd():
        params = Ppt(db, request, pops="id", byNames="label")
        file = Office(os.path.join("data", "statics"))
        path = file.up(request, "path", "ppt")
        dirName = ""
        if path:
            dirName = path.split(".")[0]
            pdf = file.ppt2pdf(path, "ppt")
            pages = file.pdf2img(pdf, "ppt", dirName)
            # file.ppt2img(path, "ppt", dirName)
            file.remove("ppt", path)
            file.remove("ppt", pdf)
        params.path = "ppt/{0}".format(dirName)
        params.page = len(pages)

        return json.dumps(params.insert())

    @bp.route("/ppt/update", methods=["POST", "GET"])
    def pptUpdate():
        params = Ppt(db, request, pops="id", byNames="label")
        file = Office(os.path.join("data", "statics"))
        path = file.up(request, "path", "ppt")
        if path:
            dirName = path.split(".")[0]
            pdf = file.ppt2pdf(path, "ppt")
            pages = file.pdf2img(pdf, "ppt", dirName)
            # file.ppt2img(path, "ppt", dirName)
            file.remove("ppt", path)
            file.remove("ppt", pdf)
            params.path = "ppt/{0}".format(dirName)
            params.page = len(pages)
        else:
            params.pops("path", "page")

        return json.dumps(params.updateById())

    @bp.route("/ppt/del", methods=["POST", "GET"])
    def pptDelete():
        params = Ppt(db, request, pops="id", byNames="label")
        return json.dumps(params.deleteById())
