from .pattern import ViewModel
class Exhibit(ViewModel):
    def __init__(self, db, request, **con):
        super(Exhibit, self).__init__(db, "exhibit", request, **con)

class Theme(ViewModel):
    def __init__(self, db, request, **con):
        super(Theme, self).__init__(db, "theme", request, **con)

class Label(ViewModel):
    def __init__(self, db, request, **con):
        super(Label, self).__init__(db, "label", request, **con)
