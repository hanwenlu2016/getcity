# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VipItem(scrapy.Item):
    phone = scrapy.Field()
    buy = scrapy.Field()
    create_time = scrapy.Field()
    city=scrapy.Field()
    province=scrapy.Field()