import logging
import logging.config
import sys
import os

# 添加项目核心目录到Python搜索路径
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_path not in sys.path:
    sys.path.append(project_path)
# 安全导入
try:
    from weather_spider.utils.path_helper import get_project_root
except ImportError:
    # 如果导入失败，确保路径已添加
    sys.path.append(project_path)
    from weather_spider.utils.path_helper import get_project_root

# 获取日志目录路径
LOG_DIR = os.path.join(get_project_root(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger_config():
    """
    核心规则：
    1. 所有日志统一格式，包含时间、模块名、级别、信息
    2. 按模块拆分日志文件（utils/爬虫/清洗脚本各一个日志文件）
    3. 日志文件按日期滚动，避免单个文件过大
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    # 统一日志格式
    LOG_FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    # 日期格式
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # 日志配置字典（Scrapy也兼容这种格式）
    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                # 标准格式（全项目复用)
                "format": LOG_FORMAT,
                "datefmt": DATE_FORMAT,
            }
        },
        "handlers": {
            # 控制台输出
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            # utils模块日志文件
            "utils_file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(LOG_DIR, "utils.log"),
                "maxBytes": 1024 * 1024 * 3,
                "backupCount": 3,
                "encoding": "utf-8",
                "formatter": "standard",
            },
            # 爬虫模块日志文件（Scrapy共用）
            "spider_file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(LOG_DIR, "spider.log"),
                "maxBytes": 1024 * 1024 * 50,
                "backupCount": 5,
                "encoding": "utf-8",
                "formatter": "standard",
            },
            # 清洗脚本专属日志（可选，也可复用utils.log）
            "clean_csv_file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(LOG_DIR, "clean_csv.log"),
                "maxBytes": 1024 * 1024 * 50,
                "backupCount": 5,
                "encoding": "utf-8",
                "formatter": "standard",
            },
        },
        "loggers": {
            # utils模块的日志器
            "utils": {
                "handlers": ["console", "utils_file"],
                "level": "INFO",
                "propagate": False,  # 不向上传递日志
            },
            # 爬虫模块的日志器（Scrapy爬虫共用）
            "spiders": {
                "handlers": ["console", "spider_file"],
                "level": "INFO",
                "propagate": False,
            },
            # 让爬虫继承 spiders 的配置
            "china_weather": {  # 具体爬虫名称
                "handlers": ["console", "spider_file"],
                "level": "INFO",
                "propagate": False,
            },
            # 清洗脚本专属日志器
            "clean_csv": {
                "handlers": ["console", "clean_csv_file"],
                "level": "INFO",
                "propagate": False,
            },
            # Scrapy核心日志器（兼容Scrapy的日志）
            "scrapy": {
                "handlers": ["console", "spider_file"],
                "level": "WARNING",  # 降低Scrapy默认日志级别，避免刷屏
                "propagate": False,
            },
        },
    }
    return logger_config


# 初始化全局日志配置
logging.config.dictConfig(get_logger_config())


# 提供通用的获取日志器函数
def get_logger(logger_name: str) -> logging.Logger:
    """
    获取指定名称的日志器（统一入口）
    :param logger_name: 日志器名（utils/spiders/clean_csv）
    :return: 配置好的日志器
    """
    return logging.getLogger(logger_name)
