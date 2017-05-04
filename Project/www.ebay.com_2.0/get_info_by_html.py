#-*-coding:utf-8-*-
'''
Created on 2015年9月24日

@author: zhengjie
'''
import StringIO
import gzip
from multiprocessing import Lock, Pool
import os
import time

from get_ebay_info_new import get_info


def start(filename):
    
    asin=filename.split('.')[0]
    try:
        htmlfile=open('./result/get/cn/home_garden/get_pro_html/home_garden_ProHtmlFile/'+filename,'r')
        content=htmlfile.read()
        try:
            data = StringIO.StringIO(content)
            gz = gzip.GzipFile(fileobj=data)
            html = gz.read()
            gz.close()
        except:
            html = content

        
        if html != "" and html != '<urlopen error [Errno -2] Name or service not known>':
            item=get_info(asin,html)
            print item['name']
#             items_list=get_info(asin,html)
#             for items_info1 in items_list:
#                 items_info=items_info1
#                 print items_info
            lock.acquire()
            result_file.write(str(item)+'\n')
            result_file.flush()
            lock.release()
            lock.acquire()
            over_asin_file.write(asin+'\n')
            over_asin_file.flush()
            lock.release()
#         print items_info
        else:
            lock.acquire()
            run_asin_file.write(asin+'\n')
            run_asin_file.flush()
            lock.release()
        htmlfile.close()
    except Exception,e:
        lock.acquire()
        run_asin_file.write(asin+'\n')
        run_asin_file.flush()
        lock.release()
        pass
        print e
        
def main(file_path):
    global lock,result_file,run_asin_file,over_asin_file
    lock=Lock()
    old_time=time.time()
    result_file=open('./result/items_finally.txt','w')
    run_asin_file=open('./result/run_asins.txt','w')
    over_asin_file=open('./result/over_asins.txt','w')
    times= time.strftime('%Y-%m-%d %X',time.localtime())
    filenames=os.listdir(file_path)
    pool=Pool(30)
    pool.map(start,filenames)
    pool.close()
    pool.join()
    
    over_asin_file.close()
    run_asin_file.close()
    result_file.close()
    need_time=time.time()-old_time
    print "we need time",len(filenames),need_time
    
if __name__ == '__main__':
    main("./result/get/cn/home_garden/get_pro_html/home_garden_ProHtmlFile/")
