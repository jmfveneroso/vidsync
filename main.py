import sys
import os
import time, threading

from PyQt4 import QtGui, QtCore

import socket, struct
import thread

import ui
import vlc_player

class MainInterface(ui.Ui_MainWindow):

    # The main interface with configuration options
    def __init__(self, MainWindow, master = None):
        self.list = []
        self.offsets = []
        self.correct_pos = 0
        self.isServer = True
        
        self.synchronizer = Synchronizer()
        self.window = MainWindow
        self.running = False
  
        self.initialize()

    def initialize(self):
        super(MainInterface, self).setupUi(self.window)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionRestart.triggered.connect(self.clear)
    
        # Start button
        self.btnServer.clicked.connect(self.playOrRestart)
        self.btnClient.clicked.connect(self.playOrRestart)
        
        # Tabs
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.setServer)
        
        # Slider
        self.window.connect(self.sliderServer, QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.timer = QtCore.QTimer(self.window)
        self.timer.setInterval(200)
        self.window.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)

    # setting the position to where the slider was dragged
    def setPosition(self, position):
        if (self.running and self.isServer):
            self.list[0].mediaplayer.set_position(position / 1000.0)

    def clear(self):
        for i in range(0, len(self.list)):
            self.list[i].close()
            self.list[i].mediaplayer.stop()
        self.list = []
        self.offsets = []
        self.running = False
        self.timer.stop()
        self.btnServer.setText("Iniciar")
        self.btnClient.setText("Iniciar")
        self.updateTables()
        self.synchronizer.close()

    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self.window, 'Abrir arquivo', '~')
        if (filename):
            self.list.append(vlc_player.Player(str(filename)))
            self.offsets.append(0)
            self.updateTables()

    def playOrRestart(self):
        if (not self.running and len(self.list) > 0):
            self.running = True
            self.timer.start()
            self.btnServer.setText("Parar")
            self.btnClient.setText("Parar")
      
            desktop = app.desktop()

            for i in range(0, len(self.list)):
                self.list[i].show()

                # Get the screen geometry in a multi screen environment.
                screenNum = 0 if (desktop.screenCount() <= i) else i
                rect = desktop.screenGeometry(screenNum)

                self.list[i].move(rect.left(), rect.top())
                self.list[i].resize(rect.width(), rect.height())
                self.list[i].showMaximized()

            # Start all players at the same time.
            for i in range(0, len(self.list)):
                self.list[i].play()

            if (self.isServer):
                self.synchronizer.send()
            else:
                self.synchronizer.receive()
        else:
            self.clear()
              
    def setServer(self, flag):
        self.clear()
        self.isServer = (flag == 0)

    def updateTables(self):
        self.tableServer.clear()
        self.tableClient.clear()
        for i in range(0, len(self.list)):
            player = self.list[i]
            self.tableServer.addRow(player.filename, self.offsets[i])
            self.tableClient.addRow(player.filename, self.offsets[i])


    # Update UI and run sync operations.
    def update(self):
        correct_pos = 0
        if (self.isServer):
            # Update the position slider.
            self.sliderServer.setValue(self.list[0].mediaplayer.get_position() * 1000)

            correct_pos = self.list[0].mediaplayer.get_position()
            self.synchronizer.sendPos(str(correct_pos))

        # Is client.
        else:
            correct_pos = self.synchronizer.receivePos()

        for i in range(0, len(self.list)):
            player = self.list[i]
            self.offsets[i] = player.mediaplayer.get_position() - correct_pos
            
            if (self.running):
                player.updatePosition(correct_pos)

        self.updateTables()

MCAST_GRP = "224.3.29.71"
MCAST_PORT = 5005

class Synchronizer():

    # Send or receive synchronization data
    def __init__(self, master=None):
        self.sock = None
        self.correct_pos = 0

    def close(self):
        if (self.sock):
            self.sock.close()

    def send(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        
        # Enable multicasting (currently only works for 2 clients)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # thread.start_new_thread(self.serverHandler, (self.sock,))

    def receive(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM, # UDP
                             socket.IPPROTO_UDP) 

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind(('', MCAST_PORT))
        
        mreq = struct.pack("4sL", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        thread.start_new_thread(self.clientHandler, (self.sock,))
    
    def clientHandler(self, sock):
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            self.correct_pos = float(data)

    def sendPos(self, correct_pos):
        self.sock.sendto(str(correct_pos), (MCAST_GRP, MCAST_PORT))

    def receivePos(self):
        return self.correct_pos

try:
    from msvcrt import getch
except ImportError:
    import termios
    import tty

    def getch():  # getchar(), getc(stdin)  #PYCHOK flake
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

# movie = os.path.expanduser(sys.argv[1])
# if not os.access(movie, os.R_OK):
#     print('Error: %s file not readable' % movie)
#     sys.exit(1)

app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = MainInterface(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
