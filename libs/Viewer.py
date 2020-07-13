# Author: 骆琦（wolfeite）
# Corp: 朗迹
# StartTime:2020.6.18
# Version:1.0
class Request():
    def __init__(self, request):
        self.request = request
        if request.method == "GET":
            self.isGet = True
            self.data = self.request.args
        else:
            self.isGet = False
            self.data = self.request.form

    def value(self, key):
        param = self.data.get(key)
        return self.request.args.get(key) if param == None and not self.isGet else param

class View():
    def __init__(self, fields, request, **con):
        self.request = Request(request)
        self.fields = fields if isinstance(fields, list) else list(fields)
        self.init(con)
        for key in fields:
            setattr(self, key, self.request.value(key))

    def param(self, name):
        return self.request.value(name)

    def init(self, con):
        self.config = {"pops": None}
        self.config.update(con)
        pops = self.config["pops"]
        if pops and not isinstance(pops, (list, tuple)):
            self.config["pops"] = (pops,)

    def pops(self, *args):
        for key in args:
            key in self.fields and self.fields.remove(key)

    def keys(self):
        pops = self.config["pops"]
        pops and self.pops(*pops)
        return self.fields

    def get(self, name, defVal=None):
        return getattr(self, name, defVal)

    def __getitem__(self, key):
        '''内置方法, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值'''
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)
