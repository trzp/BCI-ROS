#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-10-28 16:14:52
# Contact: mrtang@nudt.edu.cn 
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-10-28 17:44:04

import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mmap
from matplotlib.widgets import Button

class SignalScope(object):
    def __init__(self,signal_channels,samplingrate=100,time_length=5):
        #创建figure
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.15)
        plt.subplots_adjust(top=0.95)
        plt.subplots_adjust(right=0.95)
        plt.subplots_adjust(left=0.05)

        #创建两个button
        zoomout = plt.axes([0.7, 0.01, 0.1, 0.06])
        zoomin = plt.axes([0.85, 0.01, 0.1, 0.06])
        self.bt_zoomout = Button(zoomout, 'zoom out')
        self.bt_zoomin = Button(zoomin, 'zoom in')

        #button回调
        self.bt_zoomout.on_clicked(self.bt_zoomout_callback)
        self.bt_zoomin.on_clicked(self.bt_zoomin_callback)


        self.sig_chs = signal_channels
        self.gain = 1       #初始默认增益为1
        self.samplingrate = samplingrate
        self.time_length = time_length
        self.y_len = self.time_length*self.samplingrate

        scale = 200    #即默认的eeg信号幅值范围是-100 -> 100
        
        self.xdata = np.linspace(0,self.time_length,self.time_length*self.samplingrate)
        self.ydata = np.zeros([self.sig_chs,self.y_len])
        self.ax.set_xlim(0,self.time_length)
        self.ax.set_ylim(0,scale*self.sig_chs)
        self.ax.grid()
        self.ax.set_title('EEG signals')
        # self.ax.set_xlabel('time /seconds')
        # self.ax.set_ylabel('/uv')
        yticks = range(scale/2,scale*self.sig_chs+scale/2,scale)
        self.ax.set_yticks(yticks)
        yticklabel = ['ch%i'%(i+1) for i in xrange(len(yticks))]
        self.ax.set_yticklabels(yticklabel)
        self.y_offset = np.array([yticks]).transpose()     #即每个通道对应y轴原点

        #颜色表
        colors = [(0,0,0),(255,255,0),(176,224,230),(255,153,18),(65,105,225),(0,255,255),
                 (255,97,0),(0,255,0),(160,32,240),(255,0,0),(94,38,18)]*12
        self.lines = []
        for i in xrange(self.sig_chs):
            self.lines.append(Line2D([],[],linewidth=0.5,color=[c/255. for c in colors[i]]))
            self.ax.add_line(self.lines[i])

    def bt_zoomout_callback(self,event):
        self.gain *= 1.2

    def bt_zoomin_callback(self,event):
        self.gain /=1.2

    def update(self,y): #y: chs x points
        #self.ax.figure.canvas.draw()    #清理屏幕,似乎会造成闪烁

        if self.ydata.shape[1]>=self.y_len:     #已经满屏
            [self.lines[i].set_data([],[]) for i in xrange(self.sig_chs)]
            self.ydata = y
            return self.lines
        else:   self.ydata = np.hstack((self.ydata,y))[:,:self.y_len]
        temdata = self.gain*self.ydata + self.y_offset    
        ylen = temdata.shape[1]
        [self.lines[i].set_data(self.xdata[:ylen],temdata[i,:]) for i in xrange(self.sig_chs)]  
        return self.lines

class EEGshow(SignalScope):
    def __init__(self,signal_channels=3,samplingrate=100,time_length=5):
        super(EEGshow,self).__init__(signal_channels,samplingrate,time_length)
        self.f = open('./bci_ros_eeg_tem.dat','r')
        self.m = mmap.mmap(self.f.fileno(),6400,access=mmap.ACCESS_READ)

    def eegupdate(self,num):
        self.m.seek(0)
        data = np.fromstring(self.m.read(3*10*4),dtype=np.float32)
        data = data.reshape(3,10)
        return self.update(data)

if __name__ == '__main__':
    eegshow = EEGshow()
    ani = animation.FuncAnimation(eegshow.fig,eegshow.eegupdate,interval=100,blit=True)
    plt.show()


