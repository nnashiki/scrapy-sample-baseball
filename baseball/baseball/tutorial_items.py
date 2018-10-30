# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Item, Field

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    domain = Field()
    title = Field()
    image_urls = Field()
    pass


