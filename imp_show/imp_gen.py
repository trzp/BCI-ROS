#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-10-28 21:17:44
# Contact: mrtang@nudt.edu.cn 
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-10-28 22:25:09

import sys
sys.path.append('..//..//pipe')
from win_named_pipe import *
import numpy as np

def test():
    pipe = hWinNamedPipeServer('_bci_ros_imp_')
    for i in xrange(60):
        imp = 15*np.random.rand(32)
        print imp
        k1 = np.arange(31)
        k0 = np.array([28,3])
        buf = np.hstack((k0,k1,imp)).astype(np.int32).tostring()
        pipe.put(buf)
        time.sleep(1)

if __name__ == '__main__':
    test()