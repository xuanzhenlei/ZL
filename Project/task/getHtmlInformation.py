#!/usr/bin/python
#-*- coding:utf-8 -*-


import urllib2
import json
import sys
import re
import csv
from bs4 import BeautifulSoup
def http_get(url):
    #对系统编码进行默认设置
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #打开路径所对应的文件，并且读取html
    response=urllib2.urlopen(url)
    ret=response.read().decode('utf-8')
    #解析html
    soup=BeautifulSoup(ret,"lxml")
    #取标签ul下的数据
    all=""
    for i in soup.find_all('ul',class_="subject-list"):
        for link in i.find_all('li', class_="subject-item"):
            row_dict = {}
            for l in link.find_all('div',class_='info'):
                row_dict['name']=""
                for m in l.find_all('h2'):
                    bookname=m.get_text()
                    #去掉书名中的换行，与空格
                    bookname1= "".join(bookname.split()).split(',')
                    bookname2 = ''.join(bookname1)
                    #bookname2=bookname1.strip()
                    row_dict['name']=bookname2
                row_dict['author']=""
                row_dict['trans1']=""
                row_dict['trans2']=""
                row_dict['work']=""
                row_dict['publicplace']=""
                row_dict['publicdate']=""
                row_dict['price']=""
                for n in l.find_all('div',class_='pub'):
                    public=n.get_text()
                    publi=public.strip()
                    public1=publi.split("/")
                    if(len(public1)==4):
                        row_dict['author']=public1[0]
                        row_dict['trans1']=""
                        row_dict['trans2']=""
                        row_dict['work']=""
                        row_dict['publicplace']=public1[1]
                        row_dict['publicdate']=public1[2]
                        row_dict['price']=public1[3]
                    elif(len(public1)==7):
                        row_dict['author']=public1[0]
                        row_dict['trans1']=public1[1]
                        row_dict['trans2']=public1[2]
                        row_dict['work']=public[3]
                        row_dict['publicplace']=public1[4]
                        row_dict['publicdate']=public1[5]
                        row_dict['price']=public1[6]
                    elif(len(public1)==5):
                        row_dict['author']=public1[0]
                        row_dict['trans1']=public1[1]
                        row_dict['trans2']=""
                        row_dict['work']=""
                        row_dict['publicplace']=public1[2]
                        row_dict['publicdate']=public[3]
                        row_dict['price']=public1[4]
                    elif(len(public1)==3):
                        row_dict['author']=""
                        row_dict['trans1']=""
                        row_dict['trans2']=""
                        row_dict['work']=""
                        row_dict['publicplace']=public1[0]
                        row_dict['publicdate']=public1[1]
                        row_dict['price']=public1[2]
                row_dict['rating_num']=0
                for o in l.find_all('span',class_='rating_nums'):
                    ppnum=o.get_text()
                    ppnum1=ppnum.strip()
                    row_dict['rating_num']=ppnum1
                row_dict['counts']=0
                for p in l.find_all('span',class_='pl'):
                    count=p.get_text()
                    coun=count.strip()
                    count1=re.sub("\D","",coun)
                    row_dict['counts']=count1
                row_dict['introduction']=""
                for q in l.find_all('p'):
                     introd=q.get_text()
                     intro=introd.strip()
                     row_dict['introduction']=intro
            #allBrands = link.get_text()
            #print allBrands
            #row_dict['name']= allBrands
            #print row_dict
            row_dict['img']=""
            img = link.img.get('src')
            row_dict['img'] = img
            #allBrands += ' %s' %img
            row_str = json.dumps(row_dict,ensure_ascii=False,encoding='utf-8')
            all += row_str+'\n'
        all1=all.replace("\\n",' ')
    return all1

if __name__ == "__main__":
    url = 'https://book.douban.com/tag/%E5%8F%A4%E5%85%B8%E6%96%87%E5%AD%A6?start={page}'
    #新建csv文件用来保存数据
    fo=open('request1.csv','w')
    #对应的路径进行重写,相当与页面进行重写
    for i in range(10):
        #print i,'-'*5
        t_url = url.format(page=i*20)
        #print t_url
        content = http_get(t_url)
        print content
        fo.write(content)
    fo.close()
    #读取以字典格式保存的数据，然后转化为以csv格式保存的数据
    file = open('request1.csv','r')
    file1=open('request1_csv.csv','w')
    lines = file.readlines()
    #为转化后的csv问家添加
    data=["name","img","author","rating_num","price","work","trans1","trans2","introduction","counts","publicplace","publicdate"]
    writer=csv.writer(file1)
    writer.writerow(data)
    for d in lines:
        #将字符串转化为json格式
        d=eval(d)
        #分行写入对应的csv文件中
        file1.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(d['name'],d['img'],d['author'],d['rating_num'],d['price'],d['work'],d['trans1'],d['trans2'],d['introduction'],d['counts'],d['publicplace'],d['publicdate']))
    file1.close()

