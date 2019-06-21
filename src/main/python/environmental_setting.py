# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'environmental_setting.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_enviromental_setting(QtCore.QObject):
    # シグナルの宣言
    update_interval_changed = QtCore.pyqtSignal(int)
    window_on_top_state_changed = QtCore.pyqtSignal(int)

    # qt組み込みのシグナルと自作シグナルをコネクト
    def connect_signal(self):
        self.spinBox.valueChanged.connect(self.update_interval_changed.emit)
        self.checkBox.stateChanged.connect(self.window_on_top_state_changed.emit)

    def setupUi(self, enviromental_setting):
        enviromental_setting.setObjectName("enviromental_setting")
        enviromental_setting.resize(250, 150)
        enviromental_setting.setMinimumSize(QtCore.QSize(250, 150))
        enviromental_setting.setMaximumSize(QtCore.QSize(250, 150))
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
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_4.addWidget(self.checkBox, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        enviromental_setting.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(enviromental_setting)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 250, 22))
        self.menubar.setObjectName("menubar")
        enviromental_setting.setMenuBar(self.menubar)

        self.retranslateUi(enviromental_setting)
        QtCore.QMetaObject.connectSlotsByName(enviromental_setting)

    def retranslateUi(self, enviromental_setting):
        _translate = QtCore.QCoreApplication.translate
        enviromental_setting.setWindowTitle(_translate("enviromental_setting", "環境設定"))
        self.label.setText(_translate("enviromental_setting", "更新時間： "))
        self.label_2.setText(_translate("enviromental_setting", "秒"))
        self.checkBox.setText(_translate("enviromental_setting", "画面を一番上のままにする"))

