from libs.http import createFlaskApp
from app import config_app
import sys
from PyQt5.QtWidgets import QApplication
from gui import Gui
from libs.db import SqliteDb

if __name__ == "__main__":
    gui = Gui()
    QApp = QApplication(sys.argv)
    gui.init()
    db = SqliteDb("data/db/ccs.db")
    # httpApp = create_http_app(gui)
    httpApp = createFlaskApp({"host": "0.0.0.0", "debug": False, "port": 3500}, template_folder="data/view",
                             static_folder="data/statics")
    httpApp.attr = ("gui", gui)
    httpApp.attr = ("db", db)
    config_app(httpApp)
    # import libs.io
    sys.exit(QApp.exec_())
