# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from Fangtianxia.items import FangtianxiaItem,ESFItem
from pymongo import MongoClient

# class FangtianxiaPipeline:
#     def __init__(self):
#         self.newhouse_fp = open('newhouse.json','wb')
#         self.esf_fp = open('esfhouse.json','wb')
#         self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
#         self.esf_exporter = JsonLinesItemExporter(self.esf_fp,ensure_ascii=False)
#
#
#     def process_item(self, item, spider):
#         if isinstance(item,FangtianxiaItem):
#             self.newhouse_exporter.export_item(item)
#         else:
#             self.esf_exporter.export_item(item)
#         return item
#
#     def close_spider(self,spider):
#         self.newhouse_fp.close()
#         self.esf_fp.close()

class FangtianxiaMongoPipeline(object):
    def __init__(self):
        self.mongo_client = MongoClient(host='localhost',port=27017)
        self.db = self.mongo_client['fangtianxia']
        self.newhouse_col = self.db['NewHouse']
        self.esf_col = self.db['Esf']

    def process_item(self,item,spider):
        if isinstance(item, FangtianxiaItem):
            self.newhouse_col.insert_one(dict(item))
        else:
            self.esf_col.insert_one(dict(item))
        return item

    def close_spider(self,spider):
        self.mongo_client.close()