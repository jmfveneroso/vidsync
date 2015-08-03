import sys
import os
import vlcjoao
import time, threading

from PyQt4 import QtGui, QtCore

import socket, struct
import thread

import ui

class FileTable(QtGui.QTableWidget):
    def __init__(self, *args):
        QtGui.QTableWidget.__init__(self, *args)
        horHeaders = []
        horHeaders.append("Arquivo")
        horHeaders.append("Desvio de sincronia")
        self.setHorizontalHeaderLabels(horHeaders)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().resizeSection(0, 540);
 
    def addFile(self, filename):
        j = self.rowCount()
        
        self.insertRow(j)
        self.setItem(j, 0, QtGui.QTableWidgetItem(filename));
        self.setItem(j, 1, QtGui.QTableWidgetItem(0));

        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()

    def updateOffset(self, fileNum, offset):
        self.item(fileNum, 1).setText(str(offset));

class MainInterface(QtGui.QMainWindow):

    # The main interface with configuration options
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)

        self.list = []
        self.correct_pos = 0
        self.updated = True
        self.isServer = False
        self.synchronizer = Synchronizer()

        self.setWindowTitle("Marila")
        self.createUI()

    def createUI(self):
        # Set up the user interface, signals & slots
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)
   
        self.setGeometry(100, 100, 740, 580)
        self.vboxlayout = QtGui.QVBoxLayout()

        # Menu bar 
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Abrir arquivo')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)       

        # File table
        self.table = FileTable(0, 2)

        # Start button
        self.button = QtGui.QPushButton('Iniciar')
        self.button.clicked.connect(self.start)

        number_group = QtGui.QButtonGroup(self.widget) # Number group
        r0 = QtGui.QRadioButton("Enviar dados de sincronizacao")
        number_group.addButton(r0)
        r0.clicked.connect(self.setServer)
        r1 = QtGui.QRadioButton("Receber dados de sincronizacao")
        number_group.addButton(r1)
        r1.clicked.connect(self.setClient)
        r1.setChecked(True)

        self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.connect(self.positionslider, QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.vboxlayout.addWidget(r0)
        self.vboxlayout.addWidget(r1)
        self.vboxlayout.addWidget(self.table)
        self.vboxlayout.addWidget(self.button)
        self.vboxlayout.addWidget(self.positionslider)

        self.widget.setLayout(self.vboxlayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)

    # setting the position to where the slider was dragged
    def setPosition(self, position):
        self.list[0].mediaplayer.set_position(position / 1000.0)

    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Abrir arquivo', '~')
        self.table.addFile(filename)
        
        # self.files.append(fname)
    
        # This check is unnecessary.
        # movie = os.path.expanduser(str(fname))
        # if not os.access(movie, os.R_OK):
        #    print('Error: %s file not readable' % movie)
        #        sys.exit(1)

        self.list.append(Player(str(filename)))

    def start(self):
        self.button.setText("Reiniciar")
      
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

        # self.syncLocalVideos()
        self.timer.start()

    # def stop(self):

    def setServer(self):
        self.isServer = True

    def setClient(self):
        self.isServer = False

    # Update UI and run sync operations.
    def update(self):
        # Update the position slider.
        self.positionslider.setValue(self.list[0].mediaplayer.get_position() * 1000)

        correct_pos = 0
        if (self.isServer):
            # if (!list[0]):
                # Choose a film
            
            correct_pos = self.list[0].mediaplayer.get_position()
            self.synchronizer.sendPos(str(correct_pos))

        # Is client.
        else:
            correct_pos = self.synchronizer.receivePos()

        for num in range(0, len(self.list)):
            self.table.updateOffset(num, self.list[num].mediaplayer.get_position() - correct_pos)
            self.list[num].updatePosition(correct_pos)

class Player(QtGui.QMainWindow):

    # A simple Media Player using VLC and Qt.
    def __init__(self, filename, master = None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")
        # self.showFullScreen()

        self.end_reached = False
        self.filename = filename

        # Creating a basic vlc instance.
        self.instance = vlc.Instance()
        
        # Creating an empty vlc media player.
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False

    def createUI(self):
        # Set up the user interface, signals & slots
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window, QtGui.QColor(0,0,0))

        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setContentsMargins(0,0,0,0)

        self.widget.setLayout(self.vboxlayout)

        # self.vlc_events = self.mediaplayer.event_manager()
        # self.vlc_events.event_attach(vlc.EventType.MediaPlayerEndReached, self.media_finished)
            
        self.play()

    def openFile(self):
        self.media = self.instance.media_new(self.filename)
      
        # Put the media in the media player
        self.mediaplayer.set_media(self.media)
        
        if sys.platform.startswith('linux'): # for Linux using the X Server
          self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
          self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
          self.mediaplayer.set_nsobject(self.videoframe.winId())

        self.mediaplayer.play()

    def play(self):
        if (self.mediaplayer.play() == -1):
            self.openFile()

    def updatePosition(self, correct_pos):
        # Loop when it is finished.
        if not self.mediaplayer.is_playing():
            self.mediaplayer.stop()
            self.play()
        else:
            pos = self.mediaplayer.get_position()
            if (abs(pos - correct_pos) > 0.0005):
                self.mediaplayer.set_position(correct_pos + 0.0001)

MCAST_GRP = "224.3.29.71"
MCAST_PORT = 5005

class Synchronizer():

    # Send or receive synchronization data
    def __init__(self, master=None):
        self.sock = None
        self.correct_pos = 0

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

list = []

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

mainInterface = MainInterface()
mainInterface.show()

sys.exit(app.exec_())
