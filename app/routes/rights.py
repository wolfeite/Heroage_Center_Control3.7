from app.models.Account import Account
from app.models.Set import Theme
from libs.Viewer import Request
import json

def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]
    redirect, session, url_for = f["redirect"], f["session"], f["url_for"]

    @bp.route("/", methods=["POST", "GET"])
    def rights():
        return render("web/rights.html")

    @bp.route("/theme", methods=["POST", "GET"])
    def rightsTheme():
        params = Account(db, request, pops="id")
        print("params.theme", params.theme)
        theme = json.dumps(params.theme.split(","))
        optRes = params.model.update({"theme": theme}, clause="where id={0}".format(params.id))
        optRes["data"] = theme
        return json.dumps(optRes)

    @bp.route("/list", methods=["POST", "GET"])
    def rightsList():
        account = Account(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        # clause = "where name='{0}' and password='{1}'".format(author.name, author.password)
        res = account.model.find("id,number,nickname,rank,theme", clause=orderBy)
        params = Theme(db, request, pops="id")
        theme = params.model.find("id,name")
        res["theme"] = theme["data"]
        # return json.dumps(res, default=lambda o: o.__dict__)
        print("res:>>", res)
        return json.dumps(res)

    @bp.route("/update", methods=["POST", "GET"])
    def rightsUpdate():
        account = Account(db, request, pops="id")
        user = session.get("user")
        checkStr = "where id={0} and rank<={1}".format(account.id, user["rank"])
        checkRank = account.model.find("rank", clause=checkStr)
        optRes = {"success": False, "msg": "权限不足,拒绝操作", "data": []}
        if (len(checkRank["data"]) > 0 and user["rank"] >= int(account.rank)):
            row = {"number": account.number, "nickname": account.nickname, "rank": account.rank}
            optRes = account.model.update(row, clause="where id={0}".format(account.id))

        orderBy = "order by number ASC,id DESC"
        res = account.model.find("id,number,nickname,rank,theme", clause=orderBy)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/del", methods=["POST", "GET"])
    def rightsDelete():
        account = Account(db, request, pops="id")
        user = session.get("user")
        checkRank = account.model.find("rank", clause="where id={0} and rank<={1}".format(account.id, user["rank"]))
        optRes = {"success": False, "msg": "权限不足,拒绝操作!", "data": []}
        if (len(checkRank["data"]) > 0):
            optRes = account.model.delete(clause="where id={0}".format(account.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        res = account.model.find("id,number,nickname,rank,theme", clause=orderBy)
        optRes["data"] = res["data"]
        params = Theme(db, request, pops="id")
        theme = params.model.find("id,name")
        res["theme"] = theme["data"]
        optRes["theme"] = theme["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/pwd", methods=["POST", "GET"])
    def pwd():
        newpwd = Request(request).value("newpwd")
        account = Account(db, request, pops="id")
        user = account.findBy()["data"]
        res = {"success": False, "msg": "密码错误"}
        if len(user) > 0 and account.password == user[0]["password"]:
            row = {"password": account.md5(newpwd)}
            # clause = "where name='{0}' and password='{1}'".format(author.name, author.password)
            optRes = account.model.update(row, clause="where id={0}".format(account.id))
            res["success"] = optRes["success"]
            res["msg"] = optRes["msg"]

        return json.dumps(res)
