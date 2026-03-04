import os
import csv
from weather_spider.utils.path_helper import get_project_root
from weather_spider.utils.logger_helper import get_utils_logger


class FileHelper:
    """
    文件操作工具类
    职责：统一处理文件读写、目录创建等通用文件操作
    """

    def __init__(self):
        # 初始化日志
        self.logger = get_utils_logger()
        # 初始化项目根目录（实例化时只计算一次，提升效率）
        self.project_root = get_project_root()

    def read_csv(self, csv_path: str) -> list:
        """
        读取CSV文件
        :param csv_path: CSV文件绝对路径
        :return: CSV数据列表
        """
        if not os.path.exists(csv_path):
            self.logger.error(f"CSV文件不存在！{csv_path}")
            raise FileNotFoundError(f"CSV文件不存在！{csv_path}")

        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
        self.logger.info(f"成功读取CSV文件：{csv_path}，共{len(rows)}行数据")
        return rows

    def write_csv(self, csv_path: str, rows: list, fieldnames: list) -> None:
        """
        写入CSV文件,自动判断是否需要写入表头
        :param csv_path: CSV文件绝对路径
        :param rows: CSV数据列表
        :param fieldnames: CSV字段列表
        :return: None
        """
        with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            # 检查是否需要写入表头
            if f.tell() == 0:
                writer.writeheader()
            if rows:
                writer.writerows(rows)
        self.logger.info(f"成功写入CSV文件：{csv_path}，共{len(rows)}行数据")
