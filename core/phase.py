#!/usr/bin/env python
#-*- coding:utf-8 -*-

#Copyright (C) 2018, Nudt, JingshengTang, All Rights Reserved
#Author: Jingsheng Tang
#Email: mrtang@nudt.edu.cn


import time
import socket

from createlog import create_log_with_time as create_log
from get_clock_rz import get_clock as sysclock
from remotelog import *

try:    __INF__ = float('inf')
except: __INF__ = 0xFFFF

def register_phase(arg):
    PHASES = {}
    PHASES['start'] = {'next': '', 'duration': __INF__}
    PHASES['stop'] = {'next': '', 'duration': __INF__}
    for item in arg:
        if item.has_key('duration'):
            PHASES[item['name']]={'next':item['next'],'duration':item['duration']}
        else:
            PHASES[item['name']]={'next':'','duration':__INF__}
    return PHASES

def phase_process(phase_dict,Q_p2c,Q_c2p,E_g2p,ip,port):
    u'''
    phase_list = [{'name':'start','next':'prompt','duration':1},
                  {'name':'prompt','next':'on','duration':1},]
    
    Q_p2c: multiprocessing.Queue  phase -> core  向外部发送phase event
    Q_c2p: multiprocessing.Queue  core -> phase  接受外部发送的event动态改变phase
    格式 ['change',phase name]
    E_g2p: multiprocessing.Event  user -> phase  user cease signal  接受外部发送的强制退出的event

    进程启动后，模块将通过udp广播向6891端口发送运行的状态消息
    '''
    
    #远程发送log
    RL = RemoteLog(ip,port)
    RL.put_log('phase','[Info]process started')

    PHASES = register_phase(phase_dict)
    time.sleep(1)
    current_phase = 'start' #phase必须从start开始
    RL.put_log('phase','[Phase]%s'%current_phase)
    Q_p2c.put(current_phase)
    _clk = sysclock()

    while True:
        clk = sysclock()

        if clk - _clk > PHASES[current_phase]['duration']:  #根据时间跳转到下一个phase
            current_phase = PHASES[current_phase]['next']
            Q_p2c.put(current_phase)
            _clk = clk
            RL.put_log('phase','[Phase]%s'%current_phase)

        if not Q_c2p.empty():
            typ,p = Q_c2p.get()
            if typ == 'change' and PHASES.has_key(p):
                current_phase = p
                _clk = sysclock()
                Q_p2c.put(current_phase)
                RL.put_log('phase','[Phase]%s'%current_phase)
            else:
                RL.put_log('phase','[Warning]change phase error <%s %s>'%(typ,p))
                
        if E_g2p.is_set():
            current_phase = 'stop'
            _clk = clk
            Q_p2c.put('stop')
            RL.put_log('phase','[Phase]%s'%current_phase)
            break

        if current_phase == 'stop': break
        time.sleep(0.005)
    time.sleep(0.5)
    RL.put_log('phase','[Phase]%s'%'process exit')

def example():
    ph = [  {'name':'start','next':'prompt','duration':1},
             {'name':'prompt','next':'on','duration':1},
             {'name':'on','next':'stop','duration':1},
         ]

    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    e = Event()
    phase_process(ph,q1,q2,e)

if __name__ == '__main__':
    from multiprocessing import Queue
    from multiprocessing import Event
    example()