#!/usr/bin/env python
#-*- coding:utf-8 -*-

#Copyright (C) 2018, Nudt, JingshengTang, All Rights Reserved
#Author: Jingsheng Tang
#Email: mrtang@nudt.edu.cn


import numpy as np
import threading
from copy import deepcopy
from multiprocessing import Queue
from multiprocessing import Event
import multiprocessing

from createlog import create_log_with_time as create_log
from get_clock_rz import get_clock as sysclock
from remotelog import RemoteLog


class core(threading.Thread):
    u'''
    Q_p2c     #phase -> core -> transmit phase -> 发送phase
    Q_c2p     #core -> phase -> change phase manul -> 强制跳转phase
    Q_c2g     #core -> gui  -> update gui -> 更新gui
    Q_s2c     #sigpro -> core -> transmit signal package -> 传递信号包
    Q_g2s     #gui -> sigpro -> transmit trigger -> 传递trigger
    E_c2s     #core -> sigpro -> quit process -> 结束sigpro
    E_g2p     #gui -> phase -> user ended signal -> 用户结束信号
    '''
    
    Q_p2c = Queue()
    Q_c2p = Queue()
    Q_c2g = Queue()
    Q_s2c = Queue()
    Q_g2s = Queue()
    E_c2s = Event()
    E_g2p = Event()
    
    PHASES = []
    STIMULI = {}
    CONFIGS = {}
    Trigger = {}
    
    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.IP = ip
        self.PORT = port
        self.RL = RemoteLog(ip,port)
    
    #在子类中覆盖实现的
    def initialize(self):#在子类中实现
        pass

    def process(self,eeg,tri):#在子类中实现
        pass

    def transition(self,phase): #在子类中实现
        pass

    def changePhase(self,phase):
        self.Q_c2p.put(['change',phase])
    
    def writeLog(self,mess):
        self.RL.put_log('core',mess)

    def guiUpdate(self,sti,trigger):
        self.Q_c2g.put([sti,trigger])

    def StartRun(self):
        self.writeLog('[Info]process started')

        p1 = multiprocessing.Process(target=gui_process,args=(self.STIMULI,self.Q_c2g,self.E_g2p,self.Q_g2s))
        p2 = multiprocessing.Process(target=phase_process,args=(self.PHASES,self.Q_p2c,self.Q_c2p,self.E_g2p,self.IP,self.PORT))
        p3 = multiprocessing.Process(target=sig_process,args=(self.CONFIGS,self.Trigger,self.Q_g2s,self.Q_s2c,self.E_c2s))
        p3.start()
        p2.start()
        p1.start()
        self.start()

        while True:
            ph = self.Q_p2c.get()
            self.writeLog('[Get phase]%s'%ph)
            self.transition(ph)
            if ph == 'stop':
                self.Q_c2g.put('_q_u_i_t_') #结束gui
                self.E_c2s.set()            #结束sigpro
                break
        self.writeLog('[Info]process exit')

    def run(self):  #子线程接受信号做处理
        self.writeLog('[Info]sub thread started')

        while True:
            [sig,tri] = self.Q_s2c.get()
            self.process(sig,tri)

        self.writeLog('[Info]sub thread exit')
