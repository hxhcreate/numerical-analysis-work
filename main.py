import sys
from PyQt5 import QtWidgets
from mainwindow import MyPyqtForm



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyqtForm()
    my_pyqt_form.show()
    # help_win = HelpPyqtForm()
    # my_pyqt_form.Help.clicked.connect(help_win.showGui)
    sys.exit(app.exec_())

