# MySQL 数据库配置和使用指南

## 一、.env 文件位置

`.env` 文件应放在项目的**根目录**下：

```
weather_spider/
├── .env                    # ← 环境变量配置文件（放在这里）
├── config/
│   └── config.py
├── weather_spider/
│   ├── pipelines.py
│   └── settings.py
└── requirements.txt
```

## 二、配置步骤

### 1. 安装依赖

```bash
pip install pymysql python-dotenv
```

或者更新 requirements.txt：

```bash
pip install -r requirements.txt
```

### 2. 配置 .env 文件

编辑 `.env` 文件，填入你的 MySQL 数据库信息：

```env
# MySQL 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username      # 改为你的 MySQL 用户名
DB_PASSWORD=your_password  # 改为你的 MySQL 密码
DB_NAME=weather_spider     # 数据库名称
DB_CHARSET=utf8mb4

# 数据表配置
DB_TABLE=weather_data       # 数据表名称
```

### 3. 创建数据库和表

使用初始化脚本创建数据库和表：

```bash
python -m scripts.init_database
```

选择操作：
- 1. 测试数据库连接
- 2. 创建数据库
- 3. 创建数据表
- 4. 初始化数据库和表（完整初始化）

**推荐选择 4**，进行完整初始化。

### 4. 启用 MySQL Pipeline

在 `weather_spider/settings.py` 中，MySQL Pipeline 已经默认启用：

```python
ITEM_PIPELINES = {
    "weather_spider.pipelines.WeatherSpiderPipeline": 300,        # CSV 导出
    "weather_spider.pipelines.WeatherSpiderMySQLPipeline": 400,   # MySQL 导出
}
```

## 三、数据表结构

MySQL Pipeline 会自动创建以下数据表：

```sql
CREATE TABLE `weather_data` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `city` VARCHAR(100) NOT NULL COMMENT '城市名称',
    `date` VARCHAR(20) NOT NULL COMMENT '日期',
    `temperature` VARCHAR(50) DEFAULT NULL COMMENT '温度',
    `weather` VARCHAR(50) DEFAULT NULL COMMENT '天气状况',
    `crawl_time` DATETIME NOT NULL COMMENT '爬取时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    INDEX `idx_city` (`city`),
    INDEX `idx_crawl_time` (`crawl_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='天气数据表';
```

**字段说明：**
- `id`: 主键ID，自增
- `city`: 城市名称，如 "北京 城区"
- `date`: 日期，如 "26"
- `temperature`: 温度，可能为空
- `weather`: 天气状况，如 "多云"
- `crawl_time`: 爬取时间，如 "2026-02-26 12:41:08"
- `created_at`: 记录创建时间，自动生成

## 四、运行爬虫

### 测试模式

```bash
python -m weather_spider.run_spider test
```

### 正式模式

```bash
python -m weather_spider.run_spider
```

爬虫会同时将数据导出到：
- ✅ CSV 文件：`export_data/weather.csv`
- ✅ MySQL 数据库：`weather_data` 表

## 五、验证数据

### 查看数据库中的数据

```sql
-- 查看所有数据
SELECT * FROM weather_data ORDER BY crawl_time DESC;

-- 查看最新10条数据
SELECT * FROM weather_data ORDER BY crawl_time DESC LIMIT 10;

-- 查看特定城市的数据
SELECT * FROM weather_data WHERE city LIKE '北京%' ORDER BY crawl_time DESC;

-- 统计数据量
SELECT COUNT(*) as total FROM weather_data;

-- 查看数据分布
SELECT city, COUNT(*) as count 
FROM weather_data 
GROUP BY city 
ORDER BY count DESC;
```

### 使用 Python 查询数据

```python
import pymysql
from config.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# 连接数据库
connection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset='utf8mb4'
)

# 查询数据
cursor = connection.cursor()
cursor.execute("SELECT * FROM weather_data ORDER BY crawl_time DESC LIMIT 10")
results = cursor.fetchall()

for row in results:
    print(row)

cursor.close()
connection.close()
```

## 六、常见问题

### 1. 连接数据库失败

**错误信息：** `Access denied for user 'xxx'@'localhost'`

**解决方案：**
- 检查 `.env` 文件中的用户名和密码是否正确
- 确认 MySQL 服务是否正在运行
- 确认用户是否有访问该数据库的权限

### 2. 数据库不存在

**错误信息：** `Unknown database 'weather_spider'`

**解决方案：**
```bash
python -m scripts.init_database
# 选择 4. 初始化数据库和表（完整初始化）
```

### 3. 字符编码问题

**错误信息：** 数据库中中文显示为乱码

**解决方案：**
- 确保 `.env` 文件中 `DB_CHARSET=utf8mb4`
- 确保数据库和表的字符集为 `utf8mb4`

### 4. 端口被占用

**错误信息：** `Can't connect to MySQL server on 'localhost:3306'`

**解决方案：**
- 检查 MySQL 服务是否正在运行
- 如果使用非标准端口，修改 `.env` 文件中的 `DB_PORT`

## 七、高级配置

### 1. 禁用 CSV 导出，只使用 MySQL

编辑 `weather_spider/settings.py`：

```python
ITEM_PIPELINES = {
    "weather_spider.pipelines.WeatherSpiderMySQLPipeline": 400,   # 只启用 MySQL
}
```

### 2. 调整 Pipeline 优先级

数字越小，优先级越高：

```python
ITEM_PIPELINES = {
    "weather_spider.pipelines.WeatherSpiderMySQLPipeline": 100,   # 先写入 MySQL
    "weather_spider.pipelines.WeatherSpiderPipeline": 200,      # 后写入 CSV
}
```

### 3. 批量插入优化

如果需要大量数据插入，可以修改 `WeatherSpiderMySQLPipeline` 类，添加批量插入功能。

## 八、数据备份

### 导出数据为 SQL

```bash
mysqldump -u username -p weather_spider weather_data > backup.sql
```

### 导入数据

```bash
mysql -u username -p weather_spider < backup.sql
```

### 导出数据为 CSV

```sql
SELECT * FROM weather_data 
INTO OUTFILE '/tmp/weather_data.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

## 九、性能优化

### 1. 添加索引

数据表已自动创建以下索引：
- `idx_city`: 城市名称索引
- `idx_crawl_time`: 爬取时间索引

### 2. 定期清理旧数据

```sql
-- 删除30天前的数据
DELETE FROM weather_data 
WHERE crawl_time < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

### 3. 数据库连接池

对于高并发场景，可以考虑使用数据库连接池（如 `DBUtils`）。

## 十、监控和日志

### 查看日志

所有数据库操作都会记录到日志文件：

```bash
tail -f logs/scrapy_weather.log
```

### 监控数据库连接

```sql
-- 查看当前连接
SHOW PROCESSLIST;

-- 查看连接数
SHOW STATUS LIKE 'Threads_connected';
```

## 十一、安全建议

1. **不要将 .env 文件提交到版本控制**
   - 添加到 `.gitignore` 文件中
   - 使用 `.env.example` 作为模板

2. **使用强密码**
   - 避免使用简单密码
   - 定期更换密码

3. **限制数据库权限**
   - 为爬虫创建专用数据库用户
   - 只授予必要的权限

4. **定期备份数据**
   - 设置自动备份任务
   - 保留多个备份版本

## 十二、故障排查

### 检查数据库连接

```bash
python -m scripts.init_database
# 选择 1. 测试数据库连接
```

### 查看详细错误信息

在日志文件中查找错误信息：

```bash
grep -i "error" logs/scrapy_weather.log
```

### 重新初始化数据库

```bash
# 删除数据库（谨慎操作！）
mysql -u username -p -e "DROP DATABASE IF EXISTS weather_spider;"

# 重新创建
python -m scripts.init_database
# 选择 4. 初始化数据库和表（完整初始化）
```

## 总结

通过以上配置，你的爬虫现在可以同时将数据导出到 CSV 文件和 MySQL 数据库。MySQL 数据库提供了更强大的数据管理和查询能力，适合生产环境使用。

如果遇到问题，请查看日志文件 `logs/scrapy_weather.log` 获取详细的错误信息。
