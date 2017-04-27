# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EbaySpiderItem(scrapy.Item):
    #title-标题,price-价格,currency-币种,watching-数值,appraisal_index-评价数
    title = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    watching = scrapy.Field()
    image=scrapy.Field()
    appraisal_index = scrapy.Field()