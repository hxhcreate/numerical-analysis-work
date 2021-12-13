import shutil
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QPixmap
from PyQT_Form import Ui_Form
from helpwindow import HelpPyqtForm

from interpolation import *
from plot import *
from frozen_dir import app_path
import numpy as np

"""自定义信号类"""


"""class SignalObj(QObject):
    send_msg = pyqtSignal()

    def __init__(self, str1, str2, str3):
        super(SignalObj, self).__init__()
        self.run(str1, str2, str3)

    def run(self, str1, str2, str3):
        if str1 != "" and str2 != "" and str3 != "":
            self.send_msg.emit()

"""




def clear():
    if os.path.exists(os.path.join(app_path(), "tmpresults")):
        shutil.rmtree(os.path.join(app_path(), "tmpresults"))
        os.mkdir(os.path.join(app_path(), "tmpresults"))



class MyPyqtForm(QtWidgets.QWidget, Ui_Form):
    window = []  # 存放子窗体

    def __init__(self):
        super(MyPyqtForm, self).__init__()
        self.setupUi(self)
        self.target = 0  # 默认值
        self.x_list = [] 
        self.y_list = []
        self.method = ""
        self.result = 0  # 默认值
        self.cal_times = 0  # 计算次数

        self.desktop = QtWidgets.QApplication.desktop()
        self.screen = self.desktop.screenGeometry()
        super().move(int((self.screen.width() - self.width()) / 2), int((self.screen.height() - self.height()) / 2))
        # self.Caculate.setDisabled(True)

        """语法检查"""
        reg = QRegExp('^(((-?\d+)(\.\d+)?),)+((-?\d+)(\.\d+))$')
        single_reg = QRegExp('^(-?\d+)(\.\d+)?$')
        self.expression_validation = QRegExpValidator(reg)
        self.single_validation = QRegExpValidator(single_reg)
        self.lineEdit_x.setValidator(self.expression_validation)
        self.lineEdit_y.setValidator(self.expression_validation)
        self.lineEdit_target_x.setValidator(self.single_validation)

        """信号槽连接"""
        # self.lineEdit_x.editingFinished.connect(lambda: self.Caculate.setDisabled(False))
        self.Caculate.clicked.connect(self.calc_fun)
        self.Reset.clicked.connect(self.reset_fun)
        # self.showGraph.clicked.connect(self.select_show)
        self.destroyed.connect(clear)
        self.Method.currentIndexChanged[int].connect(self.change_method_label)
        self.Help.clicked.connect(self.helpwin)
        self.SelectFileButton.clicked.connect(self.selectInputFile)
        self.SelectFileButton_2.clicked.connect(self.selectTarget)

    def helpwin(self):
        help_win = HelpPyqtForm()
        self.window.append(help_win)
        help_win.show()

    def change_method_label(self):
        self.Method.currentIndexChanged.disconnect()
        if self.Method.currentText() == 'Inverse':
            self.label_target.setText("Ytarget")
            self.lineEdit_target_x.setPlaceholderText("请输入反插值Y")
        else:
            self.label_target.setText("Xtarget")
            self.lineEdit_target_x.setPlaceholderText("请输入X值")
        self.Method.currentIndexChanged[int].connect(self.change_method_label)

    def select_show(self):
        file_name = QFileDialog.getOpenFileName(self, "Openfile", "./", )
        image_path = file_name[0]
        if file_name[0] == "":
            QMessageBox.information(self, "提示", "没有选择文件图片!")
            return
        img = QPixmap().scaled(self.graphicsView.width(), self.graphicsView.height())
        img.load(image_path)
        self.graphicsView.scene = QGraphicsScene()
        item = QGraphicsPixmapItem(img)
        self.graphicsView.scene.addItem(item)
        self.graphicsView.setScene(self.graphicsView.scene)
        self.graphicsView.fitInView(QGraphicsPixmapItem(img))

    def auto_show_graph(self):
        last_path = os.path.join(app_path(), "tmpresults/" + str(self.cal_times) + ".png")
        img = QPixmap()
        img.load(last_path)
        self.graphicsView.scene = QGraphicsScene()
        item = QGraphicsPixmapItem(img)
        self.graphicsView.scene.addItem(item)
        self.graphicsView.setScene(self.graphicsView.scene)
        self.graphicsView.fitInView(QGraphicsPixmapItem(img))

    def selectTarget(self):
        file_name = QFileDialog.getOpenFileName(self, "Openfile", "./", "文本文档(*.txt);;*.csv")
        file_path = file_name[0]
        if file_name[0] == "":
            QMessageBox.information(self, "提示", "没有选择数据文件!")
            return
        data = np.loadtxt(file_path, str, delimiter=',')
        target_list = list(data.ravel())
        self.lineEdit_target_x.setText(",".join(target_list))

    def selectInputFile(self):
        file_name = QFileDialog.getOpenFileName(self, "Openfile", "./", "文本文档(*.txt);;*.csv")
        file_path = file_name[0]
        if file_name[0] == "":
            QMessageBox.information(self, "提示", "没有选择数据文件!")
            return
        data = np.loadtxt(file_path, str, delimiter=',')
        x_list = list(data[:, 0].ravel())
        y_list = list(data[:, 1].ravel())
        self.lineEdit_x.setText(','.join(x_list))
        self.lineEdit_y.setText(','.join(y_list))

    def get_input(self):
        self.x_list = list(np.array(eval(self.lineEdit_x.text())))
        self.y_list = list(np.array(eval(self.lineEdit_y.text())))
        self.target = eval(self.lineEdit_target_x.text())

    def calc_fun(self):
        if self.lineEdit_y.text() == "" or self.lineEdit_x.text() == "" or self.lineEdit_target_x == "":
            QMessageBox.warning(self, "提示", "输入有空!")
        else:
            self.cal_times += 1
            self.get_input()
            self.method = self.Method.currentText()
            if self.method == "Newton":
                self.result = newton(self.x_list, self.y_list, self.target)
            elif self.method == "Lagrange":
                self.result = lagrange(self.x_list, self.y_list, self.target)
            elif self.method == 'Inverse':
                self.result = newton(self.y_list, self.x_list, self.target)
            elif self.method == 'Cubic':
                self.result = cubic(self.x_list, self.y_list, self.target)[0]
            self.show_in_browser()
            self.show_in_graph()
            self.auto_show_graph()

    def reset_fun(self):
        self.lineEdit_x.setText("")
        self.lineEdit_y.setText("")
        self.lineEdit_target_x.setText("")
        self.Method.setCurrentIndex(0)

    def show_in_browser(self):
        if self.method != "Inverse":
            self.textBrowser.append(self.method + " " + "求解过程:")
            self.textBrowser.append(
                "Xvalue:" + self.lineEdit_x.text() + ' || ' + "Yvalue:" + self.lineEdit_y.text())  # 函数自带换行
            self.textBrowser.append("Xtarget:" + str(self.target))
            self.textBrowser.append("Yresult:" + str(self.result))
            cursor = self.textBrowser.textCursor()
            self.textBrowser.moveCursor(cursor.End)
        else:
            self.textBrowser.append(self.method + " " + "求解过程:")
            self.textBrowser.append(
                "Yvalue:" + self.lineEdit_y.text() + ' || ' + "Xvalue:" + self.lineEdit_x.text())  # 函数自带换行
            self.textBrowser.append("Ytarget:" + str(self.target))
            self.textBrowser.append("Xresult:" + str(self.result))
            cursor = self.textBrowser.textCursor()
            self.textBrowser.moveCursor(cursor.End)
        QApplication.processEvents()

    def show_in_graph(self):
        if self.method == 'Cubic':
            _, X_range, Y_res = cubic(self.x_list, self.y_list, self.target)
            plot_and_save_forCubic(self.x_list, self.y_list, self.target, self.result, X_range, Y_res, self.cal_times)
        else:
            plot_and_save(self.x_list, self.y_list, self.target, self.result, self.method, self.cal_times)

