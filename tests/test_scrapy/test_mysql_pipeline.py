# tests/test_scrapy/test_mysql_pipeline.py
import unittest
from unittest.mock import patch, MagicMock, Mock
from weather_spider.pipelines import WeatherSpiderMySQLPipeline
from weather_spider.items import WeatherSpiderItem


class TestWeatherSpiderMySQLPipeline(unittest.TestCase):
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建测试数据
        self.test_item = WeatherSpiderItem(
            city="福州",
            date="15",
            temperature="25°C",
            weather="多云",
            crawl_time="2024-01-15 10:30:00",
        )
        
    @patch('weather_spider.pipelines.pymysql')
    def test_open_spider(self, mock_pymysql):
        """测试 open_spider 方法"""
        # 模拟数据库连接
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_pymysql.connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        pipeline = WeatherSpiderMySQLPipeline()
        mock_spider = MagicMock()
        
        # 执行测试
        pipeline.open_spider(mock_spider)
        
        # 验证数据库连接
        mock_pymysql.connect.assert_called_once()
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called()  # 验证创建表
        
    @patch('weather_spider.pipelines.pymysql')
    def test_process_item(self, mock_pymysql):
        """测试 process_item 方法"""
        # 模拟数据库连接
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_pymysql.connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        pipeline = WeatherSpiderMySQLPipeline()
        mock_spider = MagicMock()
        
        # 初始化管道
        pipeline.open_spider(mock_spider)
        
        # 执行测试
        result = pipeline.process_item(self.test_item, mock_spider)
        
        # 验证返回值
        self.assertEqual(result, self.test_item)
        
        # 验证数据插入
        mock_cursor.execute.assert_called()
        mock_connection.commit.assert_called()
        
    @patch('weather_spider.pipelines.pymysql')
    def test_close_spider(self, mock_pymysql):
        """测试 close_spider 方法"""
        # 模拟数据库连接
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_pymysql.connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        pipeline = WeatherSpiderMySQLPipeline()
        mock_spider = MagicMock()
        
        # 初始化管道
        pipeline.open_spider(mock_spider)
        
        # 执行测试
        pipeline.close_spider(mock_spider)
        
        # 验证连接关闭
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()


if __name__ == "__main__":
    unittest.main()