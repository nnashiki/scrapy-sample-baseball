# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Item, Field

class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    domain = Field()
    title = Field()
    image_urls = Field()
    image_directory_name = Field()
    pass

    def __unicode__(self):
        return repr(self).decode('unicode_escape')

