#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-10-30 09:34:30
# Contact: mrtang@nudt.edu.cn 
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-10-30 10:43:40


from PyQt4 import QtCore, QtGui
from BaseUi import *
import threading
import numpy as np
import time

class MainWindow(QtGui.QDialog,threading.Thread): 

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.sigcanvas.initialize(2,[0,5],[0,2])
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()

    def run(self):
        while True:
            self.ui.sigcanvas.update(np.array([np.linspace(0,5,6)]),np.random.rand(1,6)-0.5)
            time.sleep(0.1)

def main():
    print 'impedance shown started!'
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp=MainWindow()
    myapp.show()
    app.exec_()

if __name__ == '__main__':
    main()
