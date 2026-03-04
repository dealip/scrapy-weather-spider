# 🌤️ 中国天气爬虫项目

一个基于 Scrapy 的企业级天气数据爬虫，支持多城市天气数据抓取、数据清洗、CSV 导出和 MySQL 数据库存储。

## 🎯 功能特性

- **多城市支持**：从全国多个城市抓取天气数据
- **数据清洗**：自动清洗和标准化城市数据
- **双格式导出**：同时导出到 CSV 文件和 MySQL 数据库
- **定时爬取**：支持定时自动爬取天气数据
- **企业级架构**：模块化设计，易于维护和扩展
- **详细日志**：完整的日志记录系统
- **测试覆盖**：完善的单元测试

## 🛠️ 技术栈

- **核心框架**：Python 3.8+, Scrapy
- **数据存储**：CSV, MySQL
- **数据处理**：Pandas
- **自动化**：Schedule, Selenium
- **配置管理**：python-dotenv
- **测试**：pytest
- **代码质量**：Flake8, Black

## 📁 项目结构

```
weather_spider/
├── 📁 weather_spider/           # 爬虫核心代码
│   ├── 📁 spiders/              # 爬虫定义
│   ├── 📁 items.py              # 数据模型
│   ├── 📁 middlewares.py        # 中间件
│   ├── 📁 pipelines.py          # 数据处理管道
│   ├── 📁 run_spider.py         # 爬虫运行入口
│   └── 📁 settings.py           # 项目配置
├── 📁 scripts/                  # 脚本工具
│   ├── 📁 init_database.py      # 数据库初始化
│   └── 📁 scheduled_spider.py   # 定时爬虫
├── 📁 config/                   # 配置文件
│   └── 📁 config.py             # 全局配置
├── 📁 docs/                     # 文档
│   ├── 📁 MYSQL_QUICKSTART.md   # MySQL 快速开始
│   └── 📁 SCHEDULED_SPIDER_README.md # 定时爬虫说明
├── 📁 export_data/              # 导出数据
├── 📁 logs/                     # 日志文件
├── 📁 tests/                    # 测试代码
├── 📄 .env.example              # 环境变量示例
├── 📄 .gitignore                # Git 忽略文件
├── 📄 PROJECT_STRUCTURE.md      # 项目结构说明
├── 📄 requirements.txt          # 依赖包
└── 📄 README.md                 # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd weather_spider

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置数据库

```bash
# 复制环境变量文件
# Windows
copy .env.example .env
# Linux/Mac
cp .env.example .env

# 编辑 .env 文件，设置数据库连接信息
```

### 3. 初始化数据库

```bash
python -m scripts.init_database
# 选择 4. 初始化数据库和表（完整初始化）
```

### 4. 运行爬虫

```bash
# 测试模式（只爬取少量数据）
python -m weather_spider.run_spider test

# 正式模式（爬取所有城市数据）
python -m weather_spider.run_spider
```

## 📊 数据输出

### CSV 文件
- **路径**：`export_data/weather.csv`
- **格式**：包含城市、日期、温度、天气状况、爬取时间

### MySQL 数据库
- **数据库**：`weather_spider`
- **表名**：`weather_data`
- **字段**：id, city, date, temperature, weather, crawl_time, created_at

## 🔄 定时爬取

### 使用 schedule 库

```bash
# 每24小时运行一次
python -m scripts.scheduled_spider schedule 24

# 立即运行一次
python -m scripts.scheduled_spider once
```

### 系统定时任务

- **Windows**：使用 `scripts/setup_scheduled_task.bat`
- **Linux**：使用 `scripts/setup_crontab.sh`

## 🔧 常见问题

### Q: 为什么控制台没有显示 MySQL 保存的日志？
**A:** Scrapy 默认只显示 `ERROR` 级别的日志。如果没有错误信息，说明数据库保存成功。

### Q: 数据库连接失败怎么办？
**A:** 检查 `.env` 文件中的数据库配置，确保 MySQL 服务正在运行。

## 📚 文档

- **MySQL 配置**：[docs/MYSQL_QUICKSTART.md](docs/MYSQL_QUICKSTART.md)
- **定时爬取**：[docs/SCHEDULED_SPIDER_README.md](docs/SCHEDULED_SPIDER_README.md)
- **项目结构**：[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 🧪 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行代码风格检查
python run_check.py
```

## 🤝 贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目使用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- **作者**：[Lin Chen]
- **Email**：[1835929226@qq.com]
- **GitHub**：[dealip]

---

⭐ 如果这个项目对你有帮助，请给它一个星标！