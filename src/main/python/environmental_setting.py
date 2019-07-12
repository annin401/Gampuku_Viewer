# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'environmental_setting.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_enviromental_setting(object):
    def setupUi(self, enviromental_setting):
        enviromental_setting.setObjectName("enviromental_setting")
        enviromental_setting.resize(350, 200)
        enviromental_setting.setMinimumSize(QtCore.QSize(350, 200))
        enviromental_setting.setMaximumSize(QtCore.QSize(350, 200))
        enviromental_setting.setStyleSheet("font: 13pt \"Hiragino Sans\";\n"
"color: \"#E7E8E8\"")
        self.centralwidget = QtWidgets.QWidget(enviromental_setting)
        self.centralwidget.setStyleSheet("background-color: \"#35383D\"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setStyleSheet("background-color: \"#67696E\"")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(9999)
        self.spinBox.setProperty("value", 2)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setStyleSheet("color: \"#6B7379\";\n"
"")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_3.addWidget(self.horizontalSlider, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setStyleSheet("color: \"#6B7379\";\n"
"")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(1)
        self.line_2.setMidLineWidth(0)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_4.addWidget(self.checkBox, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        enviromental_setting.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(enviromental_setting)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 350, 22))
        self.menubar.setObjectName("menubar")
        enviromental_setting.setMenuBar(self.menubar)

        self.retranslateUi(enviromental_setting)
        QtCore.QMetaObject.connectSlotsByName(enviromental_setting)

    def retranslateUi(self, enviromental_setting):
        _translate = QtCore.QCoreApplication.translate
        enviromental_setting.setWindowTitle(_translate("enviromental_setting", "環境設定"))
        self.label.setText(_translate("enviromental_setting", "更新時間： "))
        self.label_2.setText(_translate("enviromental_setting", "秒"))
        self.label_3.setText(_translate("enviromental_setting", "ウィンドウの透明度"))
        self.checkBox.setText(_translate("enviromental_setting", "画面を一番上のままにする"))


class Environmental_setting(QtWidgets.QMainWindow):

    # シグナルの宣言
    update_interval_changed = QtCore.pyqtSignal(int)
    opacity_changed = QtCore.pyqtSignal(int)
    window_on_top_state_changed = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.ui = Ui_enviromental_setting()
        self.ui.setupUi(self)

        self.connect_signal()

    # qt組み込みのシグナルと自作シグナルをコネクト
    def connect_signal(self):
        self.ui.spinBox.valueChanged.connect(self.update_interval_changed.emit)
        self.ui.horizontalSlider.valueChanged.connect(self.opacity_changed.emit)
        self.ui.checkBox.stateChanged.connect(self.window_on_top_state_changed.emit)

    def set_update_interval(self, m_time:int)-> None:
        time = m_time // 1000 # 1000 ミリ
        self.ui.spinBox.setProperty("value", time)

    def set_opacity(self, opacity:float)-> None:

        # 透明度を反転した透明度に直して整数化する
        reversed_opacity = (1.0 - opacity) * 100 
        self.ui.horizontalSlider.setSliderPosition(reversed_opacity)

    def set_is_on_top(self, flag:int)-> None:

        if flag == int(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint):
            self.ui.checkBox.setChecked(True)
        else:
            self.ui.checkBox.setChecked(False)