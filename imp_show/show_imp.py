#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-10-28 20:09:13
# Contact: mrtang@nudt.edu.cn 
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-10-28 22:24:48

# log: debugged ok   2018-10-28

from PyQt4 import Qt, QtGui
from frmImpedance import Ui_frmImpedanceDisplay
import numpy as np
import sys
sys.path.append('..//..//pipe')
from win_named_pipe import *

class MainWindow(QtGui.QDialog,threading.Thread):

    def __init__(self,parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_frmImpedanceDisplay()
        self.ui.setupUi(self)

        for r in xrange(7):
            for c in xrange(10):
                ch = r*10+c+1
                item = Qt.QTableWidgetItem()
                item.setTextAlignment(Qt.Qt.AlignCenter)
                item.setText(str(ch))
                self.ui.tableWidgetValues.setItem(r,c,item)

        self.pipe = WinNamedPipeClient('_bci_ros_imp_')
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()

    def run(self):
        self.ok = False
        while True:
            if self.ok:
                try:
                    buf = self.pipe.read()  #防止server中途掉线
                    self.update(buf)
                except:
                    self.ok = False
                    print '>>>> connection broken >>>>'
            else:
                try:
                    self.pipe.connect()     #尝试连接
                    print '>>>> connection built >>>>'
                    self.ok = True
                except:
                    self.ok = False
                    time.sleep(0.5)


    def update(self,buf):
        '''
        buf: chnum,refnum,chlist,reflist,chimp,refimp,gnd   #all int32
        '''
        data = np.fromstring(buf,dtype = np.int32)
        chnum = data[0]
        refnum = data[1]
        chlist = data[2:2+chnum]
        reflist = data[2+chnum:2+chnum+refnum]
        chimp = data[2+chnum+refnum:2+chnum+refnum+chnum]
        refimp = data[2+chnum+refnum+chnum:2+chnum+refnum+chnum+refnum]
        gnd = data[-1]

        temimp = np.zeros(70)
        temimp[np.hstack(data[2:2+chnum+refnum])] = data[2+chnum+refnum:-1]

        for r in xrange(7):
            for c in xrange(10):
                ch = r*10+c
                if ch in chlist:
                    item = self.ui.tableWidgetValues.item(r,c)
                    item.setText('c%d: %d'%(ch+1,temimp[ch]))
                    item.setBackgroundColor(self.get_color(temimp[ch]))
                elif ch in reflist:
                    item = self.ui.tableWidgetValues.item(r,c)
                    item.setText('r%d: %d'%(ch+1,temimp[ch]))
                    item.setBackgroundColor(self.get_color(temimp[ch]))

                else:
                    item = self.ui.tableWidgetValues.item(r,c)
                    item.setText('c%d'%(ch+1,))
                    item.setBackgroundColor(Qt.QColor(255,255,255))

        item = self.ui.tableWidgetValues.item(6,9)
        item.setText('gnd:%d'%(gnd,))
        item.setBackgroundColor(self.get_color(gnd))


    def get_color(self,value):
        v = self.ui.spinBox.value()
        if value<v/3.:
            return Qt.QColor(0,255,0)
        elif value<2*v/3.:
            return Qt.QColor(255,255,0)
        else:
            return Qt.QColor(255,0,0)

def main():
    print 'impedance shown started!'
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp=MainWindow()
    myapp.show()
    app.exec_()


if __name__ == "__main__":
    main()
