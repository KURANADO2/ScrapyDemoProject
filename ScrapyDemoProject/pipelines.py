# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymongo


class ScrapydemoprojectPipeline:
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):
    def open_spider(self, spider):
        # 打开文件
        self.file = open('C:\\Users\\Administrator\\Desktop\\ted.json', 'w', encoding='UTF-8')

    def close_spider(self, spider):
        # 关闭文件
        self.file.close()

    # 处理 item
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        # 若还有其它 pipeline 需要使用该 item，则需要 return item 将 itme 传给下一个 pipeline
        return item


class MongoPipeline(object):

    # 定义数据库表名
    collection_name = 'ted'

    # 构造方法
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 调用构造方法
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        # 连接 Mongo
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
