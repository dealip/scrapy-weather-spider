import sys

import csv
import time
import requests
from weather_spider.utils.exception_handler import handle_exceptions
from weather_spider.utils.logger_helper import get_utils_logger
from weather_spider.utils.file_helper import FileHelper
from config.config import RAW_CITIES_CSV, CLEANED_CITIES_CSV


class CityCsvCleaner:
    def __init__(self):
        self.file_helper = FileHelper()
        # 获取清洗脚本专属日志器
        self.logger = get_utils_logger()
        self.invalid_codes = []
        self.valid_codes = []
        self.total = 0
        self.valid = 0

    @handle_exceptions(logger_name="utils", re_raise=False, default_return=False)
    def is_city_weather_page_valid(self, city_code):
        """
        校验单个地区编码是否能访问到有效天气页面
        :param city_code: 地区编码
        :return: True=有效，False=无效
        """
        url = f"https://www.weather.com.cn/weather1d/{city_code}.shtml"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if len(response.content) <= 400:
            return False
        return True

    def clean_city_csv(self, original_csv, cleaned_csv):
        """
        清洗原始CSV，只保留有效地区编码
        :param original_csv: 原始CSV路径
        :param cleaned_csv: 清洗后CSV路径
        """
        # 1. 读取原始CSV表头
        with open(original_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
        # 2.遍历校验，过滤有效行
        valid_rows = []
        with open(original_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.total += 1
                city_code = row.get("城市编码", "").strip()
                if not city_code:
                    self.invalid_codes.append(f"空编码：{city_code}")
                    continue

                # 校验编码有效性
                time.sleep(0.5)
                if self.is_city_weather_page_valid(city_code):
                    self.valid += 1
                    valid_rows.append(row)
                else:
                    self.invalid_codes.append(f"无效编码：{city_code}")
                    self.logger.info(f"无效编码：{city_code}")
        # 3.写入清洗后的CSV
        with open(cleaned_csv, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(valid_rows)

        # 4.输出清洗报告
        self.logger.info("\n===== 清洗报告 =====")
        self.logger.info(f"原始总行数：{self.total}")
        self.logger.info(f"有效行数：{self.valid}")
        self.logger.info(f"无效行数：{self.total - self.valid}")
        self.logger.info(f"\n✅ 清洗完成！纯净CSV已保存至：{cleaned_csv}")


def main():
    logger = get_utils_logger()
    try:
        cleaner = CityCsvCleaner()
        cleaner.logger.info(f"开始清洗CSV：{RAW_CITIES_CSV}")
        cleaner.clean_city_csv(RAW_CITIES_CSV, CLEANED_CITIES_CSV)
        cleaner.logger.info(f"清洗完成！纯净CSV已保存至：{CLEANED_CITIES_CSV}")
    except Exception as e:
        logger.error(f"清洗CSV时出错：{str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
