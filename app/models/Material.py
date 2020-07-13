from .pattern import ViewModel
class Video(ViewModel):
    def __init__(self, db, request, **con):
        super(Video, self).__init__(db, "video", request, **con)

class Image(ViewModel):
    def __init__(self, db, request, **con):
        super(Image, self).__init__(db, "image", request, **con)

class Pdf(ViewModel):
    def __init__(self, db, request, **con):
        super(Pdf, self).__init__(db, "pdf", request, **con)

class Ppt(ViewModel):
    def __init__(self, db, request, **con):
        super(Ppt, self).__init__(db, "ppt", request, **con)
