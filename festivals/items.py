# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FestivalsItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    social = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()
    zip = scrapy.Field()
    city = scrapy.Field()
    isRegion = scrapy.Field()
    page_url = scrapy.Field()
    pass
