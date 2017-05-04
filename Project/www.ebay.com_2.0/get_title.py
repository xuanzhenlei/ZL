#*-coding:utf-8-*-
import os
import re
import time

from multiprocessing import Lock, Pool


def get_title(asin,html):
    if asin!=None:
        asin=asin
        
    title = ''    
    reg_title = re.search(r'etafsharetitle="(.*?)"\n', html)#标题
    if reg_title!=None:
        title=reg_title.group(1)
    info = {asin:title}
    
    return info 


def start(filename):
    
    asin=filename.split('.')[0]
    try:
        htmlfile=open('./result/get/cn/office/get_pro_html/office_ProHtmlFile/'+filename,'r')
        html=htmlfile.read()

        
        if html != "" and html != '<urlopen error [Errno -2] Name or service not known>':
            item=get_title(asin,html)
            print item
            lock.acquire()
            result_file.write(str(item)+'\n')
            result_file.flush()
            lock.release()
            lock.acquire()
            over_asin_file.write(asin+'\n')
            over_asin_file.flush()
            lock.release()
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
    result_file=open('./result/title_info.txt','w')
    run_asin_file=open('./result/fail_ids.txt','w')
    over_asin_file=open('./result/success_ids.txt','w')
    times= time.strftime('%Y-%m-%d %X',time.localtime())
    filenames=os.listdir(file_path)
    pool=Pool(100)
    pool.map(start,filenames)
    pool.close()
    pool.join()
    
    over_asin_file.close()
    run_asin_file.close()
    result_file.close()
    need_time=time.time()-old_time
    print "we need time",len(filenames),need_time  
                                      
if __name__=="__main__":
    main("./result/get/cn/office/get_pro_html/office_ProHtmlFile/")
    
