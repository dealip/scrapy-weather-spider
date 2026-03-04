# tests/base_test.py
import sys
import unittest
from pathlib import Path


# 自动检测项目根目录
class TestEnvironment:
    """测试环境管理器"""

    __test__ = False  # 关键：跳过这个类的测试收集

    def __init__(self):
        self.current_file = Path(__file__).resolve()
        self.project_root = self._find_project_root()
        self._setup_paths()

    def _find_project_root(self):
        """智能查找项目根目录（包含 setup.py 或特定目录的）"""
        current = self.current_file.parent
        while current != current.parent:
            # 检查是否是项目根目录
            if (
                (current / "setup.py").exists()
                or (current / "weather_spider").exists()
                or (current / "tests").exists()
            ):
                return current
            current = current.parent
        return self.current_file.parent.parent  # 默认返回上级的上级

    def _setup_paths(self):
        """设置 Python 路径"""
        if str(self.project_root) not in sys.path:
            sys.path.insert(0, str(self.project_root))

        # 自动导入并调用 add_project_path
        try:
            from weather_spider.utils.path_helper import add_project_path

            add_project_path()
        except ImportError:
            print("Warning: Could not import path_helper")


# 创建全局环境实例
env = TestEnvironment()


class BaseTestCase(unittest.TestCase):
    """测试基类"""

    @classmethod
    def setUpClass(cls):
        cls.env = env  # 所有子类共享同一个环境
        print(f"Project root: {cls.env.project_root}")
