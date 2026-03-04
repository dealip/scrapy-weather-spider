# config.py
import os
from dotenv import load_dotenv
# 添加项目核心目录到Python搜索路径
from weather_spider.utils.path_helper import (
    get_project_root,
    get_project_path,
    get_data_path,
)
# 加载 .env 文件
load_dotenv()



# 项目根目录
PROJECT_ROOT = get_project_root()
# 日志目录（自动创建）
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 数据文件路径
RAW_CITIES_CSV = get_data_path("raw", "cities_original.csv")
CLEANED_CITIES_CSV = get_data_path("cleaned", "cities_valid.csv")
WEATHER_CSV = get_project_path("export_data", "weather.csv")

# 配置Selenium WebDriver
CHROME_PATH = r"E:/Google/Chrome/Application/chrome.exe"  # 按自己Chrome安装路径填写
CHROME_DRIVER_PATH = get_project_path(
    "tools", "chromedriver.exe"
)  # 需安装对应自己Chrome版本的driver并在tools文件夹中替换掉

# MySQL 数据库配置
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "weather_spider")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")
DB_TABLE = os.getenv("DB_TABLE", "weather_data")
