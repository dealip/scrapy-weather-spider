# 定时爬取天气数据使用指南

## 一、运行模式说明

### 1. 基础运行模式

```bash
# 测试模式（爬取2条数据）
python -m weather_spider.run_spider test

# 正式模式（全量爬取）
python -m weather_spider.run_spider

# 定时模式（预留接口）
python -m weather_spider.run_spider scheduled 24
```

### 2. 定时爬取模式

使用 `scheduled_spider.py` 实现定时爬取：

```bash
# 单次运行
python -m scripts.scheduled_spider once

# 使用 schedule 库，每24小时运行一次
python -m scripts.scheduled_spider schedule 24

# 使用 APScheduler，每12小时运行一次
python -m scripts.scheduled_spider apscheduler 12
```

## 二、定时任务工具对比

| 工具 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **schedule** | 简单易用，轻量级 | 功能相对简单 | 开发测试环境 |
| **APScheduler** | 功能强大，支持持久化、错误重试 | 学习曲线稍陡 | 生产环境 |
| **系统级定时任务** | 不依赖Python进程，系统管理 | 跨平台配置复杂 | 长期稳定运行 |

## 三、推荐方案

### 方案1：APScheduler（推荐用于生产环境）

```bash
# 安装依赖
pip install apscheduler

# 运行定时爬取（每24小时）
python -m scripts.scheduled_spider apscheduler 24
```

**优点：**
- ✅ 功能强大，支持多种触发器
- ✅ 支持任务持久化（重启后不丢失）
- ✅ 支持错误重试和日志记录
- ✅ 适合生产环境长期运行

### 方案2：系统级定时任务（最稳定）

#### Windows 计划任务

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（如每天凌晨2点）
4. 设置操作：启动程序
   - 程序：`python.exe`
   - 参数：`-m weather_spider.run_spider`
   - 起始于：`E:\Code Learning\GitHub_Project_5_scrapy_weather\weather_spider`

#### Linux/Mac crontab

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天凌晨2点运行）
0 2 * * * cd /path/to/weather_spider && /path/to/python -m weather_spider.run_spider

# 每6小时运行一次
0 */6 * * * cd /path/to/weather_spider && /path/to/python -m weather_spider.run_spider
```

**优点：**
- ✅ 不依赖Python进程，系统管理
- ✅ 重启后自动运行
- ✅ 最稳定可靠

### 方案3：schedule 库（适合开发测试）

```bash
# 安装依赖
pip install schedule

# 运行定时爬取（每24小时）
python -m scripts.scheduled_spider schedule 24
```

**优点：**
- ✅ 简单易用，代码直观
- ✅ 适合快速测试

**缺点：**
- ❌ 需要保持Python进程运行
- ❌ 重启后需要手动启动

## 四、代码结构说明

### SpiderRunner 类

```python
class SpiderRunner:
    """爬虫运行器 - 支持测试模式、正式模式和定时爬取"""
    
    def __init__(self):
        self.logger = get_scrapy_logger()
        self.is_running = False
    
    def check_prerequisites(self):
        """检查运行爬虫的前置条件"""
    
    def run_spider(self, test_mode=False):
        """运行爬虫"""
    
    def run_scheduled(self, interval_hours=24):
        """定时运行爬虫（预留接口）"""
    
    def run_once(self, test_mode=False):
        """单次运行爬虫"""
    
    def run(self):
        """主运行方法 - 根据命令行参数选择运行模式"""
```

### 使用示例

```python
from weather_spider.run_spider import SpiderRunner

# 创建运行器实例
runner = SpiderRunner()

# 单次运行
runner.run_once(test_mode=False)

# 测试模式运行
runner.run_spider(test_mode=True)

# 在定时任务中使用
def scheduled_job():
    runner.run_once(test_mode=False)
```

## 五、日志监控

所有日志都会输出到 `logs/scrapy_weather.log` 文件中，包括：

- ✅ 爬虫启动和完成信息
- ✅ 数据爬取成功/失败记录
- ✅ 定时任务触发记录
- ✅ 错误和异常信息

**查看日志：**
```bash
# 实时查看日志
tail -f logs/scrapy_weather.log

# 查看最近100行
tail -n 100 logs/scrapy_weather.log
```

## 六、常见问题

### 1. 定时任务没有执行？

**检查项：**
- 确认 Python 环境和路径正确
- 检查日志文件是否有错误信息
- 确认前置条件（清洗后的CSV文件）存在

### 2. 如何修改定时间隔？

**APScheduler：**
```bash
python -m scripts.scheduled_spider apscheduler 12  # 改为12小时
```

**schedule 库：**
```bash
python -m scripts.scheduled_spider schedule 6  # 改为6小时
```

**系统级定时任务：**
修改 crontab 或计划任务的配置

### 3. 如何停止定时任务？

**APScheduler / schedule：**
按 `Ctrl+C` 停止

**系统级定时任务：**
删除或禁用对应的计划任务/crontab 条目

## 七、最佳实践

1. **开发阶段**：使用 `test` 模式快速验证
2. **测试阶段**：使用 `schedule` 库进行短期测试
3. **生产环境**：使用系统级定时任务或 APScheduler
4. **监控**：定期检查日志文件，确保爬虫正常运行
5. **备份**：定期备份爬取的数据文件

## 八、扩展功能

未来可以扩展的功能：

- [ ] 数据去重（避免重复爬取）
- [ ] 数据验证（检查数据完整性）
- [ ] 告警通知（爬虫失败时发送邮件/短信）
- [ ] 数据统计（爬取成功率、耗时等）
- [ ] 数据可视化（展示天气数据趋势）
