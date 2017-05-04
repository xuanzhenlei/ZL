#coding=utf8

import boto
import copy
import os
import Queue
import random
import re
import hashlib
import threading
import math
import time
import urllib2
import urllib
import gzip
import StringIO
import cookielib
import tarfile
import pytz
import requests


from datetime import datetime
from filechunkio import FileChunkIO

class Work(threading.Thread):
    """

    """
    def __init__(self, work_queue, result_queue, flag, lock, condition):
        threading.Thread.__init__(self)
        self._flag = flag
        self._lock = lock
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.wait = True
        self._condition = condition

    def run(self):
        #Dead cycle, to create threads under certain conditions close to exit
        while self._flag["flag"]:
            self._lock.acquire()
            if  self.work_queue.qsize() > 0:
                do = None
                args = None
                do, args = self.work_queue.get()
                #The task asynchronous dequeue, Queue internal implementation of the synchronization mechanism
                self._lock.release()
                try:
                    temp_result = do(args)
                    self.result_queue.put(temp_result)
                except Exception, e:
                    print "Unkown Exception", e
                    print str(do), str(args)
                    self.result_queue.put(None)
            else:
                self._lock.release()
                self._condition.acquire()
                self._condition.wait()
                self._condition.release()

class PoolManager(object):
    """

    """

    def __init__(self, threads_number=2):
        self.threads = []
        self._flag = {"flag" : True}
        self.work_queue = Queue.Queue()
        self.work_num = 0
        self.result_queue = Queue.Queue()
        self._threadLock = threading.Lock()
        self._condition = threading.Condition()
        self.__init_thread_pool(threads_number)

    def __init_thread_pool(self, threads_number):
        '''
        Initialization thread function
        '''
        self.threads = []
        for i in range(threads_number):
            tempthreand = Work(self.work_queue, self.result_queue, self._flag, self._threadLock, self._condition)
            self.threads.append(tempthreand)
            tempthreand.start()

    def addJob(self, func, args):
        for arg in args:
            self.work_queue.put((func, arg))
            self.work_num = self.work_num + 1

        self.notify_all()


    def map(self, func, args):
        """
        Add a working team
        """
        for arg in args:
            self.work_queue.put((func, arg))#task enqueue, Queue internal synchronization mechanism
            self.work_num = self.work_num + 1

        self.notify_all()

        self.wait_jobscomplete()

        return self.getResult()

    def close(self):
        for t in self.threads:
            t._flag["flag"] = False

        self.notify_all()

        self.threads = []

    def getResult(self):
        result = []
        while self.result_queue.qsize() > 0:
            temp = self.result_queue.get()
            self.work_num = self.work_num - 1
            result.append(temp)
        return result

    def wait_jobscomplete(self):
        i = 0
        while True and i<10:
            if self.work_num == self.result_queue.qsize():
                return 1
            else:
                time.sleep(60)

    def notify_all(self):
        self._condition.acquire()
        self._condition.notify_all()
        self._condition.release()

    def wait_allcomplete(self):
        """
        Wait for all threads to finish
        """
        for item in self.threads:
            if item.isAlive():
                item.join()

    def activateFlag(self):
        '''
        all work are added into queue,
        After threads have finished all work, the threads will stop
        '''
        self._flag["flag"] = True


def get_list_random(list_value):
    """
    :param list_value:原数组
    :return:数组的一个随机值
    """
    temp_index = random.randint(0, len(list_value) - 1)
    return list_value[temp_index]

def save_as_file(file_name, file_str):
    """
    :param name:需要保存的文件名
    :param file_str:文件內容
    :return:无返回值
    """
    with open(file_name, 'w') as temp_file:
        temp_file.write(file_str)

def get_url_html(url, proxy=None, header={}, html_type='html'):
    """
    :param url:抓取网页的url链接
    :param proxy: 是否是代理，如果是，则是代理的地址信息
    :return:返回html信息，里面具体内容则需要自己解析
    """
    # header_list = [{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},]
    # header =  header_list[0]

    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())

    if proxy:
        proxy_head = urllib2.ProxyHandler({'http':'http://' + proxy})
        opener = urllib2.build_opener(proxy_head, cookie_support, urllib2.HTTPHandler)
    else:
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

    urllib2.install_opener(opener)

    if header:
        req = urllib2.Request(url, None, header)
    else:
        req = urllib2.Request(url)

    try:
        content_gz = urllib2.urlopen(req, timeout=5).read()
        if header and header['Accept-Encoding'] == 'gzip' and html_type == 'html':
            data = StringIO.StringIO(content_gz)
            gz = gzip.GzipFile(fileobj=data)
            content = gz.read()
            gz.close()
        else:
            content = content_gz
        code_str = '<title dir="ltr">Robot Check</title>'
        if content.find(code_str) != -1:
            return 'rebot', 'Robot Check'
        else:
            return 'success', content
    except Exception, e:
        return 'failed', str(e)



def save_image_by_file(file_name):
    """
    :param file_name:保存image_url_name的文件
    :return:
    """

    url_image_list = []
    image_feilds  = ['image_name', 'image_url', 'image_size']
    with open(file_name, 'r') as temp_image_file:
        lines = temp_image_file.readlines()
        for line in lines:
            image_url_name_lit =  line.split('\t')
            url_image_list.append({'image_name' : image_url_name_lit[0].strip(''), 'image_url' : image_url_name_lit[1], 'image_size' : 0})

    os.rename(file_name,file_name+'.download')

    i = 0
    # threadpool = PoolManager(10)
    for url_image_dict in url_image_list:
        i = i + 1
        if i % 10 == 1:
            print 'download image file:', i
        try:
            image_size = urllib.urlretrieve(url_image_dict['image_url'], url_image_dict['image_name'])
        except Exception as e:
            image_size = '0'
        url_image_dict['image_size'] = str(image_size)

    #     threadpool.addJob(download_image, [url_image_dict])
    #
    # threadpool.wait_jobscomplete()
    # threadpool.getResult()
    # threadpool.close()

    with open(file_name + '.download_status', 'w') as temp_image_file:
        temp_image_file.write('\t'.join(image_feilds) + '\n')
        for url_image in url_image_list:
            image_line = [url_image[image_feild] for image_feild in image_feilds]
            temp_image_file.write('\t'.join(image_line) + '\n')

    print 'start download image'

def test_save_html(url):
    import urllib
    import urllib2
    import requests

    print 'start urlretrieve:',datetime.now(pytz.UTC).strftime('%T')
    i = 0
    while i< 1000:
        urllib.urlretrieve(url, "test.img")
        i = i +1

    print 'start urlopen:',datetime.now(pytz.UTC).strftime('%T')
    i = 0
    while i< 1000:
        f = urllib2.urlopen(url)
        data = f.read()
        with open("test.img", "wb") as code:
            code.write(data)
        i = i +1

    print 'start requests:',datetime.now(pytz.UTC).strftime('%T')
    i = 0
    while i< 1000:
        r = requests.get(url).content
        with open("test.img", "wb") as code:
             code.write(r)
        i = i +1



def tar_file(fname):
    """
    :param fname:需要压缩的文件夹名称
    :return:无返回值
    """
    with tarfile.open(fname + ".tar.gz", "w:gz") as t:
        for root, dir, files in os.walk(fname):
            print root, dir, files
            for file in files:
                fullpath = os.path.join(root, file)
                t.add(fullpath)


def tar_gz_files(fpath, relative=True, f_name_pre=None):
    """
    :param fpath:文件目录
    :return:返回文件list
    """
    file_list = []
    for root, dirs, files in os.walk(fpath):
        if root == fpath:
            continue
        print 'Tar and GZ file:',root
        if 'csv' in dirs:
            dirs.remove('csv')
        if 'image' in dirs:
            dirs.remove('image')
        if files:
            tar_file_name = root.replace(os.getcwd()+os.sep,'') if relative else os.path.join(root)
            tar_file_name = tar_file_name if not f_name_pre else f_name_pre + '_' + tar_file_name
            with tarfile.open(tar_file_name + ".tar.gz", "w:gz") as tar_file:
                for file_temp in files:
                    if file_temp.split('.')[-1] in ['csv']:
                        continue
                    fullpath = os.path.join(root, file_temp).replace(os.getcwd()+os.sep,'') if relative else os.path.join(root, file_temp)
                    tar_file.add(fullpath)
            for file_temp in files:
                # 将压缩的文件删除
                if file_temp.split('.')[-1] in ['csv']:
                    continue
                os.remove(root + os.path.sep + file_temp)
            file_list.append(tar_file_name + ".tar.gz")
    return file_list


def untar(fname, dirs):
    """
    :param fname:需要解压的文件名
    :param dirs: 解压到的目录
    :return:没有返回值
    """
    t = tarfile.open(fname)
    t.extractall(path = dirs)



class UrlGet():
    """
    通过根据file文件初始化proxy
    通过file文件初始化url
    通过内置配置文件初始化header
    来抓取html页面的一个函数
    """
    proxy_list = []
    proxy_dict_dict = {}
    request_head = {
        'Accept' :['text/plain', 'text/html', '*/*'],
        'Accept-Language' : ['en', 'zh'],
        'Accept-Encoding' : ['compress','gzip'],
        'Cache-Control' : ['no-cache'],
        'Connection' : ['close', 'keep-alive'],
        'Referer':['http://www.amazon.com/','http://www.amazon.com/ref=nav_logo'],
        'User-Agent' : [
            'Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
            'Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0'
        ]
    }

    url_dict_dict = {}
    url_list = []

    proxy_number = 0
    sleep_mul = {'success' : 1, 'rebot' : 2, 'failed' : 5}
    rebot_add = {'success' : -1, 'rebot' : 1, 'failed' : 2}

    threadpool = None

    def __init__(self, proxy_file=''):
        """
        :param proxy_file:代理文件名称
        :param url_list:url列表
        :return:
        """
        self._set_proxy_list(proxy_file)


    def _get_random_header(self):
        """
        :return:获取一个随机拼凑的header
        """
        random_header = {}
        for field in self.request_head:
            random_header[field] = get_list_random(self.request_head[field])
        # reand_head1 = copy.deepcopy(random_header)
        # reand_head1['Accept-Encoding']  =  'gzip'
        return random_header

    def _set_proxy_list(self, file_name):
        """
        根据提供的文件名，设置proxy_list
        """

        if not os.path.exists('file'):
            os.mkdir('file')

        if not os.path.exists('file/localhost'):
            os.mkdir('file/localhost')

        with open(file_name, 'r') as temp_file:
            while True:
                temp = temp_file.readline()
                if temp:
                    proxy = temp.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                    if not os.path.exists('file/' + proxy):
                        os.mkdir('file/' + proxy)
                    self.proxy_list.append(proxy)
                    self.proxy_dict_dict[proxy] = {
                        'proxy' : proxy,
                        'status' : 'success',
                        'time' : datetime.now(),
                        'value' : 0,
                        'rebot' : 0,
                        'used' : 0,
                        'success' : 0,
                        'failed' :0
                    }
                else:
                    break

    def set_url_list(self, url_list):
        """
        根据提供的url_list，设置url_dict_dict
        """
        self.url_dict_dict = {}
        self.url_list = []


        for temp in url_list:
            if temp:
                url = temp.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                try:
                    file_name = re.findall(r'Cp_6%3A(.*?)&bbn', url)[0]
                    # file_name = re.findall(r'Cp_6%3A(.*?)&bbn',url)[0] + '_' + url.split('=')[-1] #seller
                    # file_name = url.split('/')[5]  #asin
                except IndexError, e:
                    print 'not found url seller_id', url, str(e)
                    file_name = url[65, 75]
                self.url_list.append(url)
                self.url_dict_dict[temp] = {'url' : url, 'status' : 'success', 'file_name' : file_name}
            else:
                break


    def _get_proxy(self):
        """
        :param proxy_dict_dict:存储各代理状态的字典
        :param proxy_list: 代理列表
        :param number: 需要取出的位置
        :return:返回代理
        """
        return_proxy = None
        while True and self.proxy_list:

            proxy = self.proxy_list[self.proxy_number%len(self.proxy_list)]
            lock = self.threadpool._threadLock
            lock.acquire()
            self.proxy_number = self.proxy_number + 1
            lock.release()

            temp_seconds = (datetime.now() - self.proxy_dict_dict[proxy]['time']).seconds
            rebot_number = max(self.proxy_dict_dict[proxy]['value'], 1)

            if self.proxy_dict_dict[proxy]['value'] >= 0:
                if rebot_number > 10:
                    lock = self.threadpool._threadLock
                    lock.acquire()
                    self.proxy_number = self.proxy_number + 1
                    lock.release()
                    continue

                if  temp_seconds < self.sleep_mul[self.proxy_dict_dict[proxy]['status']] * rebot_number:
                    time.sleep(self.sleep_mul[self.proxy_dict_dict[proxy]['status']] * rebot_number - temp_seconds)

            return_proxy = proxy
            break

        return return_proxy



    def _save_url_html(self, args):
        """
        :param args:提供url，proxy，header，将对应的数据抓取下来并保存
        :return:
        """

        url = args['url']
        proxy = args['proxy']
        header = args['header']

        status, html = get_url_html(self.url_dict_dict[url]['url'], proxy, header)
        # 修改url_dict_dict的状态


        self.url_dict_dict[url]['status'] = status

        if proxy:
            lock = self.threadpool._threadLock
            lock.acquire()
            self.proxy_dict_dict[proxy]['status'] = status
            self.proxy_dict_dict[proxy]['time'] = datetime.now()
            self.proxy_dict_dict[proxy]['used'] = self.proxy_dict_dict[proxy]['used'] + 1
            self.proxy_dict_dict[proxy]['value'] = self.proxy_dict_dict[proxy]['value'] + self.rebot_add[status]
            self.proxy_dict_dict[proxy][status] = self.proxy_dict_dict[proxy][status] + 1
            print self.url_dict_dict[url]['url'], proxy, status, datetime.now().strftime('%F %T %f'), self.proxy_dict_dict[proxy]['used']
            lock.release()

        proxy = proxy or 'localhost'

        if status == 'success':
            save_as_file('file/'+ proxy + '/'+ self.url_dict_dict[url]['file_name'] + '.html', html)



    def _set_log_file(self):
        """
        写log文件
        并将错误的url重复处理,如果成功百分比<95，则将四百的重新运行一遍
        """

        with open('file_log.csv', 'a') as temp_file:
            file_field = ['url', 'status']
            temp_file.write('\t'.join(file_field) + '\n')
            for temp_key in self.url_dict_dict:
                temp_list = []
                for field in file_field:
                    temp_list.append(str(self.url_dict_dict[temp_key][field]))
                temp_file.write('\t'.join(temp_list) + '\n')


        with open('proxy_log.csv', 'a') as temp_file:
            file_field = ['proxy', 'status', 'time', 'value', 'used', 'success', 'rebot', 'failed']
            temp_file.write('\t'.join(file_field) + '\n')
            for temp_key in self.proxy_dict_dict:
                temp_list = []
                for field in file_field:
                    if field != 'time':
                        temp_list.append(str(self.proxy_dict_dict[temp_key][field]))
                    else:
                        temp_list.append(self.proxy_dict_dict[temp_key][field].strftime('%F %T %f'))

                temp_file.write('\t'.join(temp_list) + '\n')


    def _deal_failed_url(self, is_loop=False):
        """
        :return:
        """

        fail_url = []
        for temp_key in self.url_dict_dict:
            if self.url_dict_dict[temp_key]['status'] != 'success':
                fail_url.append(self.url_dict_dict[temp_key]['url'])

        self.set_url_list(fail_url)
        self.save_url_html_mul(5, False)


    def compare_header_compress(self, url_list):
        for url in url_list:
            print 'start--gzip--size--compress'
            header1, header2 = self._get_random_header()
            print header1
            print '-----------------'
            print header2
            proxy = self._get_proxy()
            time1 = datetime.now()

            status1, html1 = get_url_html(url, proxy, header1)
            print len(html1)
            time2 = datetime.now()
            status2, html2 = get_url_html(url, proxy, header2)
            print len(html2)

            import gzip
            import StringIO
            data = StringIO.StringIO(html2)
            gz = gzip.GzipFile(fileobj=data)
            html3 = gz.read()
            print len(html3)
            time3 = datetime.now()

            print 'no gzip:',(time2-time1).seconds,'gzip:',(time3-time2).seconds
            time.sleep(5)

    def save_url_html_mul(self, mul_number=5, is_loop=True):
        """
        :param mul_number: 线程数量
        :return:
        """

        self.threadpool = PoolManager(mul_number)

        for url in self.url_dict_dict:

            header = self._get_random_header()
            proxy = self._get_proxy()

            self.threadpool.addJob(self._save_url_html, [{'url' : url, 'proxy' : proxy, 'header' : header}])

        self.threadpool.wait_jobscomplete()
        self.threadpool.getResult()
        self.threadpool.close()
        self._set_log_file()
        if is_loop:
            self._deal_failed_url(is_loop)



class Alibaba():
    """
    用来抓取alibaba的数据
    """
    title_name_re = "-\w\d\[\]\\\'\"\.\,\}\{\(\)\=\?\*&#%;/!:@$^_+ "

    # total product list
    page_number_re = re.compile(r'<span id="pagination-max" style="display:none">(?P<page_number>\d+?)</span>')
    category_path_re =re.compile(r'<a href="http://www.aliexpress.com/(af/){0,1}category/(?P<category_id>\d+?)(/[%(title_name)s]+?).html" title="(?P<category_title>[%(title_name)s]+?)" rel="category tag">(?P<category_name>[%(title_name)s]+?)</a>' %{'title_name' : title_name_re})
    category_leaf_re = re.compile(r'<link rel="canonical" href="http://www.aliexpress.com/category/(?P<category_id>\d+?)/(?P<category_name>[%(title_name)s]+?).html"/>' % {'title_name' : title_name_re})
    product_number_re = re.compile(r'<strong class="search-count">(?P<product_number>[\d,]+?)</strong>')

    # product detail total
    product_id_re = re.compile(r'productId="(?P<product_id>\d+?)";')
    reviews_re = re.compile(r'<a href="javascript:void\(0\)".*?>Feedback \((?P<reviews>\d+?)\)</a>')
    detail_str_re = re.compile(r'<div class="ui-tab-body">.*?<h2 class="ui-box-title">(?P<title>[%(title_name)s]+?)</h2>\s*?<div class="ui-box-body">(?P<value>.*?)</div>\s*?</div>' % {'title_name' : title_name_re}, re.S)
    detail_str_dict_re = re.compile(r'<dl class="ui-attr-list util-clearfix">\s*?<dt>(<span.*?>)?(?P<key>[%(title_name)s]+?)(</span>)?</dt>\s*?<dd.*?>(?P<value>[%(title_name)s]+?)</dd>\s*?</dl>' % {'title_name' : title_name_re}, re.S)


    product_attr_list_list_re = re.compile(r'<div id="product-info-sku">\s*?(?P<product_attr_name_list><dl .*?>.*?</dl>)\s*?</div>'% {'title_name' : title_name_re}, re.S)
    product_attr_list_re = re.compile(r'<dl.*?>\s*?<dt.*?>\s*?(?P<product_attr_name>[%(title_name)s]+?)\s*?</dt>.*?<ul.*?>\s*?(?P<product_attr_list>(<li>.*?</li>\s*?)+?)\s*?</ul>'% {'title_name' : title_name_re}, re.S)
    product_attr_value_list_re = re.compile(r'<li><a.*?id="(?P<attr_id>[%(title_name)s]+?)".*?>((<span>(?P<span_value>[%(title_name)s]+?)</span>)|(<span.*?title="(?P<span_title>[%(title_name)s]+?)".*?>.*?</span>)|(<img.*?title="(?P<image_title>[%(title_name)s]+?)" (bigpic="(?P<big_image>[%(title_name)s]+?)"){0,1}.*?/>))</a></li>'% {'title_name' : title_name_re}, re.S)

    sku_dict_list_re = re.compile(r'var skuProducts=\[(?P<sku_dict_list>.*?)\];', re.S)
    sku_dict_re = re.compile(r'\{("skuAttr":"(?P<sku_attr>[\w\s#:;]+?)",){0,1}"skuPropIds":"(?P<sku_id>[\d\,]+?){0,1}","skuVal":\{.*?("actSkuMultiCurrencyDisplayPrice":"(?P<actSkuMultiCurrencyDisplayPrice>[\d\.]+?)","actSkuMultiCurrencyPrice":"(?P<actSkuMultiCurrencyPrice>.+?)){0,1}".*?"skuMultiCurrencyDisplayPrice":"(?P<skuMultiCurrencyDisplayPrice>[\d\.]+?)","skuMultiCurrencyPrice":"(?P<skuMultiCurrencyPrice>.+?)".*?\}\}')
    sku_prop_id_list_re = re.compile(r'var skuAttrIds=\[(?P<sku_prop_id_list_str>[\d,\]\[]+?)\];')
    sku_prop_id_re =  re.compile(r'\[(?:(?P<attr_list>(?:\d+,?)+?),?\])')
    image_list_re = re.compile(r'window.runParams.imageBigViewURL=\[\s?(?P<image_list>.*?)\s?\]', re.S)
    # 由于不是全部的ul 都有 data-sku-prop-id 这个属性，因此只能根据 skuAttrIds  中的列表的顺序来和 li 中的 ‘sku-1-361180’ 的中间那位数来匹配得到最后的结果
    # product detail detail


    # product list li
    category_id_re = re.compile(r'"category_id":"(?P<category_id>\d+?)",')
    key_name_re = re.compile(r'rel="category tag">(?P<key_name>[%(title_name)s]+?)</a>'% {'title_name' : title_name_re})
    product_list_re = re.compile(r'<li class="list-item.*?>(?P<product_information>.*?)</li>',re.S)
    seller_id_re = re.compile(r'<a href="http://www.aliexpress.com/store/(?P<seller_id>\d+?)" title="(?P<seller_title>[%(title_name)s]+?)" class="store"  >(?P<seller_name>[%(title_name)s]+?)</a>' %{'title_name' : title_name_re})
    product_detail_re = re.compile(r'<a class=" product " href="http://www.aliexpress.com/item/(?P<product_item>[%(title_name)s]+?)/(?P<product_id>\d+?)\.html(.*?){0,1}" title="(?P<product_title>[%(title_name)s]+?)" itemprop="name" >(?P<product_name>[%(title_name)s]+?)</a>' %{'title_name' : title_name_re})
    product_ship_re = re.compile(r'<div class="info infoprice">(?P<price_infromation>.*?)<div class="rate-history"', re.S)
    product_price_re = re.compile(r'<span class="value" itemprop="price">(?P<price>.+?)</span>', re.S)
    product_ship_price_re = re.compile(r'<span class="value">(?P<ship_price>.+?)</span>', re.S)



    # category_root
    category_list_re = re.compile(r'<div class="item util-clearfix">.*?<a href="http://www.aliexpress.com/category/(?P<id>[\d]+?)/(?P<title>[%(title_name)s]+?).html">(?P<name>[%(title_name)s]+?)</a>.*?<ul class="sub-item-cont util-clearfix">(?P<category_son_list_str>.*?)</ul>.*?</div>.*?</div>.*?</div>' % {'title_name' : title_name_re} , re.S)
    category_son_re = re.compile(r'<li>.*?<a href="http://www.aliexpress.com/category/(?P<id>[\d]+?)/(?P<title>[%(title_name)s]+?).html">(?P<name>[%(title_name)s]+?)</a>.*?</li>' % {'title_name' : title_name_re}, re.S)
    # category_leaf
    category_list_str_re = re.compile(r'<dl class="son-category">.*?<span class="current-cate">(?P<category_name>[%(title_name)s]+?)</span>(.*?<ul>(?P<category_list_str>.*?)</ul>){0,1}.*?</dl>'% {'title_name' : title_name_re}, re.S)
    category_list_leaf_re = re.compile(r'<li>.*?<a  rel="follow"  href="http://www.aliexpress.com/category/(?P<id>[\d]+?)/(?P<title>[%(title_name)s]+?)\.html.*?>(?P<name>[%(title_name)s]+?)</a>.*?<span class="num">\((?P<category_product_number>[\d]+?)\)</span>.*?</li>'% {'title_name' : title_name_re}, re.S)
    #end category

    fee_re = re.compile(r'(?P<value>\d(?:\.\d+){0,1})', re.S)
    file_type_list = ['list', 'image', 'detail','csv']

    dont_need_field_dict = {'description' : 'description', 'feature' : 'feature'}
    product_list_field_dict = {'key_name' : 'keyname',  'category' : 'category_id', 'seller_id' : 'seller_id', 'title' : 'product_name', 'ship' : 'ship_price', 'product_id' : 'product_id'}
    product_detail_fiedld_dict = {'detail' : 'detail', 'img_list' : 'img_list', 'son_product_id' : 'product_attr_id', 'brand' : 'brand_name', 'reviews' : 'reviews', 'price' : 'skuMultiCurrencyPrice', 'currency' : 'skuMultiCurrency', 'product_attr' : 'product_attr'}
    product_detail_url = 'http://www.aliexpress.com/item/product/%(product_id)s.html'


    request_head = {
        'Accept' :['text/plain', 'text/html', '*/*'],
        'Accept-Language' : ['en', 'zh'],
        'Accept-Encoding' : ['gzip'],
        'Cache-Control' : ['no-cache'],
        'Connection' : ['close', 'keep-alive'],
        # 'Cookie' : [        ],
        'Referer':['http://www.amazon.com/','http://www.amazon.com/ref=nav_logo'],
        'User-Agent' : [
            'Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
            'Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0'
        ]
    }

    proxy_list = ['23.19.34.179:8800','50.31.9.167:8800','69.147.248.32:8800','173.208.39.131:8800','173.234.59.187:8800','198.55.109.142:8800','173.234.59.55:8800','173.234.59.149:8800','173.232.7.186:8800','192.161.160.187:8800','173.234.249.24:8800','173.208.103.230:8800','192.161.160.25:8800','69.147.248.40:8800','50.31.10.198:8800','206.214.93.132:8800','69.147.248.73:8800','173.234.59.6:8800','198.55.109.187:8800','173.208.103.183:8800','206.214.93.30:8800','206.214.93.213:8800','23.19.34.195:8800','50.31.9.26:8800','173.234.59.172:8800','23.19.34.98:8800','50.31.10.88:8800','50.31.10.86:8800','173.208.39.105:8800','206.214.93.106:8800','192.161.160.185:8800','50.31.9.41:8800','69.147.248.134:8800','50.31.9.141:8800','69.147.248.21:8800','173.232.7.123:8800','173.234.249.158:8800','50.31.9.183:8800','173.232.7.188:8800','23.19.34.58:8800','173.234.249.112:8800','23.19.34.254:8800','173.234.249.234:8800','50.31.10.115:8800','23.19.34.148:8800','50.31.9.18:8800','192.161.160.100:8800','173.232.7.22:8800','192.161.160.24:8800','173.208.103.121:8800','206.214.93.60:8800','69.147.248.91:8800','173.208.39.124:8800','173.208.103.187:8800','173.234.249.42:8800','50.31.9.197:8800','173.208.39.150:8800','173.234.59.136:8800','173.234.249.8:8800','173.234.59.59:8800','50.31.10.153:8800','198.55.109.161:8800','23.19.34.75:8800','173.232.7.10:8800','23.19.34.134:8800','173.234.59.161:8800','173.208.103.168:8800','23.19.34.142:8800','173.232.7.148:8800','173.234.59.226:8800','173.208.103.8:8800','173.234.249.168:8800','173.234.249.212:8800','173.234.59.125:8800','23.19.34.80:8800','50.31.10.150:8800','50.31.9.75:8800','198.55.109.16:8800','206.214.93.136:8800','206.214.93.197:8800','50.31.10.177:8800','173.234.249.69:8800','23.19.34.174:8800','50.31.9.159:8800','23.19.34.19:8800','173.208.103.217:8800','173.208.103.18:8800','192.161.160.125:8800','23.19.34.63:8800','206.214.93.155:8800','69.147.248.247:8800','173.234.249.150:8800','192.161.160.53:8800','173.234.59.230:8800','198.55.109.183:8800','192.161.160.134:8800','173.208.39.13:8800','173.208.103.61:8800','69.147.248.102:8800','69.147.248.62:8800','173.234.249.194:8800']

    def __init__(self):
        pass

    def _get_random_header(self):
        """
        :return:获取一个随机拼凑的header
        """
        random_header = {}
        for field in self.request_head:
            random_header[field] = get_list_random(self.request_head[field])
        # reand_head1 = copy.deepcopy(random_header)
        # reand_head1['Accept-Encoding']  =  'gzip'
        return random_header

    def _get_simple_html(self, url, html_type='html'):
        header = self._get_random_header()
        proxy =  None #get_list_random(self.proxy_list)
        status, content = get_url_html(url, proxy=proxy, header=header, html_type=html_type)
        return status, content

    @staticmethod
    def ungzip_html(file_path):
        """
        :param file_path:保存的html文件路径
        :return:
        """
        with open(file_path, 'r') as temp_file:
            product_html_gz = temp_file.read()
        data = StringIO.StringIO(product_html_gz)
        gz = gzip.GzipFile(fileobj=data)
        product_html = gz.read()
        gz.close()
        return product_html

    def get_category_tree(self):
        categor_dict = self.get_category_root_dict()
        have_add = True
        while have_add:
            have_add = False
            category_dict_temp = {}
            for categor_index in categor_dict:
                # 判断此节点是否是有被标示叶子节点，如果有，则标示此节点已经处理过了，如果没有，则查找此节点信息，并标记节点的叶子节点信息
                if 'is_leaf' not in categor_dict[categor_index]:
                    # print 'categor_index:',categor_index
                    try:
                        category_leaf_dict, son_leaf_list = self.get_category_dict(categor_index)
                    except Exception as e:
                        print 'This category is a bug:',categor_index
                        continue
                    # print category_leaf_dict
                    # print '---------'
                    # print son_leaf_list
                    categor_dict[categor_index]['son_id_list'] = category_leaf_dict[categor_index]['son_id_list']

                    if son_leaf_list:
                        categor_dict[categor_index]['is_leaf'] = False

                        for son_leaf in son_leaf_list:
                            if son_leaf['id'] in categor_dict:
                                categor_dict[son_leaf['id']]['father_id_list'] += son_leaf['father_id_list']
                                categor_dict[son_leaf['id']]['category_path_list'] += [(category_path + '/' + son_leaf['name']) for category_path in categor_dict[categor_index]['category_path_list']]
                            else:
                                son_leaf['category_path_list'] = [(category_path + '/' + son_leaf['name']) for category_path in categor_dict[categor_index]['category_path_list']]
                                category_dict_temp[son_leaf['id']] = son_leaf
                                have_add = True

                    else:
                        categor_dict[categor_index]['is_leaf'] = True
                        pass
                else:
                    pass

            categor_dict.update(category_dict_temp)


        return categor_dict

    def get_category_root_dict(self):


        category_root_url = 'http://www.aliexpress.com/all-wholesale-products.html'
        category_status, category_html = self._get_simple_html(category_root_url)
        # if category_status:
        category_list_iter  = re.finditer(self.category_list_re, category_html)
        categor_dict = {'1' :{'name' : 'root', 'title' : 'root', 'id' : '1', 'father_id_list' : [], 'son_id_list' : [], 'category_path_list' : ['root'], 'is_leaf' : True}}

        while True:
            try:
                category_list_dict = category_list_iter.__iter__().next().groupdict()


                categor_dict['1']['son_id_list'].append(category_list_dict['id'])
                categor_dict['1']['is_leaf'] = False

                if category_list_dict['id'] in categor_dict:
                    categor_dict[category_list_dict['id']]['father_id_list'] += ['1']
                    categor_dict[category_list_dict['id']]['category_path_list'] += [(category_path + '/' + category_list_dict['name']) for category_path in categor_dict['1']['category_path_list']]
                else:

                    categor_dict[category_list_dict['id']] ={}
                    categor_dict[category_list_dict['id']]['name'] = category_list_dict['name']
                    categor_dict[category_list_dict['id']]['title'] = category_list_dict['title']
                    categor_dict[category_list_dict['id']]['id'] = category_list_dict['id']
                    categor_dict[category_list_dict['id']]['father_id_list'] = ['1']
                    categor_dict[category_list_dict['id']]['son_id_list'] = []
                    categor_dict[category_list_dict['id']]['category_path_list'] = [(category_path + '/' + category_list_dict['name']) for category_path in categor_dict['1']['category_path_list']]



                category_son_list = re.finditer(self.category_son_re, category_list_dict['category_son_list_str'])
                while True:
                    try:

                        category_son_dict = category_son_list.__iter__().next().groupdict()



                        categor_dict[category_list_dict['id']]['son_id_list'].append(category_son_dict['id'])
                        categor_dict[category_list_dict['id']]['is_leaf'] = False

                        if category_son_dict['id'] in categor_dict:
                            categor_dict[category_son_dict['id']]['father_id_list'] += [category_list_dict['id']]
                            categor_dict[category_son_dict['id']]['father_id_list'] += [(category_path + '/' + category_son_dict['name']) for category_path in categor_dict[category_list_dict['id']]['category_path_list']]
                        else:
                            categor_dict[category_son_dict['id']] ={}
                            categor_dict[category_son_dict['id']]['name'] = category_son_dict['name']
                            categor_dict[category_son_dict['id']]['title'] = category_son_dict['title']
                            categor_dict[category_son_dict['id']]['id'] = category_son_dict['id']
                            categor_dict[category_son_dict['id']]['father_id_list'] = [category_list_dict['id']]
                            categor_dict[category_son_dict['id']]['son_id_list'] = []
                            categor_dict[category_son_dict['id']]['category_path_list'] = [(category_path + '/' + category_son_dict['name']) for category_path in categor_dict[category_list_dict['id']]['category_path_list']]
                    except StopIteration:
                        break
                    except Exception as e:
                        print 'cagetory_son error:',str(e)
                        break

                # return categor_dict

            except StopIteration:
                break
            except Exception as e:
                print 'error:',str(e)
                break

        return categor_dict

    def get_category_dict(self, category_id):

        category_url = 'http://www.aliexpress.com/category/%(category_id)s/name.html' %{'category_id' : category_id}
        category_status, category_html = self._get_simple_html(category_url)
        # print category_html
        # if category_status:
        try:
            category_list_dict = re.finditer(self.category_list_str_re, category_html).__iter__().next().groupdict()
        except StopIteration:
            print category_id

        # print category_list_dict['category_list_str']
        category_name = category_list_dict['category_name']

        son_id_list = []
        son_dict_list = []
        is_leaf = False

        if category_list_dict['category_list_str']:
            category_leaf_list = re.finditer(self.category_list_leaf_re, category_list_dict['category_list_str'])
            while True:
                try:
                    category_leaf_dict = category_leaf_list.__iter__().next().groupdict()
                    son_id_list.append(category_leaf_dict['id'])

                    category_leaf_dict_temp = copy.deepcopy(category_leaf_dict)
                    category_leaf_dict_temp['father_id_list'] = [category_id]
                    category_leaf_dict_temp['son_id_list'] = []
                    category_leaf_dict_temp['category_path_list'] = []
                    category_leaf_dict_temp.pop('category_product_number')
                    son_dict_list.append(category_leaf_dict_temp)

                except StopIteration:
                    break
                except Exception as e:
                    print 'get category leaf error:',str(e)
                    break

        else:
            is_leaf = True

        categor_dict = {category_id :{'name' : category_name, 'title' : category_name, 'id' : category_id, 'father_id_list' : [], 'son_id_list' : son_id_list, 'category_path_list' : []}}

        if is_leaf:
            categor_dict[category_id]['is_leaf'] = is_leaf

        return categor_dict, son_dict_list

    def alibaba_get_root_url(self, category_id):
        """
        :param category:叶子品类的品类ID
        :return:
        """
        print '开始抓取页面'
        # 1,保存产品列表的html页面
        product_file_path = self.save_product_list(category_id)
        # product_file_path = {'path' : 'alibaba/file/200000156/20150919/list'}

        print '抓取产品列表页面结束'

        # 已经处理过的文件夹
        product_list_price_path_already_deal = []

        # 根据返回回来的基础path，得到所有的价格段的文件夹   ../list/
        product_list_price_path_list = os.listdir(product_file_path['path'])
        product_list_price_path_list = map(lambda file_name:product_file_path['path'] + os.sep +file_name, product_list_price_path_list)

        print '产品产品列表共有区间段为：',len(product_list_price_path_list)

        product_detail_price_path_list = []

        mul_number = 5
        self.threadpool = PoolManager(mul_number)

        product_price_list_dict = {}
        for product_list_price_path in product_list_price_path_list:
            if product_list_price_path in product_list_price_path_already_deal:
                continue
            print '开始解析产品列表，获取产品ID，和产品的运费：',product_list_price_path

            file_path_product,product_dict = self.save_product_price_list(product_list_price_path)

            print '保存产品详细列表完成'
            product_detail_price_path_list.append(file_path_product)
            product_price_list_dict.update(product_dict)

        product_dict_list = []
        print '产品详细页面文件夹为', product_detail_price_path_list


        for product_detail_price_path in product_detail_price_path_list:
            print '开始解析文件夹中的产品页面：',product_detail_price_path

            file_path_image = product_detail_price_path.replace('detail','image')
            file_html_list = os.listdir(product_detail_price_path)
            file_html_list = map(lambda file_name:product_detail_price_path + os.sep + file_name,file_html_list)

            product_price_dict_list, error_file_list = self.get_product_dict_for_file_list(file_html_list)

            print '解析该文件夹的产品页面结束,共有产品',len(product_price_dict_list)

            if  error_file_list:
                print '产品页面解析成产品失败:', error_file_list

            for product_price_dict in product_price_dict_list:
                for product_information_index in product_price_dict:
                    if product_price_dict[product_information_index]['img_list']:
                        try:
                            image_name = file_path_image + os.sep + str(product_price_dict[product_information_index][self.product_detail_fiedld_dict['son_product_id']]) + '.' +  product_price_dict[product_information_index][self.product_detail_fiedld_dict['img_list']][-1].split('.')[-1]
                            # print image_name
                            urllib.urlretrieve(product_price_dict[product_information_index][self.product_detail_fiedld_dict['img_list']][-1], image_name)
                        except Exception,e:
                            print 'save image error:',str(e), image_name, product_price_dict[product_information_index][self.product_detail_fiedld_dict['son_product_id']], product_price_dict[product_information_index][self.product_detail_fiedld_dict['img_list']][-1],str(e)

                    temp_dict = product_price_dict[product_information_index]

                    temp_field_dict = {}
                    for dont_need_field in self.dont_need_field_dict:
                        temp_field_dict[dont_need_field] = self.dont_need_field_dict[dont_need_field]

                    for product_list_field in self.product_list_field_dict:
                        temp_field_dict[product_list_field] = product_price_list_dict[product_price_dict[product_information_index]['father_id']][self.product_list_field_dict[product_list_field]]

                    for product_detail_field in self.product_detail_fiedld_dict:
                        try:
                            temp_field_dict[product_detail_field] = product_price_dict[product_information_index][self.product_detail_fiedld_dict[product_detail_field]]
                        except KeyError:
                            pass
                        except Exception as e:
                            print 'set field key error:',str(e)
                            pass

                    product_dict_list.append(temp_field_dict)

            print '保存产品的首图成功拿'
            csv_file_name = product_detail_price_path.replace('detail','csv')

            with open(csv_file_name + '.csv', 'w') as temp_file:
                for product_dict in product_dict_list:
                    temp_file.write(str(product_dict) + '\n')

    def _reslove_html(self, html='', html_type='list_product'):

        if html_type == 'list_product':
            category_id = re.finditer(self.category_id_re, html).__iter__().next().groupdict()['category_id']
            try:
                key_name = re.finditer(self.key_name_re, html).__iter__().next().groupdict()['key_name']
            except StopIteration:
                key_name = 'key_name'
            product_list_return = []
            product_list_iter = re.finditer(self.product_list_re ,html)
            while True:
                try:
                    product_list_temp = product_list_iter.__iter__().next().groupdict()['product_information']
                    try:
                        seller_id_dict = re.finditer(self.seller_id_re, product_list_temp).__iter__().next().groupdict()
                        seller_id = seller_id_dict['seller_id']
                    except StopIteration:
                        seller_id = 'No found seller'
                    try:
                        product_detail_dict = re.finditer(self.product_detail_re, product_list_temp).__iter__().next().groupdict()
                    except StopIteration:
                        product_detail_dict = {'product_id' : '00000000', 'product_name' : 'No found product'}
                    try:
                        product_price_str = re.finditer(self.product_ship_re, product_list_temp).__iter__().next().groupdict()['price_infromation']
                        try:
                            product_price = re.finditer(self.product_price_re, product_price_str).__iter__().next().groupdict()['price']
                            product_price = re.findall(self.fee_re, product_price)[0]
                        except StopIteration:
                            product_price = -1

                        try:
                            ship_price = re.finditer(self.product_ship_price_re, product_price_str).__iter__().next().groupdict()['ship_price']
                            ship_price = re.findall(self.fee_re, ship_price)[0]
                        except StopIteration:
                            ship_price = 0


                        if product_detail_dict['product_id'] == '32233100382':
                            print product_price_str,ship_price

                    except StopIteration:
                        product_price = -1
                        ship_price = -1

                    product_list_return.append({
                        'seller_id' : seller_id,
                        'product_id' : product_detail_dict['product_id'],
                        'product_name' : product_detail_dict['product_name'],
                        'price' : product_price,
                        'ship_price' : ship_price,
                        'category_id' : category_id,
                        'keyname' : key_name
                    })
                except StopIteration:
                    break
            return product_list_return

        elif html_type == 'information_product':
            product_id = re.finditer(self.product_id_re, html).__iter__().next().groupdict()['product_id']
            # print 'product_id:',product_id

            try:
                reviews = re.finditer(self.reviews_re, html).__iter__().next().groupdict()['reviews']
            except StopIteration:
                reviews = 0
                # print product_id,'not have reviews'
            try:
                detail = {}
                detail_dict = re.finditer(self.detail_str_re,html).__iter__().next().groupdict()
                detail_list_dict_str = detail_dict['value']
                detail_dict_list = re.finditer(self.detail_str_dict_re, detail_list_dict_str)
                while True:
                    try:
                        detail_dict_list_dict = detail_dict_list.__iter__().next().groupdict()
                        detail[detail_dict_list_dict['key']] = detail_dict_list_dict['value']
                    except StopIteration:
                        break

            except StopIteration:
                detail = {}

            # detail = detail_dict['value']
            brand_name = getattr(detail,'Brand Name:', 'no brand')

            try:
                image_list_str = re.finditer(self.image_list_re, html).__iter__().next().groupdict()['image_list']
            except StopIteration:
                image_list_str = None
                print product_id, 'not have image list'
            image_list = image_list_str.replace('"','').strip().split(',\n')

            # print 'image_list',image_list

            product_attr_dict = {}
            product_attr_list = [product_id]


            # 如果有子属性，就会有个子属性列表，在这里获取子属性列表的值，以及属性的顺序
            try:
                sku_prop_id_list_str = re.finditer(self.sku_prop_id_list_re, html).__iter__().next().groupdict()['sku_prop_id_list_str']
                # print sku_prop_id_list_str
                sku_prop_id_list = re.finditer(self.sku_prop_id_re, sku_prop_id_list_str)

                while True:
                    try:
                        sku_prop_id_temp_dict = sku_prop_id_list.__iter__().next().groupdict()
                        # print 'sku_prop_id_str:',sku_prop_id_temp_dict['attr_list']
                        sku_prop_id_list_temp = sku_prop_id_temp_dict['attr_list'].split(',')
                        temp_list = []
                        for sku_prop_id in sku_prop_id_list_temp:
                            for product_attr in product_attr_list:
                                temp_list.append(str(product_attr) + "__" + str(sku_prop_id))

                        product_attr_list = temp_list
                    except StopIteration:
                        # print 'error3:'
                        break
                    except Exception, e:
                        # print 'error4:', str(e)
                        break
            except StopIteration:
                pass
                # print 'not have product attr'

            # print 'product_attr_list',product_attr_list
            for product_attr in product_attr_list:
                product_attr_dict[product_attr] = {
                    'img_list' : copy.deepcopy(image_list),
                    'reviews' : reviews,
                    # 'brand_title' : brand_title,
                    'brand_name' : brand_name,
                    'product_attr_id' : product_attr,
                    'product_attr' : {},
                    'detail' : detail,
                    'father_id' : product_id

                }

            # 如果有子属性的话，获取子属性的属性的title，id，以及子product是否有图片
            try:
                product_attr_name_lsit_str = re.finditer(self.product_attr_list_list_re, html).__iter__().next().groupdict()['product_attr_name_list']
                # print 'attr start',product_attr_name_lsit_str

                product_attr_list_dict_re = re.finditer(self.product_attr_list_re, product_attr_name_lsit_str)
                while True:
                    try:
                        product_attr_list_dict_temp = product_attr_list_dict_re.__iter__().next().groupdict()
                        product_attr_name = product_attr_list_dict_temp['product_attr_name']
                        product_attr_value_list = re.finditer(self.product_attr_value_list_re, product_attr_list_dict_temp['product_attr_list'])

                        while True:
                            try:
                                attr_value_dict = product_attr_value_list.__iter__().next().groupdict()
                                # print attr_value_dict['attr_id']
                                attr_id_dict = attr_value_dict['attr_id'].split('-')
                                attr_id = attr_id_dict[2]
                                attr_number = attr_id_dict[1]
                                attr_value_title = attr_value_dict['span_value'] or attr_value_dict['span_title'] or attr_value_dict['image_title']
                                big_image = attr_value_dict['big_image']


                                for product_attr in product_attr_list:
                                    if product_attr.split('__')[int(attr_number)] == attr_id:
                                        # product_attr_dict[product_attr][product_attr_name] = {'name' : attr_value_title,'id' : attr_id}
                                        product_attr_dict[product_attr]['product_attr'][product_attr_name] = {'name' : attr_value_title,'id' : attr_id}

                                        if big_image:
                                            product_attr_dict[product_attr]['img_list'].append(big_image)

                            except Exception, e:
                                # print 'error1:', str(e)
                                break
                    except Exception, e:
                        # print 'error2:', str(e)
                        break
            except StopIteration:
                pass
                # print 'not have attr list'

            # print 'product_attr_dict*************:',product_attr_dict

            try:
                sku_attr_list_str = re.finditer(self.sku_dict_list_re, html).__iter__().next().groupdict()['sku_dict_list']
            except StopIteration:
                # print 'product:',product_id,' not have sku_dict_list'
                pass
            # print sku_attr_list_str
            sku_attr_list = re.finditer(self.sku_dict_re, sku_attr_list_str)

            # 获取sku的价格
            while True:
                try:

                    sku_attr_dict_str = sku_attr_list.__iter__().next().groupdict()
                    if sku_attr_dict_str['sku_id']:
                        product_sku_attr_str = str(product_id) + '__' + sku_attr_dict_str['sku_id'].replace(',','__')
                    else:
                        product_sku_attr_str = str(product_id)
                    # print '-------------------------'
                    # print 'sku_attr_dict_str:',sku_attr_dict_str
                    # print product_sku_attr_str
                    # print '-------------------------'
                    product_attr_dict[product_sku_attr_str]['skuMultiCurrency'] = filter(str.isalpha, sku_attr_dict_str['actSkuMultiCurrencyPrice'] or sku_attr_dict_str['skuMultiCurrencyPrice'])
                    product_attr_dict[product_sku_attr_str]['skuMultiCurrencyPrice'] = sku_attr_dict_str['actSkuMultiCurrencyDisplayPrice'] or sku_attr_dict_str['skuMultiCurrencyDisplayPrice']

                except Exception, e:
                    # print 'sku price error:',str(e)
                    break


            # print '-----------------------'
            # print 'reviews:',reviews, 'brand_name:',brand_name, 'brand_title:',brand_title,'product_attr_dict:',product_attr_dict
            # print product_attr_dict
            # print '-----------------------'
            return product_attr_dict

    def __get_url_category_information(self, html):

        category_field = ['category_id','category_name']
        category_title_dict = {'category_id' : '', 'category_name' : ''}

        category_leaf_temp_iter = re.finditer(self.category_leaf_re, html)

        category_leaf_temp_dict = category_leaf_temp_iter.__iter__().next().groupdict()
        category_name = category_leaf_temp_dict['category_name']
        category_id = category_leaf_temp_dict['category_id']


        category_split = '/'
        category_path_temp_iter = re.finditer(self.category_path_re, html)
        while True:
            try:
                temp_dict  = category_path_temp_iter.__iter__().next().groupdict()
                for field in category_field:
                    category_title_dict[field] += temp_dict[field]  + category_split
            except StopIteration:
                # print 're iteration is end.'
                break

        category_title_dict['category_id'] += category_id
        category_title_dict['category_name'] += category_name

        # print category_id, category_name, category_title_dict
        return category_id, category_name, category_title_dict['category_name']

    def _get_amazon_price_limit(self, url, min_price = 0, max_price = ''):

        print '获取分页信息'
        my_max = 64 + min_price
        LIMIT_PAGE_NUMBER = 9000

        price_limit_url = url + '&maxPrice=' + str(max_price) + '&minPrice=' + str(min_price)

        status, html = self._get_simple_html(price_limit_url)

        total_search_number = re.finditer(self.product_number_re, html).__iter__().next().groupdict()['product_number']
        total_search_number = int(filter(str.isalnum, total_search_number))
        page_number = re.finditer(self.page_number_re, html).__iter__().next().groupdict()['page_number']
        print 'min_price:',min_price,'max_price:',max_price,'total_search_number:',total_search_number,'page_number:',page_number,price_limit_url

        if total_search_number < LIMIT_PAGE_NUMBER or ((max_price or my_max)  - min_price) < 0.05:
            return [{'min_price' : min_price, 'max_price' : max_price, 'page_number' : int(page_number)}]

        else:
            price_split = ((max_price or my_max)  - min_price)*1.0/2
            return self._get_amazon_price_limit(url, min_price, min_price + price_split) + self._get_amazon_price_limit(url, min_price + price_split, max_price)

    def _create_product_file(self, root_url):
        """
        :param root_url: 根目录
        :param min_price: 最小价格
        :param max_price: 最大价格
        :return:返回文件基础路径，品类ID，品类名，品类路径
        """
        url = root_url
        file_time = datetime.now().strftime('%Y%m%d')
        status, html = self._get_simple_html(url)
        category_id, category_name, category_path = self.__get_url_category_information(html)

        if not os.path.exists(str(category_id)):
            os.mkdir(str(category_id))

        with open('category_key.csv', 'a') as temp_file:
            temp_file.write(str(category_id) + '\t' + category_name + '\t' + file_time + '\n')


        for file_type in self.file_type_list:
            if not os.path.exists(str(category_id) + os.sep + file_type):
                os.mkdir(str(category_id) + os.sep + file_type)

        file_path = str(category_id)
        return file_path, category_id, category_name, category_path

    def save_product_list(self, category_id, min_price=0, max_price=''):
        """
        :param root_url: 根目录
        :param min_price: 最小价格
        :param max_price: 最大价格
        :return:保存的文件路径
        """
        print '根据品类ID，抓取品类名称，创建文件夹'
        start_url = 'http://www.aliexpress.com/category/' + str(category_id) + '/category/1.html?needQuery=n'
        file_path, category_id, category_name, category_path = self.create_product_file(start_url, min_price, max_price)

        print '根据品类名称，抓取价格段'
        price_url = 'http://www.aliexpress.com/category/' + str(category_id) + '/' + category_name + '/1.html?needQuery=n'
        price_limit_list = self.get_amazon_price_limit(price_url, min_price, max_price)

        url_select_str = price_url.split('?')[-1]
        url_start_star = price_url.split(category_id)[0]

        print '根据价格段抓取产品列表页面'
        for price_limit in price_limit_list:
            print '抓取产品列表，价格段为：',price_limit
            now_number = 1
            price_file = str(price_limit['min_price'])+'_' + str(price_limit['max_price'])

            if not os.path.exists(file_path + os.sep + 'list' + os.sep + price_file):
                os.mkdir(file_path + os.sep + 'list' + os.sep + price_file)

            # with open(file_path + os.sep + 'csv' + os.sep + price_file + '.csv','w') as temp_file:
            while now_number <= price_limit['page_number']:
                category_split_price_url = url_start_star + str(category_id) + '/' + str(category_name) + '/' + str(now_number) + '.html?' + url_select_str + '&maxPrice='  + str(price_limit['max_price']) + '&minPrice=' + str(price_limit['min_price'])
                product_list_status, product_list_html = self.get_simple_html(category_split_price_url, html_type='gzip')
                save_as_file(file_path + os.sep + 'list' + os.sep + price_file + os.sep + str(now_number) + '.html', product_list_html)
                now_number = now_number +1

        return {'path' : file_path + os.sep + 'list'}



    def alibaba(self,category_id, min_price=0, max_price='', price_list_need=True, product_list_nedd=True, product_detail_nedd=True, is_just_download=False):


        if price_list_need:
            print '根据品类ID，抓取品类名称，创建文件夹，抓取价格段，写入文件'
            start_url = 'http://www.aliexpress.com/category/' + str(category_id) + '/category/1.html?needQuery=n'
            file_path, category_id, category_name, category_path = self._create_product_file(start_url)

            # print '根据品类名称，抓取价格段'
            price_url = 'http://www.aliexpress.com/category/' + str(category_id) + '/' + category_name + '/1.html?needQuery=n'
            price_limit_list = self._get_amazon_price_limit(price_url, min_price, max_price)

            # print '将价格段信息写入文件，以后从文件中读取价格段信息'
            with open(file_path + os.sep + 'price_limit.csv','w') as price_temp_file:
                for price_limit in price_limit_list:
                    price_file = str(price_limit['min_price']) + '_' + str(price_limit['max_price'])
                    for file_type in self.file_type_list:
                        if file_type != 'csv' and not os.path.exists(file_path + os.sep + file_type + os.sep + price_file):
                            os.mkdir(file_path + os.sep + file_type + os.sep + price_file)

                    price_temp_file.write(str(price_limit) + '\n')

            url_select_str = price_url.split('?')[-1]
            url_start_star = price_url.split(category_id)[0]
        else:
            print '从系统的价格段文件中读取价格段'
            category_id_name_dict = {
                '100006750' : 'jewelry-sets',
                '200001025' : 'bridal-jewelry-sets',
                '100006748' : 'brooches',
                '100006745' : 'hair-jewelry'
            }
            file_path, category_id, category_name, category_path = str(category_id), category_id, category_id_name_dict[category_id], 'category_path'
            url_select_str = 'needQuery=n'
            url_start_star = 'http://www.aliexpress.com/category/'

            price_limit_list = []
            with open(file_path + os.sep + 'price_limit.csv', 'r') as price_temp_file:
                lines = price_temp_file.readlines()
                [price_limit_list.append(eval(line)) for line in lines]


        # self.threadpool = PoolManager(5)
        # print '根据价格段抓取产品列表页面'
        for price_limit in price_limit_list:
            # print price_limit
            print '--每个价格段都会有多个页面，循环抓取价格段页面',price_limit
            category_split_price_url_start = url_start_star + str(category_id) + '/' + str(category_name) + '/'
            category_split_price_url_end = '.html?' + url_select_str + '&maxPrice='  + str(price_limit['max_price']) + '&minPrice=' + str(price_limit['min_price'])
            self._deal_price_limit(price_limit, category_split_price_url_start,category_split_price_url_end, file_path, product_list_nedd, product_detail_nedd, is_just_download)

        return file_path

    def _deal_price_limit(self, price_limit, category_split_price_url_start,category_split_price_url_end, file_path, product_list_nedd, product_detail_nedd, is_just_download):
        """
        :param category_id:品类ID
        :param category_name:品类名
        :param price_limit:价格段
        :param url_start_star:url拼凑
        :param url_select_str:url拼凑
        :param file_path:文件路径
        :param product_list_nedd:是否需要下载产品列表
        :param product_detail_nedd:是否需要下载产品详情页
        :param image_nedd:是否需要保存图片
        :return:
        """

        price_file = str(price_limit['min_price']) + '_' + str(price_limit['max_price'])
        file_price_limit_list = file_path + os.sep + 'list' + os.sep + price_file

        now_number = 1
        self.threadpool = PoolManager(20)
        while now_number <= price_limit['page_number']:
            args_now =  [now_number,file_price_limit_list,price_limit, category_split_price_url_start, category_split_price_url_end, product_list_nedd, product_detail_nedd, is_just_download]
            self.threadpool.addJob(self._deal_price_limit_page, [args_now])
            now_number = now_number +1

        self.threadpool.wait_jobscomplete()
        self.threadpool.getResult()
        self.threadpool.close()

    def _deal_price_limit_page(self, args):
        try:
            now_number,file_price_limit_list,price_limit, category_split_price_url_start, category_split_price_url_end, product_list_nedd, product_detail_nedd, is_just_download= args
            product_list_pagenumber_temp_file_name = file_price_limit_list + os.sep + str(now_number)
            if product_list_nedd:
                category_split_price_url = category_split_price_url_start + str(now_number) + category_split_price_url_end
                print '通过url抓取产品列表页面',category_split_price_url
                product_list_status, product_list_html = self._get_simple_html(category_split_price_url, html_type='gzip')
                if product_list_status:
                    save_as_file(product_list_pagenumber_temp_file_name + '.html', product_list_html)
                    try:
                        product_list_html_str = gzip.GzipFile(fileobj=StringIO.StringIO(product_list_html)).read()
                    except Exception as e:
                        print 'product list is not a gzip file.'
                else:
                    print 'Get product list html error',category_split_price_url
                    return False
            else:
                # print '从系统中获取产品列表页面',product_list_pagenumber_temp_file_name,'.html'
                product_list_html_str = self.ungzip_html(product_list_pagenumber_temp_file_name + '.html')

            # print '获取产品列表页面结束,获取详细产品页面开始'
            if product_list_nedd:
                # print '开始解析产品列表文件:',product_list_pagenumber_temp_file_name + '.html'
                product_dict_list = self._reslove_html(product_list_html_str, 'list_product')
            else:
                # print '从产品列表文件中获取:',product_list_pagenumber_temp_file_name + '.csv'
                product_dict_list = []
                with open(product_list_pagenumber_temp_file_name + '.csv', 'r') as product_list_temp:
                    lines = product_list_temp.readlines()
                    [product_dict_list.append(eval(line)) for line in lines]

            product_dict_dict = {}
            print '++++获取产品列表的长度,页数：',now_number,'产品个数',len(product_dict_list)


            with open(product_list_pagenumber_temp_file_name + '.csv', 'w') as product_list_temp:
                for product_dict in product_dict_list:
                    product_dict_dict[product_dict['product_id']] = product_dict
                    product_list_temp.write(str(product_dict) + '\n')

                    if product_detail_nedd:
                        # print '开始下载详细产品文件'
                        product_url = self.product_detail_url %{'product_id' : product_dict['product_id'] }
                        product_list_status, product_html = self._get_simple_html(product_url, html_type='gzip')
                        if product_list_status == 'success':
                            save_as_file(file_price_limit_list.replace('list', 'detail') + os.sep + str(product_dict['product_id'])+'.html', product_html)
                            try:
                                product_html_str = gzip.GzipFile(fileobj=StringIO.StringIO(product_html)).read()
                            except Exception as e:
                                print 'product detail html is not a gzip',str(e)
                        else:
                            print 'Get product html error',product_url
                            continue

                        if is_just_download:
                            print '只下载数据，不解析'
                            continue

                    else:
                        # print '从文件中读取产品文件'
                        product_html_str = self.ungzip_html(file_price_limit_list.replace('list', 'detail') + os.sep + str(product_dict['product_id'])+'.html')

                    file_path_image = file_price_limit_list.replace('list', 'image')
                    prodcut_dict_list = self._get_product_detail_save_image_by_file_str(product_html_str, product_dict_dict, file_path_image=file_path_image)

                    with open(file_price_limit_list.replace('list','csv') + '.csv', 'a') as product_detail_temp:
                        for prodcut_dict in prodcut_dict_list:
                            product_detail_temp.write(str(prodcut_dict) + '\n')
        except Exception as e:
            print 'why have error:',str(e)


    def _get_product_detail_save_image_by_file_str(self, product_html_str, product_price_list_dict={}, file_path_image = None):
        """
        :param product_html_str:详细产品信息的html页面
        :param file_path_image: 需要保存图片的路径
        :param product_price_list_dict:产品对列表的依赖
        :return:
        """
        prodcut_dict_list = []
        product_price_dict = self._reslove_html(product_html_str, 'information_product')
        for product_information_index in product_price_dict:
            if product_price_dict[product_information_index]['img_list']:

                try:
                    image_name = file_path_image + os.sep + str(product_price_dict[product_information_index][self.product_detail_fiedld_dict['son_product_id']]) + '.' +  product_price_dict[product_information_index][self.product_detail_fiedld_dict['img_list']][-1].split('.')[-1]
                    image_url = product_price_dict[product_information_index][self.product_detail_fiedld_dict['img_list']][-1]
                    with open(file_path_image + '.csv', 'a') as temp_image_file:
                        temp_image_file.write(image_name + '\t' + image_url + '\n')
                    # urllib.urlretrieve(image_url, image_name)
                except Exception,e:
                    print 'save image error:',str(e), image_name, product_price_dict[product_information_index][self.product_detail_fiedld_dict['son_product_id']], product_price_dict[product_information_index][self.product_detail_fiedld_dict['img_list']][-1],str(e)

            temp_field_dict = {}
            for dont_need_field in self.dont_need_field_dict:
                temp_field_dict[dont_need_field] = self.dont_need_field_dict[dont_need_field]

            for product_list_field in self.product_list_field_dict:
                temp_field_dict[product_list_field] = product_price_list_dict[product_price_dict[product_information_index]['father_id']][self.product_list_field_dict[product_list_field]]

            for product_detail_field in self.product_detail_fiedld_dict:
                try:
                    temp_field_dict[product_detail_field] = product_price_dict[product_information_index][self.product_detail_fiedld_dict[product_detail_field]]
                except KeyError:
                    pass
                except Exception as e:
                    print 'set field key error:',str(e)
                    pass

            prodcut_dict_list.append(temp_field_dict)

        return prodcut_dict_list



class S3():
    """
    用来保存文件到S3的类
    """

    access_key = 'AKIAJQH5XY2NHA3SBQNA'
    secret_key = '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'
    bucket_name = 'product-hmtl-backup'
    image_bucket_name = 'product-image-keep' #alibaba-product
    file_size = 100 * 1024 *1024
    connect = None
    bucket = None

    def __init__(self, access_key=None, secret_key=None, bucket_name=None):
        if access_key and secret_key:
            self.access_key = access_key
            self.secret_key = secret_key

        if bucket_name:
            self.bucket_name = bucket_name

        self.connect = boto.connect_s3(self.access_key, self.secret_key)
        bucket_have = self.connect.lookup(self.bucket_name)
        if bucket_have is None:
            self.connect.create_bucket(self.bucket_name)

        self.bucket = self.connect.get_bucket(self.bucket_name, validate=True)

    def upload_image_list(self, image_list, policy='public-read'):
        """
        :param file_name:文件名列表
        :param policy: 文件访问权限
        :return:返回文件名的上传状态
        """

        return_list = []

        for file_name in image_list:

            file_name_tran = self.tran_file_name(file_name)
            file_size = os.stat(file_name).st_size

            file_key = boto.s3.key.Key(self.bucket)
            file_key.key = file_name_tran

            tran_size = file_key.set_contents_from_filename(file_name, policy=policy)
            if tran_size == file_size:
                return_url = 'https://s3.amazonaws.com/' + str(self.bucket_name) + file_name_tran
                return_list.append({'status' : True, 'url' : return_url, 'file' : file_name, 'file_key' : file_name_tran})
            else:
                return_list.append({'status' : False, 'file' : file_name})
        return return_list


    def upload_file_no_split(self, file_name_list, policy='public-read'):
        """
        :param file_name:文件名列表
        :param policy: 文件访问权限
        :return:返回文件名的上传状态
        """

        return_list = []

        for file_name in file_name_list:

            file_name_tran = self.tran_file_name(file_name)
            file_size = os.stat(file_name).st_size

            file_key = boto.s3.key.Key(self.bucket)
            file_key.key = file_name_tran

            tran_size = file_key.set_contents_from_filename(file_name, policy='public-read')
            if tran_size == file_size:
                return_url = 'https://s3.amazonaws.com/' + str(self.bucket_name) + file_name_tran
                return_list.append({'status' : True, 'url' : return_url, 'file' : file_name, 'file_key' : file_name_tran})
            else:
                return_list.append({'status' : False, 'file' : file_name})
        return return_list

    @staticmethod
    def tran_file_name(file_name):
        """
        :param file_name: 传入的文件名
        :return:传入到s3的key的值
        """

        file_name_tran = hashlib.md5(file_name).hexdigest()
        return file_name_tran

    def upload_file(self, file_name):
        """
        :param file_name:需要上传的文件
        :return:返回结果
        """
        try:
            file_name_tran = self.tran_file_name(file_name)
            file_size = os.stat(file_name).st_size
            chunk_count = int(math.ceil(file_size / float(self.file_size)))
            print 'upload file:',file_name, ',size:',file_size, ',total_count:',chunk_count

            mp = self.bucket.initiate_multipart_upload(file_name_tran)
            for i in range(chunk_count):
                offset = self.file_size * i
                bytes = min(self.file_size, file_size - offset)
                with FileChunkIO(file_name, 'r', offset=offset, bytes=bytes) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)
            mp.complete_upload()
            return {'result' : True, 'file_key' : file_name_tran, 'file' : file_name}
        except Exception as e:
            return {'result' : False, 'file' : file_name}

    def upload_files(self, files):
        return_list = []
        for file in files:
            file_upload = self.upload_file(file)
            with open('upload_history.csv', 'a') as temp_upload_file:
                temp_upload_file.write(str(file_upload) + '\n')
            return_list.append(file_upload)
        return return_list

    def delete_keys(self, keys):
        try:
            delete_keys_obj = self.bucket.delete_keys(keys=keys)
        except Exception as e:
            print 'Error when delte keys:', str(e)



if __name__ == '__main__':

    just_tar_and_s3 = True

    if just_tar_and_s3:
        f_name_pre = 'cameras_photo'
        #file_list = tar_gz_files(os.getcwd(), f_name_pre=f_name_pre)

        s3 = S3(bucket_name='ebay-html-backup')
        file_all=os.listdir(os.getcwd())
        file_list=[]
        for name in file_all:
            if name.find('.tar.gz')!=-1:
                file_list.append(name)
        upload_results = s3.upload_files(file_list)
        for upload_result in upload_results:
            if upload_result['result']:
                print 'Upload file to S3 result:',upload_result['file'], 'success,It object name is:',upload_result['file_key']
                # os.remove(upload_result['file'])
            else:
                print 'Upload file to S3 result:',upload_result['file'], 'failed, Please upload again'

        print 'Upload file to S3 end:', datetime.now().strftime('%F %T')
        print '-----------------------------------------------------------------'


    else:


        base_path = os.getcwd()
        alibaba = Alibaba()



        image, download, tar_gzip, s3, category, tran = False, True, True, False, False, False
        if category:
            print 'get category start:', datetime.now().strftime('%F %T')
            aa = alibaba.get_category_tree()
            with open('category.csv', 'w') as temp_file:
                for a in aa:
                    temp_file.write(str(aa[a]) + '\n')
            print 'get category end:', datetime.now().strftime('%F %T')
            print '-----------------------------------------------------------------'

        category_id_list = ['100006750', '200001025', '100006748', '100006745', '100006741', '200000092', '200000160', '200000147', '200000117']
        for category_id in category_id_list:
            print 'Get Category Start:',category_id,'-------------------------------'
            if download:
                print 'Get product start:',datetime.now().strftime('%F %T')
                file_path_root = alibaba.alibaba(category_id)
                print 'Get product result:',file_path_root
                print 'Get product end:',file_path_root,datetime.now().strftime('%F %T')
                print '-----------------------------------------------------------------'

            if tar_gzip:
                print 'Tar and GZ file start:', datetime.now().strftime('%F %T')
                tar_file_list = tar_gz_files(base_path + os.sep + file_path_root + os.sep + 'detail')
                print 'Tar and GZ file result:',tar_file_list
                print 'Tar and GZ file end:', datetime.now().strftime('%F %T')
                print '-----------------------------------------------------------------'


            if s3:
                print 'Upload file to S3 start:', datetime.now().strftime('%F %T')
                if True:
                    file_list_s3 = tar_file_list
                elif False:
                    file_path_root = 'alibaba/file/200000110/20150928'
                    file_list_s3 = []
                    file_s3_tar_list = os.listdir(base_path + os.sep + file_path_root + os.sep + 'detail')
                    for file_s3_name in file_s3_tar_list:
                        if not file_s3_name.endswith('.tar.gz'):
                            continue
                        file_list_s3.append(base_path + os.sep + file_path_root + os.sep + 'detail' + os.sep + file_s3_name)
                else:
                    file_list_s3 = ['/mnt/alibaba/alibaba/file/200000156/20150925/detail/10.0_10.25.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/10.25_10.5.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/10.75_11.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/11.25_11.5.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/11.875_12.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/128.0_160.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/13.0_13.25.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/13.5_13.75.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/13.75_14.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/1.375_1.5.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/14.5_14.75.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/14.75_15.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/160.0_192.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/16.0_16.5.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/1.625_1.75.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/17.0_17.5.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/1.75_1.875.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/18.0_18.5.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/1.875_2.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/192.0_224.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/19.75_20.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/20.0_20.5.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/2.125_2.25.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/21.5_22.0.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/22.0_22.5.tar.gz','/mnt/alibaba/alibaba/file/200000156/20150925/detail/224.0_256.0.tar.gz']

                s3 = S3()
                upload_results = s3.upload_files(file_list_s3)
                for upload_result in upload_results:
                    if upload_result['result']:
                        print 'Upload file to S3 result:',upload_result['file'], 'success,It object name is:',upload_result['file_key']
                        os.remove(upload_result['file'])
                    else:
                        print 'Upload file to S3 result:',upload_result['file'], 'failed, Please upload again'

                print 'Upload file to S3 end:', datetime.now().strftime('%F %T')
                print '-----------------------------------------------------------------'

            if image:
                file_path_root = 'alibaba/file/200000110/20150928'
                file_image_csv_list = os.listdir(base_path + os.sep + file_path_root  + os.sep + 'image')
                for file_image_name in file_image_csv_list:
                    # 对每个csv文件解析，抓取图片
                    if not file_image_name.endswith('.csv'):
                        continue
                    file_image_root = base_path + os.sep + file_path_root  + os.sep + 'image' + os.sep + file_image_name
                    save_image_by_file(file_image_root)

                print '-----------------------------------------------------------------'

            if tran:
                rsync_str_start = 'rsync -avzP'
                rsync_str_ssh = '-e "ssh -p 622"'
                rsync_str_destination = 'yiquan@50.17.126.11:/mnt/image/product_csv/'

                file_csv_rsync_list = os.listdir(base_path + os.sep + file_path_root  + os.sep + 'csv')
                for file_rsync_name in file_image_csv_list:
                    if not file_rsync_name.endswith('.csv'):
                        continue
                    rsync_str_original = base_path + os.sep + file_path_root  + os.sep + 'csv' + os.sep + file_rsync_name
                    rsync_str = '%(start)s %(ssh)s %(original)s %(destination)s' %{'start' : rsync_str_start, 'ssh' : rsync_str_ssh, 'original' : rsync_str_original,'destination' : rsync_str_destination}
                    rysnc_times = 0
                    result = os.popen(rsync_str)
                    with open('rsync_file.csv','a') as rsync_detail_file:
                        rsync_detail_file.write(rsync_str + '\t' + result + '\n')

                rsync_str_destination = 'yiquan@50.17.126.11:/mnt/image/image_csv/'
                file_csv_rsync_list = os.listdir(base_path + os.sep + file_path_root  + os.sep + 'image')
                for file_rsync_name in file_image_csv_list:
                    if not file_rsync_name.endswith('.csv'):
                        continue
                    rsync_str_original = base_path + os.sep + file_path_root  + os.sep + 'csv' + os.sep + file_rsync_name
                    rsync_str = '%(start)s %(ssh)s %(original)s %(destination)s' %{'start' : rsync_str_start, 'ssh' : rsync_str_ssh, 'original' : rsync_str_original,'destination' : rsync_str_destination}
                    rysnc_times = 0
                    result = os.popen(rsync_str)
                    with open('rsync_image.csv','a') as rsync_image_file:
                        rsync_image_file.write(rsync_str + '\t' + result + '\n')
