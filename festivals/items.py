# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FestivalsItem(scrapy.Item):
    FESTIVAL_NAME = scrapy.Field()
    EVENT_ON = scrapy.Field()
    CATEGORY = scrapy.Field()
    URL = scrapy.Field()
    SOCIAL = scrapy.Field()
    EMAIL = scrapy.Field()
    ADDRESS = scrapy.Field()
    ZIP_CODE = scrapy.Field()
    CITY = scrapy.Field()
    isRegion = scrapy.Field()
    page_url = scrapy.Field()
    pass
