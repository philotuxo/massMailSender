# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mailer.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(957, 582)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 681, 561))
        self.tabWidget.setObjectName("tabWidget")
        self.TabProp = QtWidgets.QWidget()
        self.TabProp.setAccessibleName("")
        self.TabProp.setObjectName("TabProp")
        self.textEdit = QtWidgets.QTextEdit(self.TabProp)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 651, 511))
        self.textEdit.setObjectName("textEdit")
        self.tabWidget.addTab(self.TabProp, "")
        self.TabText = QtWidgets.QWidget()
        self.TabText.setObjectName("TabText")
        self.username = QtWidgets.QLineEdit(self.TabText)
        self.username.setGeometry(QtCore.QRect(460, 10, 211, 21))
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(self.TabText)
        self.password.setGeometry(QtCore.QRect(460, 40, 211, 21))
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.buttonTestSMTP = QtWidgets.QPushButton(self.TabText)
        self.buttonTestSMTP.setGeometry(QtCore.QRect(520, 70, 88, 21))
        self.buttonTestSMTP.setObjectName("buttonTestSMTP")
        self.tabWidget.addTab(self.TabText, "")
        self.logView = QtWidgets.QTextBrowser(self.centralwidget)
        self.logView.setGeometry(QtCore.QRect(700, 30, 251, 541))
        self.logView.setObjectName("logView")
        self.labelLog = QtWidgets.QLabel(self.centralwidget)
        self.labelLog.setGeometry(QtCore.QRect(700, 10, 251, 18))
        self.labelLog.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLog.setObjectName("labelLog")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "P2P Social Network Project"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabProp), _translate("MainWindow", "Mail Text"))
        self.username.setText(_translate("MainWindow", "mailing@pierreloti.k12.tr"))
        self.username.setPlaceholderText(_translate("MainWindow", "Enter the username."))
        self.password.setPlaceholderText(_translate("MainWindow", "Enter your password."))
        self.buttonTestSMTP.setText(_translate("MainWindow", "Test SMTP"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabText), _translate("MainWindow", "Properties"))
        self.labelLog.setText(_translate("MainWindow", "System Log:"))

