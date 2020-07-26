# from libs.IO import File
# from flask import jsonify, url_for, session
from app.models.Account import Account
import time
from app.models.Set import Theme
import json

def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]
    redirect, session, url_for = f["redirect"], f["session"], f["url_for"]
    # account = db.models["account"]
    # accountKeys = account.keys

    @bp.route("/", methods=["POST", "GET"])
    def login():
        return render("web/sign/sign.html")

    @bp.route("/in", methods=["POST", "GET"])
    def _in():
        account = Account(db, request, pops="id")
        # account = db.models["account"]
        clause = "where name='{0}' and password='{1}'".format(account.name, account.password)
        res = account.model.find("*", clause=clause)
        info = "账号或密码错误"
        if len(res["data"]) > 0:
            session.clear()
            res["data"][0].pop("password")
            session["user"] = res["data"][0]
            # return redirect(url_for("dev.lamp"))
            return redirect("/index")
        return render("web/sign/sign.html", info=info)

    @bp.route("/out", methods=["POST", "GET"])
    def out():
        session.clear()
        return redirect(url_for("sign.login"))

    @bp.route("/upper", methods=["POST", "GET"])
    def register():
        return render("web/sign/register.html")

    @bp.route("/up", methods=["POST", "GET"])
    def up():
        account = Account(db, request, pops="id")
        # author = Author(request.params)
        # account = db.models["account"]
        res = account.model.find("*", clause="where name='{0}'".format(account.name))
        if len(res["data"]) > 0:
            info = "账号已经注册"
            return render("web/sign/register.html", info=info)
        else:
            account.rank = 100
            account.number = 1
            account.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # account.insert(author.__dict__)
            theme = Theme(db, request)
            optRes = theme.findBy()["data"]
            account.theme = json.dumps([optRes[0]["id"]] if len(optRes) > 0 else [])
            account.model.insert(dict(account))

            return redirect(url_for("sign.login"))
