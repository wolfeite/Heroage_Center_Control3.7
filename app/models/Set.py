from libs.Viewer import View

class Exhibit(View):
    def __init__(self, db, request, **con):
        self.model = db.models["exhibit"]
        super(Exhibit, self).__init__(self.model.keys, request, **con)

class Theme(View):
    def __init__(self, db, request, **con):
        self.model = db.models["theme"]
        super(Theme, self).__init__(self.model.keys, request, **con)

class Label(View):
    def __init__(self, db, request, **con):
        self.model = db.models["label"]
        super(Label, self).__init__(self.model.keys, request, **con)
