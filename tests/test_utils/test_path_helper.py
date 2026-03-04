# tests/test_utils/test_path_helper.py
import os
from tests.base_test import BaseTestCase
import unittest
from weather_spider.utils.path_helper import (
    add_project_path,
    get_project_root,
    get_project_path,
)


class TestPathHelper(BaseTestCase):

    def setUp(self):
        # 确保项目路径已添加
        add_project_path()

    def test_get_project_root(self):
        """测试获取项目根目录"""
        root_path = get_project_root()
        self.assertTrue(os.path.exists(root_path))
        self.assertTrue(os.path.exists(os.path.join(root_path, "scrapy.cfg")))

    def test_get_project_path(self):
        """测试获取项目内路径"""
        config_path = get_project_path("config", "config.py")
        self.assertTrue(os.path.exists(config_path))

        utils_path = get_project_path("weather_spider", "utils")
        self.assertTrue(os.path.exists(utils_path))

    def test_add_project_path(self):
        """测试添加项目路径"""
        import sys

        root_path = get_project_root()
        self.assertIn(root_path, sys.path)


if __name__ == "__main__":
    unittest.main()
