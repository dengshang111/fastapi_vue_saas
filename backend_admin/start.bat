@echo off
echo 启动后台管理系统...

echo.
echo 1. 启动后端服务...
cd api
start "FastAPI Backend" cmd /k "python start.py"

echo.
echo 2. 启动前端服务...
cd ../web
start "Vue Frontend" cmd /k "npm run dev"

echo.
echo 服务启动中...
echo 后端: http://localhost:8000
echo 前端: http://localhost:5173
echo.
echo 按任意键退出...
pause > nul 