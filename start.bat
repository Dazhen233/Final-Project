@echo off
title StoryBot Server & Frontend

:: 启动 Flask 服务器
start cmd /k "cd /d H:\StoryBot\backend && call venv\Scripts\activate && python app.py"

:: 等待 2 秒，确保后端启动后再启动前端
timeout /t 2 /nobreak

:: 启动 React 前端
start cmd /k "cd /d H:\StoryBot\frontend\my-app && npm start"

:: 退出脚本，但不关闭窗口
exit