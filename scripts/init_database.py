"""
MySQL 数据库初始化脚本
用于创建数据库和配置

使用方法：
    python -m scripts.init_database
"""

import sys
import os


import pymysql
from config.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_CHARSET,
    DB_TABLE,
)
from weather_spider.utils.logger_helper import get_utils_logger


def create_database():
    """创建数据库（如果不存在）"""
    logger = get_utils_logger()

    try:
        logger.info(f"正在连接 MySQL 服务器: {DB_HOST}:{DB_PORT}")

        # 先连接到 MySQL 服务器（不指定数据库）
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            charset=DB_CHARSET,
        )

        cursor = connection.cursor()

        # 创建数据库
        create_db_sql = f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET {DB_CHARSET} COLLATE {DB_CHARSET}_unicode_ci"
        cursor.execute(create_db_sql)

        logger.info(f"✅ 数据库 '{DB_NAME}' 创建成功")

        cursor.close()
        connection.close()

        return True

    except Exception as e:
        logger.error(f"❌ 创建数据库失败: {str(e)}")
        return False


def create_table():
    """创建数据表"""
    logger = get_utils_logger()

    try:
        logger.info(f"正在连接数据库: {DB_NAME}")

        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset=DB_CHARSET,
        )

        cursor = connection.cursor()

        # 创建数据表
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

        cursor.execute(create_table_sql)
        connection.commit()

        logger.info(f"✅ 数据表 '{DB_TABLE}' 创建成功")

        cursor.close()
        connection.close()

        return True

    except Exception as e:
        logger.error(f"❌ 创建数据表失败: {str(e)}")
        return False


def test_connection():
    """测试数据库连接"""
    logger = get_utils_logger()

    try:
        logger.info("正在测试数据库连接...")

        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset=DB_CHARSET,
        )

        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()

        logger.info("✅ 数据库连接成功")
        logger.info(f"📊 MySQL 版本: {version[0]}")

        # 检查表是否存在
        cursor.execute(f"SHOW TABLES LIKE '{DB_TABLE}'")
        table_exists = cursor.fetchone()

        if table_exists:
            logger.info(f"✅ 数据表 '{DB_TABLE}' 已存在")
        else:
            logger.warning(f"⚠️  数据表 '{DB_TABLE}' 不存在，需要创建")

        cursor.close()
        connection.close()

        return True

    except Exception as e:
        logger.error(f"❌ 数据库连接失败: {str(e)}")
        return False


def show_config():
    """显示当前配置"""
    logger = get_utils_logger()

    logger.info("=" * 50)
    logger.info("MySQL 数据库配置信息")
    logger.info("=" * 50)
    logger.info(f"主机: {DB_HOST}:{DB_PORT}")
    logger.info(f"用户: {DB_USER}")
    logger.info(f"密码: {'*' * len(DB_PASSWORD) if DB_PASSWORD else '(未设置)'}")
    logger.info(f"数据库: {DB_NAME}")
    logger.info(f"字符集: {DB_CHARSET}")
    logger.info(f"数据表: {DB_TABLE}")
    logger.info("=" * 50)


def main():
    """主函数"""
    logger = get_utils_logger()

    print("\n" + "=" * 50)
    print("MySQL 数据库初始化工具")
    print("=" * 50 + "\n")

    # 显示配置
    show_config()

    print("\n请选择操作:")
    print("1. 测试数据库连接")
    print("2. 创建数据库")
    print("3. 创建数据表")
    print("4. 初始化数据库和表（完整初始化）")
    print("5. 退出")
    print()

    choice = input("请输入选项 (1-5): ").strip()

    if choice == "1":
        test_connection()
    elif choice == "2":
        create_database()
    elif choice == "3":
        create_table()
    elif choice == "4":
        logger.info("开始完整初始化...")
        if create_database():
            create_table()
            logger.info("✅ 初始化完成！")
        else:
            logger.error("❌ 初始化失败！")
    elif choice == "5":
        logger.info("退出程序")
        return
    else:
        logger.error("❌ 无效的选项")

    print()


if __name__ == "__main__":
    main()
