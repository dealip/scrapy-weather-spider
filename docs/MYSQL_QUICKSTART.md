# MySQL 数据库快速开始指南

## 🚀 5分钟快速配置

### 步骤1：安装依赖

```bash
pip install pymysql python-dotenv
```

### 步骤2：配置数据库连接

复制 `.env.example` 为 `.env`，并修改配置：

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root              # 改为你的 MySQL 用户名
DB_PASSWORD=your_password # 改为你的 MySQL 密码
DB_NAME=weather_spider
DB_CHARSET=utf8mb4
DB_TABLE=weather_data
```

### 步骤3：初始化数据库

```bash
python -m scripts.init_database
```

选择 `4. 初始化数据库和表（完整初始化）`

### 步骤4：运行爬虫

```bash
# 测试模式
python -m weather_spider.run_spider test

# 正式模式
python -m weather_spider.run_spider
```

## ✅ 验证数据

### 如何判断数据库保存成功

当你运行爬虫时，Scrapy 默认只在控制台显示 `ERROR` 级别的日志。如果控制台没有显示数据库相关的错误信息，说明：

- ✅ **数据库连接成功**
- ✅ **数据插入成功**
- ✅ **MySQL 管道正常工作**

**注意**：MySQL 管道的 `INFO` 级别的日志（如 "成功连接到 MySQL 数据库"、"数据插入成功"）默认不会在控制台显示，但这并不影响数据的正常保存。

### 方法1：使用 MySQL 命令行

```bash
mysql -u root -p

# 切换到数据库
USE weather_spider;

# 查看数据
SELECT * FROM weather_data ORDER BY crawl_time DESC LIMIT 10;

# 统计数据量
SELECT COUNT(*) as total FROM weather_data;
```

### 方法2：使用 Python 脚本

```python
import pymysql
from config.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

connection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset='utf8mb4'
)

cursor = connection.cursor()
cursor.execute("SELECT * FROM weather_data ORDER BY crawl_time DESC LIMIT 10")
results = cursor.fetchall()

for row in results:
    print(f"城市: {row['city']}, 天气: {row['weather']}, 时间: {row['crawl_time']}")

cursor.close()
connection.close()
```

## 📊 数据同时导出到

- ✅ **CSV 文件**：`export_data/weather.csv`
- ✅ **MySQL 数据库**：`weather_data` 表

## 🔧 常见问题

### 问题1：连接数据库失败

**检查项：**
1. MySQL 服务是否正在运行
2. `.env` 文件中的用户名和密码是否正确
3. 端口是否正确（默认 3306）

**解决方法：**
```bash
# 测试连接
python -m scripts.init_database
# 选择 1. 测试数据库连接
```

### 问题2：数据库不存在

**解决方法：**
```bash
python -m scripts.init_database
# 选择 4. 初始化数据库和表（完整初始化）
```

### 问题3：中文乱码

**检查项：**
1. `.env` 文件中 `DB_CHARSET=utf8mb4`
2. 数据库和表的字符集为 `utf8mb4`

## 📝 下一步

- 📖 阅读详细配置指南：[MYSQL_SETUP_GUIDE.md](MYSQL_SETUP_GUIDE.md)
- 🔄 设置定时爬取：[SCHEDULED_SPIDER_README.md](SCHEDULED_SPIDER_README.md)
- 📊 数据分析和可视化

## 💡 提示

- ⚠️ **不要将 `.env` 文件提交到版本控制**（已添加到 `.gitignore`）
- 🔒 使用强密码保护数据库
- 💾 定期备份数据库
- 📋 查看日志文件了解运行状态：`logs/scrapy_weather.log`
