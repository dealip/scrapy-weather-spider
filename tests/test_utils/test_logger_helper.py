# tests/test_utils/test_logger_helper.py
import unittest
from tests.base_test import BaseTestCase
from weather_spider.utils.logger_helper import (
    get_scrapy_logger,
    get_spider_logger,
    get_utils_logger,
    get_default_logger,
)


class TestLoggerHelper(BaseTestCase):

    def test_get_scrapy_logger(self):
        """测试获取Scrapy日志器"""
        logger = get_scrapy_logger()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "scrapy")

    def test_get_spider_logger(self):
        """测试获取爬虫日志器"""
        logger = get_spider_logger()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "spiders")

    def test_get_utils_logger(self):
        """测试获取工具日志器"""
        logger = get_utils_logger()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "utils")

    def test_get_default_logger(self):
        """测试获取默认日志器"""
        logger = get_default_logger("test")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test")


if __name__ == "__main__":
    unittest.main()
