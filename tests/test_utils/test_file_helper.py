# tests/test_utils/test_file_helper.py
import os
from tests.base_test import BaseTestCase
import unittest
import tempfile
from weather_spider.utils.file_helper import FileHelper


class TestFileHelper(BaseTestCase):

    def setUp(self):
        self.file_helper = FileHelper()
        # 创建临时测试文件
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.temp_dir, "test.csv")

        # 创建测试CSV文件
        with open(self.test_csv, "w", encoding="utf-8") as f:
            f.write("name,age\n")
            f.write("Alice,25\n")
            f.write("Bob,30\n")

    def tearDown(self):
        # 清理临时文件
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_read_csv(self):
        """测试读取CSV文件"""
        rows = list(self.file_helper.read_csv(self.test_csv))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["name"], "Alice")
        self.assertEqual(rows[1]["age"], "30")

    def test_write_csv(self):
        """测试写入CSV文件"""
        test_data = [{"name": "Charlie", "age": "35"}, {"name": "David", "age": "40"}]
        output_csv = os.path.join(self.temp_dir, "output.csv")

        self.file_helper.write_csv(output_csv, test_data, ["name", "age"])

        # 验证写入结果
        self.assertTrue(os.path.exists(output_csv))
        rows = list(self.file_helper.read_csv(output_csv))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["name"], "Charlie")


if __name__ == "__main__":
    unittest.main()
