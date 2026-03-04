# tests/test_utils/test_exception_handler.py
import unittest
from tests.base_test import BaseTestCase
from weather_spider.utils.exception_handler import handle_exceptions


class TestExceptionHandler(BaseTestCase):

    def test_handler_with_re_raise(self):
        """测试异常处理（重新抛出）"""

        @handle_exceptions(logger_name="utils", re_raise=True)
        def test_func():
            raise ValueError("Test exception")

        with self.assertRaises(ValueError):
            test_func()

    def test_handler_without_re_raise(self):
        """测试异常处理（不重新抛出）"""

        @handle_exceptions(logger_name="utils", re_raise=False, default_return="error")
        def test_func():
            raise ValueError("Test exception")

        result = test_func()
        self.assertEqual(result, "error")

    def test_handler_no_exception(self):
        """测试无异常情况"""

        @handle_exceptions(logger_name="utils")
        def test_func():
            return "success"

        result = test_func()
        self.assertEqual(result, "success")


if __name__ == "__main__":
    unittest.main()
