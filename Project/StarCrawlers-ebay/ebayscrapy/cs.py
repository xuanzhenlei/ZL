#-*-coding:utf-8-*-
import datetime
import config
import time,re,os
import logging
import logging.config
from myutil import httptools
import math
from multiprocessing import Pool,Lock
import sys
import chardet

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1") #记录跑完的asin
logger2 = logging.getLogger("logger2") #记录错误

"""
内存管理机制
"""

if __name__=='__main__':    
    print 'Process (%s) start...' % os.getpid()
    pid = os.fork()
    print pid
    if pid==0:
        print 'I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid())
    else:
        print 'I (%s) just created a child process (%s).' % (os.getpid(), pid)
    