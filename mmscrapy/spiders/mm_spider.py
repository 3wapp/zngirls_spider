# -*- coding: utf-8 -*-

from urllib.parse import urljoin
import scrapy
from scrapy import Request
from mmscrapy.items import ImgItem
from mmscrapy.settings import BASEURL


class MMSpider(scrapy.Spider):
    name = 'mm'
    allow_domain = [
        'www.zngirls.com',
        't2.onvshen.com'
    ]

    def __init__(self):
        self.headers = {
            'Referer': BASEURL
        }
        super().__init__()

    def start_requests(self):
        urls = [
            urljoin(BASEURL, 'rank/sum/'),
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        for li in response.xpath('//li[@class="rankli"]'):
            url = li.xpath('.//div[@class="rankli_imgdiv"]/a/@href'
                           ).extract_first()
            rank = li.xpath('.//span[@class="rank_num"]/text()'
                            ).extract_first()
            name = li.xpath('.//span[@class="rank_name"]//font/text()'
                            ).extract_first()

            name = '{0:0>3}{1}'.format(rank.strip('.'), name)

            url = urljoin(BASEURL, '{}album/'.format(url))
            yield Request(url=url, meta={'name': name}, callback=self.parse_img)

    def parse_img(self, response):
        name = response.meta['name']
        for li in response.xpath('//li[@class="igalleryli"]'):
            url = li.xpath('.//a/@href').extract_first()
            url = urljoin(BASEURL, url)
            title = li.xpath('.//a/img/@title').extract_first()
            print(url)
            request = Request(url=url,
                              headers=self.headers,
                              callback=self.parse_pic)
            # set proxy to watch request
            # request.meta['proxy'] = 'http://127.0.0.1:8080'
            request.meta['name'] = name
            request.meta['album'] = title
            yield request

    def parse_pic(self, response):
        name = response.meta['name']
        album = response.meta['album']
        urls = (_.extract() for _ in response.xpath('//ul[@id="hgallery"]/img/@src'))
        yield ImgItem(image_urls=urls, images=name, album=album)

        next_page = response.xpath('//div[@id="pages"]/a/@href')[-1].extract()
        if next_page.endswith('.html'):
            url = urljoin(BASEURL, next_page)
            yield Request(url,
                          headers=self.headers,
                          meta={'name': name, 'album': album},
                          callback=self.parse_pic)
