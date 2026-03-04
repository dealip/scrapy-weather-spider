import scrapy
from datetime import datetime
from config.config import CLEANED_CITIES_CSV
from weather_spider.items import WeatherSpiderItem
from weather_spider.utils.file_helper import FileHelper


class ChinaWeatherSpider(scrapy.Spider):
    name = "china_weather"
    allowed_domains = ["weather.com.cn"]
    start_urls = ["https://weather.com.cn/weather1d/101230112.shtml"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化文件助手实例
        self.file_helper = FileHelper()

    # 重写start_requuest,主动生成请求
    def start_requests(self):
        try:
            # 1.读取csv
            rows = self.file_helper.read_csv(CLEANED_CITIES_CSV)
            for row in rows:
                city_code = row.get("城市编码", "").strip()
                if not city_code:
                    continue
                url = f"https://www.weather.com.cn/weather1d/{city_code}.shtml"
                yield scrapy.Request(url=url, callback=self.parse)
        except FileNotFoundError:
            self.logger.error("csv文件不存在，请检查路径！")
        except StopIteration:
            self.logger.warning("csv文件没有数据！")
        except Exception:
            self.logger.error("加载csv失败！")

    def parse(self, response):
        """解析天气数据"""
        try:
            # 1. 提取城市名称
            city_parts = []
            city_name = response.xpath(
                '//div[@class="left-div"]/div[contains(@class,"ctop")]/div[contains(@class,"crumbs")]/a[2]/text()'
            )
            if city_name:
                city_parts.append(city_name.get().strip())
            urban_name = response.xpath(
                '//div[@class="left-div"]/div[contains(@class,"ctop")]/div[contains(@class,"crumbs")]/a[3]/text()'
            )
            if urban_name:
                city_parts.append(urban_name.get().strip())
            region_name = response.xpath(
                '//div[@class="left-div"]/div[contains(@class,"ctop")]/div[contains(@class,"crumbs")]/span[last()]/text()'
            )
            if region_name:
                city_parts.append(region_name.get().strip())
            city = " ".join(city_parts)
            # 2. 提取今日日期
            date = response.xpath('//div[@class="t"]/ul/li[1]/h1/text()')
            if date:
                date = date.get().split("日")[0]
            # 3.提取天气情况
            weather = response.xpath(
                '//ul[@class="clearfix"]/li[1]/p[@class="wea"]/text()'
            ).get()
            # 4 提取温度
            temperature = response.xpath(
                '//div[@id="today"]/div[@class="t"]/div/div[@class="tem"]/span/text()'
            )
            temperature = temperature.get().strip() if temperature else ""
            item = WeatherSpiderItem()
            item["city"] = city
            item["date"] = date
            item["weather"] = weather
            item["temperature"] = temperature
            item["crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info(f"爬取数据成功：{item}")
            yield item
        except Exception:
            self.logger.error("解析天气数据失败")
