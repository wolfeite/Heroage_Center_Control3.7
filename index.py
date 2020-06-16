from libs.http import createFlaskApp
from app import config_app
import sys
from PyQt5.QtWidgets import QApplication
from gui import Gui
import libs.db
import time

if __name__ == "__main__":
    gui = Gui()
    QApp = QApplication(sys.argv)
    gui.init()
    # httpApp = create_http_app(gui)
    httpApp = createFlaskApp({"host": "0.0.0.0", "debug": False, "port": 3500}, template_folder="data/view",
                             static_folder="data/statics")
    httpApp.attr = ("gui", gui)
    config_app(httpApp)
    time.sleep(2)
    # import libs.io
    sys.exit(QApp.exec_())
