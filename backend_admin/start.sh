#!/bin/bash

echo "启动后台管理系统..."

echo ""
echo "1. 启动后端服务..."
cd api
python start.py &
BACKEND_PID=$!

echo ""
echo "2. 启动前端服务..."
cd ../web
npm run dev &
FRONTEND_PID=$!

echo ""
echo "服务启动中..."
echo "后端: http://localhost:8000"
echo "前端: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止所有服务..."

# 等待用户中断
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 