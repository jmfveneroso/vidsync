# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon Aug  3 14:34:15 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 30, 561, 351))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabServer = QtGui.QWidget()
        self.tabServer.setObjectName(_fromUtf8("tabServer"))
        self.tableServer = QtGui.QTableWidget(self.tabServer)
        self.tableServer.setGeometry(QtCore.QRect(20, 20, 511, 192))
        self.tableServer.setObjectName(_fromUtf8("tableServer"))
        self.tableServer.setColumnCount(0)
        self.tableServer.setRowCount(0)
        self.sliderServer = QtGui.QSlider(self.tabServer)
        self.sliderServer.setGeometry(QtCore.QRect(20, 230, 511, 22))
        self.sliderServer.setOrientation(QtCore.Qt.Horizontal)
        self.sliderServer.setObjectName(_fromUtf8("sliderServer"))
        self.btnServer = QtGui.QPushButton(self.tabServer)
        self.btnServer.setGeometry(QtCore.QRect(220, 270, 114, 32))
        self.btnServer.setObjectName(_fromUtf8("btnServer"))
        self.tabWidget.addTab(self.tabServer, _fromUtf8(""))
        self.tabClient = QtGui.QWidget()
        self.tabClient.setObjectName(_fromUtf8("tabClient"))
        self.btnClient = QtGui.QPushButton(self.tabClient)
        self.btnClient.setGeometry(QtCore.QRect(220, 270, 114, 32))
        self.btnClient.setObjectName(_fromUtf8("btnClient"))
        self.tableClient = QtGui.QTableWidget(self.tabClient)
        self.tableClient.setGeometry(QtCore.QRect(20, 20, 511, 192))
        self.tableClient.setObjectName(_fromUtf8("tableClient"))
        self.tableClient.setColumnCount(0)
        self.tableClient.setRowCount(0)
        self.tabWidget.addTab(self.tabClient, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArquivo = QtGui.QMenu(self.menubar)
        self.menuArquivo.setObjectName(_fromUtf8("menuArquivo"))
        self.menuConfigura_es = QtGui.QMenu(self.menubar)
        self.menuConfigura_es.setObjectName(_fromUtf8("menuConfigura_es"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionRestart = QtGui.QAction(MainWindow)
        self.actionRestart.setObjectName(_fromUtf8("actionRestart"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.menuArquivo.addAction(self.actionOpen)
        self.menuArquivo.addAction(self.actionRestart)
        self.menuArquivo.addAction(self.actionExit)
        self.menuConfigura_es.addAction(self.actionSettings)
        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuConfigura_es.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnServer.setText(_translate("MainWindow", "Iniciar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabServer), _translate("MainWindow", "Servidor", None))
        self.btnClient.setText(_translate("MainWindow", "Iniciar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabClient), _translate("MainWindow", "Cliente", None))
        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo", None))
        self.menuConfigura_es.setTitle(_translate("MainWindow", "Configurações", None))
        self.actionOpen.setText(_translate("MainWindow", "Abrir", None))
        self.actionRestart.setText(_translate("MainWindow", "Reiniciar", None))
        self.actionExit.setText(_translate("MainWindow", "Sair", None))
        self.actionSettings.setText(_translate("MainWindow", "Alterar", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

