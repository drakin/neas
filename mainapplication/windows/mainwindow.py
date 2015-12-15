import numpy as np
import pyqtgraph.opengl as gl
from PyQt4 import QtGui, QtCore
from mainapplication.utils import utils
from qrangeslider import QRangeSlider


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.show()
        self.resize(400, 600)
        self.setWindowTitle('Neas')
        self._initMenuBar_()
        self.mainWidget = QtGui.QWidget()
        self.tabWidget = QtGui.QTabWidget()

        self.arrayMask = None
        self.maskIndex = 0
        self.infoFile = None
        self.dataFile = None

        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(QtGui.QGridLayout())

        self.graphicWidgetGrid = gl.GLViewWidget()
        self.graphicWidgetGrid.setCameraPosition(distance=50)
        self.graphicWidgetDisc = gl.GLViewWidget()
        self.graphicWidgetDisc.setCameraPosition(distance=50)

        self.tabWidget.addTab(self.graphicWidgetGrid, 'Grid')
        self.tabWidget.addTab(self.graphicWidgetDisc, 'Disc')
        # self.mainWidget.layout().addWidget(self.graphicWidget1, 0, 0, 2, 1)
        self.mainWidget.layout().addWidget(self.tabWidget, 0, 0, 2, 1)

        self.matrixLabel = QtGui.QLabel('',self)
        self.rangeSlider = QRangeSlider(self.mainWidget)
        self.rangeSlider.setFixedHeight(30)
        self.mainWidget.layout().addWidget(self.rangeSlider, 2, 0)

        tmp = QtGui.QGridLayout()
        tmp.setAlignment(QtCore.Qt.AlignTop)

        tmp.addWidget(QtGui.QLabel('path to info file',self),0,0)
        tmp.addWidget(QtGui.QPushButton("Change"),0,1)
        tmp.addWidget(QtGui.QLabel('path to data file',self),1,0)
        tmp.addWidget(QtGui.QPushButton("Change"),1,1)
        tmp.addWidget(QtGui.QPushButton("Change Colors"),2,0,1,3)


        # tmp.addWidget(QtGui.QLabel('Red',self),3,0)
        # tmp.addWidget(QtGui.QLabel('Green',self),3,1)
        # tmp.addWidget(QtGui.QLabel('Blue',self),3,2)

        tmp2=[]
        for i in xrange(0,3):
            tmp2.append(QtGui.QSlider(QtCore.Qt.Vertical))
            tmp2[i].setFixedHeight(100)
            tmp.addWidget(tmp2[i],4,i)

        self.combobox = QtGui.QComboBox(self)
        self.combobox.addItem("Without anti aliasing")
        self.combobox.addItem("With anti aliasing")
        self.combobox.activated[int].connect(self.onComboActivated)
        tmp.addWidget(self.combobox, 5, 0, 1, 3)
        self.arrayMaskLabel = QtGui.QLabel("")
        self.arrayMaskLabel.adjustSize()
        self.arrayMaskLabel.setAlignment(QtCore.Qt.AlignTop)
        np.set_printoptions(precision=2)
        tmp.addWidget(self.arrayMaskLabel, 6, 0, 1, 3)
        self.onComboActivated(0)
        self.mainWidget.layout().addLayout(tmp, 0, 1)

        self.startPos = 0
        self.endPos = 100
        self.connect(self.rangeSlider, QtCore.SIGNAL('startValueChanged(int)'), self.setStart)
        self.connect(self.rangeSlider, QtCore.SIGNAL('endValueChanged(int)'), self.setEnd)

        self.graph3DGrid = None
        self.graph3DDisc = None

    def _initActions_(self):
        self.exitAction = QtGui.QAction(QtGui.QIcon('exit.png'),'&Exit',self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(QtGui.QApplication.quit)

        self.openInfoFileMenu = QtGui.QAction(QtGui.QIcon('open.png'), 'Open info file', self)
        self.openInfoFileMenu.setStatusTip('Open info file')
        self.openInfoFileMenu.triggered.connect(self.loadInfoFileAction)

        self.openDataFileMenu = QtGui.QAction(QtGui.QIcon('open.png'), 'Open data file', self)
        self.openDataFileMenu.setStatusTip('Open data file')
        self.openDataFileMenu.triggered.connect(self.loadDataFileAction)

    def _initMenuBar_(self):
        self._initActions_()
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(self.openInfoFileMenu)
        file_menu.addAction(self.openDataFileMenu)
        file_menu.addAction(self.exitAction)

    def loadDataFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self.show(), 'Open file','')

        if not fileName:
            return
        dataFile = open(fileName, 'rb')
        result = np.fromfile(dataFile, dtype=np.uint32)
        return result.reshape((self.infoFile['nt'], self.infoFile['nx'], self.infoFile['ny']))

    def loadDataFileAction(self):
        self.dataFile = self.loadDataFile()
        self.plotData()

    def loadInfoFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self.show(), 'Open file', '')
        if not fileName:
            return
        infoFile = open(fileName, 'r')
        result = {}
        with infoFile:
            for row in utils.delimited(infoFile):
                tmp = row.split('=')
                if len(tmp) < 2:
                    continue
                result[tmp[0].strip()] = utils.num(tmp[1])
        print "info values:", result
        return result

    def loadInfoFileAction(self):
        self.infoFile = self.loadInfoFile()
        self.startPos = 0
        self.endPos = self.infoFile['nt']
        self.rangeSlider.setRange(0, self.infoFile['nt'])
        self.rangeSlider.setMin(0)
        self.rangeSlider.setMax(self.infoFile['nt'])
        self.rangeSlider.update()
        self.arrayMask = utils.arrayDisc((self.infoFile['nx'], self.infoFile['ny']),
                                         (self.infoFile['nx']/2-1, self.infoFile['ny']/2-1),
                                         self.infoFile['nx']/2-1,
                                         self.maskIndex
                                         )


    def onComboActivated(self, index):
        tmp = utils.arrayDisc((6, 6), (2, 2), 2, index)
        self.arrayMaskLabel.setText(' ' + str(tmp).translate(None, '[]'))
        self.arrayMaskLabel.adjustSize()
        self.maskIndex = index
        if not self.infoFile is None:
            self.arrayMask = utils.arrayDisc((self.infoFile['nx'], self.infoFile['ny']),
                                         (self.infoFile['nx']/2-1, self.infoFile['ny']/2-1),
                                         self.infoFile['nx']/2-1,
                                         self.maskIndex
                                         )
            self.plotData()

    def plotData(self):
        if self.dataFile is None:
            return
        sliceSum = np.sum(self.dataFile[self.startPos:self.endPos], 0)
        curMax = np.max(sliceSum)
        if self.graph3DGrid is None:
            # x = np.linspace(0,self.infoFile['nx'],self.infoFile['nx'])
            # y = np.linspace(0,self.infoFile['ny'],self.infoFile['ny'])
            # self.graph3D  = gl.GLSurfacePlotItem(z=sliceSum, shader='shaded', computeNormals=False, smooth=False, glOptions='opaque')
            self.graph3DGrid = gl.GLSurfacePlotItem(z=sliceSum, shader='heightColor', computeNormals=False, smooth=False)

            # self.graph3D.scale(16./49., 16./49., 1.0)
            # self.graph3D.translate(self.infoFile['nx']/2, self.infoFile['ny']/2, 3)
            #self.graph3D.rotate(-90, 0, 0, 0)
            self.graph3DGrid.translate(-18, 2, 0)
            # self.graph3D.translate(-1000,-700,-700)
            # self.graph3D.shader()['colorMap'] = [1, 1, 1, 1, 0.5, 1, 1, 0, 1]
            # self.graph3D.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
            self.graphicWidgetGrid.addItem(self.graph3DGrid)
            self.setGraph3DColor([0.01, 0.2, 0.5, 0.01, 0.1, 1, 0.01, 0, 2])
        else:
            self.graph3DGrid.setData(z=sliceSum)

        if self.graph3DDisc is None:
            self.graph3DDisc = gl.GLSurfacePlotItem(z=sliceSum*self.arrayMask, shader='heightColor', computeNormals=False, smooth=False)
            self.graph3DDisc.translate(-18, 2, 0)
            self.graphicWidgetDisc.addItem(self.graph3DDisc)
        else:
            self.graph3DDisc.setData(z=sliceSum*self.arrayMask)

        # self.graph3D.shader()['colorMap'] = np.array([0.001, 2, 0.5, 0.001, 0.7, 0.5, 0, 0, 1])

        # print "Plotted"

    def setGraph3DColor(self, color):
        self.graph3DGrid.shader()['colorMap'] = np.array(color)

    def setStart(self, pos):
        if pos != self.startPos:
            print 'setStart',pos
            self.startPos = pos
            self.plotData()

    def setEnd(self, pos):
        if pos != self.endPos:
            print 'setEnd',pos
            self.endPos = pos
            self.plotData()
