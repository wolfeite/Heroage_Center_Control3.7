# Author: 骆琦（wolfeite）
# Corp: 朗迹
# StartTime:2020.6.18
# Version:1.0
from libs.Viewer import View

class ViewModel(View):
    def __init__(self, db, name, request, **con):
        self.model = db.models[name]
        self.byNames = con.get("byNames")
        super(ViewModel, self).__init__(self.model.keys, request, **con)

    def insert(self, row=None, orderBy=None):
        row = row if row else dict(self)
        optRes = self.model.insert(row)
        print("optRes:>>", optRes)
        res = self.findBy(self.byNames, orderBy=orderBy)
        optRes["data"] = res["data"]
        return optRes if not optRes["success"] else res

    def updateById(self, row=None, orderBy=None):
        row = row if row else dict(self)
        optRes = self.model.update(row, clause="where id={0}".format(self.id))
        res = self.findBy(self.byNames, orderBy=orderBy)
        optRes["data"] = res["data"]
        return optRes if not optRes["success"] else res

    def deleteById(self, foreign_keys=False, orderBy=None):
        optRes = self.model.delete(clause="where id={0}".format(self.id), isSql=foreign_keys)
        if foreign_keys:
            optRes = self.model.db.executor(["pragma foreign_keys=on;", optRes])
        # optRes = self.model.delete(clause="where id={0}".format(self.id))
        res = self.findBy(self.byNames, orderBy=orderBy)
        optRes["data"] = res["data"]
        return optRes if not optRes["success"] else res

    def findBy(self, byNames=None, fields="*", orderBy=None):
        orderBy = orderBy if orderBy else "order by number ASC,id DESC"
        if byNames and isinstance(byNames, (str, tuple, list)):
            byNames = [byNames] if isinstance(byNames, str) else byNames
            clauseWhere = []
            for name in byNames:
                clauseWhere.append("{0}={1}".format(name, self.get(name)))
            clause = " and ".join(clauseWhere)
            orderBy = "where {0} {1}".format(clause, orderBy)
        res = self.model.find(fields, clause=orderBy)
        print("findBy{0}>>查询条件：{1}，结果：{2}".format(byNames, orderBy, res))
        return res
