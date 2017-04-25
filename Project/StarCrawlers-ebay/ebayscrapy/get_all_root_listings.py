#/usr/bin/env python
#-*-coding:utf-8-*-
from myutil import httptools
import config
import re
from common import *
from multiprocessing import Lock,Pool
    
def handle(cate_id):
    root_url=config.url.replace('[category]',cate_id)
    for k in config.category_dic.keys():
        if config.category_dic[k]==cate_id:
            break
    listings_count=get_listings(tool,root_url)
    lock.acquire()
    f.write(listings_count+'\t'+k+'\n')
    f.flush()
    lock.release()
def get_root_listings():
    global f,lock,tool
    tool=httptools.httptools()
    lock=Lock()
    cate_id_list=config.category_dic.values()
    f=open('./result/root_listing.txt','w')
    pool=Pool(20)
    pool.map(handle,cate_id_list)
    pool.close()
    pool.join()
    f.close()
    
if __name__=='__main__':
    try:
        get_root_listings()
    except Exception,e:
        print e

