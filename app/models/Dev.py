from libs.Viewer import View

class Lamp(View):
    def __init__(self, db, request, **con):
        self.model = db.models["lamp"]
        super(Lamp, self).__init__(self.model.keys, request, **con)

class Groups(View):
    def __init__(self, db, request, **con):
        self.model = db.models["groups"]
        super(Groups, self).__init__(self.model.keys, request, **con)

class Infrared(View):
    def __init__(self, db, request, **con):
        self.model = db.models["infrared"]
        super(Infrared, self).__init__(self.model.keys, request, **con)

class Serial_port(View):
    def __init__(self, db, request, **con):
        self.model = db.models["serial_port"]
        super(Serial_port, self).__init__(self.model.keys, request, **con)