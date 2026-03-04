# 项目结构说明

本文档说明天气爬虫项目的文件组织结构，帮助你快速定位文件。

## 📁 目录结构

```
weather_spider/
├── 📁 config/                    # 配置文件
│   ├── config.py                 # 主配置（数据库、路径等）
│   └── logger_config.py          # 日志配置
│
├── 📁 weather_spider/            # 爬虫核心代码
│   ├── 📁 spiders/               # 爬虫
│   │   └── china_weather.py      # 中国天气爬虫
│   ├── 📁 utils/                 # 工具类
│   │   ├── clean_csv.py          # CSV 数据清洗
│   │   ├── exception_handler.py  # 异常处理
│   │   ├── file_helper.py        # 文件操作
│   │   ├── logger_helper.py      # 日志工具
│   │   └── path_helper.py        # 路径工具
│   ├── items.py                  # 数据模型
│   ├── middlewares.py            # 中间件
│   ├── pipelines.py              # 数据管道（CSV + MySQL）
│   ├── run_spider.py             # 爬虫运行器
│   └── settings.py               # Scrapy 配置
│
├── 📁 tests/                     # 测试代码
│   ├── test_scrapy/              # Scrapy 相关测试
│   └── test_utils/               # 工具类测试
│
├── 📁 scripts/                   # ✅ 脚本工具（新增）
│   ├── init_database.py          # 数据库初始化
│   ├── scheduled_spider.py       # 定时爬虫
│   ├── setup_crontab.sh          # Linux 定时任务配置
│   └── setup_scheduled_task.bat  # Windows 定时任务配置
│
├── 📁 docs/                      # ✅ 文档（新增）
│   ├── MYSQL_QUICKSTART.md       # MySQL 快速开始
│   ├── MYSQL_SETUP_GUIDE.md      # MySQL 完整配置指南
│   └── SCHEDULED_SPIDER_README.md # 定时爬虫说明
│
├── 📁 data/                      # 数据文件
│   ├── raw/                      # 原始数据
│   └── cleaned/                  # 清洗后的数据
│
├── 📁 export_data/               # 导出数据
│   └── weather.csv               # 爬取的天气数据
│
├── 📁 logs/                      # 日志文件
├── 📁 tools/                     # 外部工具
│   └── chromedriver.exe          # Chrome 驱动
│
├── 📄 .env                       # 环境变量（数据库配置等）
├── 📄 .env.example               # 环境变量模板
├── 📄 requirements.txt           # Python 依赖
├── 📄 run_check.py               # 代码检查工具
├── 📄 scrapy.cfg                 # Scrapy 配置
└── 📄 README.md                  # 项目说明
```

## 🎯 文件分类逻辑

### 1. 配置文件 (`config/`)
- **作用**：集中管理所有配置
- **文件**：数据库连接、日志配置、路径配置等
- **修改频率**：低（部署时配置一次）

### 2. 爬虫核心 (`weather_spider/`)
- **作用**：爬虫的核心业务代码
- **文件**：爬虫、管道、中间件、工具类等
- **修改频率**：中（业务逻辑调整）

### 3. 测试代码 (`tests/`)
- **作用**：单元测试和集成测试
- **文件**：测试用例、测试基类等
- **修改频率**：中（功能迭代时更新）

### 4. 脚本工具 (`scripts/`)
- **作用**：运维脚本和工具脚本
- **文件**：
  - `init_database.py` - 数据库初始化
  - `scheduled_spider.py` - 定时爬虫
  - `setup_crontab.sh` - Linux 定时任务配置
  - `setup_scheduled_task.bat` - Windows 定时任务配置
- **修改频率**：低（配置好后很少修改）
- **使用方法**：
  ```bash
  python -m scripts.init_database
  python -m scripts.scheduled_spider once
  ```

### 5. 文档 (`docs/`)
- **作用**：项目文档和使用说明
- **文件**：
  - `MYSQL_QUICKSTART.md` - MySQL 快速开始
  - `MYSQL_SETUP_GUIDE.md` - MySQL 完整配置
  - `SCHEDULED_SPIDER_README.md` - 定时爬虫说明
- **修改频率**：低（文档更新）

### 6. 数据文件 (`data/`, `export_data/`)
- **作用**：存储数据文件
- **文件**：原始数据、清洗后的数据、导出数据
- **修改频率**：高（每次爬取都会更新）
- **注意**：已添加到 `.gitignore`，不会被提交

### 7. 日志文件 (`logs/`)
- **作用**：存储运行日志
- **文件**：爬虫日志、工具日志等
- **修改频率**：高（每次运行都会更新）
- **注意**：已添加到 `.gitignore`，不会被提交

## 🔍 快速定位文件

### 想要运行爬虫？
```bash
# 测试模式
python -m weather_spider.run_spider test

# 正式模式
python -m weather_spider.run_spider
```

### 想要配置数据库？
```bash
# 1. 编辑配置文件
.env

# 2. 初始化数据库
python -m scripts.init_database

# 3. 查看文档
docs/MYSQL_QUICKSTART.md
```

### 想要设置定时爬取？
```bash
# 1. 查看文档
docs/SCHEDULED_SPIDER_README.md

# 2. 运行定时爬虫
python -m scripts.scheduled_spider once

# 3. 配置系统定时任务（Windows）
scripts/setup_scheduled_task.bat

# 4. 配置系统定时任务（Linux/Mac）
scripts/setup_crontab.sh
```

### 想要查看数据？
```bash
# CSV 文件
export_data/weather.csv

# MySQL 数据库
# 使用 MySQL 客户端连接查看
```

### 想要修改配置？
```bash
# 数据库配置
.env

# 爬虫配置
weather_spider/settings.py

# 日志配置
config/logger_config.py
```

### 想要运行测试？
```bash
# 所有测试
pytest tests/

# 特定测试
pytest tests/test_scrapy/
pytest tests/test_utils/
```

## 📝 文件命名规范

### Python 文件
- 使用小写字母和下划线：`file_helper.py`
- 类名使用驼峰命名：`FileHelper`
- 函数名使用小写下划线：`write_csv()`

### 文档文件
- 使用大写字母和下划线：`MYSQL_SETUP_GUIDE.md`
- 清晰表达文档内容

### 脚本文件
- Shell 脚本：`.sh` 后缀
- Batch 脚本：`.bat` 后缀
- Python 脚本：`.py` 后缀

## 🚫 不要修改的文件

以下文件是自动生成的，不需要手动修改：
- `__pycache__/` - Python 缓存文件
- `.pytest_cache/` - 测试缓存
- `htmlcov/` - 测试覆盖率报告
- `logs/` - 日志文件（可以查看，但不要手动修改）

## ✅ 需要关注的文件

以下文件是项目核心，需要重点关注：
- `.env` - 环境变量（包含敏感信息，不要提交）
- `weather_spider/pipelines.py` - 数据管道
- `weather_spider/settings.py` - 爬虫配置
- `config/config.py` - 主配置

## 🔧 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行代码检查
python run_check.py

# 运行测试
pytest tests/ -v

# 运行爬虫（测试模式）
python -m weather_spider.run_spider test

# 运行爬虫（正式模式）
python -m weather_spider.run_spider

# 初始化数据库
python -m scripts.init_database

# 定时爬虫（单次）
python -m scripts.scheduled_spider once

# 定时爬虫（schedule 库）
python -m scripts.scheduled_spider schedule 24

# 定时爬虫（APScheduler）
python -m scripts.scheduled_spider apscheduler 12
```

## 📚 相关文档

- [MYSQL_QUICKSTART.md](docs/MYSQL_QUICKSTART.md) - MySQL 快速开始
- [MYSQL_SETUP_GUIDE.md](docs/MYSQL_SETUP_GUIDE.md) - MySQL 完整配置
- [SCHEDULED_SPIDER_README.md](docs/SCHEDULED_SPIDER_README.md) - 定时爬虫说明

## 💡 提示

1. **`.env` 文件**：包含敏感信息，已添加到 `.gitignore`，不会被提交
2. **`scripts/` 目录**：使用 `python -m scripts.xxx` 方式运行
3. **`docs/` 目录**：所有文档都在这里，按需求查阅
4. **定期清理**：`logs/` 和 `export_data/` 目录会不断增长，定期清理旧文件

---

**最后更新**：2026-03-04
**维护者**：Weather Spider Team
