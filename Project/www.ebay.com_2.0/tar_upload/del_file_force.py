#-*-coding:utf-8-*-
import config,time
import os,re,shutil
from datetime import datetime
from common import *

def del_file():
    file_list=get_file_list()
    for name in file_list:
        command='rm -rf '+name
        os.system(command)
if __name__=='__main__':
    try:   
        del_file()
    except Exception,e:
        print e

