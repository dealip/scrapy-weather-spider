import scrapy.cmdline as cmdline
import sys
import os
from config.config import CLEANED_CITIES_CSV
from weather_spider.utils.logger_helper import get_scrapy_logger


class SpiderRunner:
    """爬虫运行器 - 支持测试模式、正式模式和定时爬取"""

    def __init__(self):
        self.logger = get_scrapy_logger()
        self.is_running = False

    def check_prerequisites(self):
        """检查运行爬虫的前置条件"""
        if not os.path.exists(CLEANED_CITIES_CSV):
            self.logger.error(f"未找到清洗后的城市编码文件 {CLEANED_CITIES_CSV}")
            self.logger.error("请先运行：python -m weather_spider.utils.clean_csv")
            return False

        self.logger.info(f"✅ 前置条件检查通过，找到城市编码文件：{CLEANED_CITIES_CSV}")
        return True

    def run_spider(self, test_mode=False):
        """
        运行爬虫，支持测试模式（仅爬少量城市）
        :param test_mode: True=测试模式，False=正式模式
        """
        if test_mode:
            cmd = "scrapy crawl china_weather -s CLOSESPIDER_ITEMCOUNT=2"
            self.logger.info("🔍 测试模式：仅爬取2条数据验证功能...")
        else:
            cmd = "scrapy crawl china_weather"
            self.logger.info("🚀 正式模式：全量爬取天气数据...")

        self.is_running = True
        try:
            cmdline.execute(cmd.split())
        except Exception as e:
            self.logger.error(f"爬虫运行失败：{str(e)}")
            raise
        finally:
            self.is_running = False

    def run_scheduled(self, interval_hours=24):
        """
        定时运行爬虫（预留接口，未来可扩展）
        :param interval_hours: 间隔小时数，默认24小时
        """
        self.logger.info(f"⏰ 定时爬取模式已启用，间隔：{interval_hours}小时")
        self.logger.info(
            "📝 注意：定时功能需要配合定时任务工具使用（如 APScheduler、crontab 等）"
        )
        self.logger.info(
            "💡 建议使用：schedule、APScheduler 或系统级定时任务（crontab/Windows 计划任务）"
        )

    def run_once(self, test_mode=False):
        """单次运行爬虫"""
        self.logger.info("🚀 天气爬虫开始运行...")

        if not self.check_prerequisites():
            sys.exit(1)

        self.run_spider(test_mode=test_mode)
        self.logger.info("✅ 天气爬虫运行完成！")

    def run(self):
        """主运行方法 - 根据命令行参数选择运行模式"""
        self.logger.info("🚀 天气爬虫启动器初始化完成")

        if not self.check_prerequisites():
            sys.exit(1)

        if len(sys.argv) > 1:
            mode = sys.argv[1]
            if mode == "test":
                self.run_spider(test_mode=True)
            elif mode == "scheduled":
                interval = int(sys.argv[2]) if len(sys.argv) > 2 else 24
                self.run_scheduled(interval_hours=interval)
            else:
                self.logger.warning(f"未知的运行模式：{mode}，使用默认正式模式")
                self.run_spider(test_mode=False)
        else:
            self.run_spider(test_mode=False)


if __name__ == "__main__":
    runner = SpiderRunner()
    runner.run()
