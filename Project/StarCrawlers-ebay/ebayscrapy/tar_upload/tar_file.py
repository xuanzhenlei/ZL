#-*-coding:utf-8-*-
import time
import os,re
from datetime import datetime
from common import *
import config
"""
压缩文件，
若file==tar_file,则上传；
若len(tar_file)==0,则全部压缩；
若len(tar_file)>0,则把剩余的压缩文件压缩。
"""
tar_num_regx=re.compile('(\d+)')
def get_left_file(tar_list):
    tar_num_list=[]
    result=[]
    for name in tar_list:
        tar_num=tar_num_regx.search(name)
        if tar_num!=None:
            file_name=tar_num.group(1)
            tar_num_list.append(file_name)
    for file in file_list:
        if file not in tar_num_list:
            result.append(file)
    return result
def tar_file(name_list):
    pre=config.pre
    for name in name_list:
        command='tar -czf '+pre+'_'+name+'.tar.gz '+name
        os.system(command)

if __name__=='__main__':
    try:
        file_list=get_file_list()
        tar_list=get_tar_list()
        progress_monitor('file:'+str(len(file_list))+'\n')
        progress_monitor('file.tar.gz:'+str(len(file_list))+'\n')
        if len(file_list)==len(tar_list):
            progress_monitor('start: upload...'+'\n')
            os.system('nohup python upload.py >> nohup.txt 2>&1 &')
        else:
            if len(tar_list)==0:
                progress_monitor('file:'+str(len(file_list))+'\n')
                progress_monitor('file.tar.gz:'+str(len(file_list))+'\n')
                progress_monitor('start: upload...'+'\n')
                print 'file:',len(file_list)
                print 'file.tar.gz:',len(tar_list)
                print 'start: tar_file...',get_now_time()    
                tar_file(file_list)
                print 'over: tar_file',get_now_time()
            else:
                print 'file:',len(file_list)
                print 'file.tar.gz:',len(tar_list)
                left_file=get_left_file(tar_list)
                print 'left file:',len(left_file)
                print 'start: tar_file...',get_now_time()
                tar_file(left_file)
                print 'over: tar_file',get_now_time()
            tar_list=get_tar_list()
            if len(file_list)==len(tar_list):
                print 'file:',len(file_list)
                print 'file.tar.gz:',len(tar_list)
                print 'start: upload...'   
                os.system('nohup python upload.py >> nohup.txt 2>&1 &')
    except Exception,e:
        print e

