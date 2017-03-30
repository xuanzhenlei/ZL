#!/usr/bin/python
#-*- coding:utf-8 -*-

# from urllib3 import request.Request
# import http.cookiejar

#url='https://book.douban.com/tag/%E5%8F%A4%E5%85%B8%E6%96%87%E5%AD%A6'
# response=urllib.request.urlopen(url)
# code=response.getcode()
# html=response.read()
# mystr=html.decode("utf8")
# response.close()
# print mystr


# req=request.Request(url)
# with request.urlopen(req) as f:
#     print ('Status',f.status,f.reason)
#     for k,v in f.getheaders():
#         print ('%s:%s'%(k.v))
#     print('Data:',f.read().decode('utf8'))



# import urllib2
# import re
#
# def main():
#     url='https://book.douban.com/tag/%E5%8F%A4%E5%85%B8%E6%96%87%E5%AD%A6'
#     req=urllib2.Request(url)
#     resp=urllib2.urlopen(req)
#     respHtml=resp.read()
#     print "respHtml=",respHtml
#     foundH1user=re.search('(?i)<meta\s?http-equiv="Content-Type"\s?content="text/html;\s?charset=(.+?)"\s?.?>', respHtml)
#     print "foundH1user=",foundH1user
#     if(foundH1user):
#         h1user=foundH1user.group(1)
#         print "h1user=",h1user
# if __name__=="__main__":
#     main()

#test-successful

# import urllib2
# import json
# import sys
# from bs4 import BeautifulSoup
#
# def http_get():
#     url='https://book.douban.com/tag/%E5%8F%A4%E5%85%B8%E6%96%87%E5%AD%A6'
#     #url='https://book.douban.com/tag/%E5%8F%A4%E5%85%B8%E6%96%87%E5%AD%A6?start=20&type=T'
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
#     response=urllib2.urlopen(url)
#     ret=response.read()
#     #print ret
#     soup=BeautifulSoup(ret,"lxml")
#     for i in soup.find_all('ul',class_="subject-list"):
#         all=""
#         for link in i.find_all('li', class_="subject-item"):
#             allBrands =all+link.get_text()
#             img = link.img.get('src')
#             #allBrands += ' %s' %img
#             all=allBrands+img
#         toJson=json.dumps(all,ensure_ascii=False,encoding='utf-8')
#         rttoJson=toJson.replace("\\n"," ")
#         return rttoJson
# if __name__ == "__main__":
#     print http_get()
#     fo=open('request.csv','w')
#     fo.write(http_get())
#     fo.close()


import urllib2
import json
import sys
import re
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
            allBrands = link.get_text()
            #print allBrands
            row_dict['name']= allBrands
            #print row_dict
            img = link.img.get('src')
            row_dict['img'] = imgS
            #allBrands += ' %s' %img
            row_str = json.dumps(row_dict,ensure_ascii=False,encoding='utf-8')
            all += row_str
            all1=all.replace("\\n",' ')

            #show=re.split(r'\s+',str)
            # all=allBrands+img
    toJson=json.dumps(all1,ensure_ascii=False,encoding='utf-8')
    #rttoJson=toJson.replace("\\n"," ")
    #rttoJson = all
    rttoJson=toJson
    return all1

if __name__ == "__main__":
    url = 'https://book.douban.com/tag/%E5%8F%A4%E5%85%B8%E6%96%87%E5%AD%A6?start={page}'
    #新建csv文件用来保存数据
    fo=open('request.csv','w')
    #对应的路径进行重写,相当与页面进行重写
    for i in range(50):
        #print i,'-'*5
        t_url = url.format(page=i*20)
        #print t_url
        content = http_get(t_url)
        print content
        fo.write(content)
    fo.close()