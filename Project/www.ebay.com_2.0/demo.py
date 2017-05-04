#coding:utf8
'''
Created on 2016年4月13日

@author: zhengjie
'''
import datetime
import re
import urllib2

from myutil import httptools


def getDaysByNum(num):  
    today=datetime.date.today()  
    oneday=datetime.timedelta(days=1)      
    li=[]       
    for i in range(0,num):   
        today=today-oneday
        date = today.strftime('%b-%d-%y')   
        li.append(str(date))  
    return li  

def get_html(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'}
        req = urllib2.Request(url,headers=headers)  
        resp = urllib2.urlopen(req, timeout=10)
        html = resp.read()
        return html
    except Exception as e:
        get_html(url)
        print e

if __name__ == '__main__':
#     dates = getDaysByNum(14)
#     count = 0
#     url = 'http://offer.ebay.com/ws/eBayISAPI.dll?ViewBidsLogin&item=221494188545'
#     html = httptools.httptools().gethtmlproxy(url)
#     results = re.findall('class="contentValueFont">.*?<td align="middle".*?class="contentValueFont">(.*?)</td><td align="left".*?class="contentValueFont">(.*?)\s.*?</td>',html)
#     for res in results:
#         print res
#         for date in dates:
#             if res[1] == date:
#                 count += int(res[0])
#     print count
    
    url = 'http://www.ebay.com/itm/272233439470'
    html = httptools.httptools().gethtml(url)
#     with open('1.html','w') as h:
#         h.write(html)
#         html =h.read()
    price=re.search(r'class="notranslate".*?>(.*?)</span>',html)
    if price == None:
        price = re.search(r'class="notranslate".*?>\s+(.*?)</span>',html,re.S)
    if price != None:
        item_price = re.search(r'[0-9]+\.?[0-9]+',price.group(1).replace(',','')).group()
    print item_price
    
    sold = re.search('<a href=.*?>(.*?) sold</a>',html).group(1).replace(',','')
    print sold
    
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
    print image_list[0]
    print image_list[1]
    print image_list[2]
    
    reg_title = re.search(r'<title>(.*?)</title>', html)
    if reg_title != None:
        title_info=reg_title.group(1)
        title = title_info.replace('&#034;',"\"").replace('&#039;','\'').replace('&amp;','&').replace("&apos;", "").replace("&quot;", " ").replace(" | eBay", "").replace('\t','-')
    print title
    
    cate_route_ones = re.compile(r'id="vi-VR-brumb-lnkLst".*?<tr>(.*?)</tr>', re.S).search(html)
    if cate_route_ones != None:
        cate_route_ones=cate_route_ones.group(1)
        category = re.findall(r'<span itemprop="name">(.*?)</span></a></li>', cate_route_ones)
    if len(category) < 6:
        category += ['' for _i in range(6 - len(category))]
    print category[0]
    print category[1]
    print category[2]
    print category[3]
    print category[4]
    print category[5]