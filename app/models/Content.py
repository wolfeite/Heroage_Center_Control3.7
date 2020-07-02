from libs.Viewer import View

class Content(View):
    def __init__(self, db, request, **con):
        self.model = db.models["content"]
        super(Content, self).__init__(self.model.keys, request, **con)

class Content_video(View):
    def __init__(self, db, request, **con):
        self.model = db.models["content_video"]
        super(Content_video, self).__init__(self.model.keys, request, **con)

class Content_image(View):
    def __init__(self, db, request, **con):
        self.model = db.models["content_image"]
        super(Content_image, self).__init__(self.model.keys, request, **con)

class Content_web(View):
    def __init__(self, db, request, **con):
        self.model = db.models["content_web"]
        super(Content_web, self).__init__(self.model.keys, request, **con)

class Content_welcome(View):
    def __init__(self, db, request, **con):
        self.model = db.models["content_welcome"]
        super(Content_welcome, self).__init__(self.model.keys, request, **con)

class Content_cover(View):
    def __init__(self, db, request, **con):
        self.model = db.models["content_cover"]
        super(Content_cover, self).__init__(self.model.keys, request, **con)

class Content_saver(View):
    def __init__(self, db, request, **con):
        self.model = db.models["content_saver"]
        super(Content_saver, self).__init__(self.model.keys, request, **con)

class Content_caption(View):
    def __init__(self, db, request, **con):
        self.model = db.models["content_caption"]
        super(Content_caption, self).__init__(self.model.keys, request, **con)
