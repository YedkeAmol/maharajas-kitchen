@echo off
title Maharaja's Kitchen - Billing System Live Server
echo ========================================================
echo   MAHARAJA'S KITCHEN - STARTING LIVE SERVER
echo ========================================================
echo.
cd /d "%~dp0"

echo 1. Starting Flask Application...
start "Maharaja Backend" python app.py

timeout /t 2 /nobreak >nul

echo 2. Starting Secure Cloudflare Tunnel...
start "Cloudflare Live Tunnel" cloudflared.exe tunnel --url http://127.0.0.1:5001

echo.
echo ========================================================
echo Server and Tunnel launched!
echo Local Address:  http://127.0.0.1:5001
echo ========================================================
pause
