@echo off
chcp 65001 >nul
echo === SRT字幕翻译工具 ===
echo.
echo 正在启动GUI界面...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误：依赖包安装失败
        pause
        exit /b 1
    )
)

REM 启动主程序
echo 启动主程序...
python main.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)