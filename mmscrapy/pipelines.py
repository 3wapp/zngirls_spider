# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from mmscrapy.settings import BASEURL


class MmPipeline(object):
    def process_item(self, item, spider):
        return item


class PicPipeline(ImagesPipeline):
    """
    图片下载有缓存机制，计算下载图片链接的hash值，如果图片保存路径下存在该hash的图片时，
    默认不下载，做测试时最好删除下载的图片后再爬取图片，或者使用代理服务器查看请求
    """
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            request = Request(image_url,
                              headers={'Referer': BASEURL},
                              meta={'item': item})
            # set proxy to watch request
            request.meta['proxy'] = 'http://127.0.0.1:8080'
            yield request

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        """
        重写文件名，带文件路径
        """
        item = request.meta['item']
        # 从URL提取图片的文件名
        image_guid = request.url.split('/')[-1]
        filename = 'full/{0[images]}/{0[album]}//{1}'.format(item, image_guid)
        return filename
