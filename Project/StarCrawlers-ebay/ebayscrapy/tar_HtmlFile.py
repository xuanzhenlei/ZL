#-*-coding:utf-8-*-
import config,time
import os,re,shutil
from datetime import datetime

num_regx=re.compile('\d+$')

def get_now_time():#获取当前时间，返回字符型时间如：20151020 11:20:30
    now=datetime.now()
    now_list=str(now).split('.')
    now_time=now_list[0]
    return now_time
def num_legal(num_input,max):
    if num_input=='':
        exit()
    if int(num_input) in range(1,max+1):
        return 1
    else:
        return 0
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
    pre=ope+'_'+loc+'_'+cate
    print pre 
    return pre 
def del_tar():
    tar_list=get_tar_list()
    command="awk '{print $1}' upload_history.csv|wc -l"
    rows=os.popen(command).read()
    if int(rows.strip())==len(tar_list):
        for name in tar_list:
            command='rm -rf '+name
            os.system(command)
def upload():
    print 'start uplocad file...',get_now_time()
    command='python s3_uplocad.py'
    os.system(command)
    print 'over upload',get_now_time()
def del_file():
    print 'start: del file'
    file_list=get_file_list()
    print 'file:',len(file_list)
    tar_list=get_tar_list()
    print 'file.tar.gz:',len(tar_list)
    if len(file_list)==len(tar_list):
        for name in file_list:
            command='rm -rf '+name
            os.system(command)
        print 'over: del file'
    else:
        exit()
def tar_file():#进行压缩或者上传
    file_list=get_file_list()
    print 'file:',len(file_list)
    tar_list=get_tar_list()
    print 'file.tar.gz:',len(tar_list)
    print '1 tar file'
    print '2 upload tar_file'
    num_input=raw_input('input number:')
    if num_legal(num_input,2)==0:
        exit()
    else:
        if num_input=='1':
            pre=configurate()
            print 'start tar...',get_now_time()
            for name in file_list:
                command='tar -czf '+pre+'_'+name+'.tar.gz '+name
                os.system(command)
            print 'over tar',get_now_time()
        else:
            print 'del tar...',get_now_time()
            del_tar()
            print 'over del tar',get_now_time()
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
if __name__=='__main__':
    try:    
        tar_file()
        del_file()
        upload()
        del_tar()
    except Exception,e:
        print e

