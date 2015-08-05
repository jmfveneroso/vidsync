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

class FileTable(QtGui.QTableWidget):
    def __init__(self, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().resizeSection(0, 540);
        self.setGeometry(QtCore.QRect(20, 20, 511, 192))
        self.setObjectName(_fromUtf8("tableServer"))
        self.setColumnCount(2)
        horHeaders = []
        horHeaders.append("Arquivo")
        horHeaders.append("Desvio de sincronia")
        self.setHorizontalHeaderLabels(horHeaders)

    def addRow(self, filename, offset):
        i = self.rowCount()
        self.insertRow(i)
        self.setItem(i, 0, QtGui.QTableWidgetItem(filename));
        self.setItem(i, 1, QtGui.QTableWidgetItem(offset));
        self.resizeColumnsToContents()

    def clear(self):
        for i in reversed(range(self.rowCount())):
            self.removeRow(i)

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

        self.tableServer = FileTable(self.tabServer)

        self.sliderServer = QtGui.QSlider(self.tabServer)
        self.sliderServer.setGeometry(QtCore.QRect(20, 230, 511, 22))
        self.sliderServer.setOrientation(QtCore.Qt.Horizontal)
        self.sliderServer.setObjectName(_fromUtf8("sliderServer"))
        self.sliderServer.setToolTip("Posição")
        self.sliderServer.setMaximum(1000)
        self.btnServer = QtGui.QPushButton(self.tabServer)
        self.btnServer.setGeometry(QtCore.QRect(220, 270, 114, 32))
        self.btnServer.setObjectName(_fromUtf8("btnServer"))
        self.tabWidget.addTab(self.tabServer, _fromUtf8(""))
        self.tabClient = QtGui.QWidget()
        self.tabClient.setObjectName(_fromUtf8("tabClient"))
        self.btnClient = QtGui.QPushButton(self.tabClient)
        self.btnClient.setGeometry(QtCore.QRect(220, 270, 114, 32))
        self.btnClient.setObjectName(_fromUtf8("btnClient"))
        
        self.tableClient = FileTable(self.tabClient)
        
        self.tabWidget.addTab(self.tabClient, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.setStatusTip('Abrir arquivo')
        self.actionRestart = QtGui.QAction(MainWindow)
        self.actionRestart.setObjectName(_fromUtf8("actionRestart"))
        self.actionRestart.setShortcut('Ctrl+R')
        self.actionRestart.setStatusTip('Reiniciar')
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionRestart)
        self.menuFile.addAction(self.actionExit)
        self.menuSettings.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnServer.setText(_translate("MainWindow", "Iniciar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabServer), _translate("MainWindow", "Servidor", None))
        self.btnClient.setText(_translate("MainWindow", "Iniciar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabClient), _translate("MainWindow", "Cliente", None))
        self.menuFile.setTitle(_translate("MainWindow", "Arquivo", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Configurações", None))
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

