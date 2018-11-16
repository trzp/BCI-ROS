#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-10-30 09:34:30
# Contact: mrtang@nudt.edu.cn
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-11-07 00:06:38


from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QFileDialog
from mainfrm import Ui_Dialog
import threading
import numpy as np
import time
import re
import json


class MainWindow(QtGui.QDialog, threading.Thread):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_loadparm,
                               QtCore.SIGNAL("clicked()"), self.loadparm)
        QtCore.QObject.connect(self.ui.pushButton_saveparm,
                               QtCore.SIGNAL("clicked()"), self.saveparm)
        QtCore.QObject.connect(self.ui.pushButton_impedance,
                               QtCore.SIGNAL("clicked()"), self.readimp)
        QtCore.QObject.connect(self.ui.pushButton_eegacq,
                               QtCore.SIGNAL("clicked()"), self.readeeg)

        self.eeg_chs = []
        self.ref_chs = []
        self.eeg_chs_str = ''
        self.ref_chs_str = ''

    def loadparm(self):
        file_name = QFileDialog.getOpenFileName(self,'load parm','./params','*.json')
        if file_name != '':
            with open(file_name,'r') as f:
                tem = json.loads(f.read())
            self.eeg_chs_str = tem['eeg_chs']
            self.ref_chs_str = tem['ref_chs']
            if self.parse_parm(self.eeg_chs_str,self.ref_chs_str):
                self.ui.textEdit_sigch.setText(self.eeg_chs_str)
                self.ui.textEdit_refch.setText(self.ref_chs_str)

    def update_parm(self):
        self.eeg_chs_str = str(self.ui.textEdit_sigch.toPlainText())
        self.ref_chs_str = str(self.ui.textEdit_refch.toPlainText())

        return self.parse_parm(self.eeg_chs_str,self.ref_chs_str)

    def parse_parm(self,str_eeg,str_ref):
        '''
        return value:
            0  error
            1  ok
        '''

        err_str_lst = ['','incomplete input param','input illegal charactor']
        flg1,self.eeg_chs = self.__parsech(str_eeg)
        flg2,self.ref_chs = self.__parsech(str_ref)
        errstr = ''
        errstr += err_str_lst[flg1]
        if flg1 != flg2:    errstr += '\n'+err_str_lst[flg2]
        if errstr != '':
            QMessageBox.warning(self,'error',errstr)
            return 0

        return 1

    def saveparm(self):
        if self.update_parm():
            file_path = QFileDialog.getSaveFileName(self,'save param','./params','*.json')
            params = {'eeg_chs':self.eeg_chs_str,'ref_chs':self.ref_chs_str}
            jsObj = json.dumps(params)
            if file_path != '':
                with open(file_path,'w') as f:
                    f.write(jsObj)


    def __parsech(self, str):
        '''
        return value: error,ch
        error  2: including illegal charactor
               1: including incomplete input
               0: ok
        '''

        #参数检查
        num = len(re.findall(r'\d',str))+len(re.findall(',',str))+len(re.findall('-',str))
        if num != len(str):     return 2,None

        stlst = str.split(',')
        ch = []
        try:
            for s in stlst: ch += self.__parsech1(s)
        except:
            return 1,None

        return 0,ch

    def __parsech1(self, str):
        stlst = [int(item) for item in str.split('-')]

        if len(stlst) > 1:
            return range(stlst[0], stlst[1]+1)
        else:
            return stlst


    def readimp(self):
        print 'imp'

    def readeeg(self):
        print 'eeg'


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    app.exec_()


if __name__ == '__main__':
    main()
