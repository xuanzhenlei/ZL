#-*-coding:utf-8-*-
import datetime
import config
import time,re
import logging
import logging.config
from myutil import httptools

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1") #记录跑完的asin
logger2 = logging.getLogger("logger2") #记录错误

regex_listing = re.compile(r'<span class="(rcnt|listingscnt)"\s*>(.*?)</span>')
regex_num = re.compile('[\d,]+')

regex_or = re.compile(r'belong "(him|her)"')

#
if __name__=='__main__':
    a='<span class="rcnt" >66,66,666,66 listings</span>'
    e = '<span class="listingscnt">222 listings</span>'
    b = regex_listing.search(a)
    if b != None:
        b= b.group(2)
        c = regex_num.search(b)
        if c != None:
            c = c.group()
    print b,c
    
    b = regex_listing.search(e)
    if b != None:
        b= b.group(2)
        c = regex_num.search(b)
        if c != None:
            c = c.group()
    print b,c

#     a='it belong "her"'
#     b = regex_or.search(a)
#     if b != None:
#         b = b.group()
#     print b
                    
            
            