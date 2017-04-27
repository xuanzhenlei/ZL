# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class EbaySpiderPipeline(object):
#     def process_item(self, item, spider):
#         return item

from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import json
import codecs
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


# 存入数据库
class MySQLStorePipeline(object):
    """docstring for MySQLstor"""

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host='127.0.0.1',
                                            db='Spider',
                                            user='root',
                                            passwd='adminyazi',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=True
                                            )

    def process_item(self, item, spider):
        # run db query in thread pool
        self.dbpool.runInteraction(self._conditional_insert, item)
        return item
        # =======================================================================
        # asynItem=copy.deepcopy(item)
        # self.dbpool.runInteraction(self._conditional_insert,asynItem)
        # return asynItem

    def _conditional_insert(self, tx, item):
        # lentitle = len(item['title'])
        # item['price'] = lentitle
        # for n in range(lentitle):
        #     tx.execute("select * from ebay_spider where title=%s", (item['title'][n]))
        #     result = tx.fetchone()
        #     if result:
        #         pass
        #     else:
        #         tx.execute("insert into ebay_spider values(%s,%s,%s,%s,%s)", (item['title'], item['price'], item['currency'], item['watching'],item['appraisal_index']))
        # ===========================================================================================
        if item.get('title'):
            tx.execute("insert into ebay_spider values(%s,%s,%s,%s,%s,%s)", (
                item['title'], item['price'], item['currency'], item['watching'], item['appraisal_index'],
                item['image']))


# 存入json文件
class JsonWithEncodingEbayPipeline(object):
    def __init__(self):
        self.file = codecs.open('ebay.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 保存图片到文件夹
class ImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
