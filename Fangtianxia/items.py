# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtianxiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 1.省份
    province = scrapy.Field()
    # 2.城市
    city = scrapy.Field()
    # 3.地址
    address = scrapy.Field()
    # 4.名称
    name = scrapy.Field()
    # 5.住房类型
    type = scrapy.Field()
    # 6.房子面积
    area = scrapy.Field()
    # 7.单价
    price = scrapy.Field()
    # 8.是否在售
    insale = scrapy.Field()
    # 9.原始地址
    origin_url = scrapy.Field()

class ESFItem(scrapy.Item):
    # 1.省份
    province = scrapy.Field()
    # 2.城市
    city = scrapy.Field()
    # 3.地址
    address = scrapy.Field()
    # 4.小区名称
    name = scrapy.Field()
    # 5.房间规格
    type = scrapy.Field()
    # 6.面积
    area = scrapy.Field()
    # 7.楼层
    floor = scrapy.Field()
    # 8.朝向
    tarword = scrapy.Field()
    # 9.年代
    year = scrapy.Field()
    # 10.价格
    price = scrapy.Field()
    # 11.单价
    unit = scrapy.Field()
    # 12.原始链接
    origin_url = scrapy.Field()
