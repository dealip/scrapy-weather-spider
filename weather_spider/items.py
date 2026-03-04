# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherSpiderItem(scrapy.Item):
    # 城市名称
    city = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 天气状况
    weather = scrapy.Field()
    # 温度
    temperature = scrapy.Field()
    # 爬取时间
    crawl_time = scrapy.Field()
