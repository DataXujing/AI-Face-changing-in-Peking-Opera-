# -*- coding: utf-8 -*-

'''
Created by: PyQt5 UI code generator 5.15.0

xujing
2020-06-17
ui mainwindow
'''

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
 
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
 
 
class MyLabel(QLabel):
    '''
    重写label，增加单击的信号函数
    '''
    mylabelSig = pyqtSignal(str)
    # mylabelDoubleClickSig = pyqtSignal(str)
 
    def __int__(self):
        super(MyLabel, self).__init__()
 
    def mousePressEvent(self, e):    # 单击
        sigContent = self.objectName()
        self.mylabelSig.emit(sigContent)
 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        button_style = ''' 
         QPushButton
         {text-align : center;
         background-color : white;
         font: bold;
         border-color: gray;
         border-width: 2px;
         border-radius: 10px;
         padding: 6px;
         height : 14px;
         border-style: outset;
         font : 14px;}
         QPushButton:pressed
         {text-align : center;
         background-color : light gray;
         font: bold;
         border-color: gray;
         border-width: 2px;
         border-radius: 10px;
         padding: 6px;
         height : 14px;
         border-style: outset;
         font : 14px;}
        '''

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(967, 787)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/my_pic/pic/脸谱.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(149, 200))
        self.pushButton.setStyleSheet("border-image: url(:/my_pic/pic/左翻页.png);")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        # self.label = QtWidgets.QLabel(self.centralWidget)
        self.label = MyLabel()
        self.label.setMinimumSize(QtCore.QSize(131, 179))
        self.label.setMaximumSize(QtCore.QSize(262, 682))
        self.label.setStyleSheet("border-image: url(:/my_pic/pic/mask/01.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        # self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2 = MyLabel()
        self.label_2.setMaximumSize(QtCore.QSize(298, 682))
        self.label_2.setStyleSheet("border-image: url(:/my_pic/pic/mask/02.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        # self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3 = MyLabel()
        self.label_3.setMaximumSize(QtCore.QSize(298, 682))
        self.label_3.setStyleSheet("border-image: url(:/my_pic/pic/mask/03.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        # self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4 = MyLabel()
        self.label_4.setMaximumSize(QtCore.QSize(298, 682))
        self.label_4.setStyleSheet("border-image: url(:/my_pic/pic/mask/04.png);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(149, 200))
        self.pushButton_2.setStyleSheet("border-image: url(:/my_pic/pic/右翻页.png);")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 3)
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setMaximumSize(QtCore.QSize(1882, 684))
        self.label_6.setStyleSheet("image: url(:/my_pic/pic/face.png);")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 3)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setStyleSheet(button_style)
        self.pushButton_3.setMinimumSize(QtCore.QSize(200, 40))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/my_pic/pic/图片.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 4, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_5.setStyleSheet(button_style)
        self.pushButton_5.setMinimumSize(QtCore.QSize(200, 40))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/my_pic/pic/视频.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 4, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_4.setStyleSheet(button_style)
        self.pushButton_4.setMinimumSize(QtCore.QSize(200, 40))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/my_pic/pic/下载 绿色.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AI京剧换脸"))
        self.pushButton_3.setText(_translate("MainWindow", "加载图像"))
        self.pushButton_5.setText(_translate("MainWindow", "加载视频"))
        self.pushButton_4.setText(_translate("MainWindow", "保存图像"))
import my_pic_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
