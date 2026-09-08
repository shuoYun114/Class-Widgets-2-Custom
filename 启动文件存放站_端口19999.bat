@echo off
chcp 65001 >nul
title Class-Widgets-2 文件存放站 [端口 19999]
echo ============================================================
echo   Class-Widgets-2 官方发布与文件存放站 (File Release Station)
echo   正在启动 HTTP 服务...
echo   局域网访问地址: http://192.168.48.156:19999
echo   路由器外网映射: http://223.72.8.19:19999
echo   本地访问地址:   http://127.0.0.1:19999
echo ============================================================
python "%~dp0scripts\file_station_server.py"
if errorlevel 1 (
    echo Python 运行遇到异常，请按任意键查看...
    pause
)
