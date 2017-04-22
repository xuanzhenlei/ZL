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
from .items import EbaySpiderItem


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
            # tx.execute("select * from ebay_spider where title='%s'", item['title'])
            #
            # result = tx.fetchone()
            # if result:
            #     pass
            # else:
            tx.execute("insert into ebay_spider values(%s,%s,%s,%s,%s)", (
                item['title'], item['price'], item['currency'], item['watching'], item['appraisal_index']))
