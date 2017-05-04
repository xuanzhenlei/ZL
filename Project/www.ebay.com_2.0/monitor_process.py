#/usr/bin/env python
#-*-coding:utf-8-*-
from multiprocessing import Pool,Lock
from myutil import httptools
import config
from myutil.logtool import logtool
import os,re
from common import *

def get_result():
    try:
        command1='cat '+config.check_result_path+'process_record.txt'
        result1=os.popen(command1).read()
        print result1
        command2='wc -l '+config.get_ids_path+'pro_ids.csv'
        result2=os.popen(command2).read()
        print 'pro_ids.csv:',result2
        print 'ids_FromProHtmlFile.txt',len(os.listdir(config.pro_html_file_path))
        command3='wc -l '+config.pro_html_path+'SellCountMore0_ids.csv'
        result3=os.popen(command3).read()
        print 'SellCountMore0_ids.csv',result3
        command4='wc -l '+config.pro_html_path+'ids_FromProHtml.txt'
        result4=os.popen(command4).read()
        print 'count ids_FromProHtml.csv:',result4
    except:
        pass

if __name__=='__main__':
    try:
        write_content('start check_process.py:\t'+get_now_time())
        get_result()
        write_content('over check_process.py:\t'+get_now_time())
    except Exception,e:
        print e
        write_content('error:\t'+str(e))