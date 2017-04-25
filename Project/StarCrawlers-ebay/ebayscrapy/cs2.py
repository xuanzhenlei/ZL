#-*-coding:utf-8-*-
import datetime
import config
import time,re,os
import logging
import logging.config
from myutil import httptools
import math
from multiprocessing import Pool,Lock

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1") #记录跑完的asin
logger2 = logging.getLogger("logger2") #记录错误


if __name__=='__main__':
    for i in range(60):
        print 'exe cs2.py'
        time.sleep(1)
    
            
            