@echo off
REM Windows 计划任务配置脚本
REM 用于创建定时爬取天气数据的计划任务

echo ========================================
echo 天气爬虫 - Windows 计划任务配置工具
echo ========================================
echo.

REM 设置变量
set TASK_NAME=WeatherSpider
set PYTHON_PATH=F:\anaconda\envs\scrapy_weather\python.exe
set PROJECT_PATH=E:\Code Learning\GitHub_Project_5_scrapy_weather\weather_spider
set SCRIPT_PATH=-m weather_spider.run_spider

REM 检查是否已存在同名任务
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if %errorlevel% == 0 (
    echo [警告] 已存在名为 "%TASK_NAME%" 的计划任务
    echo.
    set /p DELETE_EXISTING="是否删除现有任务？(Y/N): "
    if /i "%DELETE_EXISTING%" == "Y" (
        schtasks /delete /tn "%TASK_NAME%" /f
        echo [成功] 已删除现有任务
        echo.
    ) else (
        echo [取消] 操作已取消
        pause
        exit /b 1
    )
)

echo 请选择定时策略：
echo 1. 每天凌晨 2:00 运行
echo 2. 每 6 小时运行一次
echo 3. 每 12 小时运行一次
echo 4. 自定义时间
echo.

set /p CHOICE="请输入选项 (1-4): "

if "%CHOICE%" == "1" (
    set SCHEDULE="DAILY"
    set TIME=02:00
    set INTERVAL=1
    echo [设置] 每天 02:00 运行
) else if "%CHOICE%" == "2" (
    set SCHEDULE="HOURLY"
    set TIME=00:00
    set INTERVAL=6
    echo [设置] 每 6 小时运行一次
) else if "%CHOICE%" == "3" (
    set SCHEDULE="HOURLY"
    set TIME=00:00
    set INTERVAL=12
    echo [设置] 每 12 小时运行一次
) else if "%CHOICE%" == "4" (
    set /p CUSTOM_TIME="请输入时间 (格式: HH:MM，例如: 03:30): "
    set SCHEDULE="DAILY"
    set TIME=%CUSTOM_TIME%
    set INTERVAL=1
    echo [设置] 每天 %CUSTOM_TIME% 运行
) else (
    echo [错误] 无效的选项
    pause
    exit /b 1
)

echo.
echo 正在创建计划任务...
echo.

REM 创建计划任务
schtasks /create /tn "%TASK_NAME%" /tr "\"%PYTHON_PATH%\" %SCRIPT_PATH%" /sc %SCHEDULE% /st %TIME% /mo %INTERVAL% /ru "SYSTEM" /f

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo [成功] 计划任务创建成功！
    echo ========================================
    echo.
    echo 任务名称: %TASK_NAME%
    echo 运行命令: %PYTHON_PATH% %SCRIPT_PATH%
    echo 工作目录: %PROJECT_PATH%
    echo 定时策略: %SCHEDULE% %TIME% (间隔: %INTERVAL%)
    echo.
    echo 常用操作:
    echo   查看任务详情: schtasks /query /tn "%TASK_NAME%" /fo LIST
    echo   立即运行任务: schtasks /run /tn "%TASK_NAME%"
    echo   停止任务:     schtasks /end /tn "%TASK_NAME%"
    echo   删除任务:     schtasks /delete /tn "%TASK_NAME%" /f
    echo.
    echo 日志文件: %PROJECT_PATH%\logs\scrapy_weather.log
    echo.
) else (
    echo.
    echo [错误] 计划任务创建失败！
    echo.
    echo 可能的原因:
    echo 1. Python 路径不正确，请修改脚本中的 PYTHON_PATH
    echo 2. 权限不足，请以管理员身份运行此脚本
    echo 3. 时间格式不正确
    echo.
)

pause
