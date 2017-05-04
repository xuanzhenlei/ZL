#-*-coding:utf-8-*-
'''
Created on 2016年4月13日

@author: zhengjie
'''
import sys
sys.setrecursionlimit(1000000)
import datetime
import time
import logging.config
import os
import re
# import logging
import random

from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool
import urllib2


logging.config.fileConfig("./log/logging.conf")    # 采用配置文件
logger1 = logging.getLogger("logger1")
logger2 = logging.getLogger("logger2")


class ebay_2week(object):
    '''
    spider for ebay two week sold
    '''
    def __init__(self):
        self.__int_proxy()
        self.__int_file()
        self.__int_heads()


    def __int_proxy(self):
        if os.path.exists('./myutil/proxylist.txt'):
            f=open('./myutil/proxylist.txt')
        else:
            f=open('proxylist.txt')
        self.__proxylist=f.readlines()
        f.close()
        self.dict_proxy = {}
        for pp in self.__proxylist:
            self.dict_proxy[pp.strip()] = {'time':datetime.datetime.now()}

    def __int_file(self):
        self.sold_file = open('./result/twoweeks_sold.csv','aw')
        self.success_file = open('./result/success_ids.txt','aw')
        self.fail_sold = open('./result/fail_get_twoweeks_sold.txt','aw')
        self.captcha_file = open('./result/captcha_ids.txt','aw')

    def __int_heads(self):
        self.__head={}
        self.__cookie="dp1=bexpt/00014627796311545820d8af^pcid/451496644591ce9cc^bl/US5afe1d4c^pbf/%232001804e000e000108180c2000004591ce9cc^kms/in5afe1d4c^mpc/0%7C0591ce9cc^tzo/-1e0573bc45c^exc/0%3A0%3A2%3A25763434c^u1p/emhlbmdqaWVfOQ**591ce9cc^idm/1573bbb5b^u1f/jj591ce9cc^; nonsession=BAQAAAVSS0DFjAAaAABAAClkc6cx6aGVuZ2ppZV85AEAAClkc6cx6aGVuZ2ppZV85APMAIlkc6cwkMiRVYVl0TlRnOSQyNDhjWHBJTTI1cTFITjZGZkMzcjcxADMAC1kc6cxkZWZhdWx0LFVTQQAEAApZEXLBemhlbmdqaWVfOQFkAAJZHOnMIzkACAAcV2NDTDE0NjM1MzEwODJ4MjIxODc5MzIwNTIzeDB4Mk4AygAgYKG3zDhkYjRjYjcyMTUwMGFiYzAyMWYyYzY5N2ZmZWNkOTMwAKoAAVkc6cwwAMsAAlc7vVQzNACcADhZHOnMblkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2QUFsSXVnRHBLRG9nMmRqNng5blkrc2VRPT0AnQAIWRzpzDAwMDAwMDAxKTsi0pOonV2R7wdo9/lUhGMZY9s*; npii=bcguid/8db4d4b91500a5f145108350fb97206b591ce9cb^tguid/8db4cb721500abc021f2c697ffecd930591ce9cb^; lucky9=9994802; ns1=BAQAAAVSS0DFjAAaAANgAZVkc6cxjOTd8NjAxXjE0NTM2ODg0NTYzNjJeZW1obGJtZHFhV1ZmT1E9PV4wXjN8Mnw1fDR8N3w0Mnw0M3wxMHwxMV4yXjReNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NQClAA1ZHOnMMTQ0OTE2MjEzMS8wO9iK1NiJ8dme0h3aMbUwPoV4NDcC; cid=F95qdlRn3qiUzKsi%23451496644; shs=BAQAAAVSS0DFjAAaAAVUADlkRcsE2OTc3MDQ1MTkwMDgsMvrQDrZ0cl+EWkpqRvaF2t7t22/K; JSESSIONID=4280F3078C2081976095CBAA6AD63B44; ds1=ats/0; ebay=%5EsfLMD%3D0%5Esbf%3D%2361c000000000b0000100214%5Ecos%3D2%5Ecv%3D15555%5Esin%3Din%5Ejs%3D1%5Edv%3D573bb646%5Epsi%3DAQBGBdEI*%5E; cssg=b6d69e881540a78dac4268bdfffdd4cf; s=BAQAAAVSS0DFjAAWAAPgAIFc9B8xiNmQ2OWU4ODE1NDBhNzhkYWM0MjY4YmRmZmZkZDRjZgFFAAhZHOnMNTczMDNlZTFGDh807LHRZ7bbsWKo0H1VAIkjlA**; lzstat_ss=1228062739_2_1463239639_3420969; lzstat_uv=5702910541520178162|3420969; ds2=sotr/b7pwxzzzzzzz^ssts/1463531093261^"
        self.__head['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self.__head['Accept-Language']='en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        self.__head['Connection']='keep-alive'
        self.__head['Cookie']=self.__cookie
        self.__head['Host']='www.ebay.com'
        self.__head['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'


    def get_proxy(self):
        '''
        get proxy ID
        :return: str id:port
        '''

        for k in self.dict_proxy:
            gp_time = datetime.datetime.now() - self.dict_proxy[k]['time']
            if gp_time.seconds > random.randint(10, 20):
                self.dict_proxy[k]['time'] = datetime.datetime.now()
#                 print self.dict_proxy[k]['time'],k
                return k
        time.sleep(1)
        return self.get_proxy()

    def update_proxy(self,key):
        self.dict_proxy[key]['time'] = datetime.datetime.now()

    def gethtmlproxy(self,url,proxy,data=None,heads=None):
        '''
        get url html
        '''
        if not heads:
            heads=self.__head
        else:
            heads={}
        count=0
        while True:
            try:
                proxy_support = urllib2.ProxyHandler({'http':'http://'+proxy})
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
                urllib2.install_opener(opener)
                req=urllib2.Request(url,data,heads)
                res=urllib2.urlopen(req,timeout=30)
                content=res.read()
                count+=1
                if -1== content.find('Enter a verification code to continue') or count > 5:
                    return content
                proxy = self.get_proxy()
            except Exception,e:
                print e
                count+=1
                if count>5:
                    return ''
                proxy = self.get_proxy()

    def getDaysByNum(self,num):
        '''
        get date list
        '''
        today=datetime.date.today()
        oneday=datetime.timedelta(days=1)
        li=[]
        for i in range(0,num):
            today=today-oneday
            date = today.strftime('%b-%d-%y')
            li.append(str(date))
        return li

    def handle(self,line):
        try:
            ebay_id = line.strip()
            info = []
            info.append(ebay_id)
            url='http://offer.ebay.com/ws/eBayISAPI.dll?ViewBidsLogin&item=' + ebay_id
            proxy = self.get_proxy()
            html=self.gethtmlproxy(url,proxy)
            if html == '' or -1 != html.find('Enter a verification code to continue'):
                self.captcha_file.write(line)
                self.captcha_file.flush()
                return
            dates = self.getDaysByNum(14)
            count = 0
            results = re.findall('class="contentValueFont">.*?<td align="middle".*?class="contentValueFont">(.*?)</td><td align="left".*?class="contentValueFont">(.*?)\s.*?</td>',html)
            if results != []:
                for res in results:
                    for date in dates:
                        if res[1] == date:
                            count += int(res[0].replace(',',''))
                info.append(str(count))
                print info
                self.sold_file.write('\t'.join(info) + '\n')
                self.sold_file.flush()
                self.success_file.write(line)
                self.success_file.flush()
            else:
                self.fail_sold.write(line)
                self.fail_sold.flush()
        except Exception,e:
            logger2.error(ebay_id+'\t'+str(e))

    def get_sold(self):
        '''
        main method
        :return: None
        '''
        pool = Pool(100)
        with open('./result/pets_ids.txt','r') as f:
            lines = f.readlines()
        pool.map(self.handle,lines)

        self.sold_file.close()
        self.success_file.close()
        self.fail_sold.close()
        self.captcha_file.close()

if __name__=='__main__':
    try:
        logger1.info('start get_sold.py...')
        print datetime.datetime.now()
        week = ebay_2week()
        week.get_sold()
        print datetime.datetime.now()
        logger1.info('over get_sold.py')
    except Exception,e:
        logger2.error(str(e))
