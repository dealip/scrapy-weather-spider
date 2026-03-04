# tests/test_pipelines/test_weather_spider_pipeline.py
import os
from tests.base_test import BaseTestCase
import unittest
import tempfile
import csv
from unittest.mock import patch, MagicMock
from weather_spider.pipelines import WeatherSpiderPipeline
from weather_spider.items import WeatherSpiderItem


class TestWeatherSpiderPipeline(BaseTestCase):

    def setUp(self):
        """测试前的准备工作"""
        # 创建临时目录和文件
        self.temp_dir = tempfile.mkdtemp()
        self.temp_csv = os.path.join(self.temp_dir, "weather.csv")

        # 使用patch临时替换WEATHER_CSV配置
        self.patcher = patch("weather_spider.pipelines.WEATHER_CSV", self.temp_csv)
        self.patcher.start()

        # 创建pipeline实例
        self.pipeline = WeatherSpiderPipeline()

        # 创建模拟的spider对象
        self.mock_spider = MagicMock()
        self.mock_spider.name = "china_weather"

        # 创建测试数据
        self.test_item = WeatherSpiderItem(
            city="福州",
            date="15",
            temperature="25°C",
            weather="多云",
            crawl_time="2024-01-15 10:30:00",
        )

        self.test_item2 = WeatherSpiderItem(
            city="厦门",
            date="15",
            temperature="26°C",
            weather="晴",
            crawl_time="2024-01-15 10:31:00",
        )

    def tearDown(self):
        """测试后的清理工作"""
        import shutil

        self.patcher.stop()
        shutil.rmtree(self.temp_dir)

    def _read_csv_content(self, csv_path):
        """读取CSV文件内容并返回数据行"""
        rows = []
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
        return rows

    # === 测试 open_spider 方法 ===
    def test_open_spider_creates_new_file(self):
        """测试open_spider：文件不存在时创建新文件并写入表头"""
        # 确保文件不存在
        self.assertFalse(os.path.exists(self.temp_csv))

        # 执行open_spider
        self.pipeline.open_spider(self.mock_spider)

        # 验证文件被创建
        self.assertTrue(os.path.exists(self.temp_csv))

        # 验证表头被正确写入
        rows = self._read_csv_content(self.temp_csv)
        self.assertEqual(len(rows), 0)  # 没有数据行

        # 验证字段列表被正确初始化
        expected_fields = ["city", "date", "temperature", "weather", "crawl_time"]
        self.assertEqual(self.pipeline.fieldnames, expected_fields)

    def test_open_spider_file_already_exists(self):
        """测试open_spider：文件已存在时不应该重复写入表头"""
        # 先创建一个已存在的文件
        os.makedirs(os.path.dirname(self.temp_csv), exist_ok=True)
        with open(self.temp_csv, "w", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["city", "date"])
            writer.writeheader()
            writer.writerow({"city": "test", "date": "test"})

        # 获取文件修改时间
        mod_time_before = os.path.getmtime(self.temp_csv)

        # 执行open_spider
        self.pipeline.open_spider(self.mock_spider)

        # 验证文件没有被重新创建（修改时间不变）
        mod_time_after = os.path.getmtime(self.temp_csv)
        self.assertEqual(mod_time_before, mod_time_after)

        # 验证原有数据还在
        rows = self._read_csv_content(self.temp_csv)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["city"], "test")

    def test_open_spider_empty_file(self):
        """测试open_spider：文件存在但为空时写入表头"""
        # 创建空文件
        os.makedirs(os.path.dirname(self.temp_csv), exist_ok=True)
        open(self.temp_csv, "w").close()

        # 执行open_spider
        self.pipeline.open_spider(self.mock_spider)

        # 验证表头被写入
        rows = self._read_csv_content(self.temp_csv)
        self.assertEqual(len(rows), 0)  # 只有表头，没有数据

        # 验证文件有内容
        self.assertGreater(os.path.getsize(self.temp_csv), 0)

    # === 测试 process_item 方法 ===
    def test_process_item_single_item(self):
        """测试process_item：处理单个item"""
        # 先执行open_spider初始化
        self.pipeline.open_spider(self.mock_spider)

        # 执行process_item
        result = self.pipeline.process_item(self.test_item, self.mock_spider)

        # 验证返回的是原item
        self.assertEqual(result, self.test_item)

        # 验证item被添加到列表中
        self.assertEqual(len(self.pipeline.item), 1)
        self.assertEqual(self.pipeline.item[0]["city"], "福州")

    def test_process_item_multiple_items(self):
        """测试process_item：处理多个item"""
        self.pipeline.open_spider(self.mock_spider)

        # 处理第一个item
        self.pipeline.process_item(self.test_item, self.mock_spider)
        self.assertEqual(len(self.pipeline.item), 1)

        # 处理第二个item
        self.pipeline.process_item(self.test_item2, self.mock_spider)
        self.assertEqual(len(self.pipeline.item), 2)
        self.assertEqual(self.pipeline.item[1]["city"], "厦门")

    def test_process_item_converts_to_dict(self):
        """测试process_item：确保item被转换为字典"""
        self.pipeline.open_spider(self.mock_spider)

        self.pipeline.process_item(self.test_item, self.mock_spider)

        # 验证存储的是字典而不是Item对象
        self.assertIsInstance(self.pipeline.item[0], dict)
        self.assertEqual(self.pipeline.item[0]["city"], "福州")

    @patch("weather_spider.pipelines.handle_exceptions")
    def test_process_item_exception_handling(self, mock_decorator):
        """测试process_item的异常处理装饰器"""
        # 验证process_item被装饰器包装
        self.assertTrue(hasattr(self.pipeline.process_item, "__wrapped__"))

    # === 测试 close_spider 方法 ===
    def test_close_spider_with_data(self):
        """测试close_spider：有数据时写入CSV"""
        self.pipeline.open_spider(self.mock_spider)

        # 添加测试数据
        self.pipeline.process_item(self.test_item, self.mock_spider)
        self.pipeline.process_item(self.test_item2, self.mock_spider)

        # 执行close_spider
        self.pipeline.close_spider(self.mock_spider)

        # 验证数据被写入文件
        rows = self._read_csv_content(self.temp_csv)
        self.assertEqual(len(rows), 2)

        # 验证第一条数据
        self.assertEqual(rows[0]["city"], "福州")
        self.assertEqual(rows[0]["date"], "15")
        self.assertEqual(rows[0]["temperature"], "25°C")
        self.assertEqual(rows[0]["weather"], "多云")

        # 验证第二条数据
        self.assertEqual(rows[1]["city"], "厦门")
        self.assertEqual(rows[1]["temperature"], "26°C")

    def test_close_spider_no_data(self):
        """测试close_spider：没有数据时不写入"""
        self.pipeline.open_spider(self.mock_spider)

        # 不添加任何数据，直接关闭
        self.pipeline.close_spider(self.mock_spider)

        # 验证文件只有表头，没有数据
        rows = self._read_csv_content(self.temp_csv)
        self.assertEqual(len(rows), 0)

    def test_close_spider_overwrites_existing(self):
        """测试close_spider：文件已存在时覆盖原有数据（符合业务逻辑）"""
        # 先创建已有数据的文件
        os.makedirs(os.path.dirname(self.temp_csv), exist_ok=True)
        with open(self.temp_csv, "w", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f, fieldnames=["city", "date", "temperature", "weather", "crawl_time"]
            )
            writer.writeheader()
            writer.writerow(
                {
                    "city": "existing",
                    "date": "1",
                    "temperature": "10°C",
                    "weather": "阴",
                    "crawl_time": "2024-01-01",
                }
            )

        self.pipeline.open_spider(self.mock_spider)
        self.pipeline.process_item(self.test_item, self.mock_spider)
        self.pipeline.close_spider(self.mock_spider)

        # 验证数据被覆盖（只有新增的1行，原有数据消失）
        rows = self._read_csv_content(self.temp_csv)
        self.assertEqual(len(rows), 1)  # 只有新数据，覆盖了原有数据
        self.assertEqual(rows[0]["city"], "福州")  # 验证是新数据

    # === 测试完整流程 ===
    def test_full_pipeline_flow(self):
        """测试完整的数据处理流程"""
        # 1. 打开spider
        self.pipeline.open_spider(self.mock_spider)

        # 2. 处理多个item
        items = [self.test_item, self.test_item2]
        for item in items:
            self.pipeline.process_item(item, self.mock_spider)

        # 3. 关闭spider
        self.pipeline.close_spider(self.mock_spider)

        # 4. 验证最终结果
        rows = self._read_csv_content(self.temp_csv)
        self.assertEqual(len(rows), 2)

        # 验证所有字段都存在
        expected_fields = set(["city", "date", "temperature", "weather", "crawl_time"])
        self.assertEqual(set(rows[0].keys()), expected_fields)


if __name__ == "__main__":
    unittest.main()
