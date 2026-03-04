# 只在这一个文件中导入 get_logger，其他文件都从这里导入
from config.logger_config import get_logger


# 预设项目常用的 logger 名称，避免拼写错误
def get_scrapy_logger():
    """获取 Scrapy 框架专用 logger"""
    return get_logger("scrapy")


def get_spider_logger():
    """获取爬虫业务专用 logger"""
    return get_logger("spiders")


def get_utils_logger():
    """获取工具类专用 logger"""
    return get_logger("utils")


# 通用 logger 方法（兜底）
def get_default_logger(name: str = "default"):
    return get_logger(name)
