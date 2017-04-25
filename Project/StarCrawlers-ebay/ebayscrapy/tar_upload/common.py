#-*-coding:utf-8-*-
import time
import os,re
from datetime import datetime

num_regx=re.compile('\d+$')

def get_now_time():#获取当前时间，返回字符型时间如：20151020 11:20:30
    now=datetime.now()
    now_list=str(now).split('.')
    now_time=now_list[0]
    return now_time
def get_file_list():
    file_list=[]
    file_all=os.listdir(os.getcwd())
    for name in file_all:
        num=num_regx.search(name)
        if num!=None:
            number=num.group()
            if number==name:
                file_list.append(name)
    return file_list
def get_tar_list():
    tar_list=[]
    file_all=os.listdir(os.getcwd())
    for name in file_all:
        if name.find('.tar.gz')!=-1:
            tar_list.append(name)
    return tar_list
def progress_monitor(content):
    f=open('progress_monitor.txt','aw')
    f.write(content)
    f.flush()
    f.close()
    
    
