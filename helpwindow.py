import os
import shutil
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import QRegExp, pyqtSignal, QObject
from PyQt5.QtGui import QRegExpValidator, QImage, QPixmap
from Help_Form import Ui_Help


class HelpPyqtForm(QtWidgets.QMainWindow, Ui_Help):

    def __init__(self):
        super(HelpPyqtForm, self).__init__()
        self.setupUi(self)


        self.actionabout.triggered.connect(self.aboutAuthor)
        self.actionzhixie.triggered.connect(self.gratitude)

    def aboutAuthor(self):
        QMessageBox.information(self, "关于", "author: hxh_create\ncontact me: hxh_create@163.com\n&all rights reserved")
    def gratitude(self):
        QMessageBox.information(self, "致谢", "感谢孙新老师")
    def showGui(self):
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    helpwin = HelpPyqtForm()
    helpwin.show()
    sys.exit(app.exec_())
