"""
定时爬取天气数据示例
支持多种定时任务工具：schedule、APScheduler、系统级定时任务

使用方法：
    python -m scripts.scheduled_spider once          # 单次运行
    python -m scripts.scheduled_spider schedule 24   # 使用 schedule 库，每24小时运行一次
    python -m scripts.scheduled_spider apscheduler 12 # 使用 APScheduler，每12小时运行一次
"""

import sys
import os

import time
import schedule
from datetime import datetime
from weather_spider.run_spider import SpiderRunner


def run_with_schedule(interval_hours=24):
    """
    使用 schedule 库实现定时爬取（简单易用）
    :param interval_hours: 间隔小时数，默认24小时
    """
    runner = SpiderRunner()

    def job():
        runner.logger.info(
            f"⏰ 定时任务触发 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        runner.run_once(test_mode=False)

    schedule.every(interval_hours).hours.do(job)

    runner.logger.info(f"⏰ 定时爬取已启动，间隔：{interval_hours}小时")
    runner.logger.info("💡 按 Ctrl+C 停止定时任务")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        runner.logger.info("⏹️ 定时任务已停止")


def run_with_apscheduler(interval_hours=24):
    """
    使用 APScheduler 实现定时爬取（功能强大，适合生产环境）
    :param interval_hours: 间隔小时数，默认24小时
    """
    from apscheduler.schedulers.blocking import BlockingScheduler

    runner = SpiderRunner()
    scheduler = BlockingScheduler()

    def job():
        runner.logger.info(
            f"⏰ 定时任务触发 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        runner.run_once(test_mode=False)

    scheduler.add_job(job, "interval", hours=interval_hours)

    runner.logger.info(f"⏰ 定时爬取已启动，间隔：{interval_hours}小时")
    runner.logger.info("💡 按 Ctrl+C 停止定时任务")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        runner.logger.info("⏹️ 定时任务已停止")
        scheduler.shutdown()


def run_once_example():
    """单次运行示例"""
    runner = SpiderRunner()
    runner.run_once(test_mode=False)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法：")
        print("  python scheduled_spider.py once          # 单次运行")
        print(
            "  python scheduled_spider.py schedule 24   # 使用 schedule 库，每24小时运行一次"
        )
        print(
            "  python scheduled_spider.py apscheduler 12 # 使用 APScheduler，每12小时运行一次"
        )
        print("\n💡 推荐使用 APScheduler，功能更强大，适合生产环境")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "once":
        run_once_example()
    elif mode == "schedule":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        run_with_schedule(interval_hours=interval)
    elif mode == "apscheduler":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        run_with_apscheduler(interval_hours=interval)
    else:
        print(f"❌ 未知的模式：{mode}")
        sys.exit(1)
