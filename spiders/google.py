# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from items import *


class GoogleSpider(CrawlSpider):
    name = "google"
    #
    # allowed_domains = ["play.google.com"]
    # start_urls = ["https://play.google.com/store/apps/details?id=com.rayark.implosion"]

    allowed_domains = ["play.google.com"]
    start_urls = [
        'http://play.google.com/',
        'https://play.google.com/store/apps/details?id=com.viber.voip'
    ]
    rules = [
        Rule(LinkExtractor(allow=("https://play.google.com/store/apps/details",)), callback='parse_app', follow=True),
    ]  # CrawlSpider 会根据 rules 规则爬取页面并调用函数进行处理
    # //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/div[1]/div/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/div/text()
    # //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[x]/div[1]/div[2]/div[2]/div/text()

    # //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[x]
    # main: //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[x]/div[1]
    # producer reply: //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[x]/div[2]

    # app_name: //*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div/div[2]/h1/div/text()
    # app_category: //*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div/div[3]/a/span/text()
    # title: //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[10]/div[1]/div[2]/span/text()
    # content: ('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[10]/div[1]/div[2]/text()').extract()[1]
    # author name: //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[10]/div[1]/div[1]/div[1]/span/a/text()
    # author link: //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[10]/div[1]/div[1]/div[1]/span/a/@href
    # date: //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[10]/div[1]/div[1]/div[1]/span[2]/text()
    # rating: //*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[10]/div[1]/div[1]/div[1]/div[2]/div[1]/@aria-label
    def parse_app(self, response):
        items = []
        p = 2
        sel = Selector(response)
        app_name = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/text()').extract()[0]
        category = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div/div[3]/a/span/text()').extract()[0]
        developer = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div/div[2]/a/span/text()').extract()[0]

        while p:
            item = GoogleplayItem()
            if not sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[' + str(p) + ']').extract():
                break
            item['app_name'] = app_name
            item['app_category'] = category
            item['developer'] = developer
            # print '//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[' + str(p) + ']/div[1]/div[1]/div[1]/span/a/text()'
            name = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[' + str(p) + ']/div[1]/div[1]/div[1]/span/a/text()').extract()
            if not name:
                item['name'] = None
            else:
                item['name'] = name[0]
            link = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[' + str(p) + ']/div[1]/div[1]/div[1]/span/a/@href').extract()
            if not link:
                item['link'] = None
            else:
                item['link'] = 'https://play.google.com' + link[0]
            title = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[' + str(p) + ']/div[1]/div[2]/span/text()').extract()
            if not title:
                item['title'] = None
            else:
                item['title'] = title[0]
            content = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[' + str(p) + ']/div[1]/div[2]/text()').extract()
            if len(content) <= 1:
                item['content'] = None
            else:
                item['content'] = content[1]
            date = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[' + str(p) + ']/div[1]/div[1]/div[1]/span[2]/text()').extract()
            if not date:
                item['date'] = None
            else:
                item['date'] = date[0]
            rank = sel.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[' + str(p) + ']/div[1]/div[1]/div[1]/div[2]/div[1]/@aria-label').extract()
            if not rank:
                item['rank'] = None
            else:
                item['rank'] = str(rank[0])[7]
            if item['name'] is not None:
                items.append(item)
            p += 1
        return items

