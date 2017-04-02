# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImgItem(scrapy.Item):
    # ImagesPipeline

    # image_urls mustbe list type or tuple type and etc =======
    image_urls = scrapy.Field()
    # person name
    images = scrapy.Field()
    album = scrapy.Field()
