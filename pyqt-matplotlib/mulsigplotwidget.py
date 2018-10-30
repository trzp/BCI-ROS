#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-10-30 08:56:18
# Contact: mrtang@nudt.edu.cn 
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-10-30 10:45:28


'''
this script provides a widget for pyqt4 to real time display multichannels'
data array based on matplotlib.
'''

from __future__ import division
from PyQt4 import  QtGui
from matplotlib.backends.backend_qt4agg import  FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D



class MulSigPlot(FigureCanvas):
 
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.05)    #充满绘图区
        plt.subplots_adjust(top=0.95)
        plt.subplots_adjust(right=0.95)
        plt.subplots_adjust(left=0.05)
 
        FigureCanvas.__init__(self, self.fig) #继承figurecanvas，将matplotlib绘制在画布上
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def initialize(self,chs,xlim,ylim):
        self.ax.set_xlim(xlim[0],xlim[1])
        self.ax.set_ylim(ylim[0],ylim[1])
        self.ax.grid()

        scaley = (ylim[1]-ylim[0])/chs #每个channel占多少
        yticks = np.arange(scaley/2,scaley*chs+scaley/2,scaley)
        print yticks
        yticklabel = ['ch%i'%(i+1) for i in xrange(len(yticks))]
        self.ax.set_yticks(yticks)
        self.ax.set_yticklabels(yticklabel,size=8)

        xticks = np.linspace(xlim[0],xlim[1],6)
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels([str(item) for item in xticks],size=8)

        self.colors = colors = [(255,255,0),(176,224,230),(255,153,18),(65,105,225),(0,255,255),
                 (255,97,0),(0,255,0),(0,0,0),(160,32,240),(255,0,0),(94,38,18)]*12

        self.y_offset = np.array([yticks]).transpose()     #即每个通道对应y轴原点
        self.gain = 1

        self.lines = []
        for i in xrange(chs):
            self.lines.append(Line2D([],[],linewidth=0.5,color=[c/255. for c in colors[i]]))
            self.ax.add_line(self.lines[i])
 
    def plot(self, datax, datay):
        '''
        datax and datay should be 2D array
        '''
        # for i in xrange(datax.shape[0]):
        #     self.ax.plot(datax[i],datay[i],linewidth=0.5,color=self.colors[i])
        datay = self.gain*datay + self.y_offset
        [self.lines[i].set_data(datax[i],datay[i]) for i in xrange(1)]
        self.draw()


class  MulSigPlotWidget(QtGui.QWidget):

    def __init__(self , parent =None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MulSigPlot()
        self.vbl = QtGui.QVBoxLayout() 
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

    def initialize(self,chs,xlim,ylim):
        self.canvas.initialize(chs,xlim,ylim)

    def update(self,datax,datay):
        self.canvas.plot(datax,datay)
