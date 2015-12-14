import sys
from PyQt4 import QtCore, QtGui
from windows import mainwindow


def run():
    app = QtGui.QApplication(sys.argv)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        mw = mainwindow.MainWindow()
        app.setActiveWindow(mw)
        app.exec_()