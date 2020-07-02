import hashlib
from libs.Viewer import View

class Author(View):
    rule = "wolfeite"
    def __init__(self, db, request, **con):
        self.model = db.models["account"]
        super(Author, self).__init__(self.model.keys, request, **con)
        self._md5()

    def _md5(self):
        self.password = self.md5(self.password)

    @classmethod
    def md5(cls, pwd):
        if pwd:
            _md5 = pwd + cls.rule
            md5 = hashlib.md5()
            md5.update(_md5.encode(encoding='utf-8'))
            _md5 = md5.hexdigest()
            return _md5
        else:
            return pwd
