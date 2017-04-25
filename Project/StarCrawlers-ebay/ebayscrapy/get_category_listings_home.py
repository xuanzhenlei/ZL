#/usr/bin/env python
#-*-coding:utf-8-*-
import config,re,os
from multiprocessing import Pool,Lock
from myutil import httptools
import logging
import logging.config

regex_listing = re.compile(r'<span class="listingscnt"\s*>(.*?)</span>')
regex_num = re.compile('[\d,]+')

regex_cate = re.compile(r'<span itemprop="name">(.*?)</span>')

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 


def getLeaf(parentId):
    category=''
    try:
        category=open(config.each_category,'r').read()
    except:
        pass
    p=re.compile(r'\|\|'+str(parentId)+'\t.*')
    s=re.compile(r'(?<=\|\|)\d+')#反向否定预查
    lines = p.findall(category)
    all_id_list = []
    for line in lines:
        cat_ids = s.findall(line) 
        all_id_list.append(cat_ids)
    return all_id_list

def get_listings(leaf,url):#没有解析出listings的html文件记录下来。
    try:
        for i in range(3):
            html = tool.gethtml(url)
            if html.find('We were unable to run the search you entered. Please try again in a few minutes.') == -1:
                break
        cate = regex_cate.search(html)
        if cate != None:
            cate = cate.group(1)
            cate = cate.replace('amp;','')
            if cate != 'Home & Garden':
                lock.acquire()
                f_cate_error.write(url+'\n')
                f_cate_error.flush()
                lock.release()
                return
        else:
            logger2.warning('not analyze cate'+'\n'+url)   
            return
        num = regex_listing.search(html)
        if num != None:
            num = num.group(1)
            num = regex_num.search(num)
            if num != None:
                num = num.group()
                num = num.replace(',','')
                if num != '':
                    return num
        if num == None or num == '':
            lock.acquire()
            f = open(config.category_listings_path+leaf+'_'+str(num)+'.html','w')
            f.write(html)
            f.flush()
            f.close()
            lock.release()
            return 
    except Exception,e:
        logger2.error(url+'\t'+'num:'+str(num)+'\n'+str(e))

def handle(leaf):
    try:
        leaf=leaf[-1]
        cate_url=config.url.replace('[category]',leaf)
        
        num = get_listings(leaf,cate_url)
        if num == None:
            return
        listings_count = int(num)
        
        if listings_count<=9800:#把结果写入文件
            lock.acquire()
            f_less.write(str(listings_count)+'\t'+cate_url+'\n')
            f_less.flush()
            lock.release()
        else:        
            lock.acquire()
            f_more.write(str(listings_count)+'\t'+cate_url+'\n')
            f_more.flush()
            lock.release()
    except Exception,e:
        logger2.error(cate_url+'\t'+'num:'+str(num)+'\n'+str(e))

def get_category_listings():
    global lock,f_less,f_more,tool,f_cate_error
    tool=httptools.httptools()
    lock=Lock()
    leafs=getLeaf(config.root_category_id)
    
    f_less=open(config.category_listings_path+'less_9800.csv','w')
    f_more=open(config.category_listings_path+'more_9800.csv','w')
    f_cate_error = open(config.category_listings_path+'error_cate.csv','w')
    
    pool=Pool(15)
    pool.map(handle,leafs)
    pool.close()
    pool.join()
    
    f_less.close()
    f_more.close()
    f_cate_error.close()

if __name__=='__main__':
    try:
        logger1.info('start get_category_lisitngs...')
        get_category_listings()#得到leaf品类的listings。一个大于9800，一个小于9800.
        logger1.info('over get_category_lisitngs')
#         os.system('nohup python split_more9800.py &')
    except Exception,e:
        logger2.error(str(e))
"""
问题：
1）为什么会出现这个页面？
We were unable to run the search you entered. Please try again in a few minutes
2）有时获取html页面不完整
抓取思路：
1）获取品类id，拼接url
2）获取html页面，解析listings。
    没有解析出listings的页面，保存下来，以品类id命名。
3）将结果写入文件
"""
