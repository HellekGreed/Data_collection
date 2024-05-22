# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from pymongo import MongoClient
import os
from imgparser.settings import IMAGES_STORE, BOT_NAME
import csv

class ImgparserPipeline:


    def __init__(self):

        client = MongoClient('localhost', 27017)
        self.mongo_base = client.images

    def process_item(self, item, spider):



        collection = self.mongo_base[spider.name]
        if item.get('path'):
            collection.insert_one(item)

        return item


class PhotosPipeline(ImagesPipeline):

    count_img = 0

    def get_media_requests(self, item, info):

        try:
            self.count_img += 1
            print(f'Обработано {self.count_img} ссылок')
            yield scrapy.Request(item['url'])
        except Exception as e:
            print(e)


    def file_path(self, request, response=None, info=None, *, item=None):

        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        file_name = f"{item['name']}-{image_guid}.jpg"
        basedir = str(os.path.abspath(os.path.dirname(__file__))
                      ).replace(BOT_NAME, '')
        file_path = os.path.join(basedir + IMAGES_STORE, file_name)
        item['path'] = f'{file_path}'
        item['_id'] = f'{image_guid}'

        return file_name
