#/use/bin/env python
#coding:utf-8
'''
httptools by snike
'''
import urllib2,cookielib
import os,zlib
import logging as httplog
import random
from gzip import GzipFile
from StringIO import StringIO
from logtool import logtool
from cgitb import html
httplog=logtool('httplog','http.log')
class httptools:

    def __init__(self):
        self.__head={}
        self.__cookie="dp1=bexpt/00014627796311545820d8af^pcid/451496644591cf371^bl/US5afe26f1^pbf/%232001804e000e000108180c2000004591cf371^kms/in5afe26f1^mpc/0%7C0591cf371^tzo/-1e0573bce01^exc/0%3A0%3A2%3A257634cf1^u1p/emhlbmdqaWVfOQ**591cf371^idm/1573d0eac^u1f/jj591cf371^; nonsession=BAQAAAVSS0DFjAAaAABAAClkc83F6aGVuZ2ppZV85AEAAClkc83F6aGVuZ2ppZV85APMAIlkc83EkMiRVYVl0TlRnOSQyNDhjWHBJTTI1cTFITjZGZkMzcjcxADMAC1kc83FkZWZhdWx0LFVTQQAEAApZEXLBemhlbmdqaWVfOQFkAAJZHPNxIzkACAAcV2NM8TE0NjM1MzM1NTF4MzAxOTU2ODU1NTY2eDB4Mk4AygAgYKHBcThkYjRjYjcyMTUwMGFiYzAyMWYyYzY5N2ZmZWNkOTMwAKoAAVkc83EwAMsAAlc7xvk1NgCcADhZHPNxblkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2QUFsSXVnRHBLRG9nMmRqNng5blkrc2VRPT0AnQAIWRzzcTAwMDAwMDAx8QWLacRa1s0Oih8U07t6GHE6+lw*; npii=btguid/8db4cb721500abc021f2c697ffecd930591cf33b^cguid/8db4d4b91500a5f145108350fb97206b591cf33b^; lucky9=9994802; ns1=BAQAAAVSS0DFjAAaAANgAZVkc83FjOTd8NjAxXjE0NTM2ODg0NTYzNjJeZW1obGJtZHFhV1ZmT1E9PV4wXjN8Mnw1fDR8N3w0Mnw0M3wxMHwxMV4yXjReNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NQClAA1ZHPNxMTQ0OTE2MjEzMS8wO8zfN6VHes+ZSNN4iewlkmCeMTL9; cid=F95qdlRn3qiUzKsi%23451496644; shs=BAQAAAVSS0DFjAAaAAVUADlkRcsE2OTc3MDQ1MTkwMDgsMvrQDrZ0cl+EWkpqRvaF2t7t22/K; JSESSIONID=4D5A4C099103951ED50BA7EE7261C6C1; ds1=ats/0; ebay=%5EsfLMD%3D0%5Esbf%3D%2341c000000000b0000100214%5Ecos%3D2%5Ecv%3D15555%5Esin%3Din%5Ejs%3D1%5Edv%3D573bb646%5E; cssg=8db4cb721500abc021f2c697ffecd930; s=BAQAAAVSS0DFjAAWAAPgAIFc9EXE4ZGI0Y2I3MjE1MDBhYmMwMjFmMmM2OTdmZmVjZDkzMAFFAAhZHPNxNTczMDNlZTEA7gBUVz0RcTE0Bmh0dHA6Ly93d3cuZWJheS5jb20vcC9zYW1zdW5nLTg1MC1ldm8tMjUwZ2ItZXh0ZXJuYWwtbXotNzVlMjUwYi1hbS1zc2QvMjE2MTMxOTkyB6Gld4Em4H/so4d8mZOInOFjRfyr; lzstat_ss=1228062739_2_1463239639_3420969; lzstat_uv=5702910541520178162|3420969; ds2=ssts/1463533558788^"
        self.__head['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self.__head['Accept-Language']='en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        self.__head['Connection']='keep-alive'
#         self.__head['Cookie']=self.__cookie
        self.__head['Host']='www.ebay.com'
        self.__head['User-Agent']='Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'#'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        self.__proxylist=None
    def gethtml(self,url,data=None,heads='FHBJ<KGFYOLL',gzip_page=False,set_cookie=False):
        if heads=='FHBJ<KGFYOLL':
            heads=self.__head
        if not heads:
            heads={}
        content=''
        count=0
        heads={}
        if gzip_page:
            heads['Accept-Encoding'] = "gzip"
        if set_cookie:
            heads['Cookie'] = self.__cookie
        while True:
            try:
                req=urllib2.Request(url,data,{})
                content=urllib2.urlopen(req,timeout=10).read()
#                 print 'success:',url
                return content
            except Exception,e:
                httplog.info(e)
                if "404" in str(e):
                    print '404',url
#                     return str(e)
                    return '404 error'
                count+=1
                print e,url,'crawl once more:'+str(count)
                if count==6:
#                     return str(e)
                    return ''
                
    def sgethtml(self,url):
        return self.gethtml(url,None,None)
    #抓取图片
    def get_img(self,url):
        heads = {"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        req = urllib2.Request(url,None,{})
        img_String = urllib2.urlopen(req).read()
        return img_String
        
    def gethtmlproxy(self,url,data=None,heads='FHBJ<KGFYOLL'):
        if not self.__proxylist:
            if os.path.exists('./myutil/proxylist.txt'):
                f=open('./myutil/proxylist.txt')
            else:
                f=open('proxylist.txt')
            self.__proxylist=f.readlines()
            f.close()
#         proxy_support = urllib2.ProxyHandler({'http':'http://'+random.choice(self.__proxylist)})
        if heads=='FHBJ<KGFYOLL':
            heads=self.__head
        if not heads:
            heads={}
        count=0
        while True:
            try:
                proxy_support = urllib2.ProxyHandler({'http':'http://'+random.choice(self.__proxylist)})
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)  
                req=urllib2.Request(url,data,{})
                res=urllib2.urlopen(req,timeout=30)
                content=res.read()
                if -1== content.find('Enter a verification code to continue') or count > 5:
                    count+=1
                    return content
            except Exception,e:
                print e
#                 httplog.info(e)
#                 if "404" in str(e):
# #                     return str(e) 
#                     return '404 error'    
                count+=1
                if count==6:
                    return ''
    def sgethtmlproxy(self,url):
        return self.gethtmlproxy(url,None,None)
if __name__=='__main__':
    tool=httptools()
#     html=tool.sgethtml('http://blog.ii8go.com/asdsadasdasdsa')
#     with open('test.html','w') as f:
#         f.write(html)
    html=tool.get_img('http://i.ebayimg.com/00/s/ODAwWDgwMA==/z/-kcAAOSw7aBVCWZu/$_14.JPG')
    print html
