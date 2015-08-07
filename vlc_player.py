import sys

from PyQt4 import QtGui, QtCore
import vlcjoao

class Player(QtGui.QMainWindow):

    # A simple Media Player using VLC and Qt.
    def __init__(self, filename, debug = False, master = None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        self.end_reached = False
        self.debug = debug
        self.filename = filename

        self.min_fps = 9999999999
        self.mean_fps = 0
        self.max_fps = 0

        # Creating a basic vlc instance.
        self.instance = vlcjoao.Instance()
        
        # Creating an empty vlc media player.
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = True

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.onEsc()

    def onEsc(self, fn):
        fn()

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
            self.showFullScreen()		
            self.openFile()

    def updatePosition(self, correct_pos):
        # Loop when it is finished.
        if self.mediaplayer.is_playing():
            pos = self.mediaplayer.get_position()
            if (abs(pos - correct_pos) > 0.01):
                self.mediaplayer.set_position(correct_pos)
