# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleplayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    app_name = scrapy.Field()
    app_category = scrapy.Field()
    title = scrapy.Field()
    rank = scrapy.Field()
    content = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    developer = scrapy.Field()
    # index = scrapy.Field()
    # title = scrapy.Field()
    # text = scrapy.Field()
    # author = scrapy.Field()
    # rate = scrapy.Field()
    #
    pass
