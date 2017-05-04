#-*-coding:utf-8-*-
import config,time
import os,re,shutil
from datetime import datetime
from common import *
"""
设置压缩文件的前缀：
"""
def configurate():#选择压缩文件前缀
    operation={'get':'1','add':'3','update':'2'}
    location={'cn':'45','us':'1','hk':'92'}
    category_dic={'toys':'220',
            'outdoors':'159043',
            'jewelry':'281',
            'cell_phone':'15032',
            'pets':'1281',
            'camera':'625',
            'home_garden':'11700',
            'clothing':'11450',
            'office':'25298',
            'computers':'58058',
            'video_games':'1249',
            'consumer_elec':'293'}
    for i in range(len(operation.keys())):
        print i+1, operation.keys()[i]
    num_input=raw_input('input number:')
    ope=operation.keys()[int(num_input)-1]
    for i in range(len(location.keys())):
        print i+1,location.keys()[i]
    num_input=raw_input('input number:')
    loc=location.keys()[int(num_input)-1]
    for i in range(len(category_dic.keys())):
        print i+1,category_dic.keys()[i]
    num_input=raw_input('input number:')
    cate=category_dic.keys()[int(num_input)-1]
    print '1','pro'
    print '2','twsc'
    num_input=raw_input('input number:')
    if num_input=='1':
        html='pro'
    if num_input=='2':
        html='twsc'
    pre=ope+'_'+loc+'_'+cate+'_'+html
    return pre 
def update_config(pre):
    f=open('./config.py','r')
    lines=f.readlines()
    f.close()
    f=open('./config.py','w')
    lines[1]="pre="+"'"+pre+"'"+"\n"
    f.writelines(lines)
    f.close()
def get_status():
    file_list=get_file_list()
    tar_list=get_tar_list()
    print 'file:',len(file_list)
    print 'file.tar.gz:',len(tar_list)
if __name__=='__main__':
    try: 
        get_status()
        pre=configurate()
        update_config(pre)
        reload(config)
        print config.pre
        os.system('nohup python tar_file.py > nohup.txt 2>&1 &')
    except Exception,e:
        print e
        