# from libs.IO import File
# from flask import jsonify, url_for, session
from app.models.Author import Author
import time
import json

def add_route(bp, **f):
    render, db, request = f["render_template"], f["db"], f["request"]
    redirect, session, url_for = f["redirect"], f["session"], f["url_for"]

    @bp.route("/", methods=["POST", "GET"])
    def rights():
        return render("web/rights.html")

    @bp.route("/list", methods=["POST", "GET"])
    def rightsList():
        author = Author(db, request, pops="id")
        orderBy = "order by number ASC,id DESC"
        # clause = "where name='{0}' and password='{1}'".format(author.name, author.password)
        res = author.model.find("id,number,nickname,rank", clause=orderBy)
        print("res:>>", res)
        # return json.dumps(res, default=lambda o: o.__dict__)
        return json.dumps(res)

    @bp.route("/update", methods=["POST", "GET"])
    def rightsUpdate():
        author = Author(db, request, pops="id")
        user = session.get("user")
        checkStr = "where id={0} and rank<={1}".format(author.id, user["rank"])
        checkRank = author.model.find("rank", clause=checkStr)
        optRes = {"success": False, "msg": "权限不足,拒绝操作", "data": []}
        if (len(checkRank["data"]) > 0 and user["rank"] >= int(author.rank)):
            row = {"number": author.number, "nickname": author.nickname, "rank": author.rank}
            optRes = author.model.update(row, clause="where id={0}".format(author.id))

        orderBy = "order by number ASC,id DESC"
        res = author.model.find("id,number,nickname,rank", clause=orderBy)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)

    @bp.route("/del", methods=["POST", "GET"])
    def rightsDelete():
        author = Author(db, request, pops="id")
        user = session.get("user")
        checkRank = author.model.find("rank", clause="where id={0} and rank<={1}".format(author.id, user["rank"]))
        optRes = {"success": False, "msg": "权限不足,拒绝操作!", "data": []}
        if (len(checkRank["data"]) > 0):
            optRes = author.model.delete(clause="where id={0}".format(author.id))
        # print("optRes:>>", optRes)
        orderBy = "order by number ASC,id DESC"
        res = author.model.find("id,number,nickname,rank", clause=orderBy)
        optRes["data"] = res["data"]
        return json.dumps(optRes if not optRes["success"] else res)
