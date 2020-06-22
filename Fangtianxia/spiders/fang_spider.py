# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_redis.spiders import RedisSpider
from Fangtianxia.items import FangtianxiaItem,ESFItem


class FangSpiderSpider(RedisSpider):
    name = 'fang_spider'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fang:start_urls"

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//strong/text()").get()
            province_text = re.sub('None','',str(province_text)).strip()
            if province_text:
                province = province_text
            if province == "其他":
                    continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath("./text()").get()
                link = city_link.xpath(".//@href").get()
                url_split = link.split(".")
                preffix = url_split[0]
                domain = url_split[1]
                # 新房链接
                newhouse_url = preffix + ".newhouse." + domain + ".com/house/s/"
                # 二手房链接
                esf_url = preffix + ".esf." + domain + ".com/"
                yield  scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"info":(province,city)})
                yield  scrapy.Request(url=esf_url,callback=self.parse_esf,meta={"info":(province,city)})

    def parse_newhouse(self,response):
        province,city = response.meta.get("info")

        uls = response.xpath("//div[contains(@class,'nl_con')]//ul/li")
        for ul in uls:
            address = ul.xpath(".//div[@class='address']/a/@title").get()
            name = ul.xpath(".//div[@class='nlcd_name']/a/text()").get()
            name = str(name).strip()
            type = ul.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            area = "".join(ul.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r"\s|－|/","",area)
            number = ul.xpath(".//div[@class='nhouse_price']/span/text()").get()
            unit = ul.xpath(".//div[@class='nhouse_price']/em/text()").get()
            price = str(number) + str(unit)
            insale = ul.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            origin_url = ul.xpath(".//div[@class='nlcd_name']/a/@href").get()
            origin_url = response.urljoin(origin_url)
            item = FangtianxiaItem(
                province=province,city=city,address=address,name=name,
                type=type,area=area,price=price,insale=insale,origin_url=origin_url
            )
            yield item
        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        next_url = response.urljoin(next_url)
        if next_url:
            yield scrapy.Request(url=next_url,callback=self.parse_newhouse,meta={"info":(province,city)})

    def parse_esf(self,response):
        province,city = response.meta.get("info")
        item = ESFItem(province=province,city=city)
        dls = response.xpath("//div[contains(@class,'shop_list')]/dl")
        for dl in dls:
            item['address'] = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            item['name']= dl.xpath(".//p[@class='add_shop']/a/@title").get()
            infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
            infos = list(map(lambda x:re.sub(r"\s","",x),infos))
            for info in infos:
                if "厅" in info:
                    item['type'] = info
                elif "㎡" in info:
                    item['area'] = info
                elif "层" in info:
                    item['floor'] = info
                elif "向" in info:
                    item['tarword'] = info
                elif "年" in info:
                    item['year'] = info
            item['price'] = "".join(dl.xpath(".//span[@class='red']//text()").getall())
            item['unit'] = dl.xpath(".//dd[@class='price_right']/span[2]/text()").get()
            item['origin_url'] = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").get())
            yield item
        next_url = response.xpath("//div[@class='page_al']/p[1]/a/@href").get()
        next_url = response.urljoin(next_url)
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse_esf, meta={"info": (province, city)})
