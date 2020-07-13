import json
from app.models.Set import Exhibit, Theme, Label
from app.models.Account import Account

def add_route(bp, **f):
    render, db, request, session = f["render_template"], f["db"], f["request"], f["session"]

    @bp.route("/exhibit", methods=["POST", "GET"])
    def exhibit():
        return render("web/set/exhibit.html", type="")

    @bp.route("/exhibit/list", methods=["POST", "GET"])
    def exhibitList():
        params = Exhibit(db, request, pops="id")
        res = params.model.find("*", clause="order by number ASC,id DESC")
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/exhibit/add", methods=["POST", "GET"])
    def exhibitAdd():
        params = Exhibit(db, request, pops="id")
        return json.dumps(params.insert())

    @bp.route("/exhibit/update", methods=["POST", "GET"])
    def exhibitUpdate():
        params = Exhibit(db, request, pops="id")
        return json.dumps(params.updateById())

    @bp.route("/exhibit/del", methods=["POST", "GET"])
    def exhibitDelete():
        params = Exhibit(db, request, pops="id")
        return json.dumps(params.deleteById(foreign_keys=True))

    @bp.route("/theme", methods=["POST", "GET"])
    def theme():
        return render("web/set/theme.html", type="")

    @bp.route("/theme/list", methods=["POST", "GET"])
    def themeList():
        params = Theme(db, request, pops="id")
        res = params.model.find("*", clause="order by number ASC,id DESC")
        return json.dumps(res)

    @bp.route("/theme/add", methods=["POST", "GET"])
    def themeAdd():
        params = Theme(db, request, pops="id")
        return json.dumps(params.insert())

    @bp.route("/theme/update", methods=["POST", "GET"])
    def themeUpdate():
        params = Theme(db, request, pops="id")
        return json.dumps(params.updateById())

    @bp.route("/theme/del", methods=["POST", "GET"])
    def themeDelete():
        params = Theme(db, request, pops="id")
        res = params.deleteById(foreign_keys=True)
        if res["success"]:
            # 删除与其相关联的theme内容
            account = Account(db, request, pops="id")
            others = account.model.find("id,name,theme", clause="where theme like '%{0}%'".format(params.id))
            for other in others["data"]:
                print(">>>>>相关数据：", other)
                link = json.loads(other["theme"])
                print(">>>>>相关link：", link)
                link.remove(params.id)
                link = json.dumps(link)
                print(">>>>>修改后link：", link)
                account.model.update({"theme": link}, clause="where id={0}".format(other["id"]))
        return json.dumps(res)

    @bp.route("/label", methods=["POST", "GET"])
    def label():
        return render("web/set/label.html", type="")

    @bp.route("/label/list", methods=["POST", "GET"])
    def labelList():
        params = Label(db, request, pops="id")
        res = params.model.find("*", clause="order by number ASC,id DESC")
        return json.dumps(res)

    @bp.route("/label/add", methods=["POST", "GET"])
    def labelAdd():
        params = Label(db, request, pops="id")
        return json.dumps(params.insert())

    @bp.route("/label/update", methods=["POST", "GET"])
    def labelUpdate():
        params = Label(db, request, pops="id")
        return json.dumps(params.updateById())

    @bp.route("/label/del", methods=["POST", "GET"])
    def labelDelete():
        params = Label(db, request, pops="id")
        return json.dumps(params.deleteById(foreign_keys=True))
