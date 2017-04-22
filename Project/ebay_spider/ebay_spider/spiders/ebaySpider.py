#!/usr/bin/python
# -*- coding:utf-8 -*-
# from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from ebay_spider.items import EbaySpiderItem


# 针对一些禁止被爬的网站，设置header，就可以进行爬取
# def start_requests(self):
#     yield Request("star_urls",
#                   headers={'User-Agent': "your agent string"})


class EbaySpider(CrawlSpider):
    name = 'ebay'
    allowed_domains='ebay.com'
    start_urls = [
        'http://www.ebay.com/sch/Air-Guns-Slingshots/178886/i.html?LH_ItemCondition=3&LH_BIN=1&LH_RPA=1&_udlo=&_udhi=&LH_LocatedIn=1']

    def parse(self, response):
        selector = Selector(response)
        infos = selector.xpath("//ul[@id='ListViewInner']/li")

        for info in infos:
            Ebay = EbaySpiderItem()
            title1 = info.xpath('h3/a/text()').extract()[0]
            price1 = info.xpath('ul[1]/li[1]/span/text()').extract()[1]
            currency = info.xpath('ul[1]/li[1]/span/b/text()').extract()[0]
            watching1 = info.xpath('ul[1]/li[@class="lvextras"]/div/div/text()').extract()
            appraisal_index = info.xpath('div[2]/a[2]/text()').extract()

            title = title1.replace("\n", "").replace("\r", "").replace("\t", "")
            # 获取的watching为list,将list转化为string,去除\n\t,以字符串进行显示
            watching2 = ''.join(watching1)
            watching = watching2.replace("\n", "").replace("\t", "")
            price=price1.replace(",","")
            if appraisal_index:
                pass
            else:
                appraisal_index=" "

            Ebay['title'] = title
            Ebay['price'] = price
            Ebay['currency'] = currency
            Ebay['watching'] = watching
            Ebay['appraisal_index'] = appraisal_index
            yield Ebay
