#-*-coding:UTF-8-*-
import config,re,os
from multiprocessing import Pool,Lock
from myutil import httptools
import logging
import logging.config
import chardet


logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 

regex_child = re.compile(r'<div class="cat-link">(.*?)</a>')
regex_cate_id = re.compile(r'sch/.*?/(.*?)/')

regex_root_cate_info = re.compile(r"<li itemprop='itemListElement'(.*?)</li>",re.S)
regex_root_cate_id = re.compile(r'<a href=.*?/sch/.*?/(.*?)/')

def get_root_cate_id(html):
    cate_info = regex_root_cate_info.search(html)
    if cate_info != None:
        cate_info = cate_info.group(1)
        cate_id = regex_root_cate_id.search(cate_info)
        if cate_id != None:
            cate_id = cate_id.group(1)
        return cate_id
    else:
        return

def check_leaf_cate_id(cate_id):
    cate_id = cate_id.strip()
    url = config.url.replace('[category]',cate_id)
    for i in range(3):
        html = tool.gethtml(url)
        if html.find('We were unable to run the search you entered. Please try again in a few minutes.') == -1:
            break
    if html.find('We were unable to run the search you entered. Please try again in a few minutes.') != -1:
        logger2.error(cate_id+'\t'+'We were unable to run the search you entered. Please try again in a few minutes.')
        return
    
    root_id = get_root_cate_id(html)
    print root_id,config.root_category_id
    if str(root_id) != config.root_category_id:
        lock.acquire()
        f_wrong.write(cate_id+'\n')
        f_wrong.flush()
        lock.release()
    else:
        lock.acquire()
        f_success.write(cate_id+'\n')
        f_success.flush()
        lock.release()

def handle():
    global tool,lock,f_success,f_wrong
    tool = httptools.httptools()
    lock = Lock()
    f_success = open(config.category_listings_path+'leaf_right.csv','w')
    f_wrong = open(config.category_listings_path+'leaf_wrong.csv','w')
    
    path = config.category_listings_path+'leaf_cate_id.csv'
    f = open(path)
    leaf_list = f.readlines()
    f.close() 
    
    pool = Pool(15)
    pool.map(check_leaf_cate_id,leaf_list)
    pool.close()
    pool.join()
    
    f_success.close()
    f_wrong.close()
"""
"""
if __name__ == '__main__':
    try:
        logger1.info('check_leaf_cate_id.py start...')
        handle()
        logger1.info('check_leaf_cate_id.py over')
    except Exception,e:
        logger2.error(str(e))
