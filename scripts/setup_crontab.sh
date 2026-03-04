#!/bin/bash
# Linux/Mac crontab 配置脚本
# 用于创建定时爬取天气数据的 crontab 任务

echo "========================================"
echo "天气爬虫 - Crontab 配置工具"
echo "========================================"
echo ""

# 设置变量
PYTHON_PATH=$(which python3)
PROJECT_PATH=$(pwd)
SCRIPT_PATH="-m weather_spider.run_spider"
LOG_FILE="$PROJECT_PATH/logs/scrapy_weather.log"

# 检查 Python 路径
if [ -z "$PYTHON_PATH" ]; then
    echo "[错误] 未找到 python3，请手动设置 PYTHON_PATH"
    exit 1
fi

echo "当前配置:"
echo "  Python 路径: $PYTHON_PATH"
echo "  项目路径:    $PROJECT_PATH"
echo "  脚本路径:    $SCRIPT_PATH"
echo "  日志文件:    $LOG_FILE"
echo ""

# 检查是否已存在天气爬虫的 crontab 任务
EXISTING_CRON=$(crontab -l 2>/dev/null | grep "weather_spider" || true)

if [ ! -z "$EXISTING_CRON" ]; then
    echo "[警告] 已存在天气爬虫的 crontab 任务:"
    echo "$EXISTING_CRON"
    echo ""
    read -p "是否删除现有任务？(Y/N): " DELETE_EXISTING
    if [ "$DELETE_EXISTING" = "Y" ] || [ "$DELETE_EXISTING" = "y" ]; then
        crontab -l 2>/dev/null | grep -v "weather_spider" | crontab -
        echo "[成功] 已删除现有任务"
        echo ""
    else
        echo "[取消] 操作已取消"
        exit 1
    fi
fi

echo "请选择定时策略:"
echo "1. 每天凌晨 2:00 运行"
echo "2. 每 6 小时运行一次"
echo "3. 每 12 小时运行一次"
echo "4. 自定义时间"
echo ""

read -p "请输入选项 (1-4): " CHOICE

case $CHOICE in
    1)
        CRON_EXPR="0 2 * * *"
        echo "[设置] 每天 02:00 运行"
        ;;
    2)
        CRON_EXPR="0 */6 * * *"
        echo "[设置] 每 6 小时运行一次"
        ;;
    3)
        CRON_EXPR="0 */12 * * *"
        echo "[设置] 每 12 小时运行一次"
        ;;
    4)
        read -p "请输入 cron 表达式 (例如: 0 3 * * *): " CUSTOM_CRON
        CRON_EXPR="$CUSTOM_CRON"
        echo "[设置] 使用自定义 cron 表达式: $CRON_EXPR"
        ;;
    *)
        echo "[错误] 无效的选项"
        exit 1
        ;;
esac

echo ""
echo "正在创建 crontab 任务..."
echo ""

# 创建 crontab 任务
CRON_JOB="$CRON_EXPR cd $PROJECT_PATH && $PYTHON_PATH $SCRIPT_PATH >> $LOG_FILE 2>&1"

# 添加到 crontab
(crontab -l 2>/dev/null | grep -v "weather_spider"; echo "# 天气爬虫定时任务"; echo "$CRON_JOB") | crontab -

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "[成功] Crontab 任务创建成功！"
    echo "========================================"
    echo ""
    echo "Cron 表达式: $CRON_EXPR"
    echo "执行命令:    cd $PROJECT_PATH && $PYTHON_PATH $SCRIPT_PATH"
    echo "日志文件:    $LOG_FILE"
    echo ""
    echo "常用操作:"
    echo "  查看当前 crontab:  crontab -l"
    echo "  编辑 crontab:      crontab -e"
    echo "  删除所有 crontab:  crontab -r"
    echo "  查看日志:          tail -f $LOG_FILE"
    echo ""
    echo "当前 crontab 内容:"
    crontab -l | grep -A 1 "天气爬虫"
    echo ""
else
    echo ""
    echo "[错误] Crontab 任务创建失败！"
    echo ""
    echo "可能的原因:"
    echo "1. Python 路径不正确"
    echo "2. 权限不足"
    echo "3. cron 表达式格式错误"
    echo ""
fi
