#-*-coding:utf-8-*-
import config,time
import os,re,shutil
from datetime import datetime
from common import *
from logging.config import fileConfig
"""
文件夹内有没有文件，若没有，则删掉该文件夹。
"""
def del_file():
    file_list=get_file_list()
    for path in file_list:
        file_count=len(os.listdir(path))
        if file_count==0:
            command='rm -rf '+path
            os.system(command)
if __name__=='__main__':
    try: 
        print 'start: del file',get_now_time()
        del_file()
        print 'over: del file',get_now_time()
        #os.system('nohup python del_tar.py >> nohup.txt 2>&1 &')
    except Exception,e:
        print e