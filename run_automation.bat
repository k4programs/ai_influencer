@echo off
title LENA-MARIE AUTOMATION CORE
cd /d "%~dp0"
echo 🤖 STARTING LENA-MARIE AI INFLUENCER SYSTEM...
echo ---------------------------------------------------
echo ⚠️  CLOSE THIS WINDOW TO STOP THE BOT AND FREE VRAM ⚠️
echo ---------------------------------------------------
echo.
"ComfyUI\python_embeded\python.exe" scripts/scheduler.py
pause
