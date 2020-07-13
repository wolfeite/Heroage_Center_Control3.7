from .pattern import ViewModel

class Content(ViewModel):
    def __init__(self, db, request, **con):
        super(Content, self).__init__(db, "content", request, **con)

class Content_video(ViewModel):
    def __init__(self, db, request, **con):
        super(Content_video, self).__init__(db, "content_video", request, **con)

class Content_image(ViewModel):
    def __init__(self, db, request, **con):
        super(Content_image, self).__init__(db, "content_image", request, **con)

class Content_web(ViewModel):
    def __init__(self, db, request, **con):
        super(Content_web, self).__init__(db, "content_web", request, **con)

class Content_welcome(ViewModel):
    def __init__(self, db, request, **con):
        super(Content_welcome, self).__init__(db, "content_welcome", request, **con)

class Content_cover(ViewModel):
    def __init__(self, db, request, **con):
        super(Content_cover, self).__init__(db, "content_cover", request, **con)

class Content_saver(ViewModel):
    def __init__(self, db, request, **con):
        super(Content_saver, self).__init__(db, "content_saver", request, **con)

class Content_caption(ViewModel):
    def __init__(self, db, request, **con):
        super(Content_caption, self).__init__(db, "content_caption", request, **con)
