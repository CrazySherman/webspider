# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class YahooItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class NBAItem(scrapy.Item):
    players = scrapy.Field()
    pm = scrapy.Field()

class PlayerItem(scrapy.Item):
    name = scrapy.Field()
    stats = scrapy.Field()
