# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\user_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 954)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.party = QtWidgets.QWidget(self.centralwidget)
        self.party.setObjectName("party")
        self.gridLayoutWidget = QtWidgets.QWidget(self.party)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 661, 511))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.character2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.character2.setScaledContents(True)
        self.character2.setObjectName("character2")
        self.gridLayout_3.addWidget(self.character2, 0, 1, 1, 1)
        self.character3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.character3.setScaledContents(True)
        self.character3.setObjectName("character3")
        self.gridLayout_3.addWidget(self.character3, 0, 2, 1, 1)
        self.character1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.character1.setEnabled(True)
        self.character1.setScaledContents(True)
        self.character1.setWordWrap(False)
        self.character1.setObjectName("character1")
        self.gridLayout_3.addWidget(self.character1, 0, 0, 1, 1)
        self.character4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.character4.setScaledContents(True)
        self.character4.setObjectName("character4")
        self.gridLayout_3.addWidget(self.character4, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.party)
        self.updateParty = QtWidgets.QPushButton(self.centralwidget)
        self.updateParty.setObjectName("updateParty")
        self.verticalLayout.addWidget(self.updateParty)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.character2.setText(_translate("MainWindow", "Character 2"))
        self.character3.setText(_translate("MainWindow", "Character 3"))
        self.character1.setText(_translate("MainWindow", "Character 1"))
        self.character4.setText(_translate("MainWindow", "Character 4"))
        self.updateParty.setText(_translate("MainWindow", "Update party"))
