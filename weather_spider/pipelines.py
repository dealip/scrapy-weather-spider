# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from weather_spider.utils.file_helper import FileHelper
import os
from weather_spider.utils.exception_handler import handle_exceptions
from weather_spider.utils.logger_helper import get_scrapy_logger
from config.config import (
    WEATHER_CSV,
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_CHARSET,
    DB_TABLE,
)
import pymysql
from pymysql.cursors import DictCursor


class WeatherSpiderPipeline:
    def open_spider(self, spider):
        # 配置日志 - 使用 scrapy 日志器
        self.logger = get_scrapy_logger()
        # 初始化文件助手
        self.file_helper = FileHelper()
        # 初始化csv文件
        self.fieldnames = ["city", "date", "temperature", "weather", "crawl_time"]
        # 确保目录存在
        os.makedirs(os.path.dirname(WEATHER_CSV), exist_ok=True)
        # 如果文件不存在或为空，创建并写入表头
        if not os.path.exists(WEATHER_CSV) or os.path.getsize(WEATHER_CSV) == 0:
            self.file_helper.write_csv(
                WEATHER_CSV,
                [],  # 空列表表示写入表头
                self.fieldnames,
            )
            self.logger.info(f"创建文件: {WEATHER_CSV}并写入表头")
        # 初始化item列表
        self.item = []

    @handle_exceptions(logger_name="scrapy", re_raise=False, default_return=None)
    def process_item(self, item, spider):
        self.item.append(dict(item))
        return item

    def close_spider(self, spider):
        # 写入数据
        if self.item:
            self.logger.info(f"开始写入{len(self.item)}条数据")
            self.file_helper.write_csv(
                WEATHER_CSV,
                self.item,
                self.fieldnames,
            )
            self.logger.info(f"成功写入{len(self.item)}条数据")
        else:
            self.logger.info("没有数据可写入")


class WeatherSpiderMySQLPipeline:
    """MySQL 数据库 Pipeline - 将爬取的数据存储到 MySQL 数据库"""

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.logger = None

    def open_spider(self, spider):
        """爬虫开始时建立数据库连接并创建表"""
        try:
            self.logger = get_scrapy_logger()
            self.logger.info("正在连接 MySQL 数据库...")

            self.connection = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset=DB_CHARSET,
                cursorclass=DictCursor,
            )

            self.cursor = self.connection.cursor()
            self.logger.info(f"成功连接到 MySQL 数据库: {DB_NAME}")

            self._create_table()
            self.logger.info("数据库表检查完成")

        except Exception as e:
            self.logger.error(f"连接 MySQL 数据库失败: {str(e)}")
            raise

    def _create_table(self):
        """创建数据表（如果不存在）"""
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS `{DB_TABLE}` (
            `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
            `city` VARCHAR(100) NOT NULL COMMENT '城市名称',
            `date` VARCHAR(20) NOT NULL COMMENT '日期',
            `temperature` VARCHAR(50) DEFAULT NULL COMMENT '温度',
            `weather` VARCHAR(50) DEFAULT NULL COMMENT '天气状况',
            `crawl_time` DATETIME NOT NULL COMMENT '爬取时间',
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
            INDEX `idx_city` (`city`),
            INDEX `idx_crawl_time` (`crawl_time`)
        ) ENGINE=InnoDB DEFAULT CHARSET={DB_CHARSET} COMMENT='天气数据表';
        """

        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            self.logger.info(f"数据表 {DB_TABLE} 已就绪")
        except Exception as e:
            self.logger.error(f"创建数据表失败: {str(e)}")
            raise

    @handle_exceptions(logger_name="scrapy", re_raise=False, default_return=None)
    def process_item(self, item, spider):
        """处理每个 item，插入到数据库"""
        try:
            insert_sql = f"""
            INSERT INTO `{DB_TABLE}` 
            (`city`, `date`, `temperature`, `weather`, `crawl_time`) 
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                item.get("city"),
                item.get("date"),
                item.get("temperature"),
                item.get("weather"),
                item.get("crawl_time"),
            )

            self.cursor.execute(insert_sql, values)
            self.connection.commit()

            self.logger.debug(f"数据插入成功: {item.get('city')}")

        except Exception as e:
            self.logger.error(f"插入数据失败: {str(e)}, 数据: {dict(item)}")
            self.connection.rollback()
            raise

        return item

    def close_spider(self, spider):
        """爬虫结束时关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

            self.logger.info("MySQL 数据库连接已关闭")

        except Exception as e:
            self.logger.error(f"关闭数据库连接时出错: {str(e)}")
