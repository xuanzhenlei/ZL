#-*-coding:utf-8-*-
'''
Created on 2015年9月24日

@author: zhengjie
'''
from multiprocessing import Lock, Pool
import re
import time



def start(line):
    info = []
    line = line.strip()
    ebay_id = line.split('\t')[0]
    info.append(ebay_id)
    
    try:
        htmlfile=open('./ebay_html/' + ebay_id + '.html','r')
        html=htmlfile.read()
        
        if html != "" and html != '404 error':
            price=re.search(r'class="notranslate".*?>(.*?)</span>',html)
            if price == None:
                price = re.search(r'class="notranslate".*?>\s+(.*?)</span>',html,re.S)
            if price != None:
                item_price = re.search(r'[0-9]+\.?[0-9]+',price.group(1).replace(',','')).group()
            info.append(item_price)
            
            sold = re.search('<a href=.*?>(.*?) sold</a>',html)
            if sold != None:
                sold = sold.group(1).replace(',','')
            else:
                sold = line.split('\t')[1]
            info.append(sold)
            last_sold = line.split('\t')[1]
            info.append(last_sold)
            url = 'http://www.ebay.com/itm/' + ebay_id
            info.append(url)
            
            image_list = []
            img=re.compile(r'id="vi_main_img_fs" class="fs_imgc"(.*?)</ul>', re.S).search(html)
            if img is not None:
                img_frame = img.group(1).replace('l64','l1600').replace('l500','l1600')
                image_list = re.compile(r'<img src=\"(.*?)"').findall(img_frame)
            else:
                img=re.search(r'itemprop="image" src="(.*?)"',html)
                if img!=None:
                    img=img.group(1).replace('l64','l1600').replace('l500','l1600')
                    image_list.append(img)
            if len(image_list) < 3:
                image_list += ['' for _i in range(3 - len(image_list))]
            info.append(image_list[0])
            info.append(image_list[1])
            info.append(image_list[2])
            
            reg_title = re.search(r'<title>(.*?)</title>', html)
            if reg_title != None:
                title_info=reg_title.group(1)
                title = title_info.replace('&#034;',"\"").replace('&#039;','\'').replace('&amp;','&').replace("&apos;", "").replace("&quot;", " ").replace(" | eBay", "").replace('\t','-')
            info.append(title)
            
            cate_route_ones = re.compile(r'id="vi-VR-brumb-lnkLst".*?<tr>(.*?)</tr>', re.S).search(html)
            if cate_route_ones != None:
                cate_route_ones=cate_route_ones.group(1)
                category = re.findall(r'<span itemprop="name">(.*?)</span></a></li>', cate_route_ones)
            if len(category) < 6:
                category += ['' for _i in range(6 - len(category))]
            info.append(category[0])
            info.append(category[1])
            info.append(category[2])
            info.append(category[3])
            info.append(category[4])
            info.append(category[5])
                
            lock.acquire()
            result_file.write(';'.join(info) + '\n')
            result_file.flush()
            lock.release()
            lock.acquire()
            over_asin_file.write(line + '\n')
            over_asin_file.flush()
            lock.release()
            print info
        else:
            lock.acquire()
            run_asin_file.write(line + '\n')
            run_asin_file.flush()
            lock.release()
        htmlfile.close()
    except Exception,e:
        lock.acquire()
        run_asin_file.write(line + '\n')
        run_asin_file.flush()
        lock.release()
        pass
        print e
        
def create_titles(filename):
    titles = ['ebay_id','price','total_sales','last_sales','url','image1','image2','image3','name','category1','category2','category3','category4','category5','category6']
    f = open(filename,'w')
    f.write(";".join(titles)+"\n")
    f.flush()
    f.close()

def main(file_path):
    global lock,result_file,run_asin_file,over_asin_file
    lock=Lock()
    old_time=time.time()
    create_titles('./result/items.csv')
    result_file=open('./result/items.csv','aw')
    run_asin_file=open('./result/error_asins.txt','w')
    over_asin_file=open('./result/success_asins.txt','w')
    times= time.strftime('%Y-%m-%d %X',time.localtime())
    
    with open('./result/more_twoweeks_sold.csv') as f:
        lines = f.readlines()
    pool=Pool(10)
    pool.map(start,lines)
    pool.close()
    pool.join()
    
    over_asin_file.close()
    run_asin_file.close()
    result_file.close()
    need_time=time.time()-old_time
    print "we need time",len(lines),need_time
    
if __name__ == '__main__':
    main("./ebay_html/")