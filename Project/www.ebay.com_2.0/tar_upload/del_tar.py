#-*-coding:utf-8-*-
import config
import os
from datetime import datetime
from common import *
"""
从upload_history.csv文件中读取已经上传成功的压缩文件，
删除这些压缩文件
"""
def del_tar():
    upload_files_list=upload_files()
    for name in upload_files_list:
        command='rm -rf '+name
        os.system(command)
def upload_files():
    upload_files_list=[]
    f=open('upload_history.csv')
    lines=f.readlines()
    f.close()
    for row in lines:
        row_dic=eval(row.strip())
        if row_dic['result']==True:
            upload_files_list.append(row_dic['file'])
    return upload_files_list
if __name__=='__main__':
    upload_files()
    try:    
        print 'start: del tar',get_now_time()
        del_tar()
        print 'over: del tar',get_now_time()
    except Exception,e:
        print e

