# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\wolfeite\projectPy\heroage\backend\Heroage_Center_Control3.7\gui\UI\UI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UI(object):
    def setupUi(self, UI):
        UI.setObjectName("UI")
        UI.resize(364, 115)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/66964/.designer/backup/Data/Assets/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UI.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(UI)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(60, 40, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Alef")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        UI.setCentralWidget(self.centralWidget)

        self.retranslateUi(UI)
        QtCore.QMetaObject.connectSlotsByName(UI)

    def retranslateUi(self, UI):
        _translate = QtCore.QCoreApplication.translate
        UI.setWindowTitle(_translate("UI", "中控后台系统V4.1"))
        self.label.setText(_translate("UI", "服务启动成功！"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UI = QtWidgets.QMainWindow()
    ui = Ui_UI()
    ui.setupUi(UI)
    UI.show()
    sys.exit(app.exec_())
