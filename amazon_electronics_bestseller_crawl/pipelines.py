# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

# class AmazonElectronicsBestsellerCrawlPipeline(object):
#   def process_item(self, item, spider):
#       return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            host=settings['MONGODB_SERVER'],
            port=settings['MONGODB_PORT'],
            username=settings['MONGODB_USER'],
            password=settings['MONGODB_PASSWORD'],
            authSource=settings['MONGODB_AUTH_SOURCE'],
            authMechanism=settings['MONGODB_AUTH_MECHANISM']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")

        document = item.copy()
        del document['asin']

        self.collection.update(
            {'_id': item['asin']}, dict(document), upsert=True)
        log.msg("Question added to MongoDB database!",
                level=log.DEBUG, spider=spider)
        return item
