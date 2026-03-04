# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.config import CHROME_PATH, CHROME_DRIVER_PATH
from selenium.webdriver.chrome.service import Service
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# useful for handling different item types with a single interface
from weather_spider.utils.logger_helper import get_scrapy_logger


class WeatherSpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # matching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class WeatherSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class WeatherSpiderSeleniumMiddleware:
    """Selenium 下载中间件 - 用于处理动态加载的页面"""

    def __init__(self):
        self.logger = get_scrapy_logger()
        self.driver = None
        self.request_count = 0
        self.max_requests = 30
        self._init_driver()

    def _init_driver(self):
        # 初始化Selenium WebDriver
        chrome_options = Options()
        chrome_driver_path = CHROME_DRIVER_PATH
        chrome_options.binary_location = CHROME_PATH
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")

        try:
            service = Service(chrome_driver_path)
            self.driver = webdriver.Chrome(options=chrome_options, service=service)
            self.logger.info("Selenium WebDriver 初始化成功（无头模式）")
        except Exception as e:
            self.logger.error(f"初始化 WebDriver 失败: {str(e)}")
            self.logger.error(f"Chrome 路径: {CHROME_PATH}")
            self.logger.error(f"ChromeDriver 路径: {chrome_driver_path}")
            raise

    def _restart_driver(self):
        self.logger.info(f"已处理 {self.request_count} 次请求，重新启动 WebDriver...")
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            self.logger.warning(f"关闭 WebDriver 时出错: {str(e)}")
            raise
        self._init_driver()
        self.request_count = 0
        self.logger.info("WebDriver 重新启动成功")

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_closed(self, spider):
        self.logger.info(f"Spider 关闭，总共处理了 {self.request_count} 次请求")
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("WebDriver 已关闭")
        except Exception as e:
            self.logger.warning(f"关闭 WebDriver 时出错: {str(e)}")

    def process_request(self, request, spider):
        url = request.url
        driver = self.driver

        try:
            driver.get(url)
            # 等待指定温度元素出现
            wait = WebDriverWait(driver, 4)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tem")))
            html = driver.page_source
            self.request_count += 1

            if self.request_count >= self.max_requests:
                self._restart_driver()

            return HtmlResponse(url=url, body=html, encoding="utf-8", request=request)
        except Exception as e:
            spider.logger.error(f"Selenium 处理请求失败: {url}, 错误: {str(e)}")
            return HtmlResponse(url=url, body="", encoding="utf-8", request=request)
