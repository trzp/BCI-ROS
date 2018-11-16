#!user/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-10-11 11:25:53
# Contact: mrtang@nudt.edu.cn
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-10-12 01:14:31

import time
import socket

def get_now():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

def create_log_with_time(m):
    return '[%s]%s'%(get_now(),m)

class RemoteLog():
    def __init__(self,ip,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        # self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        # self.ADDR = ('<broadcast>',port)  #慎用广播
        self.ADDR = (ip,port)

    def put_log(self,module_name,mess):
        content = create_log_with_time(mess)
        log = '*%s#%s'%(module_name,content)
        self.sock.sendto(log,self.ADDR)
