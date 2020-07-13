from .pattern import ViewModel

class Lamp(ViewModel):
    def __init__(self, db, request, **con):
        super(Lamp, self).__init__(db, "lamp", request, **con)

class Host(ViewModel):
    def __init__(self, db, request, **con):
        super(Host, self).__init__(db, "host", request, **con)

class Groups(ViewModel):
    def __init__(self, db, request, **con):
        super(Groups, self).__init__(db, "groups", request, **con)

class Infrared(ViewModel):
    def __init__(self, db, request, **con):
        super(Infrared, self).__init__(db, "infrared", request, **con)

class Serial_port(ViewModel):
    def __init__(self, db, request, **con):
        super(Serial_port, self).__init__(db, "serial_port", request, **con)
